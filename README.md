# skills

A collection of reusable Claude Code skills — job-search automation, writing,
research, PM workflows, deployment, and document generation. Some skills carry
`[PLACEHOLDER]` template tokens; fill these in with `/setup` (where present) or
by hand after cloning into your own project.

## Contents

### `.claude/skills/`

**Job search**
- **job-application-assistant** - Evaluate job postings, tailor CVs and cover letters (LaTeX/moderncv), prepare interview talking points.
- **job-scraper** - Search job portals via installed portal-search CLIs plus WebSearch, dedupe against previously seen jobs, surface new matches.
- **upskill** - Compare tracked job postings against a candidate profile to find skill gaps and generate a prioritized learning plan.

**Writing & prompting**
- **48** - Turn a rough idea into a finished, ready-to-send prompt optimized for Opus 4.8 in the chat app.
- **opus48-optimizer** - Turn a raw prompt into a precise, XML-structured prompt via a hard `prompt:` prefix trigger; API/XML-oriented workflow ported from CheswickDEV/claude-opus-4.8-prompt-optimizer.
- **fable-prompter** - Default prompt-optimization skill for Claude Fable 5 in chat/Cowork.
- **prompt-master** - Restructure messy, rambling requests into a clean task spec before executing.
- **joy-writing-voice** - Apply a personal voice profile to writing, rewriting, and ghostwriting tasks.
- **handoff** - Compress a long conversation into a structured handoff doc for a new session or teammate.
- **how-to** - Walk a non-technical user step by step from "I want to do X with Claude" to a finished result.

**Research**
- **last30days** - Deep research engine across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, and web from the last 30 days.
- **reddit-researcher** - Research a topic across Reddit, X, YouTube, LinkedIn, Hacker News, Web, and TechCrunch using Apify actors.
- **deep-research-synthesizer** - Synthesize large source sets into structured, cited insights and flag contradictions/gaps.

**Meetings & docs**
- **meeting-notes** - Turn a Granola/Notion meeting into a clean summary with action items.
- **granola-meeting-os** - Build an interactive visual dashboard from a Granola meeting, tailored to meeting type.
- **doc** - Read, create, or edit `.docx` documents with layout fidelity checks.
- **pdf** - Read, create, or review PDF files with visual rendering checks.
- **xlsx** - Open, edit, create, or clean `.xlsx`/`.csv`/`.tsv` spreadsheets.

**Presentations & visuals**
- **frontend-slides** - Build animation-rich HTML presentations from scratch or from a PPTX.
- **infographic-builder** - Turn text content into a single polished infographic PNG.
- **notebooklm** - Full programmatic access to Google NotebookLM (notebooks, sources, artifacts).
- **notebooklm-deck-branding** - Poll a NotebookLM deck, download and rebrand the PPTX once ready.
- **pm-brand-identity** - Generate brand direction and logo/icon assets from repo context using Gemini image models.
- **motion-video-hero** - Build cinematic hero sections with full-screen background video in React + Tailwind.

**Engineering workflow**
- **prep-for-claude** - Set up a repo (root CLAUDE.md, docs, hooks) so Claude Code works like a project-native engineer.
- **plan-exit-review** - End-of-plan quality gate: scope coverage, regression risk, validation evidence.
- **execute-phase** - Execute a phased plan with verification gates and tracking.
- **deploy-verify** - Deployment pipeline with pre/post verification gates for web and mobile.
- **vercel-deploy** - Deploy applications and websites to Vercel.
- **eas-apk-link** - Build Android APKs with Expo EAS and produce a shareable install link.
- **develop-web-game** - Dev/test loop for HTML/JS web games using Playwright.
- **clone-website** - Reverse-engineer and rebuild a website section by section.
- **card-copilot-reset-users** - Reset Card Co-Pilot user state for fresh testing.

**Personal utility**
- **familiar** - Reconstruct past on-screen activity and work summaries from Familiar stills data.
- **find-skills** - Discover and install other agent skills.

### `.agents/skills/`
Portal-specific job-search CLI tools (Bun/TypeScript) used by `job-scraper`:
`linkedin-search`, `jobindex-search`, `jobnet-search`, `jobdanmark-search`,
`jobbank-search`, `freehire-search`.

## Usage

Copy the relevant skill folder(s) from `.claude/skills/` (and `.agents/skills/`
for job-scraper's portal CLIs) into a project, fill in any `[PLACEHOLDER]`
tokens by hand, and the skills activate automatically based on their
`SKILL.md` descriptions.

Note: `clone-website` depends on a local `node_modules/` (Next.js) that is not
checked into this repo — run `npm install` inside that skill folder before use.
