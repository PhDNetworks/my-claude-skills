---
name: web-animation-tools
description: "Expert guidance for web animation development across Framer, Motion, GSAP, LottieFiles, Rive, Spline, After Effects, and Jitter. Use when building website animations, selecting animation tools, creating scroll effects, implementing 3D web elements, optimizing animation performance, or integrating animation libraries into React/JavaScript projects. Triggers on requests for motion design, page transitions, scroll animations, micro-interactions, loading animations, SVG animations, 3D web graphics, Lottie files, or animation tool comparisons."
---

# Web Animation Tools

Expert-level guidance for selecting and implementing web animations across the modern tooling ecosystem.

## Tool Selection Decision Tree

**Start here to recommend the right tool:**

```
What's the primary need?
│
├─ No-code website animations → Framer
│   └─ Need 3D elements? → Add Spline integration
│
├─ Programmatic control (code-based) →
│   ├─ React project, declarative API preferred → Motion
│   ├─ Complex choreography, precise timing → GSAP
│   └─ Cross-platform (web + mobile + games) → Rive
│
├─ Production-quality brand animations →
│   ├─ Already using Adobe suite → After Effects + Lottie
│   └─ File size/speed critical → Rive
│
├─ Quick marketing content at scale → Jitter
│
└─ Lightweight vector animations → LottieFiles
```

## Tool Deep Dives

### 1. Framer (No-Code Platform)

**Best for:** Designers, teams, visual animation creation without code

**Built-in capabilities:**
- Multi-step storytelling animations
- Drag/touch interactions
- Infinite loop animations
- Loading states
- Scroll-triggered effects
- Sequenced element animations

**Key insight:** Framer uses Motion under the hood, enabling code escape hatches for advanced needs.

**Integration points:**
- LottieFiles plugin for vector animations
- Rive plugin for interactive state machines
- Spline integration for 3D elements

### 2. Motion (Programmatic Animation Library)

**Best for:** React developers needing precise animation control

**Performance advantages:**
- 90% less code than GSAP for basic animations
- 75% lighter scroll animations
- Works with React and Vanilla JS

**Core pattern - Declarative animations:**

```jsx
import { motion } from "motion/react"

// Specify start/end states; Motion handles transitions
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0 }}
  transition={{ duration: 0.3 }}
/>
```

**Key use cases:**
- Layout animations (shared element transitions)
- Gesture responses (drag, tap, hover)
- Scroll-triggered animations
- Exit animations
- Physics-based interactions

**When to upgrade to GSAP:** Need frame-by-frame control over complex choreographed sequences.

### 3. GSAP (GreenSock Animation Platform)

**Best for:** Complex, precisely-timed animation sequences

