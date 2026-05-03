# Prompt Templates

Drop-in replacements for `prompt-template.md` (one directory up). Use these when the default is too generic for your use case.

## What's here

| File | For |
|---|---|
| [`church-leader.md`](church-leader.md) | Sermons / spiritual talks where the user is a pastor, ministry leader, teacher, or seminary student. Adds: leader self-application, congregation reception anticipation, and pastoral action postures (challenge / help / encourage). |
| [`infosec-leader.md`](infosec-leader.md) | Security conference talks, vendor briefings, threat-intel walkthroughs, post-mortems. Adds: speaker's threat model, surfaced + implied risks, controls in three tiers (quick wins / medium / strategic), homelab application, vendor-pitch filter, exec translation. |
| [`it-leader.md`](it-leader.md) | SRE / DevOps / platform conference talks, vendor roadmaps, ITSM training, internal architecture reviews. Adds: speaker's frame check, stability and failure-mode analysis, user adoption risk, sustainability across 6m/12m/3y horizons, rollout/rollback plan, exec translation. |

## How to use

### Bash path

```bash
# One-off override via flag
./bash/transcribe.sh --template templates/church-leader.md "URL"

# One-off override via env var
PROMPT_TEMPLATE=templates/church-leader.md ./bash/transcribe.sh "URL"

# Default for your shell — add to ~/.zshrc or ~/.bashrc
export PROMPT_TEMPLATE="$HOME/path/to/video-transcriber/templates/church-leader.md"
```

### Python path

```bash
video-transcribe --template templates/church-leader.md "URL"
```

Both paths produce identical outputs. The `--template` flag wins over the `PROMPT_TEMPLATE` env var, which wins over the default.

## Writing your own template

The script just reads a markdown file and prepends it to the transcript before copying to your clipboard. You can put anything in there. To stay consistent with the rest:

1. **Start with a `## 1. Transcription Hygiene` section** — STT mishears proper names, technical terms, and numbers. The hygiene pass keeps the AI from theorizing on top of mishearings.
2. **Number your sections** so the AI completes them in order.
3. **End with the literal line** `**TRANSCRIPT FOLLOWS BELOW.**` — that's where the script appends the transcript.

If you build a template that works well for a specific domain (lectures, all-hands meetings, interviews, technical conference talks, courtroom audio, podcast episodes, etc.), open a PR. The repo will accept curated alternatives that solve real workflows.
