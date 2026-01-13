#!/usr/bin/env python3
"""
Google Ads Urgent Issues Report

Identifies keywords and search terms that need immediate attention:
- High spend with zero conversions
- Low quality scores
- Irrelevant search terms

Usage:
    python3 get_urgent_issues.py
"""

from google_ads_client import get_client
from google.ads.googleads.errors import GoogleAdsException

# Accounts to analyze (problem accounts only)
ACCOUNTS_TO_ANALYZE = {
    "5481658097": "JLR Smith Roofing – Leeds",
    "6109184488": "Leeds Rendering"
}

DAYS = 30
SPEND_THRESHOLD = 20.0  # £20 minimum spend to flag
QUALITY_SCORE_THRESHOLD = 5  # Flag keywords below this


def check_conversion_tracking(client, customer_id: str) -> dict:
    """Check if conversion tracking is configured for the account."""
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            conversion_action.id,
            conversion_action.name,
            conversion_action.status,
            conversion_action.type,
            conversion_action.category
        FROM conversion_action
        WHERE conversion_action.status = 'ENABLED'
    """

    conversions = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            conversions.append({
                "id": row.conversion_action.id,
                "name": row.conversion_action.name,
                "type": row.conversion_action.type.name,
                "category": row.conversion_action.category.name
            })
    except GoogleAdsException as ex:
        return {"status": "ERROR", "error": str(ex), "actions": []}

    if conversions:
        return {"status": "ENABLED", "actions": conversions}
    else:
        return {"status": "NOT CONFIGURED", "actions": []}


def get_wasted_spend_keywords(client, customer_id: str) -> list:
    """Get keywords with significant spend but zero conversions."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            ad_group.name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.status,
            ad_group_criterion.effective_cpc_bid_micros,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM keyword_view
        WHERE segments.date DURING LAST_{DAYS}_DAYS
            AND ad_group_criterion.status = 'ENABLED'
            AND metrics.conversions = 0
        ORDER BY metrics.cost_micros DESC
    """

    keywords = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            cost = row.metrics.cost_micros / 1_000_000
            if cost >= SPEND_THRESHOLD:
                keywords.append({
                    "keyword": row.ad_group_criterion.keyword.text,
                    "match_type": row.ad_group_criterion.keyword.match_type.name,
                    "ad_group": row.ad_group.name,
                    "impressions": row.metrics.impressions,
                    "clicks": row.metrics.clicks,
                    "cost": cost,
                    "conversions": row.metrics.conversions,
                    "current_bid": row.ad_group_criterion.effective_cpc_bid_micros / 1_000_000 if row.ad_group_criterion.effective_cpc_bid_micros else None
                })
    except GoogleAdsException as ex:
        print(f"  Error fetching wasted spend keywords: {ex}")

    return keywords


def get_low_quality_keywords(client, customer_id: str) -> list:
    """Get keywords with low quality scores."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            ad_group.name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.status,
            ad_group_criterion.quality_info.quality_score,
            ad_group_criterion.quality_info.creative_quality_score,
            ad_group_criterion.quality_info.post_click_quality_score,
            ad_group_criterion.quality_info.search_predicted_ctr,
            ad_group_criterion.effective_cpc_bid_micros,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros
        FROM keyword_view
        WHERE segments.date DURING LAST_{DAYS}_DAYS
            AND ad_group_criterion.status = 'ENABLED'
            AND ad_group_criterion.quality_info.quality_score < {QUALITY_SCORE_THRESHOLD}
        ORDER BY ad_group_criterion.quality_info.quality_score ASC
    """

    keywords = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            keywords.append({
                "keyword": row.ad_group_criterion.keyword.text,
                "match_type": row.ad_group_criterion.keyword.match_type.name,
                "ad_group": row.ad_group.name,
                "quality_score": row.ad_group_criterion.quality_info.quality_score,
                "creative_quality": row.ad_group_criterion.quality_info.creative_quality_score.name if row.ad_group_criterion.quality_info.creative_quality_score else "N/A",
                "landing_page_quality": row.ad_group_criterion.quality_info.post_click_quality_score.name if row.ad_group_criterion.quality_info.post_click_quality_score else "N/A",
                "expected_ctr": row.ad_group_criterion.quality_info.search_predicted_ctr.name if row.ad_group_criterion.quality_info.search_predicted_ctr else "N/A",
                "current_bid": row.ad_group_criterion.effective_cpc_bid_micros / 1_000_000 if row.ad_group_criterion.effective_cpc_bid_micros else None,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "cost": row.metrics.cost_micros / 1_000_000
            })
    except GoogleAdsException as ex:
        print(f"  Error fetching low quality keywords: {ex}")

    return keywords


def get_search_terms_for_negatives(client, customer_id: str) -> list:
    """Get search terms that might need to be added as negatives."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            search_term_view.search_term,
            campaign.name,
            ad_group.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM search_term_view
        WHERE segments.date DURING LAST_{DAYS}_DAYS
            AND metrics.clicks > 0
            AND metrics.conversions = 0
        ORDER BY metrics.cost_micros DESC
        LIMIT 50
    """

    search_terms = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            cost = row.metrics.cost_micros / 1_000_000
            # Flag terms with spend but no conversions
            if cost >= 5.0:  # Lower threshold for search terms
                search_terms.append({
                    "search_term": row.search_term_view.search_term,
                    "campaign": row.campaign.name,
                    "ad_group": row.ad_group.name,
                    "impressions": row.metrics.impressions,
                    "clicks": row.metrics.clicks,
                    "cost": cost,
                    "conversions": row.metrics.conversions
                })
    except GoogleAdsException as ex:
        print(f"  Error fetching search terms: {ex}")

    return search_terms


def categorize_search_term(term: str) -> str:
    """Attempt to categorize why a search term might be irrelevant."""
    term_lower = term.lower()

    # Common irrelevant patterns
    if any(word in term_lower for word in ['job', 'jobs', 'career', 'hiring', 'salary', 'employment']):
        return "Job seeker (not customer)"
    if any(word in term_lower for word in ['diy', 'how to', 'tutorial', 'yourself']):
        return "DIY intent (not hiring)"
    if any(word in term_lower for word in ['free', 'cheap', 'budget', 'discount']):
        return "Price-sensitive (low value)"
    if any(word in term_lower for word in ['london', 'manchester', 'birmingham', 'sheffield']) and 'leeds' not in term_lower:
        return "Wrong location"
    if any(word in term_lower for word in ['course', 'training', 'apprentice', 'learn']):
        return "Training/education seeker"

    return "Review manually - low conversion rate"


def print_action_plan(account_name: str, customer_id: str,
                     conversion_status: dict,
                     wasted_keywords: list,
                     low_quality_keywords: list,
                     negative_candidates: list):
    """Print formatted action plan for an account."""

    print("=" * 70)
    print(f"ACCOUNT: {account_name} ({customer_id})")
    print("=" * 70)
    print()

    # Conversion tracking status
    if conversion_status["status"] == "ENABLED":
        print(f"CONVERSION TRACKING: ✅ ENABLED ({len(conversion_status['actions'])} actions configured)")
        for action in conversion_status["actions"][:3]:
            print(f"  - {action['name']} ({action['type']})")
    elif conversion_status["status"] == "NOT CONFIGURED":
        print("CONVERSION TRACKING: ❌ NOT CONFIGURED")
        print("  ⚠️  CRITICAL: Set up conversion tracking before spending more!")
    else:
        print(f"CONVERSION TRACKING: ⚠️ ERROR checking status")
    print()

    # Wasted spend keywords
    print("-" * 70)
    print("RECOMMENDED PAUSES (high spend, zero conversions)")
    print("-" * 70)
    if wasted_keywords:
        for kw in wasted_keywords:
            print(f"• Keyword: \"{kw['keyword']}\"")
            print(f"  Match: {kw['match_type']}, Spend: £{kw['cost']:.2f}, Clicks: {kw['clicks']}")
            print(f"  Ad Group: {kw['ad_group']}")
            print(f"  Action: PAUSE")
            print(f"  Risk: LOW (no conversions to lose)")
            print()
    else:
        print("  No keywords found with spend > £20 and 0 conversions")
        print()

    # Low quality score keywords
    print("-" * 70)
    print("RECOMMENDED BID REDUCTIONS (low quality score)")
    print("-" * 70)
    if low_quality_keywords:
        # Deduplicate by keyword text
        seen = set()
        for kw in low_quality_keywords:
            if kw['keyword'] in seen:
                continue
            seen.add(kw['keyword'])

            bid_str = f"£{kw['current_bid']:.2f}" if kw['current_bid'] else "Auto"
            print(f"• Keyword: \"{kw['keyword']}\"")
            print(f"  QS: {kw['quality_score']}/10, Current Bid: {bid_str}")
            print(f"  Ad Relevance: {kw['creative_quality']}, Landing Page: {kw['landing_page_quality']}, Expected CTR: {kw['expected_ctr']}")
            print(f"  Action: REDUCE BID 50% or improve ad/landing page")
            print(f"  Risk: MEDIUM (may lose some traffic)")
            print()
    else:
        print("  No keywords found with quality score < 5")
        print()

    # Negative keyword candidates
    print("-" * 70)
    print("NEGATIVE KEYWORDS TO ADD (from search terms)")
    print("-" * 70)
    if negative_candidates:
        for st in negative_candidates[:15]:  # Limit to top 15
            reason = categorize_search_term(st['search_term'])
            print(f"• \"{st['search_term']}\"")
            print(f"  {st['clicks']} clicks, £{st['cost']:.2f} spend, 0 conversions")
            print(f"  Reason: {reason}")
            print()
    else:
        print("  No high-spend search terms with 0 conversions found")
        print()

    print()


def main():
    print()
    print("=" * 70)
    print("GOOGLE ADS URGENT ISSUES REPORT")
    print("PhD Networks & Systems Ltd")
    print("=" * 70)
    print()
    print("⚠️  THIS IS A READ-ONLY REPORT - NO CHANGES WILL BE MADE")
    print()

    # Initialize client
    try:
        client = get_client()
    except Exception as e:
        print(f"Error initializing client: {e}")
        return

    # Analyze each account
    for customer_id, account_name in ACCOUNTS_TO_ANALYZE.items():
        print(f"Analyzing {account_name}...")

        # Gather data
        conversion_status = check_conversion_tracking(client, customer_id)
        wasted_keywords = get_wasted_spend_keywords(client, customer_id)
        low_quality_keywords = get_low_quality_keywords(client, customer_id)
        negative_candidates = get_search_terms_for_negatives(client, customer_id)

        # Print action plan
        print()
        print_action_plan(
            account_name, customer_id,
            conversion_status,
            wasted_keywords,
            low_quality_keywords,
            negative_candidates
        )

    print("=" * 70)
    print("END OF REPORT")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Review recommended pauses - consider pausing high-spend, zero-conversion keywords")
    print("2. Check conversion tracking - ensure it's properly configured")
    print("3. Add negative keywords - block irrelevant search terms")
    print("4. Improve quality scores - update ads and landing pages")
    print()


if __name__ == "__main__":
    main()
