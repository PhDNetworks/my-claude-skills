# Animations

> GSAP + Lenis patterns for premium motion design

## Setup

### Required CDN
```html
<!-- GSAP Core + Plugins -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>

<!-- Lenis Smooth Scroll -->
<script src="https://unpkg.com/lenis@1.1.18/dist/lenis.min.js"></script>
```

### Initialize Lenis
```javascript
// Smooth scroll setup
const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  direction: 'vertical',
  gestureDirection: 'vertical',
  smooth: true,
  smoothTouch: false,
  touchMultiplier: 2
});

function raf(time) {
  lenis.raf(time);
  requestAnimationFrame(raf);
}
requestAnimationFrame(raf);

// Connect to ScrollTrigger
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);
```

---

## Preferred Easing Functions

```javascript
// Smooth & Professional
'power2.out'    // Standard - most versatile
'power3.out'    // Slightly more dramatic
'power4.out'    // Bold & snappy

// Premium Feel
'expo.out'      // Luxury, high-end
'circ.out'      // Smooth deceleration

// Playful
'back.out(1.2)' // Slight overshoot
'elastic.out(1, 0.5)' // Bouncy (use sparingly)
```

---

## Loading Screen

### Full Page Loader
```html
<!-- FORGE: Loading Screen -->
<style>
.forge-loader {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--bg-primary);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.forge-loader__text {
  font-family: var(--font-display);
  font-size: clamp(2rem, 8vw, 5rem);
  color: var(--text-primary);
  overflow: hidden;
}

.forge-loader__text span {
  display: inline-block;
  transform: translateY(100%);
}

.forge-loader__progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background: var(--accent-primary);
  width: 0;
}

.forge-loader__counter {
  position: absolute;
  bottom: var(--space-lg);
  right: var(--space-lg);
  font-family: var(--font-body);
  color: var(--text-muted);
  font-size: var(--text-sm);
}
</style>

<div class="forge-loader">
  <div class="forge-loader__text">
    <span>L</span><span>O</span><span>A</span><span>D</span><span>I</span><span>N</span><span>G</span>
  </div>
  <div class="forge-loader__progress"></div>
  <div class="forge-loader__counter">0%</div>
</div>

<script>
(function() {
  const loader = document.querySelector('.forge-loader');
  const chars = document.querySelectorAll('.forge-loader__text span');
  const progress = document.querySelector('.forge-loader__progress');
  const counter = document.querySelector('.forge-loader__counter');

  const tl = gsap.timeline();

  // Animate letters in
  tl.to(chars, {
    y: 0,
    duration: 0.8,
    stagger: 0.05,
    ease: 'power4.out'
  });

  // Progress bar
  tl.to(progress, {
    width: '100%',
    duration: 1.5,
    ease: 'power2.inOut',
    onUpdate: function() {
      counter.textContent = Math.round(this.progress() * 100) + '%';
    }
  }, '-=0.3');

  // Hide loader
  tl.to(loader, {
    yPercent: -100,
    duration: 0.8,
    ease: 'power4.inOut',
    onComplete: () => loader.style.display = 'none'
  });
})();
</script>
```

---

## Scroll Reveal Patterns

### Fade Up
```javascript
gsap.registerPlugin(ScrollTrigger);

// Single element
gsap.from('.fade-up', {
  scrollTrigger: {
    trigger: '.fade-up',
    start: 'top 80%',
    toggleActions: 'play none none reverse'
  },
  y: 60,
  opacity: 0,
  duration: 1,
  ease: 'power3.out'
});

// Multiple elements with stagger
gsap.from('.fade-up-stagger', {
  scrollTrigger: {
    trigger: '.fade-up-stagger',
    start: 'top 80%'
  },
  y: 60,
  opacity: 0,
  duration: 0.8,
  stagger: 0.15,
  ease: 'power3.out'
});
```

### Slide In from Sides
```javascript
// From left
gsap.from('.slide-left', {
  scrollTrigger: {
    trigger: '.slide-left',
    start: 'top 75%'
  },
  x: -100,
  opacity: 0,
  duration: 1,
  ease: 'power3.out'
});

// From right
gsap.from('.slide-right', {
  scrollTrigger: {
    trigger: '.slide-right',
    start: 'top 75%'
  },
  x: 100,
  opacity: 0,
  duration: 1,
  ease: 'power3.out'
});
```

### Scale Reveal
```javascript
gsap.from('.scale-reveal', {
  scrollTrigger: {
    trigger: '.scale-reveal',
    start: 'top 80%'
  },
  scale: 0.8,
  opacity: 0,
  duration: 1,
  ease: 'power3.out'
});
```

### Clip Path Reveal
```javascript
gsap.from('.clip-reveal', {
  scrollTrigger: {
    trigger: '.clip-reveal',
    start: 'top 75%'
  },
  clipPath: 'inset(100% 0% 0% 0%)',
  duration: 1.2,
  ease: 'power4.out'
});
```

---

## Text Animations

### Character by Character
```javascript
// Split text into characters
function splitText(element) {
  const text = element.textContent;
  element.innerHTML = text.split('').map(char =>
    char === ' ' ? ' ' : `<span class="char">${char}</span>`
  ).join('');
  return element.querySelectorAll('.char');
}

const chars = splitText(document.querySelector('.split-text'));

gsap.from(chars, {
  scrollTrigger: {
    trigger: '.split-text',
    start: 'top 80%'
  },
  y: '100%',
  opacity: 0,
  duration: 0.6,
  stagger: 0.03,
  ease: 'power4.out'
});
```

