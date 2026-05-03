# Install Guide — Mac (Python path)

The developer-friendly path. Uses `openai-whisper` and `yt-dlp`'s Python API, and packages everything as an installable CLI named `video-transcribe`.

**Just want to transcribe a video?** Use the **[bash path](../bash/install.md)** instead — it has zero Python dependencies.

---

## ⚡ Fast Track

If you already have Homebrew, Python 3.11+, and `ffmpeg` installed:

```bash
git clone https://github.com/TheDeLay/video-transcriber.git
cd video-transcriber/python
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
video-transcribe "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

The first `pip install` pulls down PyTorch (~2 GB). Be patient.

**Don't have those prerequisites?** See the [Detailed Walkthrough](#detailed-walkthrough) below.

---

## Detailed Walkthrough

### Prerequisites

- macOS (Apple Silicon recommended)
- Python 3.11 or newer
- `ffmpeg` (Whisper uses it under the hood)

### Step 1 — Install Homebrew (if you don't already have it)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2 — Install Python and ffmpeg

```bash
brew install python ffmpeg
```

Verify:

```bash
python3 --version   # should be 3.11+
ffmpeg -version | head -1
```

### Step 3 — Clone and install

```bash
git clone https://github.com/TheDeLay/video-transcriber.git
cd video-transcriber/python
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

The `pip install` step pulls down PyTorch and is slow (~2 GB). Be patient.

### Step 4 — Run it

```bash
video-transcribe "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

Outputs land in `~/Desktop` by default (override with `--output-dir`). The AI prompt is copied to your clipboard automatically.

---

## Options

```
video-transcribe URL [OPTIONS]

  --model TEXT          Whisper model: tiny, base, small, medium, large
                        (append .en for English-only, e.g. small.en)
                        [default: small.en]
  --language TEXT       Language code (en, es, fr, ...). Default: auto-detect.
  --output-dir PATH     Where to write transcript and prompt. [default: ~/Desktop]
  --formats TEXT        Comma-separated output formats: txt,srt,vtt,json,tsv
                        [default: txt,srt]
  --no-clipboard        Skip copying the prompt to clipboard.
  --keep-audio          Keep the downloaded audio file (default: deleted).
  --help                Show help.
```

## Why this path uses `openai-whisper` and not `whisper.cpp`

The bash path uses `whisper.cpp` because it's lighter for non-developers. The Python path uses `openai-whisper` because:

- It's the canonical Python API — easy to extend, debug, and integrate
- Word-level timestamps and other advanced features are first-class
- If you're already in a Python environment, the install is fewer moving parts than calling out to a native binary

If you want to swap in `whisper.cpp` or `mlx-whisper` for speed, the transcription step is isolated to `video_transcriber/cli.py:_transcribe()`.

## Updating

```bash
cd video-transcriber
git pull
cd python
source .venv/bin/activate
pip install -e . --upgrade
```
