# Complete Schema Examples

## Electrician - Best Practice Example

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Electrician",
      "@id": "https://example-electrical.co.uk/#organization",
      "name": "Example Electrical Services",
      "description": "NICEIC-approved electricians in Leeds providing domestic, commercial and EV charging services across West Yorkshire.",
      "url": "https://example-electrical.co.uk",
      "logo": {
        "@type": "ImageObject",
        "url": "https://example-electrical.co.uk/wp-content/uploads/logo.png",
        "width": 250,
        "height": 80
      },
      "image": "https://example-electrical.co.uk/wp-content/uploads/hero.jpg",
      "telephone": "+44 113 XXX XXXX",
      "email": "info@example-electrical.co.uk",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Unit 1, Example Business Park",
        "addressLocality": "Leeds",
        "addressRegion": "West Yorkshire",
        "postalCode": "LS12 1AB",
        "addressCountry": "GB"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": "53.8008",
        "longitude": "-1.5491"
      },
      "areaServed": [
        {"@type": "City", "name": "Leeds"},
        {"@type": "City", "name": "Bradford"},
        {"@type": "City", "name": "Wakefield"},
        {"@type": "City", "name": "Pudsey"},
        {"@type": "City", "name": "Morley"},
        {"@type": "City", "name": "Horsforth"}
      ],
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
          "opens": "00:00",
          "closes": "23:59"
        }
      ],
      "priceRange": "££",
      "paymentAccepted": "Cash, Credit Card, Bank Transfer",
      "currenciesAccepted": "GBP",
      "hasCredential": [
        {
          "@type": "EducationalOccupationalCredential",
          "credentialCategory": "Professional Certification",
          "name": "NICEIC Approved Contractor"
        },
        {
          "@type": "EducationalOccupationalCredential",
          "credentialCategory": "Professional Certification",
          "name": "Which? Trusted Trader"
        }
      ],
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "47",
        "bestRating": "5",
        "worstRating": "1"
      },
      "sameAs": [
        "https://www.facebook.com/exampleelectrical",
        "https://www.instagram.com/exampleelectrical"
      ]
    },
    {
      "@type": "Service",
      "@id": "https://example-electrical.co.uk/services/ev-charger/#service",
      "name": "EV Charger Installation",
      "description": "Expert installation of home and commercial EV charging points across Leeds and West Yorkshire.",
      "provider": {"@id": "https://example-electrical.co.uk/#organization"},
      "areaServed": [
        {"@type": "City", "name": "Leeds"},
        {"@type": "City", "name": "Bradford"},
        {"@type": "City", "name": "Wakefield"}
      ],
      "serviceType": "EV Charger Installation"
    },
    {
      "@type": "Service",
      "@id": "https://example-electrical.co.uk/services/rewiring/#service",
      "name": "House Rewiring",
      "description": "Complete electrical rewiring for domestic properties with full certification.",
      "provider": {"@id": "https://example-electrical.co.uk/#organization"},
      "areaServed": {"@type": "City", "name": "Leeds"},
      "serviceType": "Electrical Rewiring"
    },
    {
      "@type": "FAQPage",
      "@id": "https://example-electrical.co.uk/#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Are you NICEIC approved?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes, we are fully NICEIC Approved Contractors. All our work is tested, certified and compliant with current BS 7671 regulations."
          }
        },
        {
          "@type": "Question",
          "name": "Do you offer 24/7 emergency callouts?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes, we provide 24/7 emergency electrical services across Leeds and West Yorkshire. Call us any time for urgent electrical issues."
          }
        },
        {
          "@type": "Question",
          "name": "How much does a full house rewire cost?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "A full house rewire typically costs between £3,000 and £5,000 for a 3-bedroom property, depending on accessibility and specification. We provide free, no-obligation quotes."
          }
        },
        {
          "@type": "Question",
          "name": "How long does EV charger installation take?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "A standard home EV charger installation typically takes 2-4 hours. We survey your property first to ensure a smooth installation and advise on the best charger location."
          }
        }
      ]
    }
  ]
}
</script>
```

## Flooring/Carpet Shop - Best Practice Example

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "HomeAndConstructionBusiness",
      "@id": "https://example-flooring.co.uk/#organization",
      "name": "Example Flooring Ltd",
      "description": "Family-run flooring specialists in Leeds offering carpets, laminate, LVT and artificial grass with free measuring service.",
      "url": "https://example-flooring.co.uk",
      "logo": {
        "@type": "ImageObject",
        "url": "https://example-flooring.co.uk/wp-content/uploads/logo.png",
        "width": 200,
        "height": 200
      },
      "telephone": "+44 113 XXX XXXX",
      "email": "info@example-flooring.co.uk",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "123 Example Lane",
        "addressLocality": "Leeds",
        "addressRegion": "West Yorkshire",
        "postalCode": "LS13 1XX",
        "addressCountry": "GB"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": "53.8156",
        "longitude": "-1.6478"
      },
      "areaServed": [
        {"@type": "City", "name": "Leeds"},
        {"@type": "City", "name": "Pudsey"},
        {"@type": "City", "name": "Bramley"},
        {"@type": "City", "name": "Horsforth"},
        {"@type": "City", "name": "Morley"}
      ],
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
          "opens": "09:00",
          "closes": "17:00"
        },
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": "Saturday",
          "opens": "09:30",
          "closes": "16:30"
        }
      ],
      "priceRange": "£-££",
      "paymentAccepted": "Cash, Credit Card, Bank Transfer",
      "currenciesAccepted": "GBP",
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "87",
        "bestRating": "5",
        "worstRating": "1"
      }
    },
    {
      "@type": "FAQPage",
      "@id": "https://example-flooring.co.uk/#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Do you offer free measuring?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes, we offer a completely free, no-obligation measuring service. Book online or call us to arrange a convenient time."
          }
        },
        {
          "@type": "Question",
          "name": "Can you fit flooring I've bought elsewhere?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes, we're happy to fit carpets, laminate, or LVT that you've purchased elsewhere. Contact us for a fitting quote."
          }
        },
        {
          "@type": "Question",
          "name": "What flooring is best for underfloor heating?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "LVT and engineered wood flooring work best with underfloor heating due to their thermal conductivity. We can advise on the best options for your home."
          }
        },
        {
          "@type": "Question",
          "name": "Do you remove old flooring?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes, we offer a full uplift and disposal service for your old flooring. This can be included in your quote."
          }
        }
      ]
    }
  ]
}
</script>
```

