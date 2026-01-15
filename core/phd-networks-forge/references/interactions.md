# Interactions

> Context-dependent cursor, magnetic buttons, and particle systems

## Interaction Modes

Four intensity levels based on client industry:

| Mode | Cursor | Magnetic | Particles | Industries |
|------|--------|----------|-----------|------------|
| **Corporate** | Subtle (16px) | Light (0.15) | Off | Legal, Finance, Healthcare |
| **Professional** | Standard (20px) | Light (0.25) | Off | Trades, B2B, Consultants |
| **Creative** | Prominent (24px) | Strong (0.35) | Optional | Agencies, Photographers |
| **Full** | Maximum (28px) | Maximum (0.45) | On | Tech, Portfolios, Showcases |

---

## Mode Configuration

```javascript
const FORGE_MODES = {
  corporate: {
    cursor: {
      enabled: true,
      size: 16,
      borderWidth: 1,
      blend: 'normal',
      hoverScale: 1.5
    },
    magnetic: {
      enabled: true,
      strength: 0.15,
      threshold: 50
    },
    particles: {
      enabled: false
    },
    animation: {
      duration: 0.8,
      ease: 'power2.out'
    }
  },

  professional: {
    cursor: {
      enabled: true,
      size: 20,
      borderWidth: 2,
      blend: 'difference',
      hoverScale: 1.8
    },
    magnetic: {
      enabled: true,
      strength: 0.25,
      threshold: 75
    },
    particles: {
      enabled: false
    },
    animation: {
      duration: 0.6,
      ease: 'power3.out'
    }
  },

  creative: {
    cursor: {
      enabled: true,
      size: 24,
      borderWidth: 2,
      blend: 'difference',
      hoverScale: 2.2
    },
    magnetic: {
      enabled: true,
      strength: 0.35,
      threshold: 100
    },
    particles: {
      enabled: true,
      count: 50,
      opacity: 0.5
    },
    animation: {
      duration: 0.5,
      ease: 'power4.out'
    }
  },

  full: {
    cursor: {
      enabled: true,
      size: 28,
      borderWidth: 2,
      blend: 'exclusion',
      hoverScale: 2.5,
      fillOnHover: true
    },
    magnetic: {
      enabled: true,
      strength: 0.45,
      threshold: 120
    },
    particles: {
      enabled: true,
      count: 100,
      opacity: 0.8
    },
    animation: {
      duration: 0.4,
      ease: 'expo.out'
    }
  }
};
```

---

## Custom Cursor System

