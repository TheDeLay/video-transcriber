# Video Transcriber

Turn a YouTube video into a clean text transcript and a ready-to-paste prompt for any AI assistant (Gemini, ChatGPT, NotebookLM, Claude, etc.) — so you can go from a recording to an outline, summary, and key takeaways in minutes. Sermon-friendly out of the box; works for any spoken-word video.

---

## ⚡ Fast Track (Mac, ~10 minutes)

If you already have Homebrew installed, paste these four blocks into Terminal one at a time:

```bash
# 1. Install the three tools
brew install whisper-cpp ffmpeg yt-dlp

# 2. Get this repo
git clone https://github.com/TheDeLay/video-transcriber.git
cd video-transcriber
chmod +x bash/transcribe.sh

# 3. Run it (replace the URL with your video)
./bash/transcribe.sh "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

When it finishes, you'll find on your Desktop:

- `<video-title>_<date>.txt` — the transcript
- `<video-title>_<date>_prompt.md` — a ready-to-paste AI prompt
- The prompt is also **already on your clipboard** — open Gemini/ChatGPT/NotebookLM and press `⌘ + V`.

**Don't have a specific URL?** Use `--latest` to grab the newest upload from a channel:

```bash
./bash/transcribe.sh --latest --filter "Contemporary" "https://www.youtube.com/@WheatonBible/streams"
```

**Don't have Homebrew yet?** See the full walkthrough → **[bash/install.md](bash/install.md)**.

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

## Customizing the AI prompt

`prompt-template.md` (at the project root) is the default prompt. It produces an outline, an insightful summary, and 5–7 takeaways for any structured talk — sermons, lectures, conference talks, podcasts, interviews. It also runs a transcription-hygiene pass first so the AI flags speech-to-text errors instead of building conclusions on top of them.

You can swap in a different template three ways:

```bash
# Bash path — flag (highest precedence)
./bash/transcribe.sh --template templates/church-leader.md "URL"

# Bash path — env var
PROMPT_TEMPLATE=templates/church-leader.md ./bash/transcribe.sh "URL"

# Python path
video-transcribe --template templates/church-leader.md "URL"
```

Or set it as your shell default:

```bash
# Add to ~/.zshrc or ~/.bashrc
export PROMPT_TEMPLATE="$HOME/path/to/video-transcriber/templates/church-leader.md"
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
