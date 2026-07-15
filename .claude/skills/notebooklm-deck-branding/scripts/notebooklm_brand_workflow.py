#!/usr/bin/env python3
"""Poll a NotebookLM slide deck artifact, download it, and brand the PPTX."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import time
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Poll NotebookLM for a slide-deck artifact, download the PPTX when "
            "complete, remove the NotebookLM footer mark, and add the M2P logo."
        )
    )
    parser.add_argument("--notebook-id", required=True, help="NotebookLM notebook UUID.")
    parser.add_argument(
        "--artifact-id",
        help="Slide deck artifact UUID. If omitted, uses the newest slide_deck artifact.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("exports/notebooklm-workflow"),
        help="Directory for raw and branded PPTX outputs.",
    )
    parser.add_argument(
        "--final-name",
        default="final-branded.pptx",
        help="Filename for the branded PPTX in output-dir.",
    )
    parser.add_argument(
        "--raw-name",
        default="raw-notebooklm.pptx",
        help="Filename for the downloaded raw PPTX in output-dir.",
    )
    parser.add_argument(
        "--logo-path",
        type=Path,
        default=Path("/Users/joy/Downloads/Brand logo (Red).png"),
        help="Path to the M2P logo PNG.",
    )
    parser.add_argument(
        "--logo-scale",
        type=float,
        default=0.038,
        help=(
            "Logo width as a fraction of slide image width. "
            "Default: 0.038 for a smaller, less intrusive corner mark."
        ),
    )
    parser.add_argument(
        "--logo-margin-scale",
        type=float,
        default=0.012,
        help="Logo margin as a fraction of slide image width. Default: 0.012.",
    )
    parser.add_argument(
        "--cli",
        default="/Users/joy/Library/Python/3.12/bin/notebooklm",
        help="Path to the notebooklm CLI.",
    )
    parser.add_argument(
        "--poll-seconds",
        type=int,
        default=600,
        help="Polling interval in seconds. Default: 600 (10 minutes).",
    )
    parser.add_argument(
        "--max-polls",
        type=int,
        default=36,
        help="Maximum poll attempts before giving up. Default: 36.",
    )
    parser.add_argument(
        "--skip-poll",
        action="store_true",
        help="Assume the artifact is already completed and skip polling.",
    )
    return parser.parse_args()


def run_json(cmd: list[str]) -> dict:
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def list_artifacts(cli: str, notebook_id: str) -> list[dict]:
    payload = run_json([cli, "artifact", "list", "-n", notebook_id, "--json"])
    return payload.get("artifacts", [])


def resolve_artifact_id(cli: str, notebook_id: str, artifact_id: str | None) -> str:
    artifacts = list_artifacts(cli, notebook_id)
    slide_decks = [a for a in artifacts if a.get("type_id") == "slide_deck"]
    if artifact_id:
        for artifact in slide_decks:
            if artifact["id"] == artifact_id:
                return artifact_id
        raise SystemExit(f"Artifact {artifact_id} not found in notebook {notebook_id}")
    if not slide_decks:
        raise SystemExit(f"No slide deck artifacts found in notebook {notebook_id}")
    slide_decks.sort(key=lambda item: item.get("created_at", ""))
    return slide_decks[-1]["id"]


def wait_for_artifact(cli: str, notebook_id: str, artifact_id: str, poll_seconds: int, max_polls: int) -> None:
    for attempt in range(1, max_polls + 1):
        artifacts = list_artifacts(cli, notebook_id)
        match = next((a for a in artifacts if a["id"] == artifact_id), None)
        if not match:
            raise SystemExit(f"Artifact {artifact_id} disappeared from notebook {notebook_id}")
        status = match.get("status", "").lower()
        print(f"[poll {attempt}/{max_polls}] artifact status: {status}", flush=True)
        if status == "completed":
            return
        if status in {"failed", "error"}:
            raise SystemExit(f"Artifact {artifact_id} failed with status: {status}")
        if attempt < max_polls:
            time.sleep(poll_seconds)
    raise SystemExit(f"Timed out waiting for artifact {artifact_id} after {max_polls} polls")


def sample_background(img: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    region = img.crop(box).resize((1, 1))
    pixel = region.getpixel((0, 0))
    if len(pixel) == 4:
        return pixel
    return (pixel[0], pixel[1], pixel[2], 255)


def patch_slide_image(
    image_path: Path,
    logo: Image.Image,
    logo_scale: float,
    logo_margin_scale: float,
) -> None:
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size

    # Cover the NotebookLM footer mark in the slide margin without touching
    # the main slide artwork.
    cover_w = max(int(width * 0.12), 150)
    cover_h = max(int(height * 0.045), 34)
    cover_x = width - cover_w
    cover_y = height - cover_h
    sample = sample_background(
        img,
        (
            max(0, width - cover_w - 80),
            max(0, height - cover_h - 80),
            max(1, width - cover_w - 20),
            max(1, height - 20),
        ),
    )
    footer_patch = Image.new("RGBA", (cover_w, cover_h), sample)
    img.alpha_composite(footer_patch, (cover_x, cover_y))

    # Add the brand logo in the top-right corner, keeping the original deck design.
    margin = max(int(width * logo_margin_scale), 12)
    logo_size = max(int(width * logo_scale), 46)
    logo_img = logo.copy()
    logo_img.thumbnail((logo_size, logo_size))
    x = width - margin - logo_img.width
    y = margin
    img.alpha_composite(logo_img, (x, y))
    img.save(image_path)


def brand_pptx(
    raw_pptx: Path,
    branded_pptx: Path,
    logo_path: Path,
    logo_scale: float,
    logo_margin_scale: float,
) -> None:
    logo = Image.open(logo_path).convert("RGBA")
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        with ZipFile(raw_pptx) as zf:
            zf.extractall(root)

        media_dir = root / "ppt" / "media"
        for image_path in sorted(media_dir.glob("image*.png")):
            patch_slide_image(image_path, logo, logo_scale, logo_margin_scale)

        with ZipFile(branded_pptx, "w", compression=ZIP_DEFLATED) as zf:
            for path in sorted(root.rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(root))


def main() -> int:
    args = parse_args()
    if not args.logo_path.exists():
        raise SystemExit(f"Logo path not found: {args.logo_path}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    raw_pptx = args.output_dir / args.raw_name
    branded_pptx = args.output_dir / args.final_name

    artifact_id = resolve_artifact_id(args.cli, args.notebook_id, args.artifact_id)
    print(f"Using artifact: {artifact_id}")
    if not args.skip_poll:
        wait_for_artifact(args.cli, args.notebook_id, artifact_id, args.poll_seconds, args.max_polls)

    print(f"Downloading raw deck to {raw_pptx}")
    run(
        [
            args.cli,
            "download",
            "slide-deck",
            str(raw_pptx),
            "--format",
            "pptx",
            "-a",
            artifact_id,
            "-n",
            args.notebook_id,
        ]
    )
    print(f"Branding deck to {branded_pptx}")
    brand_pptx(
        raw_pptx,
        branded_pptx,
        args.logo_path,
        args.logo_scale,
        args.logo_margin_scale,
    )
    print(f"Final branded deck: {branded_pptx}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
