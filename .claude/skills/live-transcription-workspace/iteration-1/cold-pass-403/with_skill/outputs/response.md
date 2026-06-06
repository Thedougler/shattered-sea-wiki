# Cold Pass 403 from HuggingFace

The 403 is coming from pyannote diarization, not from Whisper transcription. Here is why, and how to fix it.

## Why the hot pass works and the cold pass doesn't

The hot pass (`hot_pass.py`) only runs `mlx_whisper.transcribe` with the `whisper-medium-mlx` model. MLX Whisper models from `mlx-community/` are public and need no authentication.

The cold pass (`cold_pass.py`) does two things:

1. **Transcription** -- same `mlx_whisper.transcribe`, just with the larger `whisper-large-v3-mlx` model. Also public. This part works fine.
2. **Diarization** -- calls `diarize.py`, which loads `pyannote/speaker-diarization-3.1` via `Pipeline.from_pretrained()` using your `HF_TOKEN`. This is a gated model. The 403 is here.

## Root cause (pick whichever applies)

### 1. You haven't accepted the pyannote model license

Pyannote's speaker-diarization-3.1 is a gated model. Even with a valid HuggingFace token, you get a 403 until you explicitly accept the license on the model page.

**Fix:** Go to https://huggingface.co/pyannote/speaker-diarization-3.1, log in with the HuggingFace account that owns your `HF_TOKEN`, and click "Agree and access repository". You may also need to accept the license for the underlying segmentation model at https://huggingface.co/pyannote/segmentation-3.0.

### 2. Your HF_TOKEN expired or was regenerated

HuggingFace tokens can be revoked or rotated. If you recently regenerated your token, the old one returns 403.

**Fix:** Go to https://huggingface.co/settings/tokens, confirm the token is still active, and update your `HF_TOKEN` environment variable if it changed.

### 3. HF_TOKEN is set but with the wrong scope

HuggingFace fine-grained tokens need read access to gated models. A token scoped only to public repos or write-only will 403 on gated model downloads.

**Fix:** Ensure your token has at least `read` scope. If using a fine-grained token, it needs "Read access to contents of all repos you can access" enabled.

## How to verify the fix

```bash
cd tools/audio
source .venv/bin/activate
python -c "
import os
from pyannote.audio import Pipeline
p = Pipeline.from_pretrained(
    'pyannote/speaker-diarization-3.1',
    token=os.environ['HF_TOKEN']
)
print('OK')
"
```

If that prints `OK`, the cold pass will work. If it still 403s, your token or license acceptance is the issue.

## If you want to skip diarization entirely

The cold pass already handles this gracefully. In `cold_pass.py` lines 62-69, if diarization fails it logs a warning and continues without diarization labels -- speaker ID still works via voice profiles alone. But the 403 error may be noisy in the logs.

To suppress the attempt entirely, pass `skip_diarize=True` when constructing `ColdPass`, or add `skip_diarize: true` to your config if the CLI supports it.

## Most likely diagnosis

It is almost certainly cause #1 -- you have a valid `HF_TOKEN` (which is why nothing else complains), but you haven't clicked "Agree" on the pyannote model page. This is the most common reason people hit this exact error, and it is a one-time action per HuggingFace account.
