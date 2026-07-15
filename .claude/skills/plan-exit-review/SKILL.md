---
name: plan-exit-review
description: Structured end-of-plan quality gate for engineering work. Use when closing a non-trivial implementation plan, before marking work complete, before PR/merge, or before handoff to verify scope coverage, regression risk, validation evidence, and explicit follow-ups.
---

# Plan Exit Review

Run this workflow before declaring "done" on implementation work.

## Review Workflow

1. Reconfirm the finish line.
- Restate the original request and acceptance criteria.
- List the planned steps that must be complete.

2. Check delivered scope.
- Inspect changed files and compare them to intended scope.
- Flag any missing planned item or unexpected file touch.

3. Verify correctness.
- Run focused validation commands (tests, lint, typecheck, build) that cover the changed surface.
- Capture command-level evidence (pass/fail and relevant output summary).
- Record blockers explicitly if full verification cannot run.

4. Perform regression review.
- Review touched code for behavioral regressions, edge-case gaps, and contract mismatches.
- Check for missing error handling, unsafe assumptions, and stale TODO placeholders.
- Check whether tests need additions for newly introduced branches.

5. Decide release readiness.
- Mark status as `ready`, `partial`, or `blocked`.
- If not `ready`, provide the smallest next actions required to reach `ready`.

## Exit Report Template

Use this structure in the final handoff:

```md
Status: ready | partial | blocked

Scope Check
- Completed:
- Missing:
- Out-of-scope touched files:

Verification Evidence
- <command>: pass/fail (short result)
- <command>: pass/fail (short result)

Findings
- [P1/P2/P3] <issue and impact>

Residual Risks
- <risk>

Next Actions
1. <action>
2. <action>
```

## Quality Gates

Do not mark work complete until all applicable gates are satisfied:

- Align delivered behavior with acceptance criteria.
- Run at least one direct verification path for changed logic.
- Report unresolved risks and blockers explicitly.
- Provide concrete next actions when status is not `ready`.
