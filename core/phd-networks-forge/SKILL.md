---
name: phd-networks-forge
description: "PhD Networks Forge - Premium web design system for creating stunning £100k-quality pages for any client. Features 3 pre-built themes (Dark Luxury, Light Editorial, Bold Modern), custom brand extraction, 5 hero variants, GSAP animations, Lenis smooth scroll, Three.js particles, context-dependent interactions (Corporate to Full Creative modes). Outputs self-contained Elementor HTML widget code. Triggers: landing page, hero section, web design, premium UI, luxury website, client page, Elementor widget, stunning website, animated page, scroll animations."
---

# PhD Networks Forge

> Premium web design system for £100k-quality pages

## Quick Start (2 Minutes)

### Step 1: Brand Extraction

Before generating ANY code, I need to know:

```
Business: _______________
Industry: _______________
Audience: _______________
Price Point: [ Budget | Mid | Premium | Luxury ]
```

**Colors** (provide hex or say "suggest based on industry"):
- Primary: _______________
- Accent: _______________
- Background preference: [ Dark | Light | Bold ]

**Typography mood**: [ Modern | Classic | Bold | Elegant | Technical ]

### Step 2: Select Theme

| Theme | Colors | Best For |
|-------|--------|----------|
| **Dark Luxury** | Black #0a0a0a / Gold #C9A962 / Coral #E85A4F | Law, Finance, Premium Services |
| **Light Editorial** | White #FAFAFA / Navy #2C3E50 / Red #E74C3C | Healthcare, Education, Lifestyle |
| **Bold Modern** | Dark #0D1117 / Blue #58A6FF / Orange #F78166 | Tech, SaaS, Startups |
| **Custom** | I'll generate from your brand colors | Any |

### Step 3: Select Interaction Mode

| Mode | Cursor | Magnetic | Particles | Best For |
|------|--------|----------|-----------|----------|
| **Corporate** | Subtle 16px | Light | Off | Legal, Finance, Healthcare |
| **Professional** | Standard 20px | Light | Off | Trades, B2B, Consultants |
| **Creative** | Prominent 24px | Strong | Optional | Agencies, Photographers |
| **Full** | Maximum 28px | Maximum | On | Tech, Portfolios, Showcases |

---

## CDN Dependencies

Add these to your page ONCE (in Elementor: Theme Builder > Header or via Code Snippets plugin):

```html
<!-- FORGE CORE - Required -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Dark Luxury Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<!-- Light Editorial Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<!-- Bold Modern Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<!-- GSAP Animation Library -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>

<!-- Lenis Smooth Scroll -->
<script src="https://unpkg.com/lenis@1.1.18/dist/lenis.min.js"></script>

<!-- Optional: Three.js for Particle Heroes -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
```

---

## Output Format

All code is **self-contained** for Elementor HTML widgets:

```html
<!-- FORGE: [Component Name] | Theme: [X] | Mode: [Y] -->
<style>
.forge-[unique-id] { /* Scoped styles - no conflicts */ }
</style>

<div class="forge-[unique-id]">
  <!-- Component HTML -->
</div>

<script>
(function() {
  // Self-executing, no global pollution
  // Component initialization
})();
</script>
<!-- END FORGE COMPONENT -->
```

---

## Components Library

### Heroes (5 Variants)
See [references/heroes.md](references/heroes.md)

1. **Stacked Typography** - Massive overlapping text, maximum impact
2. **Split Hero** - 50/50 text + visual element
3. **Video Background** - Full-bleed video with overlay
4. **Particle/3D** - Three.js interactive particle field
5. **Minimal Statement** - Elegant single headline

### UI Components
See [references/components.md](references/components.md)

- Feature cards (numbered, icon, image variants)
- Pricing tables (3-tier, comparison, toggle)
- Testimonials (quote, avatar, video)
- Social proof (logos marquee, stats counter)
- Forms (waitlist, contact, multi-step)
- Navigation (top, side, hamburger)
- CTAs (inline, floating, sticky)
- Footers (minimal, detailed, mega)

### Animations
See [references/animations.md](references/animations.md)

- Loading screens (3 variants)
- Scroll reveals (fade, slide, scale, stagger)
- Text animations (character, word, line split)
- Counter animations
- Parallax effects
- Lenis smooth scroll integration

### Interactions
See [references/interactions.md](references/interactions.md)

- Custom cursor (4 intensity modes)
- Magnetic buttons
- Hover effects
- Three.js particle configurations

---

## Theme Quick Reference

### Dark Luxury
```css
--bg-primary: #0a0a0a;
--bg-secondary: #111111;
--text-primary: #F5E6D3;
--text-secondary: #999999;
--accent-primary: #C9A962;
--accent-secondary: #E85A4F;
--font-display: 'Bebas Neue', sans-serif;
--font-body: 'Space Grotesk', sans-serif;
```

### Light Editorial
```css
--bg-primary: #FAFAFA;
--bg-secondary: #FFFFFF;
--text-primary: #1a1a1a;
--text-secondary: #4a4a4a;
--accent-primary: #2C3E50;
--accent-secondary: #E74C3C;
--font-display: 'Playfair Display', serif;
--font-body: 'Inter', sans-serif;
```

### Bold Modern
```css
--bg-primary: #0D1117;
--bg-secondary: #161B22;
--text-primary: #FFFFFF;
--text-secondary: #C9D1D9;
--accent-primary: #58A6FF;
--accent-secondary: #F78166;
--font-display: 'Montserrat', sans-serif;
--font-body: 'Inter', sans-serif;
```

---

## Key Principles

1. **Brand First** - Always extract brand identity before coding
2. **Theme Consistency** - Use CSS custom properties throughout
3. **Self-Contained** - Every output works standalone in Elementor
4. **Progressive Enhancement** - Core content works without JS
5. **Performance Balanced** - Impressive but fast loading
6. **Mobile First** - Responsive from 320px up
7. **Context Appropriate** - Match interaction intensity to industry

---

## Detailed References

- [Brand Extraction Protocol](references/brand-extraction.md)
- [Theme System](references/themes.md)
- [Hero Sections](references/heroes.md)
- [UI Components](references/components.md)
- [Animations](references/animations.md)
- [Interactions](references/interactions.md)
- [Performance Guide](references/performance.md)