### Word by Word
```javascript
function splitWords(element) {
  const words = element.textContent.split(' ');
  element.innerHTML = words.map(word =>
    `<span class="word"><span class="word-inner">${word}</span></span>`
  ).join(' ');
  return element.querySelectorAll('.word-inner');
}

const words = splitWords(document.querySelector('.split-words'));

gsap.from(words, {
  scrollTrigger: {
    trigger: '.split-words',
    start: 'top 80%'
  },
  y: '110%',
  duration: 0.8,
  stagger: 0.08,
  ease: 'power4.out'
});
```

### Line by Line
```javascript
function splitLines(element) {
  const lines = element.innerHTML.split('<br>');
  element.innerHTML = lines.map(line =>
    `<span class="line"><span class="line-inner">${line}</span></span>`
  ).join('');
  return element.querySelectorAll('.line-inner');
}

const lines = splitLines(document.querySelector('.split-lines'));

gsap.from(lines, {
  scrollTrigger: {
    trigger: '.split-lines',
    start: 'top 80%'
  },
  y: '100%',
  duration: 0.8,
  stagger: 0.15,
  ease: 'power3.out'
});
```

---

## Counter Animation

```html
<style>
.forge-counter {
  font-family: var(--font-display);
  font-size: clamp(3rem, 10vw, 6rem);
  color: var(--accent-primary);
}
</style>

<div class="forge-counter" data-target="500">0</div>

<script>
const counters = document.querySelectorAll('.forge-counter');

counters.forEach(counter => {
  const target = parseInt(counter.dataset.target);
  const suffix = counter.dataset.suffix || '';

  ScrollTrigger.create({
    trigger: counter,
    start: 'top 80%',
    onEnter: () => {
      gsap.to(counter, {
        innerHTML: target,
        duration: 2,
        ease: 'power2.out',
        snap: { innerHTML: 1 },
        onUpdate: function() {
          counter.textContent = Math.round(counter.innerHTML) + suffix;
        }
      });
    },
    once: true
  });
});
</script>
```

---

## Parallax Effects

### Simple Parallax
```javascript
gsap.to('.parallax-element', {
  scrollTrigger: {
    trigger: '.parallax-section',
    start: 'top bottom',
    end: 'bottom top',
    scrub: 1
  },
  y: -100,
  ease: 'none'
});
```

### Multi-layer Parallax
```javascript
gsap.utils.toArray('.parallax-layer').forEach((layer, i) => {
  const depth = layer.dataset.depth || (i + 1) * 0.2;

  gsap.to(layer, {
    scrollTrigger: {
      trigger: '.parallax-container',
      start: 'top bottom',
      end: 'bottom top',
      scrub: true
    },
    y: -200 * depth,
    ease: 'none'
  });
});
```

---

## Horizontal Scroll Section

```html
<style>
.forge-horizontal {
  overflow: hidden;
}

.forge-horizontal__wrapper {
  display: flex;
  width: max-content;
}

.forge-horizontal__panel {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
</style>

<section class="forge-horizontal">
  <div class="forge-horizontal__wrapper">
    <div class="forge-horizontal__panel">Panel 1</div>
    <div class="forge-horizontal__panel">Panel 2</div>
    <div class="forge-horizontal__panel">Panel 3</div>
    <div class="forge-horizontal__panel">Panel 4</div>
  </div>
</section>

<script>
const wrapper = document.querySelector('.forge-horizontal__wrapper');
const panels = gsap.utils.toArray('.forge-horizontal__panel');

gsap.to(panels, {
  xPercent: -100 * (panels.length - 1),
  ease: 'none',
  scrollTrigger: {
    trigger: '.forge-horizontal',
    pin: true,
    scrub: 1,
    end: () => '+=' + wrapper.offsetWidth
  }
});
</script>
```

---

## Image Reveal

```javascript
// Mask reveal (image inside container)
gsap.from('.image-reveal', {
  scrollTrigger: {
    trigger: '.image-reveal',
    start: 'top 75%'
  },
  clipPath: 'polygon(0 100%, 100% 100%, 100% 100%, 0 100%)',
  duration: 1.2,
  ease: 'power4.out'
});

// Scale + fade reveal
gsap.from('.image-scale-reveal', {
  scrollTrigger: {
    trigger: '.image-scale-reveal',
    start: 'top 80%'
  },
  scale: 1.2,
  opacity: 0,
  duration: 1.5,
  ease: 'power3.out'
});
```

---

## Section Transitions

### Scrub-based Color Change
```javascript
gsap.to('body', {
  scrollTrigger: {
    trigger: '.dark-section',
    start: 'top center',
    end: 'top 20%',
    scrub: true
  },
  backgroundColor: '#0a0a0a',
  color: '#F5E6D3'
});
```

### Pin and Fade
```javascript
ScrollTrigger.create({
  trigger: '.pinned-section',
  start: 'top top',
  end: '+=100%',
  pin: true,
  onUpdate: (self) => {
    gsap.to('.pinned-content', {
      opacity: 1 - self.progress,
      y: -50 * self.progress
    });
  }
});
```
