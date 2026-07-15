# Execute Phase Skill

Execute a GSD phase with verification gates and proper tracking.

## Workflow

1. **Read Phase Plans**: Load all PLAN.md files for the current phase
2. **Sequential Execution**: Execute each plan in order, creating sub-agents only for parallelizable work
3. **Verification Gates**: After each plan completion:
   - Run `npx tsc --noEmit` to check TypeScript
   - Run `node --test tests/*.test.js` to verify tests pass
   - Verify ALL checklist items are checked off
4. **Never Skip Verification**: Do NOT declare a plan complete until:
   - All checkboxes are checked
   - TypeScript compiles with zero errors
   - All tests pass
5. **Rate Limit Resilience**: If rate-limited, save progress to PROGRESS.md and list remaining items clearly
6. **Update Tracking**: Update relevant tracking files (PROGRESS.md, handoff.md) with completion status

## Rules

- Write actual code, not planning documents
- Bold changes for UI work - match reference aesthetic, not just tokens
- Limit concurrent sub-agents to 2 maximum to avoid rate limits
- Commit after each completed plan with conventional commit message
- If blocked, document the blocker and next steps clearly
