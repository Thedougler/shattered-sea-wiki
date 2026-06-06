# Cold Pass 403 from HuggingFace — Diagnosis

## Root Cause

The cold pass uses **pyannote/speaker-diarization-3.1** for diarization, which is a gated model on HuggingFace. The hot pass does not use it. That is why only the cold pass hits a 403.

## The Code Path

The two passes use completely different model stacks:

- **Hot pass** (`hot_pass.py`): Uses `mlx_whisper.transcribe()` with `mlx-community/whisper-medium-mlx`. This is an open (ungated) model on HuggingFace. Speaker identification comes from local `resemblyzer` voice profile embeddings only — no HuggingFace API call needed.

- **Cold pass** (`cold_pass.py` line 66): Calls `diarize(chunk.wav_path)`, which loads `pyannote/speaker-diarization-3.1` via `Pipeline.from_pretrained()` in `diarize.py` (line 36-38). That call requires a HuggingFace token (`HF_TOKEN`) **and** explicit acceptance of the model's license terms on the HuggingFace website.

A 403 from HuggingFace on a gated model means one of two things:

### 1. You have not accepted the pyannote model license (most likely)

`pyannote/speaker-diarization-3.1` is a gated model. Even with a valid `HF_TOKEN`, HuggingFace returns 403 until you manually accept the license terms on the model page. You need to accept terms on **both** of these:

- <https://huggingface.co/pyannote/speaker-diarization-3.1>
- <https://huggingface.co/pyannote/segmentation-3.0> (a dependency of the diarization pipeline)

Log in to HuggingFace with the same account that owns the `HF_TOKEN`, visit each page, and click "Agree and access repository."

### 2. Your HF_TOKEN is missing, expired, or wrong

`diarize.py` (line 30) reads the token from `os.environ.get("HF_TOKEN")`. Verify it is set in the shell where you run the live session:

```
echo $HF_TOKEN
```

If it is empty, set it. If it is set, verify it is still valid — HuggingFace tokens can be revoked or expired. Generate a new one at <https://huggingface.co/settings/tokens> if needed. The token needs at least `read` scope.

## Why the Hot Pass Is Unaffected

The hot pass never touches pyannote. It transcribes with mlx-whisper (an open model that gets downloaded and cached locally with no auth) and identifies speakers using resemblyzer embeddings computed entirely on-device. No HuggingFace API call happens during hot pass execution.

## Quick Fix Checklist

1. Go to <https://huggingface.co/pyannote/speaker-diarization-3.1> and accept the license.
2. Go to <https://huggingface.co/pyannote/segmentation-3.0> and accept the license.
3. Confirm `HF_TOKEN` is set and valid: `echo $HF_TOKEN`
4. Re-run the live session. The cold pass should now load the pipeline without a 403.

## Workaround

If you need to run a session right now and cannot resolve the token/license issue, pass `--no-diarize` to skip diarization entirely. The cold pass will still run its full-accuracy whisper transcription; you just lose automatic speaker diarization (voice profile matching still works).

Note: `cold_pass.py` already has a try/except around the diarize call (lines 62-69) that logs a warning and continues without diarization if it fails. If the 403 is raising an exception caught by that block, the cold pass may actually be completing — just without diarization. Check your logs for `"Diarization unavailable:"` warnings. If you see those, the cold pass *is* working, just falling back to profile-only speaker ID. If instead the 403 is a hard crash, the exception may not be the type caught by that broad `except Exception` — but it should be. Check the full traceback to confirm.
