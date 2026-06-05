#!/usr/bin/env python3
"""Lint the Shattered Sea wiki: report problems, auto-fix the safe ones.

Two jobs, one pass:

1.  **Auto-fix (file-local, idempotent).** With ``--fix`` the linter standardizes
    frontmatter in place: adds any missing required field with a path-inferred
    default, reorders fields to canonical order, coerces booleans, and renders the
    short list fields (tags/sources/aliases) in flow style. These changes never
    invent canon and never touch another file, so they are safe to run in bulk and
    converge after one pass (a second run is a no-op).

2.  **Report (everything else).** Problems that need judgment or cross-file work —
    broken wikilinks, off-convention filenames, orphans, frontmatter relationships
    awaiting migration into the body, summaries still on their stub default — are
    reported, never silently changed. Each carries a concrete suggested action so
    the agent can fix and commit it. Structural fixes are deliberately the agent's
    call, not the script's: moving/renaming files and creating stubs rewrites the
    graph.

Why these libraries: ``ruamel.yaml`` round-trips frontmatter without mangling it,
which is what makes safe standardization possible; ``jsonschema`` checks field
*values* against ``wiki-frontmatter.schema.json`` (a declarative file — the allowed
vocabularies live there as data, not in code). Required-field-by-type lives in
``wiki_common`` because it keys off the file's path, the real source of truth.

Output is built to be cheap to read: a one-line summary to stderr, then issues
grouped by severity on stdout, one per line as ``path  rule  detail  ·fix: action``.
``--summary`` prints only the count line; ``--min-severity`` filters; ``--json`` emits
machine-readable output; ``--report`` writes the DM review queue to
``wiki/dm/review-queue.md`` (committed, regenerated each run) so flagged decisions
persist and stay visible across sessions. Exit code is 1 when any *error* is present
(warnings and quality notes do not fail), so it can gate a commit.

Usage:
    wiki_lint.py                      # lint whole vault, report only
    wiki_lint.py --fix                # standardize all frontmatter, then report
    wiki_lint.py --fix wiki/entities/characters/npcs/foo.md   # one file
    wiki_lint.py --summary            # just the counts
    wiki_lint.py --report             # also write wiki/lint-report.md
    wiki_lint.py --min-severity error # only errors
    wiki_lint.py --json               # machine-readable
    wiki_lint.py --obsidian on        # force Obsidian CLI for cross-file checks
    wiki_lint.py --markdown on        # include markdownlint-cli2 findings
"""

from __future__ import annotations

import argparse
import collections
import io
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from typing import Optional

import jsonschema
import tag_taxonomy
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from wiki_common import (
    ALLOWED_TYPES_BY_PATH,
    REPO_ROOT,
    TYPE_EXTRA_FIELDS,
    UNIVERSAL_FIELDS,
    WIKI_DIR,
    get_summary,
    infer_subtype,
    infer_type,
    iter_wiki_files,
    rel,
    today,
)

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "wiki-frontmatter.schema.json")

# Bookkeeping / generated files: don't run frontmatter/naming checks on them and
# never flag them as orphans — their frontmatter is special and inbound links to
# them aren't expected.
SKIP_CONTENT = {
    "index.md",
    "log.md",
    "work-queue.md",
    "discrepancy-log.md",
    "hot.md",
    "review-queue.md",
}

# Files whose body must NOT be scanned for outbound links. These are generated
# catalogs and bookkeeping — index.md in particular links *everything*, so
# counting it as an inbound link would mask every orphan. hot.md is deliberately
# absent: it's hand-curated navigation, so a page linked from hot.md is genuinely
# reachable and should not read as orphaned.
SKIP_AS_SOURCE = {
    "index.md",
    "log.md",
    "work-queue.md",
    "discrepancy-log.md",
    "review-queue.md",
}

# Directories whose files are legitimately stand-alone — exclude from orphan checks.
ORPHAN_EXEMPT_PREFIXES = (
    "wiki/system/",
    "wiki/dm/",
    "wiki/sessions/",
    "wiki/entities/characters/pcs/",
)

STUB_SUMMARY = "Stub — no summary yet."
SEVERITIES = ("error", "warning", "quality")
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
WIKILINK_RE = re.compile(r"(!?)\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")

# Targets with these extensions are attachments (images, media, data), not wiki
# pages — they live in an attachments folder, not as .md files, so never treat
# them as broken page links.
ASSET_EXTS = {
    ".webp",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".bmp",
    ".pdf",
    ".mp3",
    ".mp4",
    ".mov",
    ".wav",
    ".ogg",
    ".json",
    ".canvas",
    ".excalidraw",
}


# ---------------------------------------------------------------------------
# Obsidian CLI helpers
# ---------------------------------------------------------------------------

OBSIDIAN_CLI = (
    shutil.which("obsidian") or "/Applications/Obsidian.app/Contents/MacOS/obsidian"
)

_obsidian_live: Optional[bool] = None


