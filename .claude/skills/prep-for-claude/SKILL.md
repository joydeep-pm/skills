---
name: prep-for-claude
description: Prepare a repository so Claude Code behaves like a project-native engineer instead of a chatbot. Use when a repo needs a short root CLAUDE.md, progressive docs, local module memory files, hooks, and a clean handoff structure for parallel Claude implementation.
---

# Prep for Claude

Use this skill when onboarding Claude to a new or drifting repository.

The purpose is to make the repo legible to Claude through structure, not repeated prompting.

## Outcome

Produce a Claude-ready repo with:

1. A short root `CLAUDE.md`
2. Progressive context in `docs/`
3. Local `CLAUDE.md` files in critical modules
4. Guardrail scripts in `.claude/hooks/`
5. A practical handoff file for the next Claude session

## Workflow

1. Audit the repo first.
   - Identify the real product purpose
   - Identify code roots and critical modules
   - Identify canonical user data and sensitive paths
   - Identify the real verification commands

2. Tighten root memory.
   - Keep root `CLAUDE.md` short
   - Include only purpose, repo map, rules, and commands
   - Push long-form explanation into docs

3. Build progressive docs.
   - Add `docs/architecture.md`
   - Add at least one ADR in `docs/decisions/`
   - Add runbooks in `docs/runbooks/`

4. Add local context files.
   - Create local `CLAUDE.md` files in high-complexity or high-risk areas
   - Typical examples: app roots, assistant engines, integrations, infra, persistence

5. Add hook scripts.
   - Add scripts for checks or guardrails
   - Keep them simple and deterministic
   - Do not auto-wire destructive behavior
   - If Claude settings schema is uncertain, keep `.claude/settings.json` minimal

6. Create a handoff file.
   - Explain what exists
   - Explain what is missing
   - Explain what the next Claude session should build first

7. Verify the structure.
   - Confirm all referenced files exist
   - Run the repo's main verification commands if the changes touched runnable code

## Guardrails

1. Do not turn `CLAUDE.md` into a long essay.
2. Do not duplicate the same context everywhere.
3. Do not invent the project purpose; derive it from repo truth and user discovery.
4. Do not overload the repo with decorative AI files that add no operational value.
5. Keep the structure optimized for future sessions, not for one-time explanation.

## Minimum Deliverables

1. Root `CLAUDE.md`
2. `docs/architecture.md`
3. One ADR in `docs/decisions/`
4. One runbook in `docs/runbooks/`
5. One or more local `CLAUDE.md` files
6. `.claude/hooks/` scripts
7. A handoff file such as `build-plan.md` or `docs/runbooks/claude-handoff.md`

## Good Default Read Order For Claude

When you prepare the repo, make the structure support this read order:

1. `CLAUDE.md`
2. `requirements.md` or equivalent business context
3. `build-plan.md` or equivalent implementation plan
4. `docs/architecture.md`
5. relevant local `CLAUDE.md` files

## Success Check

Claude should be able to enter the repo and answer these without extra prompting:

1. Why does this system exist
2. Where does the main code live
3. What data is canonical
4. What actions are risky or forbidden
5. What should be built next
