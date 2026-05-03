# Video Transcriber

Turn a YouTube video into a clean text transcript and a ready-to-paste prompt for any AI assistant (Gemini, ChatGPT, NotebookLM, Claude, etc.) — so you can go from a recording to an outline, summary, and key takeaways in minutes. Curated prompt templates for sermons, security talks, IT/SRE talks, and other structured spoken content.

---

## Privacy & cost

Everything runs on your Mac after install. `yt-dlp` is the only network call (downloading from YouTube); `whisper.cpp` does the transcription on-device, and the prompt is copied to your local clipboard. **No API keys, no telemetry, no per-minute fees.** The AI step (paste into Gemini, ChatGPT, NotebookLM, or Claude) uses whichever assistant you already have.

---

## ⚡ Quickstart (Mac, Homebrew already installed)

```bash
brew install whisper-cpp ffmpeg yt-dlp
```

```bash
git clone https://github.com/TheDeLay/video-transcriber.git
cd video-transcriber
chmod +x bash/transcribe.sh
```

```bash
./bash/transcribe.sh "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

When it finishes, your Desktop has `<title>_<date>.txt` (transcript) and `<title>_<date>_prompt.md` (AI prompt — also auto-copied to your clipboard).

**Don't have Homebrew?** Install it from [brew.sh](https://brew.sh), then run the steps above.
**Want every step explained?** See [`bash/install.md`](bash/install.md) — full walkthrough, troubleshooting, customization.

### `--latest` for regular content

For series content (weekly podcasts, Sunday services, daily uploads, etc.), skip URL lookup:

```bash
# Most recent upload from a channel
./bash/transcribe.sh --latest "https://www.youtube.com/@SomeChannel/streams"

# Most recent upload whose title contains a keyword (case-insensitive, scans 30 most recent)
./bash/transcribe.sh --latest --filter "KEYWORD" "https://www.youtube.com/@SomeChannel/streams"
```

---

## Two installation paths

| Path | For | What you install |
| --- | --- | --- |
| **[bash/](bash/)** | Anyone on a Mac. Easiest. | Homebrew + 3 brew formulas. **No Python.** |
| **[python/](python/)** | Developers who want to extend it. | Python 3.11+, pip, a virtualenv. |

Both paths produce identical outputs.

> **Platform support:** macOS is the primary tested platform. Linux is expected to work for both paths but isn't validated in this release. Windows isn't supported yet — the bash path won't work natively, and the Python path likely works under WSL but is unverified. See [`CHANGELOG.md`](CHANGELOG.md) for what's tested per release.

## How it works

```
YouTube URL  →  yt-dlp  →  audio.wav  →  Whisper  →  transcript.txt
                                                      ↓
                                             prompt-template.md
                                                      ↓
                                             prompt.md (clipboard)
                                                      ↓
                                             Paste into your AI
                                                      ↓
                                       Outline + Summary + Takeaways
```

`yt-dlp` is the only network step; everything after the audio download runs locally.

## Customizing the AI prompt

`prompt-template.md` (at the project root) is the default prompt. It produces an outline, an insightful summary, and 5–7 takeaways for any structured talk — sermons, lectures, conference talks, podcasts, interviews. It also runs a transcription-hygiene pass first so the AI flags speech-to-text errors instead of building conclusions on top of them.

You can swap in a different template three ways:

```bash
# Bash path — flag (highest precedence)
./bash/transcribe.sh --template templates/infosec-leader.md "URL"

# Bash path — env var
PROMPT_TEMPLATE=templates/infosec-leader.md ./bash/transcribe.sh "URL"

# Python path
video-transcribe --template templates/infosec-leader.md "URL"
```

Or set it as your shell default:

```bash
# Add to ~/.zshrc or ~/.bashrc
export PROMPT_TEMPLATE="$HOME/path/to/video-transcriber/templates/infosec-leader.md"
```

### Curated alternatives

| Template | For |
|---|---|
| [`templates/church-leader.md`](templates/church-leader.md) | Sermons / spiritual talks where the user is a pastor or ministry leader. |
| [`templates/infosec-leader.md`](templates/infosec-leader.md) | Security conference talks, vendor briefings, threat intel, post-mortems. |
| [`templates/it-leader.md`](templates/it-leader.md) | SRE / DevOps / platform talks, vendor roadmaps, ITSM training, architecture reviews. |

See [`templates/README.md`](templates/README.md) for what each one adds and the convention if you want to write your own and contribute it back.

## License

MIT — see [LICENSE](LICENSE).
