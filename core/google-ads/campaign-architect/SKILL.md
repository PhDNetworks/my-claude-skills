---
name: google-ads-campaign-architect
description: Build complete Google Ads campaign structures for UK local service businesses. Generates campaign hierarchies, ad groups, keyword lists (with negatives), ad copy variations, and extension suggestions. Optimised for trades businesses including electricians, roofers, plumbers, plasterers, renderers, flooring, gas engineers, window installers, solar/renewables, dental, and recruitment. Triggers on "Google Ads campaign", "PPC campaign", "ad groups", "keyword list", "negative keywords", "ad copy", "RSA", "extensions", "sitelinks", or when setting up paid search for local service clients.
---

# Google Ads Campaign Architect

Build complete, ready-to-implement Google Ads campaign structures for UK local service businesses.

## Output Format

Provide complete campaign structures in a clear hierarchy:

```
Campaign: [Campaign Name]
├── Settings: [Location, Budget, Bidding]
├── Ad Group: [Ad Group Name]
│   ├── Keywords: [keyword list with match types]
│   ├── Negative Keywords: [negatives]
│   └── Ads: [RSA headlines + descriptions]
└── Extensions: [Sitelinks, Callouts, Snippets]
```

## Required Information

Before building, collect:

1. **Business name** and website URL
2. **Industry/trade type** (see references/campaign-structures.md)
3. **Services offered** (specific services, not just "electrician")
4. **Service areas** (towns/postcodes they cover)
5. **USPs** (24/7, free quotes, years experience, accreditations)
6. **Phone number** (for call extensions)
7. **Budget** (daily/monthly - helps determine campaign scope)
8. **Existing conversion tracking** (calls, forms, both?)

## Campaign Architecture Principles

### 1. Campaign Structure
- One campaign per service category OR location (not both)
- Service-based structure for most local businesses
- Location-based only if budgets vary significantly by area

### 2. Ad Groups
- Tightly themed: 10-20 keywords max per ad group
- Single keyword ad groups (SKAGs) for high-value terms
- Group by intent: emergency vs planned, residential vs commercial

### 3. Keywords
- Start with phrase and exact match (no broad without data)
- Include location modifiers: "[service] Leeds", "[service] near me"
- Comprehensive negative list from day one (see references/keywords.md)

### 4. Ad Copy
- 15 headlines, 4 descriptions per RSA
- Pin location in headline 1 or 2
- Include primary USP and CTA
- UK spelling and compliance (no "best" without proof)

### 5. Extensions
- Minimum: Sitelinks (4+), Callouts (4+), Structured Snippets, Call
- Add Location extension if Google Business Profile linked
- See references/extensions.md for trade-specific suggestions

## Compliance Notes

- No superlatives ("best", "cheapest") without third-party verification
- No guarantees that can't be substantiated
- Include accreditation numbers where applicable (Gas Safe, etc.)
- Price extensions need accurate, current pricing

## References

- **references/campaign-structures.md** - Campaign hierarchies by industry
- **references/keywords.md** - Keyword templates and negative lists
- **references/ad-copy.md** - Headlines, descriptions, CTAs by trade
- **references/extensions.md** - Sitelinks, callouts, snippets templates
- **references/settings.md** - Location targeting, bidding, budgets