## Rendering/Plastering - Best Practice Example

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "HomeAndConstructionBusiness",
      "@id": "https://example-rendering.co.uk/#organization",
      "name": "Example Rendering & Plastering Ltd",
      "description": "Professional rendering and plastering services in Leeds with over 20 years experience. Silicone render, K-rend and traditional plastering.",
      "url": "https://example-rendering.co.uk",
      "logo": {
        "@type": "ImageObject",
        "url": "https://example-rendering.co.uk/wp-content/uploads/logo.png",
        "width": 250,
        "height": 250
      },
      "telephone": "+44 113 XXX XXXX",
      "email": "info@example-rendering.co.uk",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "42 Example Street",
        "addressLocality": "Leeds",
        "addressRegion": "West Yorkshire",
        "postalCode": "LS13 2XX",
        "addressCountry": "GB"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": "53.8089",
        "longitude": "-1.6312"
      },
      "areaServed": [
        {"@type": "City", "name": "Leeds"},
        {"@type": "City", "name": "Bradford"},
        {"@type": "City", "name": "Wakefield"},
        {"@type": "City", "name": "Pudsey"},
        {"@type": "City", "name": "Morley"}
      ],
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
          "opens": "08:00",
          "closes": "17:00"
        },
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": "Saturday",
          "opens": "09:00",
          "closes": "13:00"
        }
      ],
      "priceRange": "££",
      "paymentAccepted": "Cash, Credit Card, Bank Transfer",
      "currenciesAccepted": "GBP",
      "hasCredential": [
        {
          "@type": "EducationalOccupationalCredential",
          "credentialCategory": "Professional Certification",
          "name": "TrustMark Registered"
        }
      ],
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "5.0",
        "reviewCount": "34",
        "bestRating": "5",
        "worstRating": "1"
      },
      "sameAs": [
        "https://www.facebook.com/examplerendering",
        "https://www.instagram.com/examplerendering"
      ]
    },
    {
      "@type": "Service",
      "@id": "https://example-rendering.co.uk/services/rendering/#service",
      "name": "External Rendering",
      "description": "Professional external rendering including silicone, monocouche, K-rend and traditional sand and cement renders.",
      "provider": {"@id": "https://example-rendering.co.uk/#organization"},
      "areaServed": [
        {"@type": "City", "name": "Leeds"},
        {"@type": "City", "name": "Bradford"}
      ],
      "serviceType": "External Rendering"
    },
    {
      "@type": "Service",
      "@id": "https://example-rendering.co.uk/services/plastering/#service",
      "name": "Internal Plastering",
      "description": "Expert internal plastering for residential and commercial properties with smooth, high-quality finishes.",
      "provider": {"@id": "https://example-rendering.co.uk/#organization"},
      "areaServed": {"@type": "City", "name": "Leeds"},
      "serviceType": "Plastering"
    },
    {
      "@type": "FAQPage",
      "@id": "https://example-rendering.co.uk/#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "How much does rendering cost per m²?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "External rendering typically costs £40-£80 per m² depending on the render system and finish chosen. We provide free site surveys and detailed quotes."
          }
        },
        {
          "@type": "Question",
          "name": "How long does external rendering take?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "An average 3-bed semi-detached house takes approximately 5-7 working days to complete, weather permitting."
          }
        },
        {
          "@type": "Question",
          "name": "What types of render do you offer?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "We offer silicone render, monocouche, K-rend, traditional sand and cement render, and through-coloured render systems in a wide range of colours."
          }
        },
        {
          "@type": "Question",
          "name": "Will rendering improve my home's insulation?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes, especially when combined with external wall insulation (EWI). This can significantly reduce heat loss and lower energy bills."
          }
        }
      ]
    }
  ]
}
</script>
```

## Gas Engineer - Best Practice Example

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "HomeAndConstructionBusiness",
      "@id": "https://example-gas.co.uk/#organization",
      "name": "Example Gas Services",
      "description": "Gas Safe registered engineers in Leeds. Boiler installations, servicing, repairs and landlord gas safety certificates.",
      "url": "https://example-gas.co.uk",
      "logo": {
        "@type": "ImageObject",
        "url": "https://example-gas.co.uk/wp-content/uploads/logo.png",
        "width": 200,
        "height": 200
      },
      "telephone": "+44 113 XXX XXXX",
      "email": "info@example-gas.co.uk",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "10 Example Road",
        "addressLocality": "Leeds",
        "addressRegion": "West Yorkshire",
        "postalCode": "LS10 1XX",
        "addressCountry": "GB"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": "53.7700",
        "longitude": "-1.5400"
      },
      "areaServed": [
        {"@type": "City", "name": "Leeds"},
        {"@type": "City", "name": "Wakefield"},
        {"@type": "City", "name": "Rothwell"},
        {"@type": "City", "name": "Morley"},
        {"@type": "City", "name": "Garforth"}
      ],
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
          "opens": "08:00",
          "closes": "18:00"
        },
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": "Saturday",
          "opens": "09:00",
          "closes": "14:00"
        }
      ],
      "priceRange": "££",
      "paymentAccepted": "Cash, Credit Card, Bank Transfer",
      "currenciesAccepted": "GBP",
      "hasCredential": [
        {
          "@type": "EducationalOccupationalCredential",
          "credentialCategory": "Professional Certification",
          "name": "Gas Safe Registered",
          "recognizedBy": {
            "@type": "Organization",
            "name": "Gas Safe Register"
          }
        }
      ],
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.8",
        "reviewCount": "62",
        "bestRating": "5",
        "worstRating": "1"
      }
    },
    {
      "@type": "FAQPage",
      "@id": "https://example-gas.co.uk/#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Are you Gas Safe registered?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes, we are fully Gas Safe registered. Our registration number is XXXXXX. You can verify this on the Gas Safe Register website."
          }
        },
        {
          "@type": "Question",
          "name": "How often should I service my boiler?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "We recommend an annual boiler service to maintain efficiency, ensure safety, and keep your manufacturer's warranty valid."
          }
        },
        {
          "@type": "Question",
          "name": "How long does a new boiler installation take?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "A straightforward boiler swap typically takes 1 day. If we need to relocate the boiler or make significant pipework changes, this may take 2 days."
          }
        },
        {
          "@type": "Question",
          "name": "Do you offer boiler finance?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes, we offer flexible finance options including 0% interest-free credit on selected boilers. Ask us for details when you get your quote."
          }
        }
      ]
    }
  ]
}
</script>
```

