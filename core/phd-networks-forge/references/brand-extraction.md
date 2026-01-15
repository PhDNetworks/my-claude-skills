# Brand Extraction Protocol

> Extract brand identity before generating any code

## Quick Extraction (2 Minutes)

### Essential Questions

```
1. BUSINESS IDENTITY
   - Business name: _______________
   - Tagline/slogan (if any): _______________
   - Industry/sector: _______________
   - Years in business: _______________

2. TARGET AUDIENCE
   - Primary customer: _______________
   - Age range: _______________
   - Income level: [ Budget | Middle | Affluent | High-Net-Worth ]
   - What problem do you solve for them? _______________

3. BRAND POSITIONING
   - Price point: [ Budget | Mid-Market | Premium | Luxury ]
   - Competitors: _______________
   - What makes you different? _______________

4. VISUAL DIRECTION
   - Existing brand colors? [ Yes - provide hex | No - suggest ]
   - Logo style: [ Text | Icon | Combined | None yet ]
   - Overall mood: [ Professional | Friendly | Bold | Elegant | Minimal | Technical ]
```

---

## Industry-Specific Defaults

### Legal & Financial Services
```css
/* Recommended: Dark Luxury or Light Editorial */
--bg-primary: #0a0a0a;
--accent-primary: #C9A962;  /* Gold = trust, premium */
--font-display: 'Playfair Display', serif;  /* Classic authority */
```
**Interaction Mode**: Corporate
**Mood**: Authoritative, trustworthy, premium

### Healthcare & Medical
```css
/* Recommended: Light Editorial */
--bg-primary: #FAFAFA;
--accent-primary: #2C7A7B;  /* Teal = health, calm */
--font-display: 'Inter', sans-serif;  /* Clean, modern */
```
**Interaction Mode**: Corporate
**Mood**: Clean, trustworthy, caring

### Trade Services (Electrical, Plumbing, Roofing)
```css
/* Recommended: Bold Modern or Custom */
--bg-primary: #1a1a1a;
--accent-primary: #F59E0B;  /* Orange/Yellow = energy, trade */
--font-display: 'Montserrat', sans-serif;  /* Strong, reliable */
```
**Interaction Mode**: Professional
**Mood**: Reliable, professional, local

### Creative Agencies & Design
```css
/* Recommended: Dark Luxury or Bold Modern */
--bg-primary: #0a0a0a;
--accent-primary: #E85A4F;  /* Coral = creative, bold */
--font-display: 'Bebas Neue', sans-serif;  /* Impact */
```
**Interaction Mode**: Creative or Full
**Mood**: Bold, innovative, impressive

### Tech & SaaS
```css
/* Recommended: Bold Modern */
--bg-primary: #0D1117;
--accent-primary: #58A6FF;  /* Electric blue = tech */
--font-display: 'Montserrat', sans-serif;
```
**Interaction Mode**: Creative or Full
**Mood**: Modern, innovative, powerful

### E-commerce & Retail
```css
/* Recommended: Light Editorial or Custom */
--bg-primary: #FFFFFF;
--accent-primary: #000000;  /* High contrast for products */
--font-display: 'Inter', sans-serif;
```
**Interaction Mode**: Professional or Creative
**Mood**: Clean, product-focused, trustworthy

### Education & Training
```css
/* Recommended: Light Editorial */
--bg-primary: #FAFAFA;
--accent-primary: #5B21B6;  /* Purple = knowledge, wisdom */
--font-display: 'Playfair Display', serif;
```
**Interaction Mode**: Professional
**Mood**: Approachable, authoritative, inspiring

---

## Color Psychology Guide

| Color | Meaning | Best For |
|-------|---------|----------|
| **Gold #C9A962** | Luxury, premium, trust | Law, Finance, High-end |
| **Navy #2C3E50** | Professional, stable, trustworthy | Corporate, B2B |
| **Coral #E85A4F** | Energy, creativity, bold | Creative, Youth |
| **Teal #2C7A7B** | Health, calm, balance | Healthcare, Wellness |
| **Electric Blue #58A6FF** | Tech, innovation, future | SaaS, Tech |
| **Orange #F59E0B** | Energy, action, friendly | Trades, Retail |
| **Purple #5B21B6** | Wisdom, creativity, premium | Education, Luxury |
| **Green #059669** | Growth, nature, health | Eco, Finance, Health |
| **Red #E74C3C** | Urgency, passion, bold | Sales, Food, Entertainment |
| **Black #0a0a0a** | Luxury, sophistication | Premium, Fashion |

---

## Typography Pairing Guide

### Modern & Clean
```css
--font-display: 'Montserrat', sans-serif;
--font-body: 'Inter', sans-serif;
```
Best for: Tech, SaaS, Modern businesses

### Classic & Elegant
```css
--font-display: 'Playfair Display', serif;
--font-body: 'Inter', sans-serif;
```
Best for: Law, Finance, Luxury, Editorial

### Bold & Impactful
```css
--font-display: 'Bebas Neue', sans-serif;
--font-body: 'Space Grotesk', sans-serif;
```
Best for: Creative agencies, Events, Sports

### Professional & Trustworthy
```css
--font-display: 'Inter', sans-serif;
--font-body: 'Inter', sans-serif;
```
Best for: Healthcare, B2B, Corporate

---

## Custom Theme Generation

When client provides brand colors, generate theme:

```css
:root[data-theme="custom"] {
  /* From client brand */
  --brand-primary: [CLIENT_PRIMARY];
  --brand-secondary: [CLIENT_SECONDARY];

  /* Derive system colors */
  --bg-primary: [DARK_VERSION or #FAFAFA];
  --bg-secondary: [LIGHTER/DARKER_VARIANT];
  --bg-tertiary: [SUBTLE_VARIANT];

  --text-primary: [CONTRAST_COLOR];
  --text-secondary: [60%_OPACITY_VARIANT];
  --text-muted: [40%_OPACITY_VARIANT];

  --accent-primary: [CLIENT_PRIMARY];
  --accent-secondary: [CLIENT_SECONDARY];
  --accent-hover: [10%_LIGHTER_PRIMARY];

  /* Borders */
  --border-subtle: rgba([TEXT_RGB], 0.05);
  --border-hover: rgba([TEXT_RGB], 0.1);
}
```

---

## Extraction Checklist

Before generating code, confirm:

- [ ] Business name captured
- [ ] Industry identified
- [ ] Target audience defined
- [ ] Theme selected (or custom colors provided)
- [ ] Interaction mode chosen
- [ ] Typography mood set
- [ ] Any specific requirements noted

---

## Example Extraction

**Client**: JP Electrical (Leeds electrician)

```
Business: JP Electrical
Industry: Trade Services - Electrical
Audience: Homeowners, 30-60, middle to affluent
Position: Premium local electrician
Mood: Professional, reliable, modern

Theme: Bold Modern (customized)
Colors:
  --accent-primary: #F59E0B (electrical yellow)
  --accent-secondary: #1E40AF (trust blue)
  --bg-primary: #0D1117 (dark, professional)

Interaction Mode: Professional
Typography: Montserrat (strong) + Inter (clean)
```
