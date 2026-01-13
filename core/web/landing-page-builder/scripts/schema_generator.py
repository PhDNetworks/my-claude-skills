#!/usr/bin/env python3
"""
Schema Generator for Landing Pages

Generates JSON-LD structured data for local service businesses.
Integrates with local-schema-generator skill patterns.
"""

import json
from typing import Dict, List, Optional


def generate_local_business_schema(site_config: Dict) -> Dict:
    """
    Generate complete LocalBusiness schema.

    Args:
        site_config: Site configuration with business details

    Returns:
        JSON-LD schema dict ready for injection
    """

    business = site_config.get("business", {})

    schema = {
        "@context": "https://schema.org",
        "@type": business.get("type", "LocalBusiness"),
        "@id": f"{site_config.get('url', '')}#localbusiness",
        "name": business.get("name", site_config.get("business_name", "")),
        "description": business.get("description", ""),
        "url": site_config.get("url", ""),
        "telephone": site_config.get("phone", ""),
        "email": site_config.get("email", ""),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": business.get("street", ""),
            "addressLocality": site_config.get("location", "Leeds"),
            "addressRegion": business.get("region", "West Yorkshire"),
            "postalCode": business.get("postcode", ""),
            "addressCountry": "GB"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": business.get("latitude", ""),
            "longitude": business.get("longitude", "")
        },
        "areaServed": generate_area_served(site_config.get("service_areas", [])),
        "openingHoursSpecification": generate_opening_hours(business.get("hours", {})),
        "priceRange": business.get("price_range", "££"),
    }

    # Add optional fields if present
    if business.get("logo"):
        schema["logo"] = business["logo"]

    if business.get("image"):
        schema["image"] = business["image"]

    if business.get("rating"):
        schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": business["rating"].get("value", 5),
            "reviewCount": business["rating"].get("count", 0),
            "bestRating": 5,
            "worstRating": 1
        }

    if site_config.get("same_as"):
        schema["sameAs"] = site_config["same_as"]

    return schema


def generate_service_schema(
    service_name: str,
    description: str,
    provider_config: Dict,
    price_range: Optional[str] = None
) -> Dict:
    """Generate Service schema for a specific service."""

    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": service_name,
        "description": description,
        "provider": {
            "@type": "LocalBusiness",
            "name": provider_config.get("business_name", ""),
            "url": provider_config.get("url", "")
        },
        "areaServed": generate_area_served(provider_config.get("service_areas", [])),
        "serviceType": service_name,
        **({"priceRange": price_range} if price_range else {})
    }


def generate_faq_schema(faqs: List[Dict]) -> Dict:
    """
    Generate FAQPage schema.

    Args:
        faqs: List of {"question": "...", "answer": "..."} dicts
    """

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"]
                }
            }
            for faq in faqs
        ]
    }


def generate_area_served(areas: List[str]) -> List[Dict]:
    """Generate areaServed array from location names."""

    if not areas:
        return [{"@type": "City", "name": "Leeds"}]

    return [
        {
            "@type": "City",
            "name": area,
            "containedInPlace": {
                "@type": "AdministrativeArea",
                "name": "West Yorkshire"
            }
        }
        for area in areas
    ]


def generate_opening_hours(hours: Dict) -> List[Dict]:
    """
    Generate opening hours specification.

    Args:
        hours: Dict like {"Mon-Fri": "08:00-18:00", "Sat": "09:00-14:00"}
    """

    day_map = {
        "Mon": "Monday",
        "Tue": "Tuesday",
        "Wed": "Wednesday",
        "Thu": "Thursday",
        "Fri": "Friday",
        "Sat": "Saturday",
        "Sun": "Sunday"
    }

    specs = []

    for days, time_range in hours.items():
        if "-" in days and len(days) <= 7:  # Range like "Mon-Fri"
            start_day, end_day = days.split("-")
            day_list = []
            in_range = False
            for short, full in day_map.items():
                if short == start_day:
                    in_range = True
                if in_range:
                    day_list.append(full)
                if short == end_day:
                    in_range = False
        else:
            day_list = [day_map.get(days, days)]

        if "-" in time_range:
            opens, closes = time_range.split("-")
        else:
            opens, closes = "09:00", "17:00"

        for day in day_list:
            specs.append({
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": day,
                "opens": opens,
                "closes": closes
            })

    return specs


def generate_graph_schema(site_config: Dict) -> Dict:
    """
    Generate complete @graph schema with all relevant types.

    This creates a comprehensive schema including:
    - LocalBusiness
    - Services offered
    - FAQs (if provided)
    """

    graph = []

    # Add LocalBusiness
    graph.append(generate_local_business_schema(site_config))

    # Add Services
    for service in site_config.get("services", []):
        graph.append(generate_service_schema(
            service_name=service.get("name", ""),
            description=service.get("description", ""),
            provider_config=site_config,
            price_range=service.get("price_range")
        ))

    # Add FAQs if present
    if site_config.get("faqs"):
        graph.append(generate_faq_schema(site_config["faqs"]))

    return {
        "@context": "https://schema.org",
        "@graph": graph
    }


def schema_to_html(schema: Dict) -> str:
    """Convert schema dict to HTML script tag."""
    json_str = json.dumps(schema, indent=2)
    return f'<script type="application/ld+json">\n{json_str}\n</script>'


if __name__ == "__main__":
    # Example usage
    example_config = {
        "business_name": "JLR Smith Roofing",
        "url": "https://jlrsmithroofing.co.uk",
        "phone": "0113 XXX XXXX",
        "email": "info@jlrsmithroofing.co.uk",
        "location": "Leeds",
        "business": {
            "type": "RoofingContractor",
            "name": "JLR Smith Roofing & Plastering",
            "description": "Expert roof repairs and roofing services in Leeds",
            "street": "123 Example Street",
            "region": "West Yorkshire",
            "postcode": "LS1 1AA",
            "latitude": "53.8008",
            "longitude": "-1.5491",
            "price_range": "££",
            "rating": {"value": 4.7, "count": 45},
            "hours": {
                "Mon-Fri": "08:00-18:00",
                "Sat": "09:00-14:00"
            }
        },
        "service_areas": ["Leeds", "Wakefield", "Bradford", "Huddersfield"],
        "services": [
            {"name": "Roof Repairs", "description": "Emergency and planned roof repairs"},
            {"name": "Chimney Repairs", "description": "Full chimney repair services"},
            {"name": "Fascias & Soffits", "description": "UPVC fascia and soffit installation"}
        ],
        "same_as": [
            "https://www.facebook.com/jlrsmithroofing",
            "https://www.checkatrade.com/jlrsmithroofing"
        ]
    }

    schema = generate_graph_schema(example_config)
    print(schema_to_html(schema))
