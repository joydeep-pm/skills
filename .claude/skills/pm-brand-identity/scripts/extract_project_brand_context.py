#!/usr/bin/env python3
"""Extract repository context into a concise brand brief input file."""

from __future__ import annotations

import argparse
import collections
import pathlib
import re

SKIP_DIRS = {
    ".git",
    ".next",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "brand-output",
    "output",
    "tasks",
    ".expo",
    "_bmad",
    "__tests__",
}
PRIORITY_FILES = [
    "README.md",
    "README.MD",
    "package.json",
    "app.json",
    "AGENTS.md",
    "SKILL.md",
    "pyproject.toml",
    "Cargo.toml",
]
TEXT_EXTENSIONS = {".md", ".txt", ".rst", ".json", ".toml", ".yaml", ".yml", ".ts", ".tsx", ".js", ".jsx", ".py"}
STOPWORDS = {
    "about", "after", "also", "because", "before", "being", "between", "build", "built", "could",
    "create", "from", "have", "into", "just", "more", "most", "other", "over", "project", "should",
    "some", "that", "their", "there", "these", "they", "this", "those", "under", "using", "what",
    "when", "where", "with", "your",
    "done", "pending", "true", "false", "runtime", "status", "report", "snapshot", "artifact",
    "json", "markdown", "file", "files", "checklist", "roadmap", "tracker", "issue", "issues",
    "import", "from", "const", "function", "return", "style", "styles", "default", "export",
    "screen", "component", "props", "state", "type", "types", "tsx", "expo", "react", "nativewind",
    "tailwind", "theme", "colors", "create", "view", "text", "value", "values", "async", "await",
    "input", "string", "number", "boolean", "null", "interface", "pass", "fail", "missing",
    "message", "warn", "error", "check", "checks", "action", "date", "primary",
}

NOISY_PATH_PATTERNS = (
    re.compile(r"/docs/device-intake-runtime-qa-", re.IGNORECASE),
    re.compile(r"/docs/.*runtime.*\.(md|json)$", re.IGNORECASE),
    re.compile(r"/docs/.*status.*\.(md|json)$", re.IGNORECASE),
    re.compile(r"/docs/.*snapshot.*\.(md|json)$", re.IGNORECASE),
    re.compile(r"/docs/.*handoff.*\.md$", re.IGNORECASE),
    re.compile(r"/docs/.*artifact.*\.json$", re.IGNORECASE),
    re.compile(r"/docs/ICO_QA_STATUS_SNAPSHOT\.(md|json)$", re.IGNORECASE),
)


def is_text_candidate(path: pathlib.Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name in PRIORITY_FILES


def is_noisy_path(path: pathlib.Path) -> bool:
    path_text = path.as_posix()
    return any(pattern.search(path_text) for pattern in NOISY_PATH_PATTERNS)


def path_priority(path: pathlib.Path, project_root: pathlib.Path) -> int:
    rel = path.relative_to(project_root).as_posix().lower()
    name = path.name.lower()
    score = 0
    if name in {"readme.md", "readme.md"}:
        score += 120
    if name in {"package.json", "app.json", "agents.md"}:
        score += 110
    if rel.startswith("app/"):
        score += 90
    if rel.startswith("src/"):
        score += 80
    if rel.startswith("src/ui/"):
        score += 30
    if rel.startswith("src/recommendation/") or rel.startswith("src/milestone/"):
        score += 30
    if rel.startswith("src/analytics/"):
        score -= 60
    if "/__tests__/" in f"/{rel}":
        score -= 100
    if rel.startswith("docs/") and any(token in name for token in ("roadmap", "feature", "vision", "product")):
        score += 70
    if rel.startswith("docs/"):
        score += 30
    if rel.startswith("scripts/"):
        score += 20
    if rel.startswith("tasks/"):
        score -= 60
    if rel.startswith("docs/") and any(token in name for token in ("handoff", "snapshot", "runtime", "status", "report")):
        score -= 80
    return score


def iter_candidate_files(project_root: pathlib.Path, max_files: int) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    seen: set[pathlib.Path] = set()

    for name in PRIORITY_FILES:
        candidate = project_root / name
        if candidate.exists() and candidate.is_file():
            files.append(candidate)
            seen.add(candidate)

    weighted: list[tuple[int, pathlib.Path]] = []
    for path in sorted(project_root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if is_noisy_path(path):
            continue
        if not is_text_candidate(path):
            continue
        if path in seen:
            continue
        weighted.append((path_priority(path, project_root), path))

    weighted.sort(key=lambda item: (-item[0], str(item[1])))
    for _, path in weighted:
        if len(files) >= max_files:
            break
        files.append(path)
        seen.add(path)

    return files[:max_files]


def read_snippet(path: pathlib.Path, max_chars: int) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""
    return text[:max_chars].strip()


def extract_keywords(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9-]{3,}", text.lower())
    filtered = [word for word in words if word not in STOPWORDS]
    counts = collections.Counter(filtered)
    return [word for word, _ in counts.most_common(30)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Project root directory.")
    parser.add_argument("--output-file", required=True, help="Output markdown file path.")
    parser.add_argument("--max-files", type=int, default=30, help="Maximum files to scan.")
    parser.add_argument("--chars-per-file", type=int, default=1600, help="Max chars to keep per file.")
    args = parser.parse_args()

    project_root = pathlib.Path(args.project_root).resolve()
    output_file = pathlib.Path(args.output_file).resolve()

    files = iter_candidate_files(project_root, args.max_files)
    snippets: list[tuple[pathlib.Path, str]] = []
    keyword_corpus: list[str] = []
    for path in files:
        snippet = read_snippet(path, args.chars_per_file)
        if not snippet:
            continue
        snippets.append((path, snippet))
        suffix = path.suffix.lower()
        if suffix in {".md", ".txt", ".rst"} or path.name.lower().startswith("readme"):
            keyword_corpus.append(snippet)

    keywords = extract_keywords("\n".join(keyword_corpus))
    lines: list[str] = [
        "# Repository Brand Context",
        "",
        "## Source Files",
    ]
    lines.extend([f"- `{path.relative_to(project_root)}`" for path, _ in snippets])
    lines.extend(["", "## Candidate Keywords", ", ".join(keywords) if keywords else "(none)", ""])

    for path, snippet in snippets:
        rel = path.relative_to(project_root)
        lines.extend(
            [
                f"## Extract: `{rel}`",
                "```text",
                snippet,
                "```",
                "",
            ]
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Wrote context file: {output_file}")


if __name__ == "__main__":
    main()
