# Changelog

All notable changes to **video-transcriber** are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (with the usual caveats for pre-1.0 software — minor versions may include breaking changes if necessary, though we try to avoid them).

---

## [Unreleased]

Nothing yet.

---

## [0.2.0] — 2026-05-03

First formally tagged release. Significant feature additions and a default-template overhaul since `0.1.0`.

### Added

- **`--latest` flag** for `bash/transcribe.sh` to transcribe the newest upload from a YouTube channel or playlist URL, removing the need to look up specific video URLs.
- **`--filter <keyword>`** (with `--latest`) to pick the newest entry whose title contains a case-insensitive keyword. Searches up to 30 most recent entries. Practical example: keep `--filter "Contemporary"` in a shell alias for a weekly church service.
- **`--template <path>` flag** and **`PROMPT_TEMPLATE` env var** for `bash/transcribe.sh`, mirroring the `--template` flag the Python CLI already had. Both paths now have parity. Precedence: flag > env var > default.
- **`templates/` directory** with curated alternatives that share a common §1 Transcription Hygiene preamble and structural conventions. See [`templates/README.md`](templates/README.md) for usage and contribution guide.
  - **`templates/church-leader.md`** — sermon / spiritual-talk analysis. Adds leader self-application, congregation reception anticipation, and three pastoral postures (challenge / help / encourage).
  - **`templates/infosec-leader.md`** — security-talk analysis. Adds speaker's threat model, surfaced + implied risks, controls in three tiers (quick wins / medium / strategic), homelab application, vendor-pitch filter, and exec translation.
  - **`templates/it-leader.md`** — IT-leader-talk analysis. Adds speaker's frame check, stability and failure-mode analysis, user adoption risk, sustainability across 6m/12m/3y horizons, rollout/rollback plan, and exec translation.
- **§1 Transcription Hygiene pass** in all templates — the AI flags speech-to-text errors (mishears of proper names, technical terms, version numbers, scripture references) before drawing conclusions, so a misheard line doesn't end up driving a real-world decision.

### Changed

- **Default `prompt-template.md` rewritten.** Religion-neutral framing, hygiene pass first, illustrations treated as load-bearing rather than decoration, and an explicit "read between the lines" pass to surface what the speaker is hoping the listener catches but didn't say outright.
- **README "Customizing the AI prompt" section.** Replaced the old "edit it to fit your use case" paragraph (which assumed users would fork and never pull) with override-via-env-var and override-via-flag patterns, plus a curated-alternatives table pointing at `templates/`.
- **Performance estimates updated to measured numbers.** Apple Silicon + Metal + `small.en` transcribes at roughly 6% of video length — about 10× faster than the original pessimistic estimate.

### Fixed

- **`--filter` no-match silent exit.** When `--filter <kw>` matched nothing in the 30 most recent entries, the script exited 1 cleanly but the documented `die` message *"No upload in the 30 most recent entries matched 'X'."* was swallowed by `set -e + pipefail`. Pipeline now uses `|| true` inside the command substitution so the existing die check fires correctly.

### Tested

- macOS (Apple Silicon): bash path end-to-end with a 90-minute video and Python path end-to-end with a short video. Both paths produce identical output.
- Linux: not validated in this release. Expected to work for both paths.
- Windows: not supported. Bash path won't work natively; Python path may work under WSL but is unverified.

---

## [0.1.0] — 2026-05-03 (untagged)

Initial release. Untagged at the time, included here for completeness.

### Added

- **`bash/transcribe.sh`** — Mac-friendly shell script using `whisper-cpp`, `ffmpeg`, `yt-dlp`. No Python required.
- **`python/video_transcriber/`** — Python package and `video-transcribe` CLI. For developers who want to extend the tool. Includes `--template` flag, `--model` selection, virtualenv-friendly install via `pip install -e .`.
- **`prompt-template.md`** — default AI prompt: outline + summary + 5–7 takeaways for any structured spoken-word video.
- **README.md, `bash/install.md`, `python/install.md`** — quickstart and full-walkthrough documentation per path.
- **MIT license.**

---

[Unreleased]: https://github.com/TheDeLay/video-transcriber/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/TheDeLay/video-transcriber/releases/tag/v0.2.0
