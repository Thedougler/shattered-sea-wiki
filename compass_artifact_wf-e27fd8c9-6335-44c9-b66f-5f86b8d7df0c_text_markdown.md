# Detecting Laughter in Audio Locally on a MacBook Air M4: Models, Tools, and a Recommended Pipeline

## TL;DR
- **Use a purpose-built laughter model, not a general tagger.** The strongest local option is the Interspeech 2024 **omine-me/LaughterSegmentation** (wav2vec2-based, ~315M params, MIT-licensed code) which outputs precise start/end timestamps and beats the prior standard; the StandUp4AI authors (arXiv:2505.18903) explicitly switched to "the state-of-the-art model of Omine et al. (2024), which has shown better performances for this task." For a lighter, permissively-licensed path, **jrgillick/laughter-detection** (ResNet, threshold-tunable) is the proven workhorse.
- **General audio taggers (YAMNet, PANNs CNN14, AST) all include a "Laughter" AudioSet class** and run fine on Apple Silicon, but they are clip/frame taggers needing your own windowing + smoothing, and they confuse laughter with other excited vocal sounds (cheering, crying, screaming). They're best as a fast first-pass or feature extractor.
- **Everything here runs comfortably on a 16GB M4.** Use PyTorch's MPS backend with `PYTORCH_ENABLE_MPS_FALLBACK=1`; for the lightest footprint use YAMNet (3.7M params) or PANNs via `panns_inference`. Apple's own built-in **SoundAnalysis** classifier even ships native `laughter`/`giggling`/`baby_laughter` classes with timestamps.

## Key Findings

1. **Dedicated laughter models exist and are the best choice.** Two mature open-source projects specifically target laughter detection/segmentation with timestamp output: jrgillick/laughter-detection (Interspeech 2021) and omine-me/LaughterSegmentation (Interspeech 2024). The latter is state-of-the-art.
2. **General taggers include laughter as a labeled class.** YAMNet, PANNs, and AST are all trained on AudioSet, whose ontology has six laughter-related classes: Laughter, Baby laughter, Giggle, Snicker, Belly laugh, and "Chuckle, chortle."
3. **Toolkits like pyAudioAnalysis/openSMILE don't ship a ready laughter classifier** — they provide features/energy methods you must train or threshold yourself. Energy-based peak detection is unreliable.
4. **LLM/multimodal audio models (Qwen2-Audio) can describe laughter** but are heavyweight and don't natively give burst timestamps; better for verification than for segmentation.
5. **Apple Silicon support is good** across PyTorch MPS, ONNX, Core ML, and MLX, with known MPS operator gaps mitigated by a CPU fallback flag.
6. **The most accurate, lowest-false-positive route is a dedicated model with post-processing** (merge gaps, drop short segments, tune threshold).

## Details

### 1 & 2. Dedicated laughter models and general taggers

**omine-me/LaughterSegmentation (Interspeech 2024) — recommended for accuracy.** Taisei Omine, Kenta Akita, Reiji Tsuruno, "Robust Laughter Segmentation with Automatic Diverse Data Synthesis" (doi:10.21437/Interspeech.2024-1644). It extends **wav2vec 2.0** for time-series frame classification, built on the `jonatasgrosman/wav2vec2-large-xlsr-53-english` checkpoint, ~315M parameters, classifying roughly every 0.02s. It takes 7.0s windows (overlapping by 2s for longer files). On its own podcast-derived eval set it achieved detection Accuracy 0.943 / Precision 0.932 / Recall 0.955 / F1 0.943, and importantly improved segmentation **start-time mean absolute error to ~0.31s** vs ~1.5s for the older Gillick model. On the AMI corpus it scored F1 0.784 vs Gillick's 0.583. Per the GitHub README it requires `torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2`, "Python<=3.11 is required," and it was "Tested on Windows 11 with GeForce RTX 2060 SUPER." Code is MIT-licensed; the trained `model.safetensors` (1.26 GB) on Hugging Face is research-use-only. It outputs JSON. Reported speed: ~1 minute to segment an hour of audio on an RTX 2080 Ti GPU. Its superiority is independently corroborated by StandUp4AI (arXiv:2505.18903), whose authors moved from Gillick to "the state-of-the-art model of Omine et al. (2024), which has shown better performances for this task."

