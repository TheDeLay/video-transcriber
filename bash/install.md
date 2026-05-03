# Install Guide — Mac (bash path)

You will **not** need to learn or install Python. Everything runs as native Mac apps. Apple Silicon Macs (M1/M2/M3/M4) are recommended; Intel Macs work but transcription will be slower.

---

## ⚡ Fast Track

**Just want it working?** Open Terminal (`⌘ + Space`, type `Terminal`, press `Return`), then paste each of these blocks one at a time. Press `Return` after each, and wait for the `$` prompt to come back before pasting the next.

```bash
# 1. Install Homebrew (skip if you already have `brew`)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```bash
# 2. Install the three tools
brew install whisper-cpp ffmpeg yt-dlp
```

```bash
# 3. Download the Whisper model (one-time, ~500 MB)
mkdir -p ~/.whisper-models && \
  curl -L -o ~/.whisper-models/ggml-small.en.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin
```

```bash
# 4. Get the script
cd ~ && git clone https://github.com/TheDeLay/video-transcriber.git && \
  cd video-transcriber && chmod +x bash/transcribe.sh
```

```bash
# 5. Run it — replace the URL with your video
./bash/transcribe.sh "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

That's it. When it finishes you'll have a transcript on your Desktop and an AI prompt on your clipboard. Paste it into Gemini, ChatGPT, NotebookLM, or Claude.

**Stuck?** Read the [Detailed Walkthrough](#detailed-walkthrough) below — every step is explained.

---

## Detailed Walkthrough

### Step 1 — Open Terminal

Press `⌘ + Space` to open Spotlight, type `Terminal`, press `Return`.

A black or white window opens with a blinking cursor. This is where you'll paste commands. To run a command: paste it, press `Return`, wait until you see the cursor again.

### Step 2 — Install Homebrew (one-time)

Homebrew is the standard "app store for the Terminal" on Macs. It's how we'll install everything else.

Paste this into Terminal and press `Return`:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

It will:
1. Ask for your Mac password (the one you use to log in). You won't see the characters as you type — that's normal. Press `Return` when done.
2. Show a list of what it's about to do. Press `Return` to continue.
3. Take 5–10 minutes. Lots of text will scroll by — that's fine.

When it finishes, it may print **two lines** under a heading like "Next steps:" that begin with `(echo ...` and `eval ...`. **Copy and paste those two lines into Terminal exactly as shown** and press `Return` after each. This adds Homebrew to your shell so the `brew` command works. (If you don't see those lines, you can skip this — Homebrew is already configured.)

Verify Homebrew is installed:

```bash
brew --version
```

You should see something like `Homebrew 4.x.x`.

### Step 3 — Install the three tools

Paste this single command:

```bash
brew install whisper-cpp ffmpeg yt-dlp
```

This installs:
- **whisper-cpp** — the speech-to-text engine (a fast, native version of OpenAI's Whisper)
- **ffmpeg** — handles audio/video formats
- **yt-dlp** — downloads YouTube videos

Takes 2–5 minutes. When it's done, verify:

```bash
whisper-cli --help | head -5
yt-dlp --version
ffmpeg -version | head -1
```

Each command should print a few lines. If any one says `command not found`, see [Troubleshooting](#troubleshooting) at the bottom.

### Step 4 — Download a Whisper model (one-time)

Whisper needs a "model file" to do transcription. You only download this once. We recommend **small.en** (~500 MB) — fast and accurate for English videos. If you want maximum accuracy and don't mind it taking longer, use **medium.en** (~1.5 GB).

Paste:

```bash
mkdir -p ~/.whisper-models
cd ~/.whisper-models
curl -L -O https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin
```

Takes a few minutes depending on your internet. When done, verify:

```bash
ls -lh ~/.whisper-models/
```

You should see `ggml-small.en.bin` listed at around 488M.

> **Tip:** The `transcribe.sh` script will auto-download the model on first run if you skip this step — but doing it now means your first transcription will be faster.

### Step 5 — Get the script

Download this repo:

```bash
cd ~
git clone https://github.com/TheDeLay/video-transcriber.git
cd video-transcriber
chmod +x bash/transcribe.sh
```

(If `git` isn't installed, the first command will prompt you to install Apple's developer command-line tools — accept and try again.)

### Step 6 — Run it

```bash
./bash/transcribe.sh "https://www.youtube.com/watch?v=YOUR_VIDEO_URL"
```

Replace the URL with the actual YouTube link. **Quotes are important.**

You'll see progress messages. When it finishes (typically 1–3× the length of the video, depending on model and Mac), you'll find two files on your Desktop:

- `<Video-Title>_<date>.txt` — the transcript
- `<Video-Title>_<date>_prompt.md` — the AI prompt with the transcript built in

The prompt is also **automatically copied to your clipboard**. Open Gemini, ChatGPT, NotebookLM, or your AI of choice, paste (`⌘ + V`), and send.

---

## Troubleshooting

**`brew: command not found`** — You missed Step 2's "Next steps" lines. Re-run the Homebrew installer or paste the `eval ...` line that the installer printed.

**`whisper-cli: command not found`** — Try `brew install whisper-cpp` again. On older versions of the formula the binary is called `main` instead — if that's what you have, the script handles it automatically.

**The script ran but the transcript looks garbled or empty** — The video may have very poor audio, music-only sections, or be in a language other than English. Try `WHISPER_MODEL=medium.en ./bash/transcribe.sh ...` for higher accuracy.

**Transcription is taking forever** — The first run downloads the model (~500 MB), which is one-time. After that, transcription on an M3/M4 Mac should run roughly as fast as the video plays (a 30-min video = ~30 min, or faster).

**Need help?** Send a screenshot of the Terminal window with the error message visible.

---

## Customization

The script honors a few environment variables:

```bash
WHISPER_MODEL=medium.en ./bash/transcribe.sh "URL"          # Higher accuracy, slower
OUTPUT_DIR=~/Documents/Transcripts ./bash/transcribe.sh "URL"  # Save somewhere other than Desktop
WHISPER_MODEL_DIR=~/whisper-models ./bash/transcribe.sh "URL"  # Custom model location
```

Available models (smallest → largest): `tiny.en`, `base.en`, `small.en` (default), `medium.en`, `large-v3`. Drop the `.en` to allow non-English transcription.
