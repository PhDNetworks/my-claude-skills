#!/usr/bin/env python3
"""
Update Landing Page URLs for Google Ads
Updates ad final URLs to point to new optimized landing pages.
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google_ads_client import get_client, DEFAULT_CONFIG
from google.ads.googleads.errors import GoogleAdsException


# Landing page URL mappings
URL_MAPPINGS = {
    # Leeds Rendering (Customer ID: 6109184488)
    "6109184488": {
        "keywords": {
            "rendering": "https://leedsrendering.co.uk/rendering-leeds/",
            "k-rend": "https://leedsrendering.co.uk/k-rend-leeds/",
            "k rend": "https://leedsrendering.co.uk/k-rend-leeds/",
            "plastering": "https://leedsrendering.co.uk/rendering-leeds/",
            "render": "https://leedsrendering.co.uk/rendering-leeds/",
        },
        "default": "https://leedsrendering.co.uk/rendering-leeds/"
    },
    # JLR Smith Roofing (Customer ID: 5481658097)
    "5481658097": {
        "keywords": {
            "roofer": "https://jlrsmith.co.uk/roofers-leeds/",
            "roofers": "https://jlrsmith.co.uk/roofers-leeds/",
            "roofing": "https://jlrsmith.co.uk/roofers-leeds/",
            "roof repair": "https://jlrsmith.co.uk/roof-repairs-leeds/",
            "roof repairs": "https://jlrsmith.co.uk/roof-repairs-leeds/",
            "leak": "https://jlrsmith.co.uk/roof-repairs-leeds/",
        },
        "default": "https://jlrsmith.co.uk/roofers-leeds/"
    }
}


def get_ads_with_urls(client, customer_id: str) -> list:
    """Get all ads with their current final URLs."""
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            ad_group_ad.ad.id,
            ad_group_ad.ad.resource_name,
            ad_group_ad.ad.type,
            ad_group_ad.ad.final_urls,
            ad_group_ad.ad.responsive_search_ad.headlines,
            ad_group_ad.status,
            ad_group.id,
            ad_group.name,
            campaign.id,
            campaign.name
        FROM ad_group_ad
        WHERE ad_group_ad.status != 'REMOVED'
            AND campaign.status = 'ENABLED'
    """

    ads = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            final_urls = list(row.ad_group_ad.ad.final_urls) if row.ad_group_ad.ad.final_urls else []
            ads.append({
                "ad_id": row.ad_group_ad.ad.id,
                "resource_name": row.ad_group_ad.ad.resource_name,
                "ad_type": row.ad_group_ad.ad.type.name,
                "final_urls": final_urls,
                "status": row.ad_group_ad.status.name,
                "ad_group_id": row.ad_group.id,
                "ad_group_name": row.ad_group.name,
                "campaign_id": row.campaign.id,
                "campaign_name": row.campaign.name
            })
    except GoogleAdsException as ex:
        print(f"Error fetching ads for {customer_id}: {ex}")

    return ads


def get_keywords_for_ad_group(client, customer_id: str, ad_group_id: int) -> list:
    """Get keywords for an ad group to determine appropriate landing page."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type
        FROM ad_group_criterion
        WHERE ad_group.id = {ad_group_id}
            AND ad_group_criterion.type = 'KEYWORD'
            AND ad_group_criterion.status = 'ENABLED'
    """

    keywords = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            keywords.append(row.ad_group_criterion.keyword.text.lower())
    except GoogleAdsException as ex:
        print(f"Error fetching keywords: {ex}")

    return keywords


def determine_landing_page(customer_id: str, keywords: list) -> str:
    """Determine the best landing page URL based on keywords."""
    if customer_id not in URL_MAPPINGS:
        return None

    mapping = URL_MAPPINGS[customer_id]

    # Check each keyword against our mappings
    for keyword in keywords:
        for key, url in mapping["keywords"].items():
            if key in keyword:
                return url

    return mapping.get("default")


def update_ad_final_url(client, customer_id: str, ad_resource_name: str, new_url: str) -> dict:
    """
    Update an ad's final URL.
    Note: For RSAs, you typically need to create a new ad rather than update.
    This function updates the final_urls field where possible.
    """
    from google.protobuf import field_mask_pb2

    ad_service = client.get_service("AdService")

    operation = client.get_type("AdOperation")
    ad = operation.update
    ad.resource_name = ad_resource_name
    ad.final_urls.append(new_url)

    operation.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["final_urls"]))

    try:
        response = ad_service.mutate_ads(
            customer_id=customer_id,
            operations=[operation]
        )
        return {
            "success": True,
            "resource_name": response.results[0].resource_name,
            "new_url": new_url
        }
    except GoogleAdsException as ex:
        return {
            "success": False,
            "error": str(ex),
            "note": "RSAs may require creating new ads instead of updating"
        }


def analyze_and_report(client, customer_id: str, account_name: str) -> dict:
    """Analyze ads and generate update recommendations."""
    print(f"\n{'='*60}")
    print(f"Account: {account_name} ({customer_id})")
    print(f"{'='*60}")

    ads = get_ads_with_urls(client, customer_id)

    results = {
        "customer_id": customer_id,
        "account_name": account_name,
        "total_ads": len(ads),
        "recommendations": []
    }

    for ad in ads:
        keywords = get_keywords_for_ad_group(client, customer_id, ad["ad_group_id"])
        recommended_url = determine_landing_page(customer_id, keywords)

        current_url = ad["final_urls"][0] if ad["final_urls"] else "None"

        print(f"\nAd Group: {ad['ad_group_name']}")
        print(f"  Current URL: {current_url}")
        print(f"  Keywords: {', '.join(keywords[:3])}...")

        if recommended_url:
            if current_url != recommended_url:
                print(f"  >> RECOMMENDED: {recommended_url}")
                results["recommendations"].append({
                    "ad_id": ad["ad_id"],
                    "ad_group": ad["ad_group_name"],
                    "current_url": current_url,
                    "recommended_url": recommended_url,
                    "resource_name": ad["resource_name"],
                    "keywords": keywords[:5]
                })
            else:
                print(f"  ✓ Already using optimized landing page")

    return results


def main():
    """Main function to analyze and optionally update ad URLs."""
    print("=" * 60)
    print("Landing Page URL Updater for Google Ads")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    try:
        client = get_client()
    except Exception as e:
        print(f"Error initializing client: {e}")
        return

    accounts = [
        {"id": "6109184488", "name": "Leeds Rendering"},
        {"id": "5481658097", "name": "JLR Smith Roofing"},
    ]

    all_results = []

    for account in accounts:
        results = analyze_and_report(client, account["id"], account["name"])
        all_results.append(results)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    total_recommendations = sum(len(r["recommendations"]) for r in all_results)

    print(f"\nTotal recommendations: {total_recommendations}")

    for r in all_results:
        print(f"\n{r['account_name']}:")
        print(f"  - Total ads: {r['total_ads']}")
        print(f"  - URLs to update: {len(r['recommendations'])}")

        for rec in r["recommendations"]:
            print(f"    • {rec['ad_group']}: {rec['current_url']} → {rec['recommended_url']}")

    # Save results
    output_file = f"url_update_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nReport saved to: {output_file}")

    return all_results


if __name__ == "__main__":
    main()
