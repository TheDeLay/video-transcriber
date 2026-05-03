"""Video Transcriber CLI.

Pipeline: YouTube URL -> yt-dlp (audio) -> Whisper -> transcript files -> prompt.
"""

from __future__ import annotations

import datetime as dt
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import click


PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent.parent
DEFAULT_TEMPLATE = PROJECT_ROOT / "prompt-template.md"

VALID_FORMATS = {"txt", "srt", "vtt", "json", "tsv"}


def _slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "_", text.strip())
    return text or "video"


def _download_audio(url: str, workdir: Path) -> tuple[Path, str]:
    """Download audio as 16kHz mono WAV and return (audio_path, video_title)."""
    import yt_dlp

    out_template = str(workdir / "audio.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
        "postprocessor_args": ["-ar", "16000", "-ac", "1"],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "video")

    audio_path = workdir / "audio.wav"
    if not audio_path.exists():
        raise click.ClickException(f"Expected audio file not found at {audio_path}.")
    return audio_path, title


def _transcribe(audio_path: Path, model_name: str, language: str | None) -> dict:
    """Run Whisper and return the result dict."""
    import whisper

    model = whisper.load_model(model_name)
    kwargs: dict = {"verbose": False}
    if language:
        kwargs["language"] = language
    return model.transcribe(str(audio_path), **kwargs)


def _write_outputs(
    result: dict,
    base_path: Path,
    formats: list[str],
) -> Path:
    """Write requested transcript formats. Return the path to the .txt file."""
    import whisper.utils as wu

    txt_path = base_path.with_suffix(".txt")
    for fmt in formats:
        writer = wu.get_writer(fmt, str(base_path.parent))
        writer(result, str(base_path), {"max_line_width": None, "max_line_count": None, "highlight_words": False})
    return txt_path


def _build_prompt(template_path: Path, transcript_path: Path, prompt_path: Path) -> None:
    template = template_path.read_text(encoding="utf-8")
    transcript = transcript_path.read_text(encoding="utf-8")
    prompt_path.write_text(template + "\n" + transcript, encoding="utf-8")


def _copy_to_clipboard(text: str) -> bool:
    """Try to copy to the macOS clipboard. Return True on success."""
    if not shutil.which("pbcopy"):
        return False
    try:
        proc = subprocess.run(
            ["pbcopy"],
            input=text.encode("utf-8"),
            check=True,
        )
        return proc.returncode == 0
    except subprocess.CalledProcessError:
        return False


@click.command()
@click.argument("url")
@click.option(
    "--model",
    default="small.en",
    show_default=True,
    help="Whisper model name (tiny, base, small, medium, large; append .en for English-only).",
)
@click.option(
    "--language",
    default=None,
    help="Language code (e.g. en, es, fr). Default: auto-detect.",
)
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path.home() / "Desktop",
    show_default=True,
    help="Where to write transcript and prompt files.",
)
@click.option(
    "--formats",
    default="txt,srt",
    show_default=True,
    help="Comma-separated transcript formats: txt, srt, vtt, json, tsv.",
)
@click.option(
    "--template",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=DEFAULT_TEMPLATE,
    show_default=False,
    help="Path to the AI prompt template.",
)
@click.option("--no-clipboard", is_flag=True, help="Don't copy the prompt to the clipboard.")
@click.option("--keep-audio", is_flag=True, help="Keep the downloaded audio file alongside outputs.")
def main(
    url: str,
    model: str,
    language: str | None,
    output_dir: Path,
    formats: str,
    template: Path,
    no_clipboard: bool,
    keep_audio: bool,
) -> None:
    """Download a YouTube video, transcribe it with Whisper, and prepare an AI prompt."""

    requested_formats = [f.strip().lower() for f in formats.split(",") if f.strip()]
    bad = [f for f in requested_formats if f not in VALID_FORMATS]
    if bad:
        raise click.BadParameter(
            f"Unknown format(s): {', '.join(bad)}. Valid: {', '.join(sorted(VALID_FORMATS))}."
        )
    if "txt" not in requested_formats:
        requested_formats.append("txt")  # always need .txt for the prompt

    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="video-transcriber-") as tmp:
        workdir = Path(tmp)

        click.secho("==> Downloading audio...", fg="blue", bold=True)
        audio_path, title = _download_audio(url, workdir)
        click.echo(f"    Title: {title}")

        slug = _slugify(title)
        date = dt.date.today().isoformat()
        base_path = output_dir / f"{slug}_{date}"

        click.secho(f"==> Transcribing with {model} (this can take a while)...", fg="blue", bold=True)
        result = _transcribe(audio_path, model, language)

        click.secho("==> Writing transcript files...", fg="blue", bold=True)
        transcript_path = _write_outputs(result, base_path, requested_formats)

        prompt_path = base_path.with_name(base_path.name + "_prompt.md")
        _build_prompt(template, transcript_path, prompt_path)

        if keep_audio:
            shutil.copy2(audio_path, base_path.with_suffix(".wav"))

    click.secho("\nDone!", fg="green", bold=True)
    click.echo(f"  Transcript : {transcript_path}")
    for fmt in requested_formats:
        if fmt == "txt":
            continue
        sibling = base_path.with_suffix(f".{fmt}")
        if sibling.exists():
            click.echo(f"  {fmt.upper():<10} : {sibling}")
    click.echo(f"  AI prompt  : {prompt_path}")

    if not no_clipboard:
        if _copy_to_clipboard(prompt_path.read_text(encoding="utf-8")):
            click.echo("\nPrompt copied to clipboard. Paste into Gemini, ChatGPT, NotebookLM, or Claude.")
        else:
            click.echo(f"\n(Could not copy to clipboard. Open {prompt_path} and copy manually.)")


if __name__ == "__main__":
    main()
