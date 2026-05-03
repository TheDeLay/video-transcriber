# Contributing to video-transcriber

Thanks for your interest. This is a small, focused tool, so contributions that match its scope are welcome and will move quickly.

## What fits

- **New prompt templates** for specific domains (lectures, all-hands meetings, interviews, technical conference talks, courtroom audio, podcast episodes, etc.). See [`templates/README.md`](templates/README.md) for the convention.
- **Bug fixes** in `bash/transcribe.sh` or `python/video_transcriber/`.
- **Documentation improvements** — README clarifications, install troubleshooting, new "Fast Track" recipes.
- **Performance work** — anything that makes Whisper faster on consumer hardware without bloating the install.
- **Cross-platform validation** — Linux test reports, WSL notes, Windows path support if you've got a clean approach.

## What's out of scope (for now)

- New transcription backends beyond `whisper.cpp` / `openai-whisper`. The goal is "Mac-friendly minimal install"; adding alternatives means more dependency footprint and more support surface.
- GUI wrappers. Keep this CLI-only.
- Web app frontends.
- Cloud-hosted transcription. The point of this tool is local, private, no API keys.

If you want one of those things, fork happily — but the upstream will likely stay focused.

## How to submit

1. **Open an issue first** if it's a feature change or anything beyond a small fix, so we can discuss scope before you sink time into it.
2. **Fork → branch → PR to `main`.**
3. **Match the existing voice** in docs and templates — terse, opinionated, concrete. No fluff.
4. **Test what you can on macOS.** Linux is expected to work; Windows is unsupported pending separate validation.

## Style notes

- **Bash scripts**: keep `set -euo pipefail` enabled. Pipelines that include `grep` (which exits 1 on no-match) need `|| true` to avoid swallowing intended `die` messages — see the `--filter` resolution block in `transcribe.sh` for the pattern.
- **Templates**: structure must follow the convention — `## 1. Transcription Hygiene` first, numbered sections after, and `**TRANSCRIPT FOLLOWS BELOW.**` at the very end. The script appends the transcript right after that line.
- **Commit messages**: conventional style — `feat:`, `fix:`, `docs:`, `chore:`, etc. Subject under 70 chars; body explains the *why* and the *how-it-was-verified*, not the *what* (the diff covers that).
- **No unrelated changes** in the same PR. If your fix surfaces a second thing worth fixing, open a second PR.

## Templates: the convention in detail

Every template under `templates/`:

1. **Starts with a clear `# Title` and a one-paragraph framing** of who the template is for and what it does differently.
2. **Has a numbered `## 1. Transcription Hygiene (do this first)` section** that scans for STT errors specific to the domain (proper names, technical terms, numbers, transliterations, etc.).
3. **Numbered sections after that** in the order the AI should complete them. Section names should be descriptive, not generic ("The Speaker's Threat Model" beats "Analysis").
4. **Ends with a `## N. Key Takeaways`** that asks for 5–7 specific, actionable items.
5. **Final line is `**TRANSCRIPT FOLLOWS BELOW.**`** followed by `---`. The script appends the transcript right after.

Templates should be **opinionated**. A template that tries to serve every possible domain serves none. If your template is for SRE post-mortem analysis, lean into that — be specific to SRE language, common SRE failure modes, and the SRE leader's audience.

## Code of conduct

Be useful. Be honest about what doesn't work. Don't pad. Don't argue about scope after a maintainer has called something out of scope — fork and ship your own.
