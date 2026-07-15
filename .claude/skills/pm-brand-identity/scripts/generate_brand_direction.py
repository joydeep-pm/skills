#!/usr/bin/env python3
"""Generate a brand brief and logo prompt directions from repository context."""

from __future__ import annotations

import argparse
import json
import pathlib
import re

README_CANDIDATES = ("README.md", "README.MD", "readme.md")
SIGNAL_DOC_CANDIDATES = (
    "AGENTS.md",
    "docs/ICO_FULL_FEATURE_ROADMAP.md",
    "docs/ICO_EXECUTION_ROADMAP_2026_H1.md",
)
FALLBACK_KEYWORDS = ["clarity", "precision", "trust", "momentum", "signal", "focus"]
GENERIC_KEYWORDS = {
    "step", "next", "global", "components", "baseline", "must", "only", "unless",
    "specific", "active", "framework", "router", "stack", "server", "data",
    "workflow", "workflows", "design-system", "expo-router", "zustand", "react-query",
    "animations", "layout", "exclusively", "user", "users",
}
FEATURE_HINT_WORDS = (
    "card",
    "wallet",
    "reward",
    "milestone",
    "recommend",
    "search",
    "onboarding",
    "gmail",
    "sync",
    "consent",
    "privacy",
    "analytics",
)