## Minimal Quick-Start Template

Replace placeholder values in [BRACKETS]:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "[BUSINESS_TYPE - see industries.md]",
      "@id": "[WEBSITE_URL]/#organization",
      "name": "[BUSINESS_NAME]",
      "description": "[150-160 CHARACTER DESCRIPTION WITH LOCATION AND KEY SERVICES]",
      "url": "[WEBSITE_URL]",
      "telephone": "+44 [PHONE_NUMBER]",
      "email": "[EMAIL_ADDRESS]",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "[STREET_ADDRESS]",
        "addressLocality": "[CITY]",
        "addressRegion": "West Yorkshire",
        "postalCode": "[POSTCODE]",
        "addressCountry": "GB"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": "[LATITUDE]",
        "longitude": "[LONGITUDE]"
      },
      "areaServed": [
        {"@type": "City", "name": "Leeds"}
      ],
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
          "opens": "08:00",
          "closes": "17:00"
        }
      ],
      "priceRange": "££",
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "[RATING_OUT_OF_5]",
        "reviewCount": "[NUMBER_OF_REVIEWS]",
        "bestRating": "5",
        "worstRating": "1"
      }
    }
  ]
}
</script>
```

## Best Practice Checklist

1. **Always use @graph** - Combines multiple schema types cleanly
2. **Use @id references** - Links Service schemas back to the main LocalBusiness
3. **Include geo coordinates** - Lookup at latlong.net if not provided
4. **Keep descriptions 150-160 chars** - Optimal for search snippets
5. **Format phone as +44** - International format for consistency
6. **Include aggregateRating only** if you have genuine Google reviews
7. **hasCredential for certifications** - Proper way to list trade qualifications
8. **Validate before deploying** - Always check at validator.schema.org
9. **One @graph per page** - Don't duplicate schemas across pages
10. **Update review counts** - Keep aggregateRating current quarterly
