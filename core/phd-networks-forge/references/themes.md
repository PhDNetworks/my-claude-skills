# Theme System

> Three pre-built themes + custom theme generation

## Theme Architecture

All themes use CSS custom properties for instant switching:

```html
<!-- Theme applied via data attribute -->
<div data-theme="dark-luxury">
  <!-- All children inherit theme variables -->
</div>
```

---

## Theme 1: Dark Luxury

Premium, authoritative, sophisticated. Inspired by luxury fashion and high-end editorial.

```css
:root[data-theme="dark-luxury"],
.forge-dark-luxury {
  /* Backgrounds */
  --bg-primary: #0a0a0a;
  --bg-secondary: #111111;
  --bg-tertiary: #1a1a1a;
  --bg-elevated: #1f1f1f;

  /* Text */
  --text-primary: #F5E6D3;
  --text-secondary: #999999;
  --text-muted: #666666;
  --text-inverse: #0a0a0a;

  /* Accents */
  --accent-primary: #C9A962;
  --accent-secondary: #E85A4F;
  --accent-hover: #E8D5A3;
  --accent-muted: rgba(201, 169, 98, 0.2);

  /* Borders */
  --border-subtle: rgba(255, 255, 255, 0.05);
  --border-default: rgba(255, 255, 255, 0.1);
  --border-hover: rgba(255, 255, 255, 0.2);

  /* Shadows */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);

  /* Typography */
  --font-display: 'Bebas Neue', 'Impact', sans-serif;
  --font-body: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;

  /* Font Weights */
  --weight-light: 300;
  --weight-regular: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --weight-bold: 700;

  /* Spacing Scale */
  --space-xs: 0.5rem;
  --space-sm: 1rem;
  --space-md: 2rem;
  --space-lg: 3rem;
  --space-xl: 5rem;
  --space-2xl: 7rem;

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-full: 9999px;

  /* Transitions */
  --transition-fast: 0.15s ease;
  --transition-base: 0.3s ease;
  --transition-slow: 0.5s ease;
}
```

**Best For**: Law firms, financial services, luxury brands, creative agencies, premium services

**Font CDN**:
```html
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

---

## Theme 2: Light Editorial

Clean, trustworthy, elegant. Inspired by editorial design and modern healthcare.

```css
:root[data-theme="light-editorial"],
.forge-light-editorial {
  /* Backgrounds */
  --bg-primary: #FAFAFA;
  --bg-secondary: #FFFFFF;
  --bg-tertiary: #F0F0F0;
  --bg-elevated: #FFFFFF;

  /* Text */
  --text-primary: #1a1a1a;
  --text-secondary: #4a4a4a;
  --text-muted: #888888;
  --text-inverse: #FFFFFF;

  /* Accents */
  --accent-primary: #2C3E50;
  --accent-secondary: #E74C3C;
  --accent-hover: #1a252f;
  --accent-muted: rgba(44, 62, 80, 0.1);

  /* Borders */
  --border-subtle: rgba(0, 0, 0, 0.05);
  --border-default: rgba(0, 0, 0, 0.1);
  --border-hover: rgba(0, 0, 0, 0.2);

  /* Shadows */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.12);

  /* Typography */
  --font-display: 'Playfair Display', Georgia, serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

  /* Font Weights */
  --weight-light: 300;
  --weight-regular: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --weight-bold: 700;

  /* Spacing Scale */
  --space-xs: 0.5rem;
  --space-sm: 1rem;
  --space-md: 2rem;
  --space-lg: 3rem;
  --space-xl: 5rem;
  --space-2xl: 7rem;

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-full: 9999px;

  /* Transitions */
  --transition-fast: 0.15s ease;
  --transition-base: 0.3s ease;
  --transition-slow: 0.5s ease;
}
```

**Best For**: Healthcare, education, lifestyle brands, professional services, editorial sites

**Font CDN**:
```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

---

## Theme 3: Bold Modern

Energetic, innovative, powerful. Inspired by tech companies and modern SaaS.

