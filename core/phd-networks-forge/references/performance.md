# Performance Guide

> Optimization strategies for balanced impact and speed

## Core Principles

1. **Progressive Enhancement** - Core content works without JavaScript
2. **Graceful Degradation** - Animations enhance but don't block
3. **Mobile First** - Optimize for mobile, enhance for desktop
4. **Lazy Loading** - Load assets as needed
5. **Minimal DOM** - Keep markup clean and efficient

---

## CDN Loading Strategy

### Recommended Load Order
```html
<head>
  <!-- 1. Critical CSS inline in <head> -->
  <style>
    /* Critical above-the-fold styles */
  </style>

  <!-- 2. Preconnect to CDNs -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://cdnjs.cloudflare.com">

  <!-- 3. Font loading with display=swap -->
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>

<body>
  <!-- Content here -->

  <!-- 4. JS at end of body -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
  <script src="https://unpkg.com/lenis@1.1.18/dist/lenis.min.js"></script>

  <!-- 5. Initialize last -->
  <script>
    // Your initialization code
  </script>
</body>
```

### Defer Non-Critical Libraries
```html
<!-- Three.js only when needed -->
<script>
  // Load Three.js dynamically for particle heroes
  if (document.querySelector('.forge-hero-particle')) {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
    script.onload = initParticleHero;
    document.body.appendChild(script);
  }
</script>
```

---

## Animation Performance

### Use will-change Sparingly
```css
/* Only on elements that WILL animate */
.will-animate {
  will-change: transform, opacity;
}

/* Remove after animation completes */
.animation-complete {
  will-change: auto;
}
```

### GPU-Accelerated Properties
```css
/* GOOD - GPU accelerated */
transform: translateX(100px);
transform: scale(1.1);
opacity: 0.5;

/* AVOID - causes reflow/repaint */
left: 100px;
width: 200px;
height: 200px;
```

### GSAP Best Practices
```javascript
// Use transforms instead of position
gsap.to(element, {
  x: 100,        // ✓ Good
  y: 50,         // ✓ Good
  // left: 100,  // ✗ Avoid
  // top: 50,    // ✗ Avoid
});

// Force GPU acceleration
gsap.to(element, {
  x: 100,
  force3D: true  // Adds translateZ(0)
});

// Clean up ScrollTriggers
ScrollTrigger.getAll().forEach(trigger => trigger.kill());
```

---

## Image Optimization

### Responsive Images
```html
<picture>
  <source
    srcset="image-400.webp 400w, image-800.webp 800w, image-1200.webp 1200w"
    sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
    type="image/webp"
  >
  <source
    srcset="image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w"
    sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
    type="image/jpeg"
  >
  <img src="image-800.jpg" alt="Description" loading="lazy">
</picture>
```

### Lazy Loading
```html
<!-- Native lazy loading -->
<img src="image.jpg" loading="lazy" alt="Description">

<!-- For background images -->
<div class="lazy-bg" data-bg="image.jpg"></div>

<script>
const lazyBgs = document.querySelectorAll('.lazy-bg');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el = entry.target;
      el.style.backgroundImage = `url(${el.dataset.bg})`;
      observer.unobserve(el);
    }
  });
}, { rootMargin: '100px' });

lazyBgs.forEach(bg => observer.observe(bg));
</script>
```

---

## Graceful Degradation

### No-JS Fallback
```html
<noscript>
  <style>
    /* Show content without animations */
    .fade-up, .slide-in, .scale-reveal {
      opacity: 1 !important;
      transform: none !important;
    }

    /* Hide JS-only elements */
    .forge-cursor,
    .forge-loader {
      display: none !important;
    }
  </style>
</noscript>
```

### Reduced Motion Support
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

```javascript
// Check for reduced motion preference
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

if (!prefersReducedMotion.matches) {
  // Initialize animations
  initGSAPAnimations();
  initLenis();
  initParticles();
}
```

### Touch Device Detection
```javascript
const isTouchDevice = () => {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
};

// Disable cursor and magnetic on touch
if (!isTouchDevice()) {
  initCustomCursor();
  initMagneticButtons();
}
```

---

## Elementor-Specific Optimizations

### Scope Styles to Avoid Conflicts
```css
/* Always use unique prefixes */
.forge-hero-stacked { /* ... */ }
.forge-feature-card { /* ... */ }

/* Never use generic selectors */
/* ✗ Avoid */
.hero { }
.card { }
.btn { }
```

### Self-Contained IIFE Pattern
```javascript
(function() {
  // All code wrapped to avoid global pollution
  const element = document.querySelector('.forge-component');
  if (!element) return;

  // Component code here
})();
```

### Check for Dependencies
```javascript
(function() {
  // Check GSAP loaded
  if (typeof gsap === 'undefined') {
    console.warn('FORGE: GSAP not loaded');
    return;
  }

  // Check ScrollTrigger registered
  if (typeof ScrollTrigger === 'undefined') {
    console.warn('FORGE: ScrollTrigger not loaded');
    return;
  }

  gsap.registerPlugin(ScrollTrigger);
  // Continue with code
})();
```

---

## Loading Performance

### Critical CSS
```html
<style>
/* Inline critical above-the-fold styles */
:root {
  --bg-primary: #0a0a0a;
  --text-primary: #F5E6D3;
  /* ... other CSS variables */
}

body {
  margin: 0;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: system-ui, sans-serif;
}

.forge-hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
}
</style>
```

### Font Loading Strategy
```css
/* Use font-display: swap */
@font-face {
  font-family: 'Bebas Neue';
  src: url('bebas-neue.woff2') format('woff2');
  font-display: swap;
}

/* Fallback stack for web fonts */
--font-display: 'Bebas Neue', 'Impact', 'Arial Black', sans-serif;
--font-body: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

---

## Debugging Performance

### Chrome DevTools Checklist

1. **Lighthouse Audit**
   - Performance score > 90
   - First Contentful Paint < 1.8s
   - Largest Contentful Paint < 2.5s
   - Cumulative Layout Shift < 0.1

2. **Performance Panel**
   - Check for long tasks (> 50ms)
   - Identify layout thrashing
   - Monitor memory usage

3. **Coverage Panel**
   - Remove unused CSS/JS
   - Identify code that can be deferred

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Janky scroll | Layout thrashing | Use transforms, not position |
| Slow load | Large images | Compress, use WebP, lazy load |
| Flash of unstyled content | Fonts loading | Use font-display: swap |
| Memory leaks | Uncleared listeners | Clean up on page unload |
| Animation stutter | Too many elements | Reduce particle count, batch updates |

---

## Performance Budget

### Recommended Limits

| Resource | Budget |
|----------|--------|
| HTML | < 100KB |
| CSS (total) | < 100KB |
| JS (total) | < 300KB |
| Images (above fold) | < 200KB |
| Web fonts | < 100KB |
| First Contentful Paint | < 1.5s |
| Time to Interactive | < 3s |

### Per-Component Budget
- Each Forge component: < 15KB (HTML + CSS + JS)
- GSAP core: ~60KB (shared across all)
- ScrollTrigger: ~25KB (shared across all)
- Lenis: ~10KB (shared across all)
