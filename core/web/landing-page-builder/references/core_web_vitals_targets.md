# Core Web Vitals Targets & Optimization

## Overview

Core Web Vitals are Google's metrics for measuring real-world user experience. They directly impact:
- Search rankings (since 2021)
- Google Ads Quality Score
- User engagement and conversions

---

## The Three Metrics

### LCP - Largest Contentful Paint

**What it measures:** Loading performance - time until the largest content element is visible

**Targets:**
| Rating | Threshold |
|--------|-----------|
| Good | ≤ 2.5s |
| Needs Improvement | 2.5s - 4.0s |
| Poor | > 4.0s |

**Our Target: < 2.0s**

**Common LCP Elements:**
- Hero images
- Background images
- Large text blocks
- Video poster images

**Optimization Techniques:**

```markdown
1. Server Response Time
   □ Use fast hosting (target TTFB < 200ms)
   □ Enable server-side caching
   □ Use CDN for static assets
   □ Enable GZIP/Brotli compression

2. Resource Loading
   □ Preload LCP image: <link rel="preload" as="image" href="...">
   □ Inline critical CSS
   □ Defer non-critical JavaScript
   □ Remove render-blocking resources

3. Image Optimization
   □ Use modern formats (WebP, AVIF)
   □ Responsive images with srcset
   □ Proper sizing (no oversized images)
   □ Lazy load below-fold images only

4. Font Optimization
   □ Preload critical fonts
   □ Use font-display: swap
   □ Limit font variations
   □ Consider system font stack
```

---

### CLS - Cumulative Layout Shift

**What it measures:** Visual stability - how much the page layout shifts during load

**Targets:**
| Rating | Threshold |
|--------|-----------|
| Good | ≤ 0.1 |
| Needs Improvement | 0.1 - 0.25 |
| Poor | > 0.25 |

**Our Target: < 0.05**

**Common CLS Causes:**
- Images without dimensions
- Ads/embeds without reserved space
- Dynamically injected content
- Web fonts causing FOIT/FOUT

**Optimization Techniques:**

```markdown
1. Images & Media
   □ Always include width/height attributes
   □ Use aspect-ratio CSS property
   □ Reserve space with placeholder containers

2. Ads & Embeds
   □ Reserve space for ad slots
   □ Set explicit dimensions on iframes
   □ Use skeleton loaders for dynamic content

3. Fonts
   □ Preload critical fonts
   □ Use font-display: optional (prevents FOUT)
   □ Match fallback font metrics to web font

4. Dynamic Content
   □ Never insert content above existing content
   □ Use CSS transforms for animations
   □ Reserve space for lazy-loaded elements
```

**CSS for Zero CLS Images:**

```css
img {
  width: 100%;
  height: auto;
  aspect-ratio: 16 / 9; /* Set appropriate ratio */
}

/* Alternative: explicit dimensions */
.hero-image {
  width: 1200px;
  height: 600px;
  max-width: 100%;
  height: auto;
}
```

---

### INP - Interaction to Next Paint

**What it measures:** Responsiveness - time from user interaction to visual feedback

**Replaced FID (First Input Delay) in March 2024**

**Targets:**
| Rating | Threshold |
|--------|-----------|
| Good | ≤ 200ms |
| Needs Improvement | 200ms - 500ms |
| Poor | > 500ms |

**Our Target: < 150ms**

**Common INP Issues:**
- Heavy JavaScript execution
- Long tasks blocking main thread
- Slow event handlers
- Layout thrashing

**Optimization Techniques:**

```markdown
1. JavaScript Optimization
   □ Break up long tasks (> 50ms)
   □ Use requestIdleCallback for non-urgent work
   □ Defer non-critical JavaScript
   □ Use web workers for heavy computation

2. Event Handlers
   □ Debounce scroll/resize handlers
   □ Use passive event listeners
   □ Avoid layout reads in handlers
   □ Use event delegation

3. Rendering Performance
   □ Avoid forced synchronous layouts
   □ Use CSS transforms for animations
   □ Minimize DOM size (< 1500 nodes ideal)
   □ Use content-visibility for off-screen content

4. Third-Party Scripts
   □ Audit all third-party scripts
   □ Load non-critical scripts async
   □ Use facade pattern for embeds
   □ Set up resource hints (preconnect)
```