```css
:root[data-theme="bold-modern"],
.forge-bold-modern {
  /* Backgrounds */
  --bg-primary: #0D1117;
  --bg-secondary: #161B22;
  --bg-tertiary: #21262D;
  --bg-elevated: #30363D;

  /* Text */
  --text-primary: #FFFFFF;
  --text-secondary: #C9D1D9;
  --text-muted: #8B949E;
  --text-inverse: #0D1117;

  /* Accents */
  --accent-primary: #58A6FF;
  --accent-secondary: #F78166;
  --accent-hover: #79C0FF;
  --accent-muted: rgba(88, 166, 255, 0.15);

  /* Borders */
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-default: rgba(255, 255, 255, 0.16);
  --border-hover: rgba(255, 255, 255, 0.24);

  /* Shadows */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.4);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.5);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.6);

  /* Typography */
  --font-display: 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

  /* Font Weights */
  --weight-light: 300;
  --weight-regular: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --weight-bold: 700;
  --weight-black: 900;

  /* Spacing Scale */
  --space-xs: 0.5rem;
  --space-sm: 1rem;
  --space-md: 2rem;
  --space-lg: 3rem;
  --space-xl: 5rem;
  --space-2xl: 7rem;

  /* Border Radius */
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-full: 9999px;

  /* Transitions */
  --transition-fast: 0.15s ease;
  --transition-base: 0.3s ease;
  --transition-slow: 0.5s ease;
}
```

**Best For**: Tech startups, SaaS, digital agencies, gaming, innovation-focused brands

**Font CDN**:
```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

---

## Custom Theme Template

Generate custom themes from client brand colors:

```css
:root[data-theme="custom"],
.forge-custom {
  /* === CUSTOMIZE THESE === */
  --brand-primary: #YOUR_PRIMARY;
  --brand-secondary: #YOUR_SECONDARY;
  --brand-background: #YOUR_BG;

  /* === AUTO-DERIVED === */
  /* Backgrounds */
  --bg-primary: var(--brand-background);
  --bg-secondary: /* 5% lighter/darker */;
  --bg-tertiary: /* 10% lighter/darker */;
  --bg-elevated: /* 15% lighter/darker */;

  /* Text - ensure contrast */
  --text-primary: /* High contrast to bg */;
  --text-secondary: /* 70% opacity of primary */;
  --text-muted: /* 50% opacity of primary */;
  --text-inverse: var(--brand-background);

  /* Accents */
  --accent-primary: var(--brand-primary);
  --accent-secondary: var(--brand-secondary);
  --accent-hover: /* 15% lighter primary */;
  --accent-muted: /* 15% opacity primary */;

  /* Rest inherits from base */
}
```

---

## Theme Switching in JavaScript

```javascript
// Set theme
function setTheme(themeName) {
  document.documentElement.setAttribute('data-theme', themeName);
  localStorage.setItem('forge-theme', themeName);
}

// Get current theme
function getTheme() {
  return document.documentElement.getAttribute('data-theme') || 'dark-luxury';
}

// Initialize from storage
function initTheme() {
  const saved = localStorage.getItem('forge-theme');
  if (saved) setTheme(saved);
}
```

---

## Responsive Typography Scale

```css
/* Base (Mobile) */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 2rem;      /* 32px */
--text-4xl: 2.5rem;    /* 40px */
--text-5xl: 3rem;      /* 48px */

/* Display sizes use clamp for fluid scaling */
--display-sm: clamp(2rem, 5vw, 3rem);
--display-md: clamp(3rem, 8vw, 5rem);
--display-lg: clamp(4rem, 12vw, 8rem);
--display-xl: clamp(5rem, 15vw, 12rem);
--display-hero: clamp(4rem, 18vw, 16rem);
```

---

## Container Widths

```css
--container-sm: 640px;
--container-md: 768px;
--container-lg: 1024px;
--container-xl: 1280px;
--container-2xl: 1536px;

.forge-container {
  width: 100%;
  max-width: var(--container-xl);
  margin: 0 auto;
  padding: 0 var(--space-md);
}
```
