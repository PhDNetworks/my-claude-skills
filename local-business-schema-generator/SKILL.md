---
name: local-business-schema-generator
description: Generate complete JSON-LD structured data (LocalBusiness, Service, FAQPage, AggregateRating) for UK trades and local service businesses. Output is ready-to-paste into WordPress/Elementor HTML widgets. Use when building websites for electricians, roofers, plumbers, plasterers, renderers, flooring specialists, gas engineers, window/door installers, dental practices, solicitors, recruitment agencies, renewables/solar installers, or any local service business. Triggers on "schema markup", "JSON-LD", "structured data", "LocalBusiness schema", "FAQ schema", "review schema", or when creating/auditing local business websites for SEO.
---

# Local Business Schema Generator

Generate complete, valid JSON-LD structured data for UK local service businesses, optimised for WordPress/Elementor sites.

## Output Format

Always output complete JSON-LD wrapped in script tags, ready to paste into Elementor HTML widget:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    // LocalBusiness, Service, FAQPage schemas combined
  ]
}
</script>
```

## Required Information

Before generating, collect:

1. **Business name** (and trading name if different)
2. **Industry/trade type** (see references/industries.md for @type mappings)
3. **Full address** including postcode
4. **Phone number** (format: +44 xxx xxx xxxx)
5. **Email and website URL**
6. **Opening hours** (including emergency/24hr if applicable)
7. **Services offered** (list of main services)
8. **Service areas** (see references/service-areas.md for Leeds/West Yorkshire)
9. **Review data** (Google rating, review count)
10. **Accreditations** (NICEIC, Gas Safe, FENSA, etc.)

## Schema Components

### 1. LocalBusiness

Use the most specific @type from references/industries.md. Always include:
- @id as canonical URL anchor
- address with full PostalAddress
- geo coordinates (lookup if not provided)
- areaServed array for service coverage
- aggregateRating if reviews exist
- hasCredential for trade certifications

### 2. Service Schemas

Generate one Service schema per main service offering. Link to LocalBusiness via provider @id reference.

### 3. FAQPage

Include 3-5 industry-relevant FAQs. See references/industries.md for suggested questions per trade.

## Validation

Remind user to validate at: https://validator.schema.org/

## Implementation

Output goes into Elementor > Add Widget > HTML, placed in page footer or site-wide footer for homepage schema.

## References

- **references/industries.md** - @type mappings, certifications, FAQ templates per industry
- **references/service-areas.md** - Leeds & West Yorkshire towns/postcodes
- **references/examples.md** - Complete working examples