def read_text_if_exists(path: pathlib.Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def parse_keywords(context_text: str) -> list[str]:
    match = re.search(r"## Candidate Keywords\s*\n([^\n]+)", context_text)
    if not match:
        return []
    line = match.group(1).strip()
    if not line or line == "(none)":
        return []
    return [part.strip() for part in line.split(",") if part.strip()]


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

    for candidate in README_CANDIDATES:
        readme_path = project_root / candidate
        text = read_text_if_exists(readme_path)
        if not text:
            continue
        heading_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if heading_match:
            return heading_match.group(1).strip()

    return project_root.name


def detect_value_proposition(project_root: pathlib.Path) -> str:
    package_path = project_root / "package.json"
    if package_path.exists():
        try:
            package_data = json.loads(package_path.read_text(encoding="utf-8"))
            description = str(package_data.get("description", "")).strip()
            if description:
                return description
        except json.JSONDecodeError:
            pass

    app_json = project_root / "app.json"
    if app_json.exists():
        try:
            app_data = json.loads(app_json.read_text(encoding="utf-8"))
            expo = app_data.get("expo", {}) if isinstance(app_data, dict) else {}
            description = str(expo.get("description", "")).strip()
            if description:
                return description
        except json.JSONDecodeError:
            pass

    for candidate in README_CANDIDATES:
        readme_path = project_root / candidate
        text = read_text_if_exists(readme_path)
        if not text:
            continue
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("#") or line.startswith("-") or line.startswith("*"):
                continue
            if line.startswith("```"):
                continue
            if len(line) >= 20:
                return line
    if "card" in project_root.name.lower() or "wallet" in project_root.name.lower():
        return "Helps users choose and optimize credit cards with smarter rewards guidance and progress tracking."

    return "Delivers a focused product experience with clear utility and trustworthy guidance."


def extract_core_features(project_root: pathlib.Path, keywords: list[str]) -> list[str]:
    features: list[str] = []
    for candidate in (*README_CANDIDATES, *SIGNAL_DOC_CANDIDATES):
        readme_path = project_root / candidate
        text = read_text_if_exists(readme_path)
        if not text:
            continue
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if line.startswith("- ") or line.startswith("* "):
                value = line[2:].strip()
                if len(value) < 8:
                    continue
                if not any(hint in value.lower() for hint in FEATURE_HINT_WORDS):
                    continue
                if any(token in value for token in ("`", "@", "src/", "app/", "=>")):
                    continue
                if value not in features:
                    features.append(value)
                if len(features) >= 5:
                    return features

    if "card" in project_root.name.lower() or "wallet" in project_root.name.lower():
        return [
            "Personalized card recommendations by merchant, amount, and channel",
            "Wallet management with card tracking and issuer/network context",
            "Milestone forecasting and nudges to maximize reward outcomes",
            "Privacy-first data access controls and consent-aware sync flows",
        ]

    fallback = [
        f"Supports workflows around {keywords[0]}" if keywords else "Supports end-to-end brand workflows",
        f"Surfaces insights around {keywords[1]}" if len(keywords) > 1 else "Surfaces reusable visual directions",
        f"Delivers production-ready visual assets for {keywords[2]}" if len(keywords) > 2 else "Delivers production-ready visual assets",
    ]
    return fallback


def infer_domain(keywords: list[str], project_name: str) -> str:
    terms = {word.lower() for word in keywords}
    lower_name = project_name.lower()
    if any(token in lower_name for token in ("card", "wallet", "rewards", "fintech", "copilot")):
        return "Fintech"
    if any(term in terms for term in {"card", "payment", "wallet", "bank", "transaction", "reward"}):
        return "Fintech"
    if any(term in terms for term in {"brand", "logo", "icon", "design"}) or "brand" in lower_name:
        return "Brand and design tooling"
    if any(term in terms for term in {"repo", "script", "cli", "workflow", "automation"}):
        return "Developer tooling"
    return "Software product"


def infer_audience(domain: str) -> str:
    if domain == "Fintech":
        return "Credit-card users optimizing rewards, spend decisions, and milestone progress"
    if domain == "Brand and design tooling":
        return "Product designers and engineers shipping branded interfaces"
    if domain == "Developer tooling":
        return "Developers and product teams building software workflows"
    return "Digital product users and builders"


def infer_palette(domain: str) -> str:
    if domain == "Fintech":
        return "Deep navy neutrals with one restrained warm accent"
    if domain == "Brand and design tooling":
        return "Charcoal and off-white with a crisp accent color"
    if domain == "Developer tooling":
        return "Dark graphite base with a focused highlight accent"
    return "Neutral base with one consistent accent"


def ensure_keywords(keywords: list[str]) -> list[str]:
    cleaned = [word for word in keywords if re.match(r"^[a-zA-Z0-9-]+$", word)]
    merged = cleaned + [word for word in FALLBACK_KEYWORDS if word not in cleaned]
    return merged[:8]


def normalize_keywords(keywords: list[str], domain: str, project_name: str) -> list[str]:
    cleaned: list[str] = []
    for word in keywords:
        lower = word.lower()
        if lower in GENERIC_KEYWORDS:
            continue
        if not re.match(r"^[a-zA-Z0-9-]+$", word):
            continue
        if lower not in cleaned:
            cleaned.append(lower)

    if domain == "Fintech" or any(token in project_name.lower() for token in ("card", "wallet", "reward", "copilot")):
        seeded = ["card", "rewards", "milestone", "insight", "trust", "optimization"]
        ordered = seeded[:]
        for word in cleaned:
            if word not in ordered:
                ordered.append(word)
        return ordered[:8]

    return cleaned[:8]


def write_brand_brief(
    *,
    brief_path: pathlib.Path,
    project_name: str,
    value_prop: str,
    audience: str,
    domain: str,
    features: list[str],
    keywords: list[str],
    palette: str,
) -> None:
    personality = ", ".join(keywords[:4]) if keywords else "clarity, confidence"
    feature_lines = "\n".join([f"  - {item}" for item in features[:4]])
    must_communicate = "\n".join([
        "  - Recognizable silhouette",
        "  - Product confidence and trust",
        "  - Scalability from 16x16 favicon to large logo",
    ])
    must_avoid = "\n".join([
        "  - Cluttered details or thin fragile lines",
        "  - Trademark mimicry or lookalike logos",
        "  - Photoreal mockups, text overlays, and watermarks",
    ])

    brief_text = "\n".join(
        [
            "# Brand Brief",
            "",
            "## Product",
            f"- Name: {project_name}",
            f"- One-line value proposition: {value_prop}",
            f"- Primary users: {audience}",
            "",
            "## Functional Context",
            f"- Core features:\n{feature_lines}",
            f"- Domain: {domain}",
            f"- Personality signals from docs/copy: {personality}",
            "",
            "## Visual Guardrails",
            "- Must communicate:",
            must_communicate,
            "- Must avoid:",
            must_avoid,
            f"- Color constraints: {palette}",
            "- Shape constraints: geometric simplicity, strong icon silhouette, centered composition",
            "- Accessibility constraints: clear contrast on both light and dark backgrounds",
            "",
        ]
    )
    brief_path.parent.mkdir(parents=True, exist_ok=True)
    brief_path.write_text(brief_text, encoding="utf-8")


def write_logo_prompts(*, prompt_path: pathlib.Path, keywords: list[str], palette: str) -> None:
    motifs = ensure_keywords(keywords)

    directions = [
        {
            "name": "Clean geometric minimal",
            "style": "Minimal, modern, geometric icon mark",
            "motifs": ", ".join(motifs[0:3]),
            "palette": palette,
            "composition": "centered icon mark, transparent background, square-safe silhouette",
        },
        {
            "name": "Bold expressive symbol",
            "style": "Confident, high-contrast emblem with strong presence",
            "motifs": ", ".join(motifs[2:5]),
            "palette": "high-contrast neutral base with one warm or vivid accent",
            "composition": "single dominant symbol, thick readable geometry, no tiny details",
        },
        {
            "name": "Abstract symbolic monogram",
            "style": "Abstract premium symbol with restrained structure",
            "motifs": ", ".join(motifs[4:7]),
            "palette": "mostly monochrome with subtle accent option",
            "composition": "compact abstract mark optimized for favicon readability",
        },
    ]

    blocks = []
    for direction in directions:
        blocks.append(
            "\n".join(
                [
                    f"Direction name: {direction['name']}",
                    f"Style intent: {direction['style']}",
                    f"Primary motifs: {direction['motifs']}",
                    f"Palette direction: {direction['palette']}",
                    f"Composition: {direction['composition']}",
                    "Favicon constraints: readable at 16x16 and 32x32 with a clear silhouette",
                    "Negative constraints: no text, no watermark, no mockup background, no trademark imitation, no intricate gradients",
                ]
            )
        )

    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text("\n---\n".join(blocks) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context-file", required=True, help="Path to repository brand context markdown.")
    parser.add_argument("--project-root", default=".", help="Project root used to infer product details.")
    parser.add_argument("--brief-output", required=True, help="Output path for brand brief markdown.")
    parser.add_argument("--prompts-output", required=True, help="Output path for logo prompts text.")
    args = parser.parse_args()

    context_path = pathlib.Path(args.context_file).resolve()
    project_root = pathlib.Path(args.project_root).resolve()
    brief_output = pathlib.Path(args.brief_output).resolve()
    prompts_output = pathlib.Path(args.prompts_output).resolve()

    context_text = context_path.read_text(encoding="utf-8", errors="ignore")
    raw_keywords = parse_keywords(context_text)
    project_name = detect_project_name(project_root)
    value_prop = detect_value_proposition(project_root)
    domain = infer_domain(raw_keywords, project_name)
    keywords = normalize_keywords(raw_keywords, domain, project_name)
    audience = infer_audience(domain)
    palette = infer_palette(domain)
    features = extract_core_features(project_root, keywords)

    write_brand_brief(
        brief_path=brief_output,
        project_name=project_name,
        value_prop=value_prop,
        audience=audience,
        domain=domain,
        features=features,
        keywords=keywords,
        palette=palette,
    )
    write_logo_prompts(prompt_path=prompts_output, keywords=keywords, palette=palette)

    print(f"[OK] Wrote brand brief: {brief_output}")
    print(f"[OK] Wrote logo prompts: {prompts_output}")


if __name__ == "__main__":
    main()
