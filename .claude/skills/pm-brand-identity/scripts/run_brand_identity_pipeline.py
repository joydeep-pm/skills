#!/usr/bin/env python3
"""Run the full brand identity workflow from repo context to packaged assets."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys


def run_command(command: list[str]) -> None:
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        raise SystemExit(f"Command failed ({completed.returncode}): {' '.join(command)}")


def detect_project_name(project_root: pathlib.Path) -> str:
    package_path = project_root / "package.json"
    if package_path.exists():
        try:
            package_data = json.loads(package_path.read_text(encoding="utf-8"))
            package_name = str(package_data.get("name", "")).strip()
            if package_name:
                return package_name
        except json.JSONDecodeError:
            pass

    for candidate in ("README.md", "README.MD"):
        readme_path = project_root / candidate
        if not readme_path.exists():
            continue
        text = readme_path.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if match:
            return match.group(1).strip()

    return project_root.name


def sanitize_name(name: str) -> str:
    value = name.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "product"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Project root to analyze.")
    parser.add_argument("--work-dir", default="brand-output", help="Output workspace directory.")
    parser.add_argument("--name", help="Product name for final filenames and manifest.")
    parser.add_argument("--model", help="Gemini model name (optional).")
    parser.add_argument("--api-key", help="Gemini API key (optional; falls back to GEMINI_API_KEY).")
    parser.add_argument("--selected-index", type=int, default=1, help="Logo concept index to package (1-based).")
    parser.add_argument("--max-files", type=int, default=30, help="Max files for context extraction.")
    parser.add_argument("--chars-per-file", type=int, default=1600, help="Max chars per file in context extraction.")
    parser.add_argument(
        "--skip-generate",
        action="store_true",
        help="Skip Gemini generation and package an existing raw/logo-XX.png.",
    )
    args = parser.parse_args()

    script_dir = pathlib.Path(__file__).resolve().parent
    project_root = pathlib.Path(args.project_root).resolve()
    work_dir = pathlib.Path(args.work_dir).resolve()
    raw_dir = work_dir / "raw"
    final_dir = work_dir / "final"

    context_file = work_dir / "brand-context.md"
    brief_file = work_dir / "brand-brief.md"
    prompts_file = work_dir / "logo-prompts.txt"

    work_dir.mkdir(parents=True, exist_ok=True)

    extract_script = script_dir / "extract_project_brand_context.py"
    direction_script = script_dir / "generate_brand_direction.py"
    generate_script = script_dir / "generate_logos_gemini.py"
    package_script = script_dir / "build_logo_assets.py"

    run_command(
        [
            sys.executable,
            str(extract_script),
            "--project-root",
            str(project_root),
            "--output-file",
            str(context_file),
            "--max-files",
            str(args.max_files),
            "--chars-per-file",
            str(args.chars_per_file),
        ]
    )

    run_command(
        [
            sys.executable,
            str(direction_script),
            "--context-file",
            str(context_file),
            "--project-root",
            str(project_root),
            "--brief-output",
            str(brief_file),
            "--prompts-output",
            str(prompts_file),
        ]
    )

    if not args.skip_generate:
        generation_cmd = [
            sys.executable,
            str(generate_script),
            "--brief-file",
            str(brief_file),
            "--prompt-file",
            str(prompts_file),
            "--output-dir",
            str(raw_dir),
        ]
        if args.model:
            generation_cmd.extend(["--model", args.model])
        if args.api_key:
            generation_cmd.extend(["--api-key", args.api_key])
        run_command(generation_cmd)

    logo_path = raw_dir / f"logo-{args.selected_index:02d}.png"
    if not logo_path.exists():
        raise SystemExit(
            f"Selected logo not found: {logo_path}. "
            "Run generation first or choose a valid --selected-index."
        )

    product_name = args.name or sanitize_name(detect_project_name(project_root))

    run_command(
        [
            sys.executable,
            str(package_script),
            "--input",
            str(logo_path),
            "--name",
            product_name,
            "--output-dir",
            str(final_dir),
        ]
    )

    print("[OK] Brand identity pipeline complete")
    print(f"[OK] Context: {context_file}")
    print(f"[OK] Brief: {brief_file}")
    print(f"[OK] Prompts: {prompts_file}")
    print(f"[OK] Raw logos: {raw_dir}")
    print(f"[OK] Final assets: {final_dir}")


if __name__ == "__main__":
    main()