### Base Cursor HTML/CSS
```html
<!-- FORGE: Custom Cursor | Mode: [MODE] -->
<style>
.forge-cursor {
  pointer-events: none;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9998;
  mix-blend-mode: var(--cursor-blend, difference);
}

.forge-cursor__outer {
  width: var(--cursor-size, 20px);
  height: var(--cursor-size, 20px);
  border: var(--cursor-border, 2px) solid var(--accent-primary);
  border-radius: 50%;
  position: absolute;
  transform: translate(-50%, -50%);
  transition: width 0.3s, height 0.3s, background 0.3s, border 0.3s;
}

.forge-cursor__inner {
  width: 4px;
  height: 4px;
  background: var(--accent-primary);
  border-radius: 50%;
  position: absolute;
  transform: translate(-50%, -50%);
}

/* Hover state */
.forge-cursor.is-hovering .forge-cursor__outer {
  width: calc(var(--cursor-size, 20px) * var(--cursor-hover-scale, 1.8));
  height: calc(var(--cursor-size, 20px) * var(--cursor-hover-scale, 1.8));
  border-color: var(--accent-secondary);
}

/* Link hover - fill */
.forge-cursor.is-link .forge-cursor__outer {
  background: var(--accent-primary);
  border-color: var(--accent-primary);
}

/* Text hover */
.forge-cursor.is-text .forge-cursor__outer {
  width: 4px;
  height: calc(var(--cursor-size, 20px) * 2);
  border-radius: 2px;
}

/* Hide default cursor */
body.has-cursor {
  cursor: none;
}

body.has-cursor a,
body.has-cursor button,
body.has-cursor [data-cursor] {
  cursor: none;
}

/* Disable on touch devices */
@media (hover: none) {
  .forge-cursor {
    display: none !important;
  }
  body.has-cursor {
    cursor: auto;
  }
}
</style>

<div class="forge-cursor">
  <div class="forge-cursor__outer"></div>
  <div class="forge-cursor__inner"></div>
</div>

<script>
(function() {
  // Check for touch device
  if ('ontouchstart' in window) return;

  const cursor = document.querySelector('.forge-cursor');
  const outer = cursor.querySelector('.forge-cursor__outer');
  const inner = cursor.querySelector('.forge-cursor__inner');

  let mouseX = 0, mouseY = 0;
  let outerX = 0, outerY = 0;
  let innerX = 0, innerY = 0;

  // Set mode variables (customize per project)
  const mode = 'professional'; // corporate | professional | creative | full
  const config = FORGE_MODES[mode].cursor;

  document.documentElement.style.setProperty('--cursor-size', config.size + 'px');
  document.documentElement.style.setProperty('--cursor-blend', config.blend);
  document.documentElement.style.setProperty('--cursor-border', config.borderWidth + 'px');
  document.documentElement.style.setProperty('--cursor-hover-scale', config.hoverScale);

  document.body.classList.add('has-cursor');

  // Track mouse position
  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  // Smooth follow animation
  function animate() {
    // Outer cursor - slower follow
    outerX += (mouseX - outerX) * 0.15;
    outerY += (mouseY - outerY) * 0.15;
    outer.style.left = outerX + 'px';
    outer.style.top = outerY + 'px';

    // Inner cursor - faster follow
    innerX += (mouseX - innerX) * 0.35;
    innerY += (mouseY - innerY) * 0.35;
    inner.style.left = innerX + 'px';
    inner.style.top = innerY + 'px';

    requestAnimationFrame(animate);
  }
  animate();

  // Hover states
  const interactiveElements = document.querySelectorAll('a, button, [data-cursor]');

  interactiveElements.forEach(el => {
    el.addEventListener('mouseenter', () => {
      cursor.classList.add('is-hovering');
      if (el.tagName === 'A' || el.tagName === 'BUTTON') {
        cursor.classList.add('is-link');
      }
      if (el.dataset.cursor === 'text') {
        cursor.classList.add('is-text');
      }
    });

    el.addEventListener('mouseleave', () => {
      cursor.classList.remove('is-hovering', 'is-link', 'is-text');
    });
  });

  // Hide when leaving window
  document.addEventListener('mouseleave', () => {
    cursor.style.opacity = '0';
  });

  document.addEventListener('mouseenter', () => {
    cursor.style.opacity = '1';
  });
})();
</script>
```

---

## Magnetic Buttons

### Basic Magnetic Effect
```html
<!-- FORGE: Magnetic Button -->
<style>
.magnetic-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-sm) var(--space-lg);
  background: var(--accent-primary);
  color: var(--text-inverse);
  font-family: var(--font-body);
  font-weight: var(--weight-semibold);
  text-decoration: none;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background 0.3s ease;
  will-change: transform;
}

.magnetic-btn:hover {
  background: var(--accent-hover);
}

.magnetic-btn__text {
  position: relative;
  z-index: 1;
}
</style>

<a href="#" class="magnetic-btn">
  <span class="magnetic-btn__text">Get Started</span>
</a>

<script>
(function() {
  const mode = 'professional'; // Set per project
  const config = FORGE_MODES[mode].magnetic;

  if (!config.enabled) return;

  const buttons = document.querySelectorAll('.magnetic-btn');

  buttons.forEach(btn => {
    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;

      gsap.to(btn, {
        x: x * config.strength,
        y: y * config.strength,
        duration: 0.3,
        ease: 'power2.out'
      });
    });

    btn.addEventListener('mouseleave', () => {
      gsap.to(btn, {
        x: 0,
        y: 0,
        duration: 0.5,
        ease: 'elastic.out(1, 0.5)'
      });
    });
  });
})();
</script>
```