**jrgillick/laughter-detection (Interspeech 2021) — recommended for simplicity/license.** Jon Gillick et al., "Robust Laughter Detection in Noisy Environments." A ResNet over spectrograms trained on Switchboard, with AudioSet eval annotations. CLI: `python segment_laughter.py --input_audio_file=x.wav --output_dir=./out --min_length=0.2 --threshold=0.5`. The threshold (0–1) directly trades precision vs recall, and it can save segments as audio files or TextGrid. There's a maintained Python 3.11 fork (Mega-Gorilla/laughter-detection) using PyTorch. This is the model most widely reused in academic humor/laughter pipelines.

**YAMNet (Google).** MobileNet-v1, 521 AudioSet classes including Laughter (+ Baby laughter, Giggle, Snicker, Belly laugh, "Chuckle, chortle"). Only 3.7M weights, 69.2M multiplies per 0.96s frame; processes 16kHz mono, one frame every 0.48s. Per TensorFlow's official YAMNet README: "On the 20,366-segment AudioSet eval set, over the 521 included classes, the balanced average d-prime is 2.318, balanced mAP is 0.306, and the balanced average lwlrap is 0.393" — these are across all 521 classes, not laughter specifically. Excellent as a fast first-pass; needs calibration/fine-tuning per Google's own guidance. Note: relies on Keras 2 / TensorFlow, incompatible with Keras 3.

**PANNs CNN14 (Qiuqiang Kong).** Trained on AudioSet, 527 classes, 81M params, overall mAP 0.431 (Wavegram-Logmel-CNN variant 0.439). Dead-simple inference via `pip install panns_inference` exposing `AudioTagging` (clip-level) and `SoundEventDetection` (framewise, using `Cnn14_DecisionLevelMax_mAP=0.385.pth`). The SED model gives framewise probabilities you can threshold to get laughter timestamps. Supports `device='cpu'` or `'cuda'`; on Mac you'd run CPU or adapt to MPS.

**AST (Audio Spectrogram Transformer, MIT).** `MIT/ast-finetuned-audioset-10-10-0.4593` on Hugging Face, a transformer over spectrograms and the strongest pure tagger. Per Gong, Chung & Glass, "AST: Audio Spectrogram Transformer" (Interspeech 2021, arXiv:2104.01778), the weight-averaged model "achieves an mAP of 0.459±0.000, which is our best single model," while Ensemble-M "achieves an mAP of 0.485, this is our best full model on AudioSet." Integrated in HF Transformers (`ASTForAudioClassification`), easy to run on MPS. Clip-level by default; you window it yourself.

**Per-class laughter accuracy is not separately published.** None of YAMNet, PANNs CNN14, AST, or the Google AudioSet baseline publish an explicit numeric Average Precision for the "Laughter" class (AudioSet index 16, /m/01j3sz); class-wise AP appears only as sorted bar-chart figures (PANNs paper Fig. 3/Fig. 12; PSLA Fig. 7). Published nearby anchors: the "Speech" class reaches AP ≈ 0.80 in PANNs CNN14 and PSLA; "Music" ≈ 0.896 in the Google baseline (Gemmeke et al.); while fine-grained vocal classes can be much lower (PSLA, arXiv:2102.01243, reports Male/Female/Child Speech AP of 0.07/0.09/0.45). To get an exact laughter number you must run the released checkpoint on the AudioSet eval set yourself and compute `average_precision_score` for class index 16.

### 3. Speech/audio toolkits
**pyAudioAnalysis** provides feature extraction, segmentation, and SVM/classifier training, but ships **no pretrained laughter classifier** — community examples use crude energy-threshold peak detection (high false positives) or train your own SVM on features. **openSMILE** offers the ComParE/IS13 paralinguistics feature sets (`config/is09-13/IS13_ComParE_Voc.conf` was literally the Interspeech 2013 vocalizations/laughter sub-challenge config), but again it's a feature extractor you must pair with a classifier. **Kaldi** is ASR-oriented and not a laughter tool. Verdict: use these only if you intend to train a custom model.