def _obsidian_available() -> bool:
    global _obsidian_live
    if _obsidian_live is not None:
        return _obsidian_live
    try:
        r = subprocess.run(
            [OBSIDIAN_CLI, "vault", "info=name"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        _obsidian_live = r.returncode == 0 and bool(r.stdout.strip())
    except Exception:
        _obsidian_live = False
    return _obsidian_live


def _obsidian_json(args: str):
    """Run `obsidian {args} format=json` and return parsed JSON."""
    cmd = [OBSIDIAN_CLI] + args.split() + ["format=json"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        raise RuntimeError(f"obsidian {args}: {r.stderr.strip()}")
    return json.loads(r.stdout)


def _obsidian_lines(args: str) -> list[str]:
    """Run `obsidian {args}` and return stdout lines."""
    cmd = [OBSIDIAN_CLI] + args.split()
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        raise RuntimeError(f"obsidian {args}: {r.stderr.strip()}")
    return [line for line in r.stdout.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# markdownlint-cli2 helpers
# ---------------------------------------------------------------------------

MARKDOWNLINT_CLI = shutil.which("markdownlint-cli2")

MARKDOWNLINT_LINE_RE = re.compile(
    r"^(.+?):(\d+)(?::(\d+))?\s+error\s+(MD\d+)/(\S+)\s+(.+)$"
)


def _run_markdownlint(scope_paths: Optional[list[str]]) -> list["Issue"]:
    """Shell out to markdownlint-cli2 and convert findings to Issues."""
    if not MARKDOWNLINT_CLI:
        return []
    globs = scope_paths if scope_paths else [os.path.join(WIKI_DIR, "**", "*.md")]
    cmd = [MARKDOWNLINT_CLI] + globs
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=REPO_ROOT)
    issues = []
    for line in r.stdout.splitlines() + r.stderr.splitlines():
        m = MARKDOWNLINT_LINE_RE.match(line)
        if m:
            path, lineno, _col, rule_id, rule_name, detail = m.groups()
            relpath = (
                rel(os.path.join(REPO_ROOT, path))
                if not path.startswith("wiki/")
                else path
            )
            issues.append(
                Issue(
                    "quality",
                    f"md-{rule_name}",
                    relpath,
                    f"line {lineno}: {detail}",
                    fix=f"fix markdown formatting ({rule_id})",
                )
            )
    return issues


# Python-native defaults for missing required fields. Field LISTS come from
# wiki_common (the source of truth); only the default VALUES live here, matching
# fix_frontmatter.py.
def field_defaults(relpath: str) -> dict:
    return {
        "type": infer_type(relpath),
        "subtype": infer_subtype(relpath),
        "campaign": "shattered-sea",
        "status": "unknown",
        "audience": "dm",
        "publish": False,
        "summary": STUB_SUMMARY,
        "created": today(),
        "updated": today(),
        "tags": [],
        "sources": ["Unknown"],
        "confidence_level": "medium",
        "relationships": [],
        "lifecycle": "dormant",
        "island": None,
        "portable": False,
        "entry_points": [],
        "contains_situations": [],
        "session_number": 0,
        "session_date": "unknown",
        "system_role": "unknown",
        "token_profile": "on-demand",
        "mandatory_for": [],
        "update_trigger": "",
    }


BLOCK_LIST_FIELDS = ("tags", "sources", "aliases")


@dataclass
class Issue:
    severity: str
    rule: str
    path: str
    detail: str
    fix: Optional[str] = None

    def line(self) -> str:
        suffix = f"  ·fix: {self.fix}" if self.fix else ""
        return f"  {self.path}  {self.rule}  {self.detail}{suffix}"


def required_fields(relpath: str):
    return UNIVERSAL_FIELDS + TYPE_EXTRA_FIELDS.get(infer_type(relpath), [])


def make_yaml() -> YAML:
    y = YAML()
    y.preserve_quotes = True
    y.width = 4096  # don't wrap long summaries
    y.indent(mapping=2, sequence=4, offset=2)
    return y


def split_doc(text: str):
    """Return (frontmatter_text, body_text, had_frontmatter). Frontmatter text
    excludes the --- fences."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return "", text, False
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = "\n".join(lines[1:i])
            body = "\n".join(lines[i + 1 :])
            return fm, body, True
    return "", text, False


def scannable(body: str) -> str:
    """Body text ready for wikilink scanning: code fences removed and Obsidian's
    table-escaped pipes (``\\|``) normalized back to ``|`` so links inside tables
    parse like any other. Fenced and inline code are dropped so example wikilinks
    in documentation (e.g. ``[[npc-slug|Name]]`` in doctrine) aren't read as real
    links."""
    stripped = INLINE_CODE_RE.sub("", FENCE_RE.sub("", body))
    return stripped.replace("\\|", "|")


def is_asset(target: str) -> bool:
    return os.path.splitext(target)[1].lower() in ASSET_EXTS


def slug_of(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def wikilink_targets(text: str):
    """Yield (target_slug, has_alias, is_embed) for each wikilink. Slugs are
    basenames with any .md stripped; asset targets are yielded as-is so callers
    can skip them."""
    for m in WIKILINK_RE.finditer(text):
        is_embed = bool(m.group(1))
        target = os.path.basename(m.group(2).strip())
        if target.endswith(".md"):
            target = target[:-4]
        yield target, bool(m.group(3)), is_embed


# ---------------------------------------------------------------------------
# Per-file checks
# ---------------------------------------------------------------------------


def load_frontmatter(yaml: YAML, fm_text: str):
    if not fm_text.strip():
        return CommentedMap()
    data = yaml.load(fm_text)
    if data is None:
        return CommentedMap()
    return data


def relationship_entries(node):
    """Pull (target_slug, note) pairs out of a frontmatter `relationships` value,
    handling both shapes seen in the vault: bare strings
    ('[[slug|Label]] — note') and mappings ({relation: ..., target: '[[slug]]'})."""
    entries = []
    if node is None:
        return entries
    items = node if isinstance(node, list) else [node]
    for item in items:
        if isinstance(item, dict):
            target_raw = str(item.get("target", ""))
            note = str(item.get("relation", "")).strip()
            for t, _, _ in wikilink_targets(target_raw):
                entries.append((t, note))
        else:
            text = str(item)
            targets = [t for t, _, _ in wikilink_targets(text)]
            note = WIKILINK_RE.sub("", text).strip(" —-:|")
            for t in targets:
                entries.append((t, note))
    return entries


def check_file(relpath: str, data, body: str, yaml: YAML, validator):
    issues = []

    # Schema: value vocabularies of known fields.
    plain = json.loads(json.dumps(_to_plain(data)))
    for err in validator.iter_errors(plain):
        field = err.path[0] if err.path else "(root)"
        issues.append(
            Issue("error", "invalid-value", relpath, f"{field}: {err.message}")
        )

    # Required fields present (path-keyed).
    for field in required_fields(relpath):
        if field not in data:
            issues.append(
                Issue(
                    "warning",
                    "missing-required-field",
                    relpath,
                    field,
                    fix=f"run wiki_lint.py --fix {relpath}",
                )
            )

    # type matches the path it lives at.
    expected_type = infer_type(relpath)
    actual_type = str(data.get("type", "")).strip()
    allowed_types = next(
        (
            types
            for prefix, types in ALLOWED_TYPES_BY_PATH
            if relpath.startswith(prefix)
        ),
        None,
    )
    type_ok = (
        not actual_type
        or expected_type in ("unknown", "governance")
        or (allowed_types is not None and actual_type in allowed_types)
        or (allowed_types is None and actual_type == expected_type)
    )
    if not type_ok:
        issues.append(
            Issue(
                "warning",
                "type-path-mismatch",
                relpath,
                f"type: {actual_type!r} but path implies {expected_type!r}",
            )
        )

    # Summary quality.
    summary = get_summary(data) if data else ""
    if not summary or summary == STUB_SUMMARY:
        issues.append(
            Issue(
                "quality",
                "summary-stale",
                relpath,
                "summary missing or still the stub default — write a concrete one",
            )
        )

    # Relationships belong in the body prose, not frontmatter. Flag any that
    # remain so they can be woven in. We surface, per target, whether it's
    # already wikilinked in the body — if it is, weaving is usually just folding
    # the note into a sentence near the existing link; if not, the relationship
    # isn't reflected in the prose at all yet.
    rels = (
        relationship_entries(data.get("relationships")) if hasattr(data, "get") else []
    )
    if rels:
        body_links = {
            t.lower()
            for t, _, _ in wikilink_targets(scannable(body))
            if not is_asset(t)
        }
        parts = []
        for tgt, note in rels:
            where = "in body" if tgt.lower() in body_links else "NOT in body"
            note_bit = f" — {note}" if note else ""
            parts.append(f"[[{tgt}]] ({where}){note_bit}")
        issues.append(
            Issue(
                "warning",
                "relationships-in-frontmatter",
                relpath,
                f"{len(rels)} relationship(s) to migrate: " + "; ".join(parts),
                fix="weave each into the prose with a wikilink (carry the note), then delete the relationships field",
            )
        )

    # Situation lifecycle vs folder.
    if relpath.startswith("wiki/situations/"):
        folder = relpath.split("/")[2] if len(relpath.split("/")) > 3 else ""
        lifecycle = str(data.get("lifecycle", "")).strip()
        if (
            folder in ("active", "dormant", "resolved")
            and lifecycle
            and lifecycle != folder
        ):
            issues.append(
                Issue(
                    "warning",
                    "lifecycle-folder-mismatch",
                    relpath,
                    f"lifecycle: {lifecycle!r} but file is in situations/{folder}/",
                    fix=f"set lifecycle to {folder!r} or move the file",
                )
            )

    return issues


def _to_plain(data):
    """ruamel CommentedMap/Seq + scalar wrappers -> plain python for jsonschema."""
    if isinstance(data, dict):
        return {str(k): _to_plain(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_to_plain(v) for v in data]
    if isinstance(data, bool) or data is None:
        return data
    if isinstance(data, (int, float, str)):
        return data
    return str(data)


def check_naming(relpath: str):
    name = slug_of(relpath)
    if not KEBAB_RE.match(name):
        return Issue(
            "error",
            "naming-convention",
            relpath,
            f"filename {name!r} is not kebab-case",
            fix="rename to kebab-case and update inbound wikilinks",
        )
    return None


# ---------------------------------------------------------------------------
# Cross-file checks
# ---------------------------------------------------------------------------


def _obsidian_broken_links() -> list[Issue]:
    """Use Obsidian CLI to find unresolved links (more accurate than regex)."""
    try:
        data = _obsidian_json("unresolved verbose")
    except Exception as exc:
        sys.stderr.write(f"wiki_lint: obsidian unresolved failed: {exc}\n")
        return []
    issues = []
    for entry in data:
        link = entry.get("link", "")
        if is_asset(link):
            continue
        sources_raw = entry.get("sources", "")
        sources = [s.strip() for s in sources_raw.split(",") if s.strip()]
        for src in sources:
            src_rel = (
                src if src.startswith("wiki/") else rel(os.path.join(REPO_ROOT, src))
            )
            if not src_rel.startswith("wiki/"):
                continue
            if os.path.basename(src_rel) in SKIP_AS_SOURCE:
                continue
            issues.append(
                Issue(
                    "error",
                    "broken-wikilink",
                    src_rel,
                    f"[[{link}]] resolves to no page (via Obsidian)",
                    fix=f"create a stub for {link!r} or fix the link",
                )
            )
    return issues


def _obsidian_deadends() -> list[Issue]:
    """Use Obsidian CLI to find files with no outgoing links."""
    try:
        lines = _obsidian_lines("deadends")
    except Exception as exc:
        sys.stderr.write(f"wiki_lint: obsidian deadends failed: {exc}\n")
        return []
    issues = []
    for path in lines:
        if not path.startswith("wiki/"):
            continue
        if not path.endswith(".md"):
            continue
        if os.path.basename(path) in SKIP_CONTENT:
            continue
        if path.startswith(ORPHAN_EXEMPT_PREFIXES):
            continue
        issues.append(
            Issue(
                "quality",
                "deadend",
                path,
                "no outgoing wikilinks",
                fix="add wikilinks to related pages",
            )
        )
    return issues


def cross_file_checks(records, slug_to_paths, use_obsidian=False):
    """records: list of (relpath, data, body). Returns dict relpath -> [Issue]."""
    by_file = {r[0]: [] for r in records}
    inbound = {r[0]: set() for r in records}
    lower_index = {}
    for slug, paths in slug_to_paths.items():
        lower_index.setdefault(slug.lower(), []).extend(paths)

    # Duplicate slugs: two files sharing a basename make every [[slug]] to them
    # ambiguous — Obsidian picks one arbitrarily. Flag each colliding file.
    # Exception: "index" is an intentional per-directory convention — every
    # directory may have its own index.md. Links to them use path-qualified
    # syntax ([[wiki/lore/index|...]]), not bare [[index]], so the ambiguity
    # is never exercised in practice.
    for low, paths in lower_index.items():
        if low == "index":
            continue
        if len(paths) > 1:
            others = sorted(paths)
            for p in paths:
                rest = [o for o in others if o != p]
                by_file[p].append(
                    Issue(
                        "error",
                        "duplicate-slug",
                        p,
                        f"slug also used by: {', '.join(rest)} — wikilinks to it are ambiguous",
                        fix="rename one file to a distinct slug and update its inbound links",
                    )
                )

    has_outgoing = set()

    for relpath, data, body in records:
        if os.path.basename(relpath) in SKIP_AS_SOURCE:
            continue
        scan = scannable(body)
        seen_broken = set()
        file_has_links = False
        for target, has_alias, is_embed in wikilink_targets(scan):
            if is_asset(target):
                continue
            file_has_links = True
            matches = lower_index.get(target.lower())
            if matches:
                for tgt_path in matches:
                    if tgt_path != relpath:
                        inbound[tgt_path].add(relpath)
                if not has_alias and not is_embed:
                    by_file[relpath].append(
                        Issue(
                            "quality",
                            "bare-wikilink",
                            relpath,
                            f"[[{target}]] has no display alias",
                            fix=f"alias it: [[{target}|Display Name]]",
                        )
                    )
            elif not use_obsidian:
                if target in seen_broken:
                    continue
                seen_broken.add(target)
                by_file[relpath].append(
                    Issue(
                        "error",
                        "broken-wikilink",
                        relpath,
                        f"[[{target}]] resolves to no page",
                        fix=f"create a stub for {target!r} or fix the link",
                    )
                )
        if file_has_links:
            has_outgoing.add(relpath)

    # When Obsidian CLI is active, use it for broken links and deadends.
    if use_obsidian:
        for issue in _obsidian_broken_links():
            by_file.setdefault(issue.path, []).append(issue)
        for issue in _obsidian_deadends():
            by_file.setdefault(issue.path, []).append(issue)
    else:
        # Fallback deadend detection from the scan pass.
        for relpath, data, body in records:
            if os.path.basename(relpath) in SKIP_CONTENT:
                continue
            if relpath.startswith(ORPHAN_EXEMPT_PREFIXES):
                continue
            if os.path.basename(relpath) in SKIP_AS_SOURCE:
                continue
            if relpath not in has_outgoing:
                by_file[relpath].append(
                    Issue(
                        "quality",
                        "deadend",
                        relpath,
                        "no outgoing wikilinks",
                        fix="add wikilinks to related pages",
                    )
                )

    return _finish_orphans(records, inbound, by_file)


def _finish_orphans(records, inbound, by_file):
    """Append orphan issues (no inbound wikilink, not exempt) and return by_file."""
    for relpath, data, body in records:
        if os.path.basename(relpath) in SKIP_CONTENT:
            continue
        if relpath.startswith(ORPHAN_EXEMPT_PREFIXES):
            continue
        if not inbound.get(relpath):
            by_file[relpath].append(
                Issue(
                    "quality",
                    "orphan",
                    relpath,
                    "no other page links here",
                    fix="link it from a natural parent page",
                )
            )
    return by_file


# ---------------------------------------------------------------------------
# Vault-wide checks (tags, property names)
# ---------------------------------------------------------------------------


def check_tag_variants(records) -> list[Issue]:
    """Flag tags that look like plural/singular variants of each other."""
    tag_counter: dict[str, int] = collections.Counter()
    tag_files: dict[str, list[str]] = collections.defaultdict(list)
    for relpath, data, _body in records:
        tags = data.get("tags") if hasattr(data, "get") else None
        if not isinstance(tags, list):
            continue
        for tag in tags:
            t = str(tag).strip().lower()
            if t:
                tag_counter[t] += 1
                tag_files[t].append(relpath)

    issues = []
    seen = set()
    for tag in sorted(tag_counter):
        if tag in seen:
            continue
        # Check plural/singular pairs.
        variants = []
        if tag.endswith("s") and tag[:-1] in tag_counter:
            variants.append(tag[:-1])
        if tag + "s" in tag_counter:
            variants.append(tag + "s")
        for var in variants:
            if var in seen:
                continue
            # Flag the less-used one.
            if tag_counter[tag] < tag_counter[var]:
                lesser, greater = tag, var
            else:
                lesser, greater = var, tag
            seen.add(lesser)
            for f in tag_files[lesser][:3]:
                issues.append(
                    Issue(
                        "quality",
                        "tag-variant",
                        f,
                        f"tag '{lesser}' may be a variant of '{greater}' ({tag_counter[greater]} uses)",
                        fix=f"consolidate to '{greater}'",
                    )
                )
    return issues


def check_tags(records) -> list[Issue]:
    """Validate tags against the controlled vocabulary in tag_taxonomy.py.

    Every tag violation requires the agent to read the file and choose
    appropriate canonical replacements — the fix is never mechanical.
    Only visibility/* tags are left untouched (reserved group).
    """
    issues = []
    fix_suffix = "read this file and select canonical tags from wiki/system/taxonomy.md"

    for relpath, data, _body in records:
        if os.path.basename(relpath) in SKIP_CONTENT:
            continue
        if not hasattr(data, "get"):
            continue
        tags = data.get("tags")
        if not isinstance(tags, list):
            continue

        content_tags = []
        for raw in tags:
            tag = str(raw).strip()
            if not tag:
                continue
            category, canonical = tag_taxonomy.classify(tag)

            if category == "canonical":
                content_tags.append(tag)

            elif category == "alias":
                content_tags.append(tag)
                issues.append(
                    Issue(
                        "warning",
                        "tag-alias",
                        relpath,
                        f"'{tag}' is an alias — canonical form is '{canonical}'",
                        fix=f"replace with '{canonical}'; then {fix_suffix}",
                    )
                )

            elif category == "deprecated-fm":
                content_tags.append(tag)
                issues.append(
                    Issue(
                        "warning",
                        "tag-deprecated",
                        relpath,
                        f"'{tag}' duplicates a frontmatter field — remove it",
                        fix=fix_suffix,
                    )
                )

            elif category == "deprecated-entity":
                content_tags.append(tag)
                issues.append(
                    Issue(
                        "warning",
                        "tag-deprecated",
                        relpath,
                        f"'{tag}' is an entity name — use a wikilink in the body instead",
                        fix=f"add wikilink to [[{tag}]] in body; {fix_suffix}",
                    )
                )

            elif category == "deprecated-source":
                content_tags.append(tag)
                issues.append(
                    Issue(
                        "warning",
                        "tag-deprecated",
                        relpath,
                        f"'{tag}' is a source citation — move to sources: frontmatter field",
                        fix=f"move to sources: field; {fix_suffix}",
                    )
                )

            elif category == "deprecated-system":
                content_tags.append(tag)
                issues.append(
                    Issue(
                        "warning",
                        "tag-deprecated",
                        relpath,
                        f"'{tag}' is a system/process tag — remove it",
                        fix=fix_suffix,
                    )
                )

            elif category == "unknown":
                content_tags.append(tag)
                issues.append(
                    Issue(
                        "quality",
                        "tag-unknown",
                        relpath,
                        f"'{tag}' not in controlled vocabulary",
                        fix=f"{fix_suffix}, or propose adding '{tag}' if it covers 5+ files across 3+ entity types",
                    )
                )

            # "visibility" tags: silently skip, no issue raised

        if len(content_tags) > tag_taxonomy.TAG_LIMIT:
            issues.append(
                Issue(
                    "warning",
                    "tag-over-limit",
                    relpath,
                    f"{len(content_tags)} content tags (limit {tag_taxonomy.TAG_LIMIT}): {', '.join(content_tags)}",
                    fix=fix_suffix,
                )
            )

    return issues


SINGLETON_WHITELIST = {
    "cr",
    "aliases",
    "region",
    "species",
    "pronouns",
    "portrait",
    "ship_class",
    "hull_points",
    "crew_capacity",
    "speed",
    "captain",
    "current_holder",
    "parent_location",
    "narrative_island",
    "session_number",
    "session_date",
    "alignment",
    "ac",
    "hp",
    "size",
    "challenge_rating",
    "damage_resistances",
    "damage_immunities",
    "condition_immunities",
    "senses",
    "languages",
    "environment",
    "rarity",
    "attunement",
    "item_type",
    "weight",
    "cost",
    "faction",
    "domain",
    "pantheon",
    "population",
    "government",
    "defenses",
    "trade_goods",
    "climate",
}


def check_singleton_properties(records, schema_props: set[str]) -> list[Issue]:
    """Flag frontmatter properties that appear in only one file and aren't in the schema."""
    prop_counter: dict[str, int] = collections.Counter()
    prop_files: dict[str, str] = {}
    for relpath, data, _body in records:
        if not hasattr(data, "keys"):
            continue
        for key in data.keys():
            k = str(key)
            prop_counter[k] += 1
            prop_files[k] = relpath

    known = schema_props | SINGLETON_WHITELIST
    issues = []
    for prop, count in prop_counter.items():
        if count == 1 and prop not in known:
            issues.append(
                Issue(
                    "quality",
                    "singleton-property",
                    prop_files[prop],
                    f"property '{prop}' appears only in this file and is not in the schema",
                    fix="verify this isn't a typo, or add it to the schema if intentional",
                )
            )
    return issues


# ---------------------------------------------------------------------------
# Lore consistency checks (cross-file)
# ---------------------------------------------------------------------------

# Frontmatter fields that hold wikilink references to other entities.
XREF_ROLE_FIELDS = {
    "captain": "captains",
    "current_holder": "holds",
    "owner": "owns",
}

DEAD_STATUSES = frozenset({"dead", "deceased", "destroyed", "presumed_dead"})

STATUS_CANONICAL = {
    "deceased": "dead",
    "presumed_dead": "dead",
    "open": "active",
}


def _extract_slug(value: str) -> Optional[str]:
    """Extract a wikilink slug from a frontmatter value string."""
    m = WIKILINK_RE.search(str(value))
    if not m:
        return None
    target = os.path.basename(m.group(2).strip())
    if target.endswith(".md"):
        target = target[:-3]
    return target.lower()


def check_lore_consistency(records, slug_to_paths) -> list[Issue]:
    """Cross-file lore checks: dead-entity refs, parent-location gaps,
    narrative-island mismatches, status vocabulary drift."""
    lower_index = {}
    for slug, paths in slug_to_paths.items():
        lower_index[slug.lower()] = paths

    # Build data/body lookup by relpath.
    data_by_path = {}
    body_by_path = {}
    for relpath, data, body in records:
        data_by_path[relpath] = data
        body_by_path[relpath] = body

    # Build slug -> relpath lookup (first match).
    slug_to_first = {}
    for slug, paths in slug_to_paths.items():
        slug_to_first[slug.lower()] = paths[0]

    # Collect entity statuses.
    entity_status = {}
    for relpath, data, _body in records:
        status = (
            str(data.get("status", "")).strip().lower() if hasattr(data, "get") else ""
        )
        if status:
            slug = slug_of(relpath).lower()
            entity_status[slug] = status

    issues = []

    for relpath, data, body in records:
        if not hasattr(data, "get"):
            continue

        # 1. Cross-reference fields pointing to dead entities.
        for field, verb in XREF_ROLE_FIELDS.items():
            val = data.get(field)
            if not val:
                continue
            target_slug = _extract_slug(val)
            if not target_slug:
                continue
            target_status = entity_status.get(target_slug, "")
            if target_status in DEAD_STATUSES:
                issues.append(
                    Issue(
                        "warning",
                        "dead-entity-ref",
                        relpath,
                        f"{field}: [[{target_slug}]] is {target_status}",
                        fix=f"update {field} or mark this file's status accordingly",
                    )
                )

        # 2. parent_location bidirectionality.
        parent_val = data.get("parent_location")
        if parent_val:
            parent_slug = _extract_slug(parent_val)
            if parent_slug:
                parent_path = slug_to_first.get(parent_slug)
                if parent_path:
                    parent_body = body_by_path.get(parent_path, "")
                    child_slug = slug_of(relpath).lower()
                    if child_slug not in parent_body.lower():
                        issues.append(
                            Issue(
                                "quality",
                                "parent-gap",
                                relpath,
                                f"parent_location [[{parent_slug}]] doesn't mention this page",
                                fix=f"add a wikilink to [[{child_slug}]] in {parent_path}",
                            )
                        )

        # 3. contains_situations ↔ narrative_island consistency.
        cs = data.get("contains_situations")
        if isinstance(cs, list):
            island_slug = slug_of(relpath).lower()
            for sit in cs:
                sit_slug = _extract_slug(str(sit))
                if not sit_slug:
                    continue
                sit_path = slug_to_first.get(sit_slug)
                if not sit_path:
                    continue
                sit_data = data_by_path.get(sit_path, {})
                sit_ni = str(sit_data.get("narrative_island", "")).strip().lower()
                if sit_ni and sit_ni != "none" and island_slug not in sit_ni:
                    issues.append(
                        Issue(
                            "warning",
                            "island-situation-mismatch",
                            sit_path,
                            f"narrative_island={sit_ni!r} but listed in {relpath}",
                            fix=f"set narrative_island to match {island_slug!r}",
                        )
                    )
                elif not sit_ni or sit_ni == "none":
                    issues.append(
                        Issue(
                            "warning",
                            "island-situation-mismatch",
                            sit_path,
                            f"narrative_island is unset but listed in {relpath}",
                            fix=f"set narrative_island to {island_slug!r}",
                        )
                    )

        # 4. Status vocabulary drift.
        status = str(data.get("status", "")).strip().lower()
        if status in STATUS_CANONICAL:
            canonical = STATUS_CANONICAL[status]
            issues.append(
                Issue(
                    "warning",
                    "status-drift",
                    relpath,
                    f"status '{status}' — use '{canonical}' for consistency",
                    fix=f"set status to '{canonical}'",
                )
            )

    return issues


def _dump_node(node) -> str:
    y = make_yaml()
    buf = io.StringIO()
    try:
        y.dump({"x": node}, buf)
    except Exception:
        return str(node)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Auto-fix: standardize frontmatter
# ---------------------------------------------------------------------------


def standardize(relpath: str, data, yaml: YAML):
    """Return (new_data, changed_fields). File-local, idempotent."""
    changed = []
    defaults = field_defaults(relpath)

    # 0. Strip junk fields that waste tokens with no signal for the agent.
    for f in ("title", "cssclasses"):
        if f in data:
            del data[f]
            changed.append(f"-{f}")

    # Strip null-valued fields.
    null_keys = [k for k, v in data.items() if v is None]
    for k in null_keys:
        del data[k]
    if null_keys:
        changed.append("-nulls")

    # sources: ["Unknown"] -> []
    sources = data.get("sources")
    if isinstance(sources, list) and list(sources) == ["Unknown"]:
        data["sources"] = []
        changed.append("sources(clean)")

    # aliases: [] -> strip
    aliases = data.get("aliases")
    if isinstance(aliases, list) and len(aliases) == 0:
        del data["aliases"]
        changed.append("-aliases")

    # Drop empty relationships: []
    rel = data.get("relationships")
    if isinstance(rel, list) and len(rel) == 0:
        del data["relationships"]
        changed.append("-relationships")

    # 0b. Status-drift: mechanical synonym replacement. The canonical forms
    #     are unambiguous rewrites ("deceased" is always "dead"), so this is
    #     safe to auto-fix without reading the file for context.
    status = data.get("status")
    if isinstance(status, str) and status.strip().lower() in STATUS_CANONICAL:
        data["status"] = STATUS_CANONICAL[status.strip().lower()]
        changed.append("status")

    # 0c. Lifecycle-folder sync: when a situation file lives in active/,
    #     dormant/, or resolved/ and lifecycle disagrees, the folder is the
    #     source of truth (the user moved the file there intentionally).
    if relpath.startswith("wiki/situations/"):
        parts = relpath.split("/")
        if len(parts) > 3:
            folder = parts[2]
            lifecycle = str(data.get("lifecycle", "")).strip()
            if (
                folder in ("active", "dormant", "resolved")
                and lifecycle
                and lifecycle != folder
            ):
                data["lifecycle"] = folder
                changed.append("lifecycle")

    # 1. Add missing required fields.
    for field in required_fields(relpath):
        if field not in data:
            data[field] = defaults[field]
            changed.append(field)

    # 2. Coerce known booleans.
    for field in ("publish", "portable"):
        if field in data and isinstance(data[field], str):
            v = data[field].strip().lower()
            if v in ("true", "false"):
                data[field] = v == "true"
                changed.append(field)

    # 3. Render list fields in block style per Obsidian convention.
    for field in BLOCK_LIST_FIELDS:
        node = data.get(field)
        if isinstance(node, list):
            seq = CommentedSeq(node)
            seq.fa.set_block_style()
            data[field] = seq

    # 4. Canonical key order.
    order = [f for f in required_fields(relpath) if f in data]
    order += [k for k in data if k not in order]
    if list(data.keys()) != order:
        changed.append("(reorder)")
    new = CommentedMap()
    for k in order:
        new[k] = data[k]
    return new, changed


def fix_safe_tags(data) -> list[str]:
    """Auto-fix tag issues that are purely mechanical (no file-reading needed).

    - Aliases: replace with canonical form (e.g. 'maw' -> 'drowned-maw')
    - Deprecated-fm: remove tags that duplicate a frontmatter field
    - Deprecated-system: remove system/process tags

    Returns list of changes made. Tags requiring judgment (deprecated-entity,
    deprecated-source, unknown) are left for the report.
    """
    tags = data.get("tags")
    if not isinstance(tags, list):
        return []

    new_tags = []
    changes = []
    seen = set()
    for raw in tags:
        tag = str(raw).strip()
        if not tag:
            continue
        category, canonical = tag_taxonomy.classify(tag)

        if category == "alias" and canonical:
            if canonical.lower() not in seen:
                new_tags.append(canonical)
                seen.add(canonical.lower())
                if canonical != tag:
                    changes.append(f"tag:{tag}->{canonical}")
            else:
                changes.append(f"tag:-{tag}(dup)")
        elif category in ("deprecated-fm", "deprecated-system"):
            changes.append(f"tag:-{tag}")
        elif category == "canonical":
            if tag.lower() not in seen:
                new_tags.append(tag)
                seen.add(tag.lower())
        else:
            if tag.lower() not in seen:
                new_tags.append(tag)
                seen.add(tag.lower())

    if changes:
        seq = CommentedSeq(new_tags)
        seq.fa.set_block_style()
        data["tags"] = seq

    return changes


def dump_frontmatter(data, yaml: YAML) -> str:
    buf = io.StringIO()
    yaml.dump(data, buf)
    return buf.getvalue().rstrip("\n")


FM_BLOCK_RE = re.compile(r"^---[ \t]*\n(.*?\n)---[ \t]*\n?", re.DOTALL)


def apply_fix(path: str, relpath: str, yaml: YAML, fix_tags: bool = False):
    """Standardize frontmatter in place, preserving the body byte-for-byte.

    Only the frontmatter block is rewritten; everything after the closing fence
    (including the exact trailing newline) is spliced back untouched. Returns the
    list of changed fields, or [] when the file is already canonical (a true
    no-op — nothing is written).

    When fix_tags is True, also applies safe tag fixes (alias replacement,
    deprecated-fm removal) in addition to standard frontmatter cleanup."""
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    m = FM_BLOCK_RE.match(text)
    if m:
        fm_text = m.group(1)
        body = text[m.end() :]  # verbatim, including its leading/trailing newlines
    else:
        fm_text = ""
        body = text

    data = load_frontmatter(yaml, fm_text)
    new_data, changed = standardize(relpath, data, yaml)
    if fix_tags:
        changed.extend(fix_safe_tags(new_data))
    new_fm = dump_frontmatter(new_data, yaml)
    rebuilt = f"---\n{new_fm}\n---\n" + body

    if rebuilt == text:
        return []
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(rebuilt)
    return changed or ["(reformat)"]


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def gather_records(yaml: YAML):
    records = []
    parse_errors = []
    for path in iter_wiki_files():
        relpath = rel(path)
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
        fm_text, body, had = split_doc(text)
        if not had:
            parse_errors.append(
                Issue("error", "missing-frontmatter", relpath, "no frontmatter block")
            )
            records.append((relpath, CommentedMap(), body))
            continue
        try:
            data = load_frontmatter(yaml, fm_text)
        except Exception as exc:
            parse_errors.append(
                Issue(
                    "error",
                    "unparseable-frontmatter",
                    relpath,
                    str(exc).splitlines()[0],
                )
            )
            records.append((relpath, CommentedMap(), body))
            continue
        records.append((relpath, data, body))
    return records, parse_errors


def in_scope(relpath: str, scope_rel) -> bool:
    if scope_rel is None:
        return True
    for s in scope_rel:
        if relpath == s or relpath.startswith(s.rstrip("/") + "/"):
            return True
    return False


def resolve_scope(paths):
    if not paths:
        return None
    out = []
    for p in paths:
        ap = os.path.abspath(p)
        out.append(rel(ap))
    return out


def files_changed_since(ref: str) -> list[str]:
    """Return wiki/ file relpaths changed since a git ref or date.

    Accepts a commit SHA, branch name, tag, or a date string like '3 days ago'
    or '2026-06-01'. Date strings are converted to a git commit via rev-list.
    Includes both modified and untracked files.
    """
    # Try as a date first — if git rev-parse fails, interpret as --since date.
    try:
        subprocess.run(
            ["git", "rev-parse", "--verify", ref],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            check=True,
        )
        git_ref = ref
    except subprocess.CalledProcessError:
        # Treat as a date: find the earliest commit after that date.
        r = subprocess.run(
            ["git", "rev-list", "-1", f"--before={ref}", "HEAD"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        git_ref = r.stdout.strip() or "HEAD~50"

    # Changed tracked files.
    r = subprocess.run(
        ["git", "diff", "--name-only", git_ref, "--", "wiki/"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    changed = {line.strip() for line in r.stdout.splitlines() if line.strip()}

    # Untracked files in wiki/.
    r = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "wiki/"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    changed.update(line.strip() for line in r.stdout.splitlines() if line.strip())

    return sorted(f for f in changed if f.endswith(".md"))


# Rules a human must decide on (rewrite the graph, resolve identity, pick a value)
# vs. rules cleared mechanically by --fix or worked down as content. The review
# queue leads with decisions; the rest is summarized so the file stays skimmable.
DECISION_RULES = {
    "missing-frontmatter",
    "unparseable-frontmatter",
    "broken-wikilink",
    "naming-convention",
    "duplicate-slug",
    "invalid-value",
    "type-path-mismatch",
    "lifecycle-folder-mismatch",
    "dead-entity-ref",
    "island-situation-mismatch",
}
BACKLOG_HINT = {
    "missing-required-field": "run `wiki_lint.py --fix`",
    "relationships-in-frontmatter": "weave into body prose, then delete the field",
    "bare-wikilink": "add display aliases",
    "orphan": "link from a natural parent",
    "summary-stale": "write a concrete summary",
    "deadend": "add wikilinks to related pages",
    "tag-deprecated": "read the file; remove deprecated tag and choose canonical replacements",
    "tag-alias": "read the file; replace alias with canonical form shown in the fix message",
    "tag-unknown": "read the file; replace with canonical tags or propose adding to taxonomy",
    "tag-over-limit": "read the file; trim to ≤5 canonical tags",
    "tag-variant": "consolidate plural/singular tag variants",
    "singleton-property": "verify not a typo, or add to schema",
    "status-drift": "use the canonical status value",
    "parent-gap": "add wikilink in the parent page",
}


def write_report(issues, counts):
    """Write wiki/dm/review-queue.md — a committed, DM-facing snapshot. It's
    regenerated each run (no hand-edits survive), so it shrinks as issues are
    resolved; identity/lore judgment calls belong in wiki/discrepancy-log.md."""
    report_path = os.path.join(WIKI_DIR, "dm", "review-queue.md")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    decisions = sorted(
        [i for i in issues if i.rule in DECISION_RULES],
        key=lambda x: (SEVERITIES.index(x.severity), x.rule, x.path),
    )
    backlog = collections.Counter(
        i.rule for i in issues if i.rule not in DECISION_RULES
    )

    lines = [
        "---",
        "type: dm-intelligence",
        "subtype: review-queue",
        "campaign: shattered-sea",
        "status: active",
        "audience: agent",
        "publish: false",
        'summary: "Generated by wiki_lint.py on {d}. {n} items need a DM decision. '
        'Regenerated each run; do not hand-edit — fix the underlying file instead."'.format(
            d=today(), n=len(decisions)
        ),
        f"created: {today()}",
        f"updated: {today()}",
        "tags: [system, lint, review]",
        "sources: []",
        "---",
        "",
        "# Wiki Review Queue",
        "",
        f"Generated {today()}. **{len(decisions)} items need a decision** "
        f"({counts['error']} errors · {counts['warning']} warnings · "
        f"{counts['quality']} quality total).",
        "",
        "This file is regenerated by `wiki_lint.py --report` and shrinks as issues "
        "are resolved — don't hand-edit it; fix the file it points to. Identity and "
        "lore-contradiction calls live in `wiki/discrepancy-log.md`.",
        "",
        "## Decisions needed",
        "",
    ]
    if decisions:
        for i in decisions:
            fixpart = f" — _fix:_ {i.fix}" if i.fix else ""
            lines.append(
                f"- [{i.severity}] `{i.path}` **{i.rule}** — {i.detail}{fixpart}"
            )
    else:
        lines.append("_None — every detectable structural issue is resolved._")
    lines += ["", "## Backlog (mechanical / content)", ""]
    if backlog:
        for rule, n in backlog.most_common():
            hint = BACKLOG_HINT.get(rule, "")
            lines.append(f"- **{rule}**: {n}" + (f" — {hint}" if hint else ""))
    else:
        lines.append("_Clear._")
    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines).rstrip() + "\n")
    return rel(report_path)


# ---------------------------------------------------------------------------
# Batch grouping and priority ordering
# ---------------------------------------------------------------------------

RULE_PRIORITY = {
    "broken-wikilink": 1,
    "missing-frontmatter": 1,
    "unparseable-frontmatter": 1,
    "naming-convention": 2,
    "invalid-value": 2,
    "duplicate-slug": 2,
    "type-path-mismatch": 3,
    "lifecycle-folder-mismatch": 3,
    "dead-entity-ref": 4,
    "island-situation-mismatch": 4,
    "status-drift": 4,
    "missing-required-field": 5,
    "relationships-in-frontmatter": 6,
    "tag-deprecated": 7,
    "tag-alias": 7,
    "tag-unknown": 8,
    "tag-over-limit": 7,
    "tag-variant": 8,
    "summary-stale": 9,
    "orphan": 10,
    "deadend": 10,
    "bare-wikilink": 11,
    "parent-gap": 9,
    "singleton-property": 12,
}


def _batch_key(i: "Issue") -> tuple:
    return (i.rule, i.fix or "")


def batch_issues(issues: list["Issue"]) -> list[dict]:
    """Group issues that share the same rule + fix into batches."""
    groups = collections.defaultdict(list)
    for i in issues:
        groups[_batch_key(i)].append(i)

    batches = []
    for (rule, fix), items in groups.items():
        sev = min(items, key=lambda i: SEVERITIES.index(i.severity)).severity
        files = sorted({i.path for i in items})
        priority = RULE_PRIORITY.get(rule, 50)
        batches.append(
            {
                "rule": rule,
                "severity": sev,
                "fix": fix,
                "count": len(items),
                "files": files,
                "detail": items[0].detail
                if len(items) == 1
                else f"{len(items)} instances",
                "priority": priority,
            }
        )
    batches.sort(key=lambda b: (b["priority"], -b["count"]))
    return batches


def format_top_actions(issues: list["Issue"], n: int) -> str:
    """Format the top N highest-leverage batched actions."""
    batches = batch_issues(issues)
    lines = [
        f"TOP {min(n, len(batches))} ACTIONS (of {len(batches)} distinct issue types)"
    ]
    for i, b in enumerate(batches[:n], 1):
        fix_part = f"  →  {b['fix']}" if b["fix"] else ""
        if b["count"] == 1:
            lines.append(
                f"  {i}. [{b['severity']}] {b['rule']}  "
                f"{b['files'][0]}  {b['detail']}{fix_part}"
            )
        else:
            sample = ", ".join(b["files"][:3])
            more = f" +{b['count'] - 3} more" if b["count"] > 3 else ""
            lines.append(
                f"  {i}. [{b['severity']}] {b['rule']} × {b['count']}  "
                f"({sample}{more}){fix_part}"
            )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Diff against previous snapshot
# ---------------------------------------------------------------------------


def diff_snapshots(current_issues: list["Issue"], prev_path: str) -> str:
    """Compare current issues against a previous --json snapshot."""
    with open(prev_path, "r", encoding="utf-8") as fh:
        prev = json.load(fh)

    prev_counts = prev.get("summary", {})
    cur_counts = {
        s: sum(1 for i in current_issues if i.severity == s) for s in SEVERITIES
    }

    prev_by_rule = collections.Counter(i["rule"] for i in prev.get("issues", []))
    cur_by_rule = collections.Counter(i.rule for i in current_issues)

    all_rules = sorted(set(prev_by_rule) | set(cur_by_rule))

    lines = ["DIFF vs previous snapshot:"]

    for sev in SEVERITIES:
        p = prev_counts.get(sev, 0)
        c = cur_counts.get(sev, 0)
        delta = c - p
        arrow = "→" if delta == 0 else ("↑" if delta > 0 else "↓")
        lines.append(f"  {sev}: {p} {arrow} {c} ({delta:+d})")

    changed_rules = []
    for rule in all_rules:
        p = prev_by_rule.get(rule, 0)
        c = cur_by_rule.get(rule, 0)
        if p != c:
            changed_rules.append((rule, p, c))

    if changed_rules:
        lines.append("")
        lines.append("  Changed rules:")
        for rule, p, c in sorted(changed_rules, key=lambda x: x[1] - x[2]):
            delta = c - p
            marker = "IMPROVED" if delta < 0 else "REGRESSED"
            lines.append(f"    {rule}: {p} → {c} ({delta:+d}) {marker}")

    prev_files = {i["path"] for i in prev.get("issues", [])}
    new_files = sorted({i.path for i in current_issues} - prev_files)
    if new_files:
        lines.append(f"\n  New files with issues: {len(new_files)}")
        for f in new_files[:5]:
            lines.append(f"    {f}")
        if len(new_files) > 5:
            lines.append(f"    ... +{len(new_files) - 5} more")

    return "\n".join(lines)


def main(argv) -> int:
    ap = argparse.ArgumentParser(description="Lint the Shattered Sea wiki.")
    ap.add_argument(
        "paths", nargs="*", help="limit to these files/dirs (default: whole vault)"
    )
    ap.add_argument(
        "--fix", action="store_true", help="standardize frontmatter in place"
    )
    ap.add_argument(
        "--fix-tags",
        action="store_true",
        help="also fix safe tag issues (aliases, deprecated-fm/system tags)",
    )
    ap.add_argument(
        "--since",
        metavar="REF",
        help="only lint files changed since this git ref or date (e.g. HEAD~5, 2026-06-01, '3 days ago')",
    )
    ap.add_argument(
        "--report",
        action="store_true",
        help="also write the DM review queue to wiki/dm/review-queue.md",
    )
    ap.add_argument("--summary", action="store_true", help="print only the count line")
    ap.add_argument(
        "--min-severity",
        choices=SEVERITIES,
        default="quality",
        help="suppress issues below this severity (default: quality = show all)",
    )
    ap.add_argument("--json", action="store_true", help="emit issues as JSON to stdout")
    ap.add_argument(
        "--top",
        type=int,
        metavar="N",
        help="show the top N highest-leverage actions (batches identical issues)",
    )
    ap.add_argument(
        "--diff",
        metavar="SNAPSHOT",
        help="compare against a previous --json snapshot file and show deltas",
    )
    ap.add_argument(
        "--obsidian",
        choices=["auto", "on", "off"],
        default="auto",
        help="use Obsidian CLI for cross-file checks (default: auto-detect)",
    )
    ap.add_argument(
        "--markdown",
        choices=["auto", "on", "off"],
        default="auto",
        help="run markdownlint-cli2 for formatting checks (default: auto-detect)",
    )
    args = ap.parse_args(argv)

    # Resolve tool availability.
    use_obsidian = args.obsidian == "on" or (
        args.obsidian == "auto" and _obsidian_available()
    )
    use_markdown = args.markdown == "on" or (
        args.markdown == "auto" and MARKDOWNLINT_CLI is not None
    )
    if args.obsidian == "off":
        use_obsidian = False
    if args.markdown == "off":
        use_markdown = False

    if use_obsidian:
        sys.stderr.write("wiki_lint: Obsidian CLI active\n")
    if use_markdown:
        sys.stderr.write("wiki_lint: markdownlint-cli2 active\n")

    yaml = make_yaml()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as fh:
        schema = json.load(fh)
    validator = jsonschema.Draft202012Validator(schema)
    schema_props = set(schema.get("properties", {}).keys())

    scope = resolve_scope(args.paths)
    if args.since:
        since_files = files_changed_since(args.since)
        if scope:
            since_set = set(since_files)
            scope = [s for s in scope if s in since_set]
        else:
            scope = since_files
        if not scope:
            sys.stderr.write("wiki_lint: no wiki files changed since that ref\n")
            return 0
        sys.stderr.write(f"wiki_lint: --since {args.since} → {len(scope)} files\n")

    # --fix-tags implies --fix (tag fixes require frontmatter standardization).
    if args.fix_tags:
        args.fix = True

    # Auto-fix pass first (so the subsequent report reflects the fixed state).
    fixed = []
    if args.fix:
        for path in iter_wiki_files():
            relpath = rel(path)
            if not in_scope(relpath, scope):
                continue
            if os.path.basename(relpath) in SKIP_CONTENT:
                continue
            try:
                changed = apply_fix(path, relpath, yaml, fix_tags=args.fix_tags)
            except Exception as exc:
                sys.stderr.write(f"wiki_lint: fix error on {relpath}: {exc}\n")
                continue
            if changed:
                fixed.append((relpath, changed))
        for relpath, changed in fixed:
            sys.stderr.write(f"fixed: [{', '.join(changed)}] — {relpath}\n")

    # Report pass.
    records, parse_errors = gather_records(yaml)
    slug_to_paths = {}
    for relpath, data, body in records:
        slug_to_paths.setdefault(slug_of(relpath), []).append(relpath)

    all_issues = list(parse_errors)
    for relpath, data, body in records:
        if os.path.basename(relpath) not in SKIP_CONTENT:
            all_issues.extend(check_file(relpath, data, body, yaml, validator))
            naming = check_naming(relpath)
            if naming:
                all_issues.append(naming)

    cross = cross_file_checks(records, slug_to_paths, use_obsidian=use_obsidian)
    for relpath, file_issues in cross.items():
        all_issues.extend(file_issues)

    # Vault-wide checks.
    all_issues.extend(check_tags(records))
    all_issues.extend(check_tag_variants(records))
    all_issues.extend(check_singleton_properties(records, schema_props))
    all_issues.extend(check_lore_consistency(records, slug_to_paths))

    # markdownlint pass.
    if use_markdown:
        scope_paths = [os.path.join(REPO_ROOT, s) for s in scope] if scope else None
        all_issues.extend(_run_markdownlint(scope_paths))

    # Scope + severity filter.
    min_idx = SEVERITIES.index(args.min_severity)
    issues = [
        i
        for i in all_issues
        if in_scope(i.path, scope) and SEVERITIES.index(i.severity) <= min_idx
    ]

    counts = {
        s: sum(1 for i in all_issues if i.severity == s and in_scope(i.path, scope))
        for s in SEVERITIES
    }
    summary = (
        f"WIKI LINT: {counts['error']} errors · {counts['warning']} warnings · "
        f"{counts['quality']} quality"
        + (f" · {len(fixed)} files standardized" if args.fix else "")
    )

    # JSON output includes per-rule breakdown for snapshot diffing.
    by_rule = collections.Counter(i.rule for i in issues)
    if args.json:
        print(
            json.dumps(
                {
                    "summary": counts,
                    "by_rule": dict(by_rule.most_common()),
                    "fixed": fixed,
                    "issues": [asdict(i) for i in issues],
                },
                indent=2,
            )
        )
        return 1 if counts["error"] else 0

    report_path = None
    if args.report:
        report_path = write_report(issues, counts)

    sys.stderr.write(summary + "\n")
    if report_path:
        sys.stderr.write(f"wrote {report_path}\n")

    # --diff: compare against a previous snapshot.
    if args.diff:
        print(diff_snapshots(issues, args.diff))
        print()

    # --top N: priority-ordered batched action list.
    if args.top:
        print(format_top_actions(issues, args.top))
    elif not args.summary:
        for sev in SEVERITIES:
            sev_issues = [i for i in issues if i.severity == sev]
            if not sev_issues:
                continue
            print(f"{sev.upper()} ({len(sev_issues)})")
            for i in sorted(sev_issues, key=lambda x: (x.path, x.rule)):
                print(i.line())

    return 1 if counts["error"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
