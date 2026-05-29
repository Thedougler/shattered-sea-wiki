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
machine-readable output; ``--report`` also writes ``wiki/lint-report.md`` so the list
survives across sessions. Exit code is 1 when any *error* is present (warnings and
quality notes do not fail), so it can gate a commit.

Usage:
    wiki_lint.py                      # lint whole vault, report only
    wiki_lint.py --fix                # standardize all frontmatter, then report
    wiki_lint.py --fix wiki/entities/characters/npcs/foo.md   # one file
    wiki_lint.py --summary            # just the counts
    wiki_lint.py --report             # also write wiki/lint-report.md
    wiki_lint.py --min-severity error # only errors
    wiki_lint.py --json               # machine-readable
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from typing import Optional

import jsonschema
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

from wiki_common import (
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
    "lint-report.md",
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
    "lint-report.md",
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
    ".webp", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".bmp", ".pdf",
    ".mp3", ".mp4", ".mov", ".wav", ".ogg", ".json", ".canvas", ".excalidraw",
}

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


FLOW_LIST_FIELDS = ("tags", "sources", "aliases")


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
    if expected_type not in ("unknown", "governance") and actual_type and actual_type != expected_type:
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
    rels = relationship_entries(data.get("relationships")) if hasattr(data, "get") else []
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
        if folder in ("active", "dormant", "resolved") and lifecycle and lifecycle != folder:
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

def cross_file_checks(records, slug_to_paths):
    """records: list of (relpath, data, body). Returns dict relpath -> [Issue]."""
    by_file = {r[0]: [] for r in records}
    inbound = {r[0]: set() for r in records}
    # Obsidian resolves wikilinks case-insensitively; match on lowered slugs.
    lower_index = {}
    for slug, paths in slug_to_paths.items():
        lower_index.setdefault(slug.lower(), []).extend(paths)

    for relpath, data, body in records:
        if os.path.basename(relpath) in SKIP_AS_SOURCE:
            continue  # generated catalogs / bookkeeping aren't link sources
        scan = scannable(body)
        seen_broken = set()
        for target, has_alias, is_embed in wikilink_targets(scan):
            if is_asset(target):
                continue  # attachment, not a page
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
            else:
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

    # 0. Drop an empty `relationships: []` — relationships live in the body now,
    #    and an empty list carries nothing to migrate, so removing it is safe.
    #    Populated relationships are left untouched for the agent to weave in.
    rel = data.get("relationships")
    if isinstance(rel, list) and len(rel) == 0:
        del data["relationships"]
        changed.append("-relationships")

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

    # 3. Render short list fields in flow style ([a, b]) deterministically.
    #    Rebuild as a flow CommentedSeq so the result is identical whether the
    #    field arrived as a plain default list or an authored block sequence —
    #    otherwise the first --fix and the second would disagree (block → flow).
    for field in FLOW_LIST_FIELDS:
        node = data.get(field)
        if isinstance(node, list):
            seq = CommentedSeq(node)
            seq.fa.set_flow_style()
            data[field] = seq

    # 4. Canonical key order: required first (in canonical order), then the rest
    #    in their existing order.
    order = [f for f in required_fields(relpath) if f in data]
    order += [k for k in data if k not in order]
    if list(data.keys()) != order:
        changed.append("(reorder)")
    new = CommentedMap()
    for k in order:
        new[k] = data[k]
    return new, changed


def dump_frontmatter(data, yaml: YAML) -> str:
    buf = io.StringIO()
    yaml.dump(data, buf)
    return buf.getvalue().rstrip("\n")


FM_BLOCK_RE = re.compile(r"^---[ \t]*\n(.*?\n)---[ \t]*\n?", re.DOTALL)