---

## Testing Tools

### Lab Tools (Simulated)

| Tool | URL | Best For |
|------|-----|----------|
| PageSpeed Insights | pagespeed.web.dev | Quick audits |
| Lighthouse | Chrome DevTools | Detailed analysis |
| WebPageTest | webpagetest.org | Advanced testing |

### Field Tools (Real User Data)

| Tool | URL | Best For |
|------|-----|----------|
| Chrome UX Report | CrUX Dashboard | Real user data |
| Search Console | search.google.com/search-console | Site-wide metrics |
| web-vitals.js | npm package | Custom monitoring |

---

## Optimization Priority Matrix

Based on impact and implementation effort:

| Priority | Optimization | Impact | Effort |
|----------|-------------|--------|--------|
| 1 | Image optimization | High | Low |
| 2 | Critical CSS inline | High | Low |
| 3 | Defer non-critical JS | High | Medium |
| 4 | Preload LCP image | High | Low |
| 5 | Add image dimensions | Medium | Low |
| 6 | Font optimization | Medium | Medium |
| 7 | CDN implementation | High | Medium |
| 8 | Server caching | High | Medium |

---

## WordPress-Specific Optimizations

### Recommended Plugins

```markdown
Performance:
- WP Rocket (premium) - Caching, minification, lazy load
- Autoptimize (free) - CSS/JS optimization
- ShortPixel (freemium) - Image optimization

Alternatives:
- LiteSpeed Cache (for LiteSpeed servers)
- W3 Total Cache (free comprehensive caching)
```

### wp-config.php Settings

```php
// Increase memory limit
define('WP_MEMORY_LIMIT', '256M');

// Disable post revisions
define('WP_POST_REVISIONS', 3);

// Increase autosave interval
define('AUTOSAVE_INTERVAL', 300);
```

### .htaccess Caching Rules

```apache
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
</IfModule>

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript
</IfModule>
```

---

## Elementor-Specific Optimizations

### Settings to Configure

```markdown
Elementor > Settings > Performance:
□ Improved Asset Loading: ON
□ CSS Print Method: External File
□ Google Fonts Load: Swap

Elementor > Settings > Advanced:
□ Generator Tag: OFF
□ Load Font Awesome 4: OFF (unless needed)

Page Settings > Layout:
□ Page Layout: Elementor Full Width (no theme overhead)
```

### Avoid These Elementor Patterns

```markdown
❌ Excessive sections/columns (aim < 50 per page)
❌ Background videos on hero (use image + play button)
❌ Multiple slider widgets
❌ Excessive animations
❌ Global widgets overuse
❌ Third-party Elementor addons (unless necessary)
```

---

## Monitoring & Alerts

### PageSpeed Insights API

```bash
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&strategy=mobile"
```

### Recommended Monitoring Schedule

| Check | Frequency |
|-------|-----------|
| PageSpeed audit | Weekly |
| Search Console CWV | Weekly |
| Real User Monitoring | Daily (automated) |
| Post-deployment check | Every change |

### Alert Thresholds

Set up alerts when metrics exceed:
- LCP > 3.0s
- CLS > 0.15
- INP > 250ms

---

## Quick Reference Card

```
┌──────────────────────────────────────────┐
│         CORE WEB VITALS TARGETS          │
├──────────────────────────────────────────┤
│  LCP (Loading)     │  < 2.5s  (aim 2.0s) │
│  CLS (Stability)   │  < 0.1   (aim 0.05) │
│  INP (Interactivity)│ < 200ms (aim 150ms)│
├──────────────────────────────────────────┤
│  QUICK WINS:                             │
│  • Optimize/compress images              │
│  • Add width/height to images            │
│  • Inline critical CSS                   │
│  • Defer non-critical JS                 │
│  • Preload LCP element                   │
│  • Use font-display: swap                │
└──────────────────────────────────────────┘
```
