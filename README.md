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

`prompt-template.md` is plain text. Edit it to fit your use case:

- The default is tuned for **sermons and other structured spoken content** (asks for an outline, summary, and 5–7 takeaways).
- For lectures, podcasts, or interviews, soften the religious framing in the opening line.
- For meeting notes, replace the takeaways section with "Action items" and "Decisions made."

## License

MIT — see [LICENSE](LICENSE).
