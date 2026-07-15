---
name: notebooklm-deck-branding
description: Poll a NotebookLM slide-deck artifact, download the PPTX when it completes, remove the NotebookLM footer mark, add the M2P logo, and write a final branded PPTX without changing the generated slide design. Use when the user wants a NotebookLM deck automatically checked every 10 minutes until ready and then post-processed for M2P branding.
---

# NotebookLM Deck Branding

Use this skill when a user wants a NotebookLM-generated slide deck turned into a final M2P-branded PPTX with the original NotebookLM design preserved.

## What this does

- Polls NotebookLM for a slide-deck artifact every 10 minutes by default
- Downloads the PPTX when the artifact is completed
- Removes the NotebookLM footer mark from each slide image
- Adds the M2P logo in the top-right corner
- Writes both the raw and final branded PPTX files
- Uses a conservative default logo size so the mark reads as branding, not an overlay

## Required inputs

- `notebook_id`: full NotebookLM notebook UUID
- `artifact_id`: optional slide-deck artifact UUID; if omitted, the newest `slide_deck` artifact is used
- `logo_path`: optional; defaults to `/Users/joy/Downloads/Brand logo (Red).png`
- `output_dir`: optional; defaults to `exports/notebooklm-workflow`

## Before running

1. Verify NotebookLM CLI auth:
   - `/Users/joy/Library/Python/3.12/bin/notebooklm status`
   - `/Users/joy/Library/Python/3.12/bin/notebooklm list --json`
2. Prefer explicit notebook and artifact IDs. Do not rely on `notebooklm use` for automation.
3. If the artifact is already complete, use `--skip-poll`.

## Run

```bash
python3 /Users/joy/.codex/skills/notebooklm-deck-branding/scripts/notebooklm_brand_workflow.py \
  --notebook-id <NOTEBOOK_ID> \
  --artifact-id <ARTIFACT_ID> \
  --poll-seconds 600 \
  --logo-scale 0.038 \
  --logo-path "/Users/joy/Downloads/Brand logo (Red).png" \
  --output-dir /desired/output/dir
```

## Fast path for an already completed artifact

```bash
python3 /Users/joy/.codex/skills/notebooklm-deck-branding/scripts/notebooklm_brand_workflow.py \
  --notebook-id <NOTEBOOK_ID> \
  --artifact-id <ARTIFACT_ID> \
  --skip-poll
```

## Notes

- This workflow keeps the NotebookLM deck design intact; it only removes the footer mark and applies M2P branding.
- The script uses explicit `-n <notebook_id>` and `-a <artifact_id>` flags for NotebookLM CLI safety.
- Default branding is intentionally small; use `--logo-scale` only when the user explicitly wants a larger corner mark.
- Final output paths are printed at the end of the run.
