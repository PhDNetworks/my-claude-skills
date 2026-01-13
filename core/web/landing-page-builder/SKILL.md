---
name: landing-page-builder
description: World-class landing page deployment for Google Ads campaigns. Creates high-converting, Core Web Vitals-optimized WordPress/Elementor pages via SSH/WP-CLI. Integrates with Google Ads quality score requirements, local SEO schema, GA4 conversion tracking, and modern animations (Framer patterns, Motion, GSAP, LottieFiles). Use when deploying landing pages for PPC campaigns, optimizing page speed, improving Google Ads quality scores, or creating conversion-focused WordPress pages.
---

# Landing Page Builder

Expert-level landing page deployment system for Google Ads campaigns, optimized for Quality Score and Core Web Vitals.

## Capabilities

1. **WordPress/Elementor Deployment** - Create pages via SSH/WP-CLI
2. **Quality Score Optimization** - Match landing pages to ad keywords
3. **Core Web Vitals** - Performance-first page architecture
4. **Schema Markup** - Local business JSON-LD injection
5. **Conversion Tracking** - GA4 + Google Ads integration
6. **Animations** - Lightweight, CLS-safe motion design

---

## Google Ads Quality Score Targets

| Factor | Target | Implementation |
|--------|--------|----------------|
| Landing Page Experience | ABOVE_AVERAGE | Core Web Vitals pass, mobile-first, fast load |
| Ad Relevance | ABOVE_AVERAGE | H1/title/content match ad keywords exactly |
| Expected CTR | AVERAGE+ | Clear CTA, trust signals, social proof |

**Quality Score Components:**
- Page relevance to keyword (H1 must contain primary keyword)
- Mobile usability (responsive, touch-friendly)
- Page load speed (LCP < 2.5s critical)
- Secure (HTTPS required)
- Original content (no duplicate/thin content)

---

## Core Web Vitals Targets

| Metric | Target | How to Achieve |
|--------|--------|----------------|
| LCP (Largest Contentful Paint) | < 2.5s | Optimize hero image, preload fonts, minimize render-blocking |
| CLS (Cumulative Layout Shift) | < 0.1 | Set image dimensions, reserve space for dynamic content |
| INP (Interaction to Next Paint) | < 200ms | Minimize main thread work, defer non-critical JS |
| TTFB (Time to First Byte) | < 800ms | Server optimization, caching, CDN |

---

## Page Structure (High-Converting Layout)

```
┌─────────────────────────────────────────────────┐
│ HEADER: Logo | Phone (click-to-call) | CTA      │
├─────────────────────────────────────────────────┤
│ HERO SECTION                                    │
│ ├─ H1: Primary Keyword + Location               │
│ ├─ Subheading: Value proposition                │
│ ├─ Primary CTA button                           │
│ ├─ Trust badge row (5★, Years, Accreditations) │
│ └─ Hero image (WebP, lazy=false for LCP)        │
├─────────────────────────────────────────────────┤
│ TRUST SIGNALS                                   │
│ ├─ Review count & rating                        │
│ ├─ Years in business                            │
│ ├─ Accreditation logos                          │
│ └─ "As seen on" / media mentions                │
├─────────────────────────────────────────────────┤
│ SERVICES/BENEFITS (3-4 items)                   │
│ ├─ Icon + Title + Description                   │
│ └─ Links to detail pages                        │
├─────────────────────────────────────────────────┤
│ SOCIAL PROOF                                    │
│ ├─ Testimonials with names/photos               │
│ ├─ Before/after gallery (if applicable)         │
│ └─ Case study snippets                          │
├─────────────────────────────────────────────────┤
│ CTA SECTION                                     │
│ ├─ Phone number (prominent)                     │
│ ├─ Contact form (name, phone, message)          │
│ └─ Service areas / map                          │
├─────────────────────────────────────────────────┤
│ FOOTER                                          │
│ ├─ Local business schema (JSON-LD)              │
│ ├─ NAP (Name, Address, Phone)                   │
│ ├─ Service area list                            │
│ └─ Legal links                                  │
└─────────────────────────────────────────────────┘
```