**Key differentiator:** Imperative control over every animation step (vs Motion's declarative approach).

**Core pattern - Timeline sequences:**

```javascript
import gsap from "gsap"

const tl = gsap.timeline()
tl.to(".box", { x: 100, duration: 1 })
  .to(".box", { rotation: 360, duration: 0.5 })
  .to(".circle", { scale: 2, duration: 0.8 }, "-=0.3") // overlap
```

**Plugin ecosystem:**
- ScrollTrigger - scroll-based animations
- MorphSVG - shape morphing
- SplitText - text animations
- DrawSVG - SVG path drawing
- MotionPath - animate along paths

**Trade-offs:** Larger file size, steeper learning curve, more verbose code.

### 4. LottieFiles

**Best for:** Lightweight vector animations from design tools

**Performance stats:**
- Lottie JSON: 60% smaller than GIFs
- dotLottie: 98% smaller than GIFs
- 5x faster loading than traditional formats

**Workflow:**
1. Design in After Effects (or Lottie creator)
2. Export via Bodymovin plugin or LottieFiles
3. Embed via Lottie player

**Implementation:**

```html
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
<lottie-player 
  src="animation.json"
  background="transparent"
  speed="1"
  loop
  autoplay
></lottie-player>
```

**React implementation:**

```jsx
import Lottie from "lottie-react"
import animationData from "./animation.json"

<Lottie animationData={animationData} loop={true} />
```

**Ideal for:** Hero sections, loading indicators, icons, micro-interactions.

### 5. Rive

**Best for:** Interactive animations with state machines, cross-platform deployment

**Key advantages over Lottie:**
- Smaller file sizes
- Built-in state machine support
- Real-time editing
- Works on web, iOS, Android, Flutter, game engines

**Advanced features:**
- Skeletal animation
- Mesh deformation
- Responsive layouts
- Dynamic assets
- Audio integration

**Implementation:**

```jsx
import { useRive } from "@rive-app/react-canvas"

function Animation() {
  const { RiveComponent } = useRive({
    src: "animation.riv",
    stateMachines: "State Machine 1",
    autoplay: true,
  })
  return <RiveComponent />
}
```

**State machine triggers:**

```jsx
const { rive, RiveComponent } = useRive({...})
// Trigger state changes
rive.setTextRunValue("score", "100")
rive.setBooleanStateAtPath("isHovered", true, "Button")
```

### 6. Adobe After Effects + Lottie

**Best for:** Production-quality brand animations, complex motion graphics

**Export workflow:**
1. Create animation in After Effects
2. Install Bodymovin extension
3. Export as Lottie JSON
4. Optimize via LottieFiles

**Supported exports:**
- Lottie JSON (web-optimized)
- CSS keyframes
- SVG animations
- GIF (fallback)

**When to use:** Teams already in Adobe ecosystem, complex brand animations, cinematic quality needs.

**When to consider Rive instead:** File size critical, need real-time state machines, cross-platform deployment.

### 7. Spline (3D Animation)

**Best for:** 3D web elements without traditional 3D software complexity

**Capabilities:**
- Physics simulations
- Game controls
- 3D sculpting
- Parametric modeling
- Boolean operations
- Video textures
- Material layering

**Framer integration:**

```jsx
// In Framer, use Spline component
import Spline from "@splinetool/react-spline"

<Spline scene="https://prod.spline.design/xxx/scene.splinecode" />
```

**Standalone React:**

```jsx
import Spline from "@splinetool/react-spline"

function Scene() {
  return <Spline scene="https://prod.spline.design/xxx/scene.splinecode" />
}
```

**Event handling:**

```jsx
function onSplineEvent(e) {
  if (e.target.name === "Cube") {
    console.log("Cube clicked")
  }
}

<Spline scene={url} onMouseDown={onSplineEvent} />
```

### 8. Jitter

**Best for:** Quick marketing animations, team collaboration, social media content

**Export formats:** Video, GIF, Lottie

**Key features:**
- Pre-made animation templates
- Reusable components
- Shared team libraries
- Timeline-based editor

**Workflow:**
1. Select template or create from scratch
2. Customize timing, colors, content
3. Export to needed format
4. Embed or upload

**Ideal for:** Social media content, promotional banners, email animations, rapid iteration.

## Performance Optimization Guidelines

**File size priorities (smallest to largest):**
1. Rive (.riv)
2. dotLottie (.lottie)
3. Lottie JSON (.json)
4. Optimized GIF
5. Video (MP4/WebM)

**Animation performance checklist:**
- [ ] Use `transform` and `opacity` (GPU-accelerated)
- [ ] Avoid animating `width`, `height`, `margin`, `padding`
- [ ] Use `will-change` sparingly for heavy animations
- [ ] Implement `prefers-reduced-motion` media query
- [ ] Lazy-load off-screen animations
- [ ] Use Intersection Observer for scroll triggers

**Reduced motion support:**

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

```jsx
// React hook
const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)"
).matches
```

## Common Implementation Patterns

### Scroll-triggered fade-in (Motion)

```jsx
import { motion, useInView } from "motion/react"
import { useRef } from "react"

function FadeInSection({ children }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true })
  
  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6 }}
    >
      {children}
    </motion.div>
  )
}
```

### Staggered list animation (Motion)

```jsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(i => (
    <motion.li key={i} variants={item}>{i}</motion.li>
  ))}
</motion.ul>
```

### Parallax scroll effect (GSAP)

```javascript
import gsap from "gsap"
import { ScrollTrigger } from "gsap/ScrollTrigger"

gsap.registerPlugin(ScrollTrigger)

gsap.to(".parallax-bg", {
  yPercent: -30,
  ease: "none",
  scrollTrigger: {
    trigger: ".parallax-section",
    start: "top bottom",
    end: "bottom top",
    scrub: true
  }
})
```

## Quick Reference: When to Use What

| Need | Tool | Why |
|------|------|-----|
| No-code website | Framer | Visual editor, built-in effects |
| React animations | Motion | Declarative, lightweight |
| Complex sequences | GSAP | Frame-level control |
| Vector icons/loaders | LottieFiles | Tiny files, wide support |
| Interactive states | Rive | State machines, cross-platform |
| 3D elements | Spline | Browser-based, Framer integration |
| Brand production | After Effects | Industry standard, Lottie export |
| Marketing at scale | Jitter | Templates, team collaboration |
