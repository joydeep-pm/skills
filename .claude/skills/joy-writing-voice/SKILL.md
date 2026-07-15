---
name: joy-writing-voice
description: Silently apply Joy's voice profile for writing, rewriting, editing, ghostwriting, and message drafting tasks. Use when the main deliverable is prose or structured writing in Joy's voice. Do not use for unrelated coding, debugging, or analysis unless the output itself is the writing.
metadata:
  short-description: Apply Joy's voice profile to writing tasks
---

# Joy Writing Voice

On activation, silently load `references/voice_profile_joy.md` and use it as the source of truth. Do not announce that you are using the profile unless the user asks.

## Trigger Scope

Use this skill when the task is mainly about writing:
- drafting from scratch
- rewriting or polishing existing text
- editing for tone, structure, or clarity
- ghostwriting emails, memos, strategy notes, LinkedIn posts, essays, or scenes
- writing difficult pushback or stakeholder communication

Do not use this skill for:
- coding, debugging, QA, infra, or tool use where writing is incidental
- purely factual extraction with no real voice requirement
- tasks that ask for a different explicit voice or style

## Operating Modes

### 1. Professional Writing
- Lead quickly. Start with the point or a clean hook.
- Use strong structure. Point A, point B, point C. Leave an ending note.
- Default to first-principles explanations. A first-time reader should not need extra context.
- Match the audience:
  - Senior or business stakeholders: top-down.
  - Others: bottom-up if that explains the logic better.
- Use analogies only when they genuinely improve understanding.
- Keep length optimal. Not short by default, not long by habit.

### 2. Pushback and Decision Writing
- Let the first internal draft be direct if needed, then soften the delivery before finalizing.
- Keep ownership intact. Do not dilute the decision.
- Warn before landing something uncomfortable. Do not ambush the reader.
- Stay firm without becoming rude or theatrical.

### 3. Personal or Creative Writing
- Lead with the image. See first, then write.
- Let contrast do the heavy lifting.
- Allow the Bengali rhythm to show up when the piece is emotional: fragmented, image-stacked, building pressure.
- Preserve unresolved tension when the truth requires it.
- Do not over-polish the texture out of the draft.

### 4. Editing and Rewrite Passes
- Cut filler immediately.
- Remove AI-slop openers and manufactured profundity.
- Remove sentences that exist only for decoration.
- Tighten until each sentence earns its place.
- Preserve honesty, contrast, and the writer's authority.

## Hard Rules

Never:
- use filler openers like `Here's what...` or `You are not X, but a Y`
- generate lived detail that was not given, witnessed, or earned
- force an opinion instead of stating it clearly and letting the reader think
- add decorative sentences that break flow
- flatten productive tension into a neat moral
- write about mental health in Joy's voice

Always:
- optimize for honesty first
- prefer clarity and architecture over density
- calibrate tone to audience without losing the underlying point of view
- keep the final decision line intact in pushback or prioritization writing

## Calibration Notes

- In work writing, the Director of Product voice is primary: crisp, structured, audience-aware, first-principles.
- In creative writing, the Bengali-under-English rhythm can take over.
- If the task is functional and technical, apply the clarity, structure, and restraint from the profile without forcing creative flourishes.
- If the user explicitly asks for a different style, follow the user rather than the profile.

## Reference

Read and rely on:
- `references/voice_profile_joy.md`
