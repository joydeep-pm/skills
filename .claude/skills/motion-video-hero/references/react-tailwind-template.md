# React + Tailwind Motion Hero Template

Use this as a base pattern and replace placeholder text/content.

```jsx
import { useEffect, useRef, useState } from "react";

const VIDEO_URLS = ["<primary-mp4>", "<secondary-mp4-or-same>"];

export default function MotionHero() {
  const videoRef = useRef(null);
  const [videoIndex, setVideoIndex] = useState(0);
  const [videoFailed, setVideoFailed] = useState(false);

  useEffect(() => {
    const el = videoRef.current;
    if (!el) return;
    el.play().catch(() => {});
  }, [videoIndex]);

  const onVideoError = () => {
    if (videoIndex < VIDEO_URLS.length - 1) {
      setVideoIndex((x) => x + 1);
      return;
    }
    setVideoFailed(true);
  };

  const onLoadedData = () => {
    const el = videoRef.current;
    if (!el) return;
    el.play().catch(() => {});
  };

  return (
    <section className="relative min-h-screen overflow-hidden bg-black text-white">
      {!videoFailed ? (
        <video
          key={VIDEO_URLS[videoIndex]}
          ref={videoRef}
          className="absolute inset-0 h-full w-full origin-top-left scale-150 object-cover object-left-top"
          src={VIDEO_URLS[videoIndex]}
          autoPlay
          loop
          muted
          playsInline
          preload="auto"
          onError={onVideoError}
          onLoadedData={onLoadedData}
        />
      ) : (
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_75%_75%,rgba(255,60,132,0.55),transparent_34%),linear-gradient(180deg,#070707_0%,#000_100%)]" />
      )}

      <div className="absolute inset-0 bg-black/30" />
      <div className="absolute inset-0 bg-gradient-to-b from-black/75 via-black/40 to-black/80" />

      <nav className="absolute top-0 z-30 w-full px-6 py-4">...</nav>
      <main className="relative z-20 mx-auto flex min-h-screen max-w-5xl flex-col items-center justify-center px-6 text-center">...</main>
      <aside className="pointer-events-none absolute bottom-4 z-20 w-full px-4">...</aside>
    </section>
  );
}
```

## Tailwind v4 reminder
Use this in `src/index.css`:

```css
@import "tailwindcss";
```

And add plugin in `vite.config.js`:

```js
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```