### 4. LLM-based / multimodal
**Qwen2-Audio** (Alibaba, built on a Whisper-large-v3 encoder + Qwen LLM) sets a new SOTA on Vocal Sound Classification — the Qwen2-Audio Technical Report (Chu et al., arXiv:2407.10759) reports "Vocal Sound Classification (VocalSound): 92.9%–93.9% accuracy, setting new SOTA" (VocalSound's classes include laughter, sighs, coughs, etc.). It can answer "is there laughter?" and describe audio, but it does not natively emit laughter burst timestamps and is heavy (7B). On 16GB it's feasible only quantized and slowly. Best used to **verify/label** candidate clips, not to scan a long file. **Whisper-AT** (Yuan Gong, MIT) is a clever middle path: it adds 527-class AudioSet tagging (including Laughter) on top of Whisper ASR for <1% extra compute, with a configurable `at_time_res` (multiple of 0.4s) so you get audio-event tags at chosen temporal resolution alongside the transcript. The recent **TIC-TALK** stand-up-comedy pipeline (Zribi, Cafiero, Lépinay & Vidal-Gorène, arXiv:2603.21803), spanning "90 professionally filmed stand-up comedy specials (2015–2024)," "combines BERTopic for 60s thematic segmentation … Whisper-AT for 0.8 s laughter detection" — a direct precedent for exactly this use case.

### 5. Apple Silicon / M4 compatibility
- **PyTorch MPS**: All PyTorch models here (LaughterSegmentation, jrgillick, PANNs, AST, Qwen2-Audio) can target `mps`. Requires macOS 12.3+. Some ops aren't implemented on MPS (wav2vec2 historically hit `aten::_weight_norm_interface`); set `PYTORCH_ENABLE_MPS_FALLBACK=1` to fall back to CPU per-op. The whole model must fit in unified memory (no CPU offload), which is fine at 16GB for these sizes. Older macOS (<15) had silent MPS kernel bugs (e.g., `addcmul_`/`addcdiv_` on non-contiguous tensors); keep macOS and PyTorch current.
- **YAMNet**: TensorFlow/TF-Hub or the `.tflite` build; also convertible to Core ML. Runs on CPU very fast (~100ms per 2s of audio reported on a phone).
- **Core ML / SoundAnalysis**: Apple's native **SoundAnalysis** framework ships a built-in classifier (`SNClassifySoundRequest` `version1`) recognizing 300+ sounds including native `laughter`, `baby_laughter`, and `giggling` classes, returns confidence + timestamp per window (window 0.5–15s), and is hardware-accelerated. This is the lowest-effort, most Mac-native route if you're willing to write a little Swift.
- **MLX / ONNX**: MLX has excellent Whisper ports (mlx-whisper, lightning-whisper-mlx with 4-bit quant) for the ASR side; there's no dedicated laughter MLX model, but AST/PANNs export cleanly to ONNX for `onnxruntime` on Mac.

### 6. Recommended pipeline (Python, runs on M4)
**Best path (accuracy):** clone omine-me/LaughterSegmentation, download `model.safetensors`, run `python inference.py --audio_path your.wav` → JSON of laughter segments with start/end. The model already does internal 7s windowing with 2s overlap and post-processing (merges segments <0.2s apart, drops <0.2s). Set device to mps with the fallback flag.

**Simplest robust path:** jrgillick — `python segment_laughter.py --input_audio_file=x.wav --threshold=0.5 --min_length=0.2`. Lower threshold → more recall/more false positives.

**DIY tagger path (full control), conceptual code:**
```python
import torch, librosa, numpy as np
from transformers import ASTForAudioClassification, ASTFeatureExtractor

device = "mps" if torch.backends.mps.is_available() else "cpu"
model = ASTForAudioClassification.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593").to(device)
fe = ASTFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
labels = model.config.id2label
laugh_ids = [i for i,l in labels.items()
             if any(k in l.lower() for k in ("laugh","giggle","chuckle","snicker"))]

wav, sr = librosa.load("input.wav", sr=16000, mono=True)
win, hop = int(1.0*sr), int(0.5*sr)        # 1s window, 0.5s hop
events = []
for start in range(0, len(wav)-win, hop):
    seg = wav[start:start+win]
    inp = fe(seg, sampling_rate=16000, return_tensors="pt").to(device)
    with torch.no_grad():
        probs = torch.sigmoid(model(**inp).logits)[0]
    score = probs[laugh_ids].max().item()
    events.append((start/sr, score))
# threshold + merge contiguous windows into bursts, drop short ones
```
Run with `PYTORCH_ENABLE_MPS_FALLBACK=1 python script.py`. For PANNs, swap in `panns_inference.SoundEventDetection` whose `framewise_output` gives per-frame class probabilities directly (then index the laughter columns and threshold).

### 7. Accuracy & false positives
- **Dedicated models win on precision.** The Gillick model is high-precision/lower-recall by default (tune threshold down to recover laughs). The Omine model is more balanced and far more accurate on start-time localization (~0.31s MAE vs ~1.5s).
- **Common failure modes for general taggers:** confusing laughter with **cheering, applause, crying/sobbing, screaming, baby cry, and excited speech** — these are acoustically adjacent and share AudioSet neighbors. Singing/vibrato can also trigger false positives; the Omine paper specifically notes vibrato in music and bursts of laughter sometimes share frequencies. Background noise sharply degrades all models (the entire premise of the Gillick "noisy environments" paper).
- **Mitigations:** require a minimum burst length (≥0.2–0.3s), merge nearby detections, raise threshold, and optionally **cross-check candidates with a second model** (e.g., confirm AST/PANNs hits with the Gillick model, or have Qwen2-Audio verify a handful of highlight candidates).

## Recommendations
1. **Start with omine-me/LaughterSegmentation** on your M4 (PyTorch + MPS, `PYTORCH_ENABLE_MPS_FALLBACK=1`). It directly outputs timestamped JSON and is the current SOTA. Mind the research-only model license for any commercial use.
2. **If you want minimal dependencies or a permissive license**, use jrgillick/laughter-detection (or the Py3.11 fork) and tune `--threshold` (start 0.5; lower to ~0.3 for more recall) and `--min_length 0.2`.
3. **If you want a quick baseline or are already transcribing**, add Whisper-AT (`at_time_res=0.8–1.0`, as TIC-TALK used 0.8s) to get laughter tags alongside the transcript at <1% extra cost — ideal since you likely want highlight clips with context.
4. **If you prefer a native Mac, zero-Python-model route**, use Apple's SoundAnalysis built-in classifier (Swift) — it has a real `laughter` class with timestamps and Neural Engine acceleration.
5. **Build post-processing regardless of model:** merge detections <0.2s apart, drop bursts <0.3s, and set a confidence threshold. **Thresholds that should change your approach:** if precision is too low (too many false highlights), raise the threshold and add a second-model cross-check; if you're missing obvious laughs (low recall), lower the threshold or switch from a general tagger to the dedicated Omine model. Calibrate on ~10–20 minutes of your own hand-labeled audio.
6. **Reserve Qwen2-Audio for verification**, not scanning — run it only on candidate clips to confirm genuine laughter.

## Caveats
- The Omine model checkpoint is **research-use-only**; the code is MIT. Check licensing before any commercial deployment.
- **No published per-class "Laughter" AP** exists for YAMNet/PANNs/AST; their headline mAP numbers (YAMNet 0.306, PANNs 0.431, AST 0.459 single) are across all classes and should not be read as laughter accuracy.
- Reported speeds (e.g., "1 minute per hour of audio" for Omine; "~100ms per 2s" for YAMNet) are on **NVIDIA GPUs or phones**; expect different throughput on M4 MPS, though still well faster than real-time for these model sizes. Exact M4 throughput for these specific laughter models was not benchmarked in available sources — plan to measure.
- MPS remains a **beta backend**; keep macOS (ideally 15+) and PyTorch updated, and use the CPU fallback flag to avoid unsupported-op crashes (notably with wav2vec2-based models like Omine's).
- Energy/threshold methods (pyAudioAnalysis examples) are **not reliable** for distinguishing laughter from other loud/excited sounds — avoid them as a primary detector.
- General taggers were trained largely on YouTube audio; expect a **domain mismatch** on your specific recordings and budget for threshold calibration on a small labeled sample of your own audio.

### Quick reference — links
- omine-me/LaughterSegmentation — github.com/omine-me/LaughterSegmentation (model on HF: huggingface.co/omine-me/LaughterSegmentation)
- jrgillick/laughter-detection — github.com/jrgillick/laughter-detection (Py3.11 fork: github.com/Mega-Gorilla/laughter-detection)
- PANNs — github.com/qiuqiangkong/audioset_tagging_cnn; `pip install panns_inference`
- AST — huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593
- YAMNet — github.com/tensorflow/models/tree/master/research/audioset/yamnet
- Whisper-AT — github.com/YuanGongND/whisper-at; `pip install whisper-at`
- Apple SoundAnalysis — developer.apple.com/documentation/soundanalysis
- Qwen2-Audio — github.com/QwenLM/Qwen2-Audio