### Advanced Magnetic with Background Reveal
```html
<style>
.magnetic-btn-advanced {
  position: relative;
  padding: var(--space-md) var(--space-xl);
  background: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-default);
  overflow: hidden;
}

.magnetic-btn-advanced__bg {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: var(--accent-primary);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.4s ease, height 0.4s ease;
  z-index: 0;
}

.magnetic-btn-advanced:hover .magnetic-btn-advanced__bg {
  width: 300%;
  height: 300%;
}

.magnetic-btn-advanced:hover {
  color: var(--text-inverse);
  border-color: var(--accent-primary);
}
</style>

<a href="#" class="magnetic-btn magnetic-btn-advanced">
  <span class="magnetic-btn-advanced__bg"></span>
  <span class="magnetic-btn__text">Explore</span>
</a>
```

---

## Hover Effects

### Card Lift
```css
.forge-card-lift {
  transition: transform 0.4s ease, box-shadow 0.4s ease;
}

.forge-card-lift:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}
```

### Border Reveal
```html
<style>
.forge-border-reveal {
  position: relative;
  overflow: hidden;
}

.forge-border-reveal::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--accent-primary);
  transform: translateX(-100%);
  transition: transform 0.4s ease;
}

.forge-border-reveal:hover::before {
  transform: translateX(0);
}
</style>
```

### Image Zoom
```css
.forge-image-zoom {
  overflow: hidden;
}

.forge-image-zoom img {
  transition: transform 0.6s ease;
}

.forge-image-zoom:hover img {
  transform: scale(1.08);
}
```

### Text Underline Reveal
```html
<style>
.forge-underline-reveal {
  position: relative;
  display: inline-block;
}

.forge-underline-reveal::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--accent-primary);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.4s ease;
}

.forge-underline-reveal:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}
</style>

<a href="#" class="forge-underline-reveal">Hover me</a>
```

---

## Three.js Particle Background

### Floating Particles (Ambient)
```html
<canvas id="particle-bg"></canvas>

<script>
(function() {
  const mode = 'creative'; // Set per project
  const config = FORGE_MODES[mode].particles;

  if (!config.enabled) return;

  const canvas = document.getElementById('particle-bg');
  const ctx = canvas.getContext('2d');

  canvas.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
  `;

  let width, height;
  const particles = [];

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  // Create particles
  for (let i = 0; i < config.count; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      size: Math.random() * 3 + 1,
      opacity: Math.random() * config.opacity
    });
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;

      // Wrap around edges
      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(201, 169, 98, ${p.opacity})`;
      ctx.fill();
    });

    requestAnimationFrame(animate);
  }
  animate();
})();
</script>
```

### Interactive Particles (Mouse Follow)
```javascript
// Add mouse interaction to particles
let mouseX = width / 2;
let mouseY = height / 2;

document.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
});

function animate() {
  ctx.clearRect(0, 0, width, height);

  particles.forEach(p => {
    // Mouse attraction
    const dx = mouseX - p.x;
    const dy = mouseY - p.y;
    const dist = Math.sqrt(dx * dx + dy * dy);

    if (dist < 200) {
      const force = (200 - dist) / 200;
      p.vx += (dx / dist) * force * 0.02;
      p.vy += (dy / dist) * force * 0.02;
    }

    // Apply velocity with damping
    p.x += p.vx;
    p.y += p.vy;
    p.vx *= 0.99;
    p.vy *= 0.99;

    // Draw particle
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(201, 169, 98, ${p.opacity})`;
    ctx.fill();

    // Draw connections
    particles.forEach(p2 => {
      const dx2 = p.x - p2.x;
      const dy2 = p.y - p2.y;
      const dist2 = Math.sqrt(dx2 * dx2 + dy2 * dy2);

      if (dist2 < 100) {
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.strokeStyle = `rgba(201, 169, 98, ${0.1 * (1 - dist2 / 100)})`;
        ctx.stroke();
      }
    });
  });

  requestAnimationFrame(animate);
}
```

---

## Disable Interactions on Mobile

```javascript
// Utility to check for touch device
const isTouchDevice = () => {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
};

// Initialize interactions only on desktop
if (!isTouchDevice()) {
  initCustomCursor();
  initMagneticButtons();
  initParticles();
}
```
