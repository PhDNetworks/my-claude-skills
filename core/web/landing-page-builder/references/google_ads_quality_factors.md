# Google Ads Quality Score Factors

## Overview

Quality Score is Google's rating of the quality and relevance of your keywords, ads, and landing pages. It affects:
- **Ad Rank** - Position in search results
- **CPC** - Cost per click (higher QS = lower CPC)
- **Eligibility** - Whether ads show at all

Score range: 1-10 (10 = best)

---

## Three Core Components

### 1. Landing Page Experience

**Weight:** ~39% of Quality Score

**What Google Evaluates:**
- Page relevance to keyword/ad
- Page load speed (Core Web Vitals)
- Mobile-friendliness
- Transparency & trustworthiness
- Easy navigation
- Clear contact information

**Ratings:**
- Above Average
- Average
- Below Average

**Optimization Targets:**
```
Core Web Vitals:
- LCP (Largest Contentful Paint): < 2.5s
- CLS (Cumulative Layout Shift): < 0.1
- INP (Interaction to Next Paint): < 200ms

Mobile:
- Responsive design (mandatory)
- Touch-friendly buttons (min 44x44px)
- No horizontal scrolling
- Readable text without zooming
```

### 2. Ad Relevance

**Weight:** ~22% of Quality Score

**What Google Evaluates:**
- Keyword appears in ad copy
- Ad matches search intent
- Ad group structure (tight themes)

**Best Practices:**
- Include keyword in headline
- Match ad messaging to landing page
- Use Single Keyword Ad Groups (SKAGs) for important terms
- Dynamic Keyword Insertion where appropriate

### 3. Expected Click-Through Rate (CTR)

**Weight:** ~39% of Quality Score

**What Google Evaluates:**
- Historical CTR of keyword
- Historical CTR of account
- Ad position normalization
- Device performance

**Improvement Strategies:**
- Strong, compelling headlines
- Clear value proposition
- Call-to-action in description
- Use of ad extensions (sitelinks, callouts, structured snippets)

---

## Landing Page Quality Checklist

### Content Requirements

```markdown
□ H1 contains primary keyword
□ Keyword appears in first 100 words
□ Clear service/product description
□ Unique, valuable content (not duplicate)
□ No thin content (min 300 words)
□ Clear call-to-action
□ Contact information visible
□ Business address (for local)
□ Trust signals (reviews, certifications)
```

### Technical Requirements

```markdown
□ HTTPS enabled
□ Mobile responsive
□ LCP < 2.5 seconds
□ CLS < 0.1
□ INP < 200ms
□ No intrusive interstitials
□ No auto-playing media with sound
□ Accessible (WCAG 2.1 AA)
```

### User Experience

```markdown
□ Clear navigation
□ Easy to find contact info
□ Form above the fold (or clear path to it)
□ No forced account creation
□ Transparent pricing (if applicable)
□ Privacy policy linked
□ Terms of service linked
```

---

## Quality Score by Component Status

| LP Experience | Ad Relevance | Expected CTR | Typical QS |
|--------------|--------------|--------------|------------|
| Above Avg | Above Avg | Above Avg | 8-10 |
| Above Avg | Above Avg | Average | 7-8 |
| Above Avg | Average | Above Avg | 7-8 |
| Average | Above Avg | Above Avg | 6-7 |
| Average | Average | Average | 5-6 |
| Below Avg | Any | Any | 1-4 |

---

## Impact on CPC

Quality Score significantly affects actual CPC through the Ad Rank formula:

```
Ad Rank = Max CPC × Quality Score × Ad Extension Impact

Actual CPC = (Competitor Ad Rank / Your QS) + £0.01
```

**Example Cost Savings:**

| Quality Score | Relative CPC |
|--------------|--------------|
| 10 | 50% discount |
| 8 | 25% discount |
| 6 | Baseline |
| 4 | 25% premium |
| 2 | 150% premium |

---

## Diagnostic Tools

### Google Ads Interface
- Keywords > Columns > Quality Score
- Shows component-level diagnostics

### PageSpeed Insights
- URL: https://pagespeed.web.dev/
- Tests Core Web Vitals
- Mobile and Desktop scores

### Google Search Console
- Core Web Vitals report
- Mobile Usability report

### Lighthouse
- Built into Chrome DevTools
- Performance, Accessibility, Best Practices, SEO

---

## Common Issues & Fixes

### "Below Average" Landing Page Experience

| Issue | Fix |
|-------|-----|
| Slow load time | Optimize images, enable caching, minimize JS |
| Not mobile-friendly | Implement responsive design |
| Thin content | Add detailed service descriptions |
| Missing contact info | Add phone, address, contact form |
| No trust signals | Add reviews, certifications, insurance badges |

### "Below Average" Ad Relevance

| Issue | Fix |
|-------|-----|
| Keyword not in ad | Add keyword to headline |
| Too many keywords per group | Split into tighter ad groups |
| Generic ad copy | Write specific ads per keyword theme |

### "Below Average" Expected CTR

| Issue | Fix |
|-------|-----|
| Weak headlines | Test stronger value propositions |
| No urgency | Add limited-time offers |
| Missing extensions | Add all relevant extensions |
| Poor ad position | Increase bids or improve QS |

---

## Landing Page Template Structure

For trade businesses (roofing, rendering, electrical, etc.):

```
1. Hero Section
   - H1 with primary keyword
   - Subheadline with location
   - Primary CTA (phone/quote)
   - Trust badges (4.9 stars, insured, X years)

2. Trust Signals Bar
   - Star rating
   - Insurance status
   - Years experience
   - Local badge

3. Services Section
   - 3-4 main services
   - Icon + title + description
   - Link to full service page

4. CTA Section
   - Prominent phone number
   - "Call Now" and "Request Callback" buttons
   - Urgency messaging

5. Contact Form
   - Name, Phone, Email, Message
   - Clear submit button
   - Success message

6. Footer
   - Contact details
   - Service areas
   - Accreditations
```

---

## Monitoring Schedule

| Task | Frequency |
|------|-----------|
| Check Quality Scores | Weekly |
| Run PageSpeed audits | Monthly |
| Review component diagnostics | Weekly |
| Test landing page changes | Per change |
| Competitor landing page review | Monthly |