---

## Animation Rules

**Guiding Principle:** Animations should enhance UX without impacting performance.

### Safe Animations (Use Freely)
- CSS `opacity` and `transform` transitions (GPU-accelerated)
- Scroll-triggered fade-ins (IntersectionObserver)
- Hover states on CTAs
- Subtle micro-interactions

### Use Sparingly
- Motion.js for scroll effects
- GSAP for complex sequences
- LottieFiles for icons/illustrations

### Avoid
- Animations that delay LCP (no animated hero text on load)
- Layout-shifting animations (causes CLS)
- Heavy JS animation libraries on critical path
- Auto-playing video above fold

### Implementation Pattern
```css
/* Safe scroll reveal */
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
```

---

## Deployment Workflow

### Prerequisites
- SSH access to WordPress server
- WP-CLI installed on server
- Elementor Pro active (for templates)

### Steps

1. **Generate Content**
   - Extract keywords from Google Ads campaign
   - Map keyword to H1, title, meta description
   - Generate service-specific copy

2. **Prepare Assets**
   - Optimize hero image (WebP, max 200KB)
   - Prepare trust badges
   - Format testimonials

3. **Deploy via SSH/WP-CLI**
   ```bash
   # Create page
   wp post create --post_type=page --post_title="Service in Location" --post_status=publish

   # Import Elementor template
   wp elementor library import template.json --page_id=123
   ```

4. **Inject Schema**
   - Local business JSON-LD
   - Service schema
   - FAQ schema (if applicable)

5. **Configure Tracking**
   - GA4 event tracking
   - Google Ads conversion pixel
   - Phone call tracking

6. **Validate**
   - Run PageSpeed Insights
   - Check mobile usability
   - Verify conversion tracking fires

---

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `local-schema-generator` | Generate JSON-LD for local business |
| `technical-seo` | Crawl/index verification |
| `web-performance-audit` | Core Web Vitals audit |
| `web-animation-tools` | Animation implementation patterns |
| `google-ads-manager` | Update ad URLs, monitor quality scores |

---

## File Structure

```
core/web/landing-page-builder/
├── SKILL.md                          # This file
├── scripts/
│   ├── deploy_landing_page.py        # Main orchestrator
│   ├── wp_cli_commands.py            # WordPress operations
│   ├── performance_optimizer.py      # Image/CSS optimization
│   ├── schema_generator.py           # JSON-LD generation
│   └── conversion_tracking.py        # GA4/Ads pixel setup
├── templates/
│   ├── elementor/                    # Elementor JSON templates
│   │   ├── hero-section.json
│   │   ├── trust-signals.json
│   │   ├── service-features.json
│   │   ├── cta-section.json
│   │   └── contact-form.json
│   └── css/
│       ├── critical.css              # Above-fold critical CSS
│       └── animations.css            # Safe animation classes
├── references/
│   ├── google_ads_quality_factors.md
│   ├── core_web_vitals_targets.md
│   └── wordpress_optimization.md
└── config/
    ├── ssh_config.json               # Server credentials (gitignored)
    └── site_configs/                 # Per-site configurations
        ├── jlr_smith_roofing.json
        └── leeds_rendering.json
```

---

## Usage Examples

### Create Landing Page for Keyword
```
User: Create a landing page for "roof repairs leeds" targeting JLR Smith Roofing
Assistant: [Uses landing-page-builder to generate optimized page]
```

### Audit and Improve Existing Page
```
User: The landing page for Leeds Rendering has BELOW_AVERAGE quality score. Fix it.
Assistant: [Audits page, identifies issues, deploys optimized version]
```

### Bulk Deployment
```
User: Create landing pages for all JLR Smith Roofing services
Assistant: [Creates pages for roof repairs, chimney repairs, fascias, guttering]
```

---

## Contact

**Owner:** Danny Doherty
**Company:** PhD Networks & Systems Ltd
**Location:** Leeds, UK
