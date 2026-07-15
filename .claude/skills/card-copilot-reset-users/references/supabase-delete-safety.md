# Supabase Auth Deletion Safety

## Purpose
This runbook is for deleting test users from Supabase Auth when QA needs a clean account state.

## Preconditions
- You have explicit approval for deletion in the current conversation.
- You are targeting test users only.
- Environment variables are set:
  - `SUPABASE_URL`
  - `SUPABASE_SERVICE_ROLE_KEY`

## Required sequence
1. Run a dry run first.
2. Validate matched users.
3. Run confirmed deletion.
4. Relaunch app and sign in again.

## Commands
Dry run:

```bash
node /Users/joy/.codex/skills/card-copilot-reset-users/scripts/delete_supabase_auth_users.mjs --email tester@example.com --dry-run
```

Delete one email:

```bash
node /Users/joy/.codex/skills/card-copilot-reset-users/scripts/delete_supabase_auth_users.mjs --email tester@example.com --confirm
```

Delete all auth users (high risk):

```bash
node /Users/joy/.codex/skills/card-copilot-reset-users/scripts/delete_supabase_auth_users.mjs --all --confirm
```

## Notes
- Auth deletion removes Supabase Auth identity.
- App-local data still requires Android local reset (`reset_card_copilot_local_state.sh`).