def apply_fix(path: str, relpath: str, yaml: YAML):
    """Standardize frontmatter in place, preserving the body byte-for-byte.

    Only the frontmatter block is rewritten; everything after the closing fence
    (including the exact trailing newline) is spliced back untouched. Returns the
    list of changed fields, or [] when the file is already canonical (a true
    no-op — nothing is written)."""
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    m = FM_BLOCK_RE.match(text)
    if m:
        fm_text = m.group(1)
        body = text[m.end():]  # verbatim, including its leading/trailing newlines
    else:
        fm_text = ""
        body = text

    data = load_frontmatter(yaml, fm_text)
    new_data, changed = standardize(relpath, data, yaml)
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
                Issue("error", "unparseable-frontmatter", relpath, str(exc).splitlines()[0])
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


def write_report(issues, counts):
    report_path = os.path.join(WIKI_DIR, "lint-report.md")
    lines = [
        "---",
        "type: system",
        "subtype: lint-report",
        "campaign: shattered-sea",
        "status: active",
        "audience: agent",
        "publish: false",
        'summary: "Generated by wiki_lint.py on {d}. '
        '{e} errors, {w} warnings, {q} quality notes. Do not hand-edit."'.format(
            d=today(), e=counts["error"], w=counts["warning"], q=counts["quality"]
        ),
        f"created: {today()}",
        f"updated: {today()}",
        "tags: [system, lint]",
        "sources: []",
        "---",
        "",
        "# Wiki Lint Report",
        "",
        f"Generated {today()} — {counts['error']} errors · "
        f"{counts['warning']} warnings · {counts['quality']} quality.",
        "",
        "Auto-fixable frontmatter is already handled by `--fix`; what remains here "
        "needs judgment or a cross-file change. Each line ends with a suggested action.",
        "",
    ]
    for sev in SEVERITIES:
        sev_issues = [i for i in issues if i.severity == sev]
        if not sev_issues:
            continue
        lines.append(f"## {sev.upper()} ({len(sev_issues)})")
        lines.append("")
        for i in sorted(sev_issues, key=lambda x: (x.path, x.rule)):
            fixpart = f" — _fix:_ {i.fix}" if i.fix else ""
            lines.append(f"- `{i.path}` **{i.rule}** — {i.detail}{fixpart}")
        lines.append("")
    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines).rstrip() + "\n")
    return rel(report_path)


def main(argv) -> int:
    ap = argparse.ArgumentParser(description="Lint the Shattered Sea wiki.")
    ap.add_argument("paths", nargs="*", help="limit to these files/dirs (default: whole vault)")
    ap.add_argument("--fix", action="store_true", help="standardize frontmatter in place")
    ap.add_argument("--report", action="store_true", help="also write wiki/lint-report.md")
    ap.add_argument("--summary", action="store_true", help="print only the count line")
    ap.add_argument(
        "--min-severity",
        choices=SEVERITIES,
        default="quality",
        help="suppress issues below this severity (default: quality = show all)",
    )
    ap.add_argument("--json", action="store_true", help="emit issues as JSON to stdout")
    args = ap.parse_args(argv)

    yaml = make_yaml()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as fh:
        schema = json.load(fh)
    validator = jsonschema.Draft202012Validator(schema)

    scope = resolve_scope(args.paths)

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
                changed = apply_fix(path, relpath, yaml)
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

    cross = cross_file_checks(records, slug_to_paths)
    for relpath, issues in cross.items():
        all_issues.extend(issues)

    # Scope + severity filter.
    min_idx = SEVERITIES.index(args.min_severity)
    issues = [
        i
        for i in all_issues
        if in_scope(i.path, scope) and SEVERITIES.index(i.severity) <= min_idx
    ]

    counts = {s: sum(1 for i in all_issues if i.severity == s and in_scope(i.path, scope)) for s in SEVERITIES}
    summary = (
        f"WIKI LINT: {counts['error']} errors · {counts['warning']} warnings · "
        f"{counts['quality']} quality"
        + (f" · {len(fixed)} files standardized" if args.fix else "")
    )

    if args.json:
        print(json.dumps({"summary": counts, "fixed": fixed, "issues": [asdict(i) for i in issues]}, indent=2))
        return 1 if counts["error"] else 0

    report_path = None
    if args.report:
        report_path = write_report(issues, counts)

    sys.stderr.write(summary + "\n")
    if report_path:
        sys.stderr.write(f"wrote {report_path}\n")

    if not args.summary:
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
