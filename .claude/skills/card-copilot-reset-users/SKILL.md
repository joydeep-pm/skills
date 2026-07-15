---
name: card-copilot-reset-users
description: Reset Card Co-Pilot user state for fresh testing. Use this when the user asks to delete users, start onboarding from scratch, clear app data on Android, or remove Supabase Auth users for test accounts.
---

# Card Co-Pilot Reset Users

## Overview
Use this skill to perform safe, repeatable user resets for Card Co-Pilot.
It supports local Android app resets and optional Supabase Auth user deletion for test environments.

## When To Use
- User asks to "delete users" or "start fresh onboarding".
- Local app state must be wiped on a connected Android device.
- QA requires deleting test accounts from Supabase Auth.

## Workflow
1. Run local reset first (fastest way to verify onboarding from zero).
2. If requested, run remote Supabase Auth deletion with explicit scope.
3. Relaunch app and confirm it opens to fresh auth/onboarding.

## Local Reset (Android Device)
Run from repo root:

```bash
bash /Users/joy/.codex/skills/card-copilot-reset-users/scripts/reset_card_copilot_local_state.sh \
  --package com.cardcopilot.app \
  --apk android/app/build/outputs/apk/release/app-release.apk
```

Behavior:
- Tries `pm clear` first.
- If OEM blocks `pm clear`, automatically falls back to uninstall/reinstall.
- Launches app after reset.

## Remote Reset (Supabase Auth)
Read [references/supabase-delete-safety.md](references/supabase-delete-safety.md) before running.

Dry run for one email:

```bash
node /Users/joy/.codex/skills/card-copilot-reset-users/scripts/delete_supabase_auth_users.mjs \
  --email tester@example.com \
  --dry-run
```

Execute for one email:

```bash
node /Users/joy/.codex/skills/card-copilot-reset-users/scripts/delete_supabase_auth_users.mjs \
  --email tester@example.com \
  --confirm
```

Execute for all Auth users (dangerous):

```bash
node /Users/joy/.codex/skills/card-copilot-reset-users/scripts/delete_supabase_auth_users.mjs \
  --all \
  --confirm
```

## Required Environment (remote reset only)
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

## Guardrails
- Always run dry-run first for remote deletion.
- Never run `--all` without explicit user confirmation in the same turn.
- Prefer local reset when user only needs fresh onboarding on one device.
