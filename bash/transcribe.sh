#!/usr/bin/env bash
# Video Transcriber — bash path
# Downloads a YouTube video, transcribes it with whisper.cpp, and copies an AI
# prompt to the clipboard with the transcript pre-loaded.
#
# Usage:
#   ./transcribe.sh "https://www.youtube.com/watch?v=..."
#
# Optional environment variables:
#   WHISPER_MODEL       Model name without prefix (default: small.en)
#                       Options: tiny.en, base.en, small.en, medium.en, large-v3
#   WHISPER_MODEL_DIR   Where models are stored (default: ~/.whisper-models)
#   OUTPUT_DIR          Where to write transcript + prompt (default: ~/Desktop)

set -euo pipefail

# ---------- helpers ------------------------------------------------------------

color_blue()  { printf "\033[1;34m%s\033[0m\n" "$1"; }
color_green() { printf "\033[1;32m%s\033[0m\n" "$1"; }
color_red()   { printf "\033[1;31m%s\033[0m\n" "$1" >&2; }

die() {
  color_red "ERROR: $1"
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "'$1' is not installed. See bash/install.md."
}

# ---------- args ---------------------------------------------------------------

URL="${1:-}"
if [[ -z "$URL" ]]; then
  cat <<EOF
Usage: $0 <youtube-url>

Example:
  $0 "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

EOF
  exit 1
fi

# ---------- config -------------------------------------------------------------

MODEL="${WHISPER_MODEL:-small.en}"
MODEL_DIR="${WHISPER_MODEL_DIR:-$HOME/.whisper-models}"
MODEL_FILE="$MODEL_DIR/ggml-${MODEL}.bin"
OUTPUT_DIR="${OUTPUT_DIR:-$HOME/Desktop}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE="$SCRIPT_DIR/../prompt-template.md"

# ---------- preflight ----------------------------------------------------------

color_blue "==> Checking dependencies..."
require_cmd yt-dlp
require_cmd ffmpeg

# whisper.cpp ships as 'whisper-cli' in modern brew, 'main' in older builds
if command -v whisper-cli >/dev/null 2>&1; then
  WHISPER_BIN="whisper-cli"
elif command -v main >/dev/null 2>&1 && main --help 2>&1 | grep -q -i whisper; then
  WHISPER_BIN="main"
else
  die "whisper.cpp is not installed. Run: brew install whisper-cpp"
fi

[[ -f "$TEMPLATE" ]] || die "prompt-template.md not found at $TEMPLATE"
mkdir -p "$OUTPUT_DIR"

# ---------- model download (one-time) ------------------------------------------

if [[ ! -f "$MODEL_FILE" ]]; then
  color_blue "==> Whisper model not found; downloading $MODEL (one-time)..."
  mkdir -p "$MODEL_DIR"
  curl -L --fail --progress-bar \
    -o "$MODEL_FILE" \
    "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-${MODEL}.bin" \
    || { rm -f "$MODEL_FILE"; die "Failed to download model. Check your internet connection."; }
  color_green "    Model saved to $MODEL_FILE"
fi

# ---------- workspace ----------------------------------------------------------

WORKDIR="$(mktemp -d -t video-transcriber-XXXXXX)"
trap 'rm -rf "$WORKDIR"' EXIT

# ---------- get title for filename --------------------------------------------

color_blue "==> Looking up video title..."
RAW_TITLE="$(yt-dlp --no-warnings --get-title "$URL" 2>/dev/null || echo "video")"
# Sanitize: keep alnum, dash, underscore, space; collapse spaces to underscores
SAFE_TITLE="$(printf "%s" "$RAW_TITLE" | tr -c '[:alnum:]-_ ' '_' | tr -s '_ ' '_' | sed 's/^_//;s/_$//')"
[[ -n "$SAFE_TITLE" ]] || SAFE_TITLE="video"
DATE_STAMP="$(date +%Y-%m-%d)"
OUT_BASE="$OUTPUT_DIR/${SAFE_TITLE}_${DATE_STAMP}"
echo "    Title: $RAW_TITLE"

# ---------- download audio -----------------------------------------------------

color_blue "==> Downloading audio..."
yt-dlp \
  --no-warnings \
  --no-playlist \
  -x --audio-format wav \
  --postprocessor-args "ffmpeg:-ar 16000 -ac 1" \
  -o "$WORKDIR/audio.%(ext)s" \
  "$URL" \
  || die "yt-dlp failed. Is the URL correct and public?"

AUDIO_FILE="$WORKDIR/audio.wav"
[[ -f "$AUDIO_FILE" ]] || die "Audio file was not produced. Check yt-dlp output above."

# ---------- transcribe ---------------------------------------------------------

color_blue "==> Transcribing with $MODEL (this takes a while)..."
"$WHISPER_BIN" \
  -m "$MODEL_FILE" \
  -f "$AUDIO_FILE" \
  -otxt -osrt \
  -of "$OUT_BASE" \
  --print-progress \
  || die "Whisper transcription failed."

TRANSCRIPT="${OUT_BASE}.txt"
[[ -f "$TRANSCRIPT" ]] || die "Transcript was not produced."

# ---------- build AI prompt ---------------------------------------------------

color_blue "==> Building AI prompt..."
PROMPT_FILE="${OUT_BASE}_prompt.md"
{
  cat "$TEMPLATE"
  echo
  cat "$TRANSCRIPT"
} > "$PROMPT_FILE"

# ---------- copy to clipboard --------------------------------------------------

if command -v pbcopy >/dev/null 2>&1; then
  pbcopy < "$PROMPT_FILE"
  CLIPBOARD_NOTE="Prompt copied to clipboard — paste into Gemini, ChatGPT, NotebookLM, or Claude."
else
  CLIPBOARD_NOTE="(pbcopy not available; open $PROMPT_FILE and copy manually.)"
fi

# ---------- done ---------------------------------------------------------------

echo
color_green "Done!"
echo "  Transcript : $TRANSCRIPT"
echo "  Subtitles  : ${OUT_BASE}.srt"
echo "  AI prompt  : $PROMPT_FILE"
echo
echo "$CLIPBOARD_NOTE"
