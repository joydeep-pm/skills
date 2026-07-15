---
name: motion-video-hero
description: Build and iterate high-impact landing-page hero sections with full-screen background motion video in React + Tailwind CSS. Use when users ask for cinematic hero sections, glassmorphism overlays, modern fintech/SaaS hero layouts, navbar + centered copy + bottom feature strip composition, or screenshot/reference matching with video scaling and focal-point tuning.
---

# Motion Video Hero

Follow this workflow when implementing or refining motion-video hero sections.

## 1) Capture design inputs
Collect and confirm:
- Video URL(s)
- Hero copy (tag, headline, subtitle, CTA)
- Navbar items and actions
- Bottom feature cards/steps
- Required video scale/focal point (example: `scale-150`, `object-left-top`, `origin-top-left`)
- Reference screenshot priorities (typography, spacing, card treatment, corner radius)

## 2) Compose the layout skeleton
Implement this structure in React:
1. Full-viewport section wrapper: `relative min-h-screen overflow-hidden bg-black text-white`
2. Absolute background video layer
3. Overlay layers (dark tint + gradient)
4. Absolute top navbar
5. Centered hero content stack
6. Floating or anchored bottom feature strip

Keep content layers above video with explicit `z-*` values.

## 3) Use reliable video playback behavior
Use all of these by default:
- `autoPlay`, `loop`, `muted`, `playsInline`, `preload="auto"`
- `onLoadedData` handler that attempts `video.play()`
- `useRef` + `useEffect` that retries `play()` after source changes

If a URL may contain an accidental space in filename, try both URL variants:
- no-space filename
- `%20` encoded variant

If video fails entirely, render a designed fallback background (gradient/radial glow), not a blank block.

## 4) Match the visual system
Default styling direction:
- High contrast black base
- White typography with opacity hierarchy (`text-white`, `text-white/80`, `text-white/65`)
- Glassmorphism accents: `bg-black/70`, `backdrop-blur-xl`, `border border-white/15`
- CTA emphasis with white pill buttons and subtle hover scale (`hover:scale-105`)

For screenshot matching, prioritize in this order:
1. Layout proportions and spacing
2. Typography scale/line-height
3. Overlay darkness and readability
4. Fine details (icon size, border alpha, corner radius)

## 5) Responsive and implementation checks
Before finishing:
- Verify mobile layout does not clip headline/CTA
- Verify bottom cards collapse cleanly (`grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`)
- Ensure nav center links hide/adjust on small screens
- Keep copy text exact when user provides fixed wording

## 6) Output style
When delivering changes:
- Mention where the component lives
- Mention any playback fallbacks added
- Provide exact run command(s)

For reusable starter patterns, read `references/react-tailwind-template.md`.
