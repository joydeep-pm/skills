# skills

A collection of reusable Claude Code skills, extracted from a personal job-search
automation framework. Personal profile data has been redacted back to
`[PLACEHOLDER]` template form - fill these in with `/setup` (or manually) after
cloning into your own project.

## Contents

### `.claude/skills/`
- **job-application-assistant** - Evaluate job postings against a candidate profile,
  tailor CVs and cover letters (LaTeX/moderncv), and prepare interview talking points.
- **job-scraper** - Search job portals via installed portal-search CLIs (see
  `.agents/skills/`) plus WebSearch, dedupe against previously seen jobs, and
  surface new matches with a quick fit assessment.
- **upskill** - Compare tracked job postings against a candidate profile to find
  skill gaps and generate a prioritized learning plan.

### `.agents/skills/`
Portal-specific job-search CLI tools (Bun/TypeScript) used by `job-scraper`:
`linkedin-search`, `jobindex-search`, `jobnet-search`, `jobdanmark-search`,
`jobbank-search`, `freehire-search`.

## Usage

Copy the `.claude/skills/` and `.agents/skills/` directories into a project,
run `/setup` (if using the companion setup skill) or fill in the
`[PLACEHOLDER]` tokens by hand, and the skills activate automatically based on
their `SKILL.md` descriptions.
