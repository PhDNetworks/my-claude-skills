#!/usr/bin/env python3
"""
Execute Urgent Google Ads Fixes

Pauses high-spend, zero-conversion keywords identified in the urgent issues report.
Creates a rollback file for recovery if needed.

Usage:
    python3 execute_urgent_fixes.py
"""

import json
from datetime import datetime
from google_ads_client import get_client
from google.ads.googleads.errors import GoogleAdsException

# Keywords to pause - identified from urgent issues report
KEYWORDS_TO_PAUSE = {
    "5481658097": {  # JLR Smith Roofing – Leeds
        "account_name": "JLR Smith Roofing – Leeds",
        "keywords": [
            "roof repair leeds",
            "fascias soffits guttering leeds",
            "roofing company leeds",
            "chimney repair leeds"
        ]
    },
    "6109184488": {  # Leeds Rendering
        "account_name": "Leeds Rendering",
        "keywords": [
            "rendering near me"
        ]
    }
}

DAYS = 30


def get_keyword_details(client, customer_id: str, keyword_texts: list) -> dict:
    """Get current details for keywords including resource names."""
    ga_service = client.get_service("GoogleAdsService")

    # Query all keywords and filter in Python (GAQL OR syntax is problematic)
    query = f"""
        SELECT
            ad_group_criterion.resource_name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.status,
            ad_group.name,
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros
        FROM keyword_view
        WHERE segments.date DURING LAST_{DAYS}_DAYS
        ORDER BY metrics.cost_micros DESC
    """

    keywords = {}
    keyword_texts_lower = [kw.lower() for kw in keyword_texts]

    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            kw_text = row.ad_group_criterion.keyword.text
            # Filter to only keywords we're looking for
            if kw_text.lower() not in keyword_texts_lower:
                continue
            # Only keep first occurrence (avoid duplicates from date segments)
            if kw_text.lower() not in [k.lower() for k in keywords.keys()]:
                keywords[kw_text] = {
                    "resource_name": row.ad_group_criterion.resource_name,
                    "keyword_text": kw_text,
                    "match_type": row.ad_group_criterion.keyword.match_type.name,
                    "status": row.ad_group_criterion.status.name,
                    "ad_group": row.ad_group.name,
                    "campaign": row.campaign.name,
                    "impressions": row.metrics.impressions,
                    "clicks": row.metrics.clicks,
                    "cost": row.metrics.cost_micros / 1_000_000
                }
    except GoogleAdsException as ex:
        print(f"  Error fetching keyword details: {ex}")

    return keywords


def pause_keyword(client, customer_id: str, resource_name: str) -> bool:
    """Pause a single keyword using mutate operation."""
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    # Create the operation
    operation = client.get_type("AdGroupCriterionOperation")
    criterion = operation.update
    criterion.resource_name = resource_name
    criterion.status = client.enums.AdGroupCriterionStatusEnum.PAUSED

    # Set the update mask using protobuf field mask
    from google.protobuf import field_mask_pb2
    operation.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["status"]))

    try:
        response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id,
            operations=[operation]
        )
        return True
    except GoogleAdsException as ex:
        print(f"    ❌ Error pausing keyword: {ex}")
        return False


def verify_keyword_paused(client, customer_id: str, resource_name: str) -> str:
    """Verify the keyword status after pausing."""
    ga_service = client.get_service("GoogleAdsService")

    # Extract criterion ID from resource name
    # Format: customers/{customer_id}/adGroupCriteria/{ad_group_id}~{criterion_id}
    parts = resource_name.split("/")
    ad_group_criterion_id = parts[-1]
    ad_group_id = ad_group_criterion_id.split("~")[0]
    criterion_id = ad_group_criterion_id.split("~")[1]

    query = f"""
        SELECT
            ad_group_criterion.status
        FROM ad_group_criterion
        WHERE ad_group_criterion.criterion_id = {criterion_id}
            AND ad_group.id = {ad_group_id}
    """

    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            return row.ad_group_criterion.status.name
    except GoogleAdsException as ex:
        print(f"    ⚠️ Error verifying status: {ex}")

    return "UNKNOWN"


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rollback_data = {
        "timestamp": datetime.now().isoformat(),
        "description": "Rollback data for urgent keyword pauses",
        "changes": []
    }

    results = {
        "success": [],
        "failed": [],
        "skipped": []
    }

    print()
    print("=" * 70)
    print("EXECUTING URGENT GOOGLE ADS FIXES")
    print("PhD Networks & Systems Ltd")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 70)
    print()

    # Initialize client
    try:
        client = get_client()
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return

    # Process each account
    for customer_id, account_data in KEYWORDS_TO_PAUSE.items():
        account_name = account_data["account_name"]
        keywords_to_pause = account_data["keywords"]

        print(f"📋 ACCOUNT: {account_name} ({customer_id})")
        print("-" * 70)
        print()

        # Get current keyword details
        print("  Fetching keyword details...")
        keyword_details = get_keyword_details(client, customer_id, keywords_to_pause)

        if not keyword_details:
            print(f"  ⚠️ No keywords found matching criteria")
            print()
            continue

        # Process each keyword
        for kw_text in keywords_to_pause:
            # Case-insensitive lookup
            matching_key = None
            for key in keyword_details.keys():
                if key.lower() == kw_text.lower():
                    matching_key = key
                    break

            if matching_key is None:
                print(f"  ⚠️ Keyword not found: \"{kw_text}\"")
                results["skipped"].append({
                    "account": account_name,
                    "keyword": kw_text,
                    "reason": "Not found in account"
                })
                continue

            kw = keyword_details[matching_key]

            print(f"  📍 Keyword: \"{kw['keyword_text']}\"")
            print(f"     Match Type: {kw['match_type']}")
            print(f"     Ad Group: {kw['ad_group']}")
            print(f"     Campaign: {kw['campaign']}")
            print(f"     Current Status: {kw['status']}")
            print(f"     Spend (30d): £{kw['cost']:.2f}")
            print(f"     Clicks (30d): {kw['clicks']}")
            print(f"     Resource: {kw['resource_name']}")

            # Check if already paused
            if kw['status'] != 'ENABLED':
                print(f"     ⏭️ SKIPPED - Already {kw['status']}")
                results["skipped"].append({
                    "account": account_name,
                    "keyword": kw_text,
                    "reason": f"Already {kw['status']}"
                })
                print()
                continue

            # Save to rollback data before making changes
            rollback_data["changes"].append({
                "account_id": customer_id,
                "account_name": account_name,
                "resource_name": kw['resource_name'],
                "keyword_text": kw['keyword_text'],
                "match_type": kw['match_type'],
                "previous_status": kw['status'],
                "ad_group": kw['ad_group'],
                "campaign": kw['campaign']
            })

            # Execute pause
            print(f"     ⏸️ PAUSING...")
            success = pause_keyword(client, customer_id, kw['resource_name'])

            if success:
                # Verify the change
                new_status = verify_keyword_paused(client, customer_id, kw['resource_name'])
                if new_status == "PAUSED":
                    print(f"     ✅ SUCCESS - Status changed to PAUSED")
                    results["success"].append({
                        "account": account_name,
                        "keyword": kw_text,
                        "spend_saved": kw['cost'],
                        "resource_name": kw['resource_name']
                    })
                else:
                    print(f"     ⚠️ WARNING - Status is {new_status} (expected PAUSED)")
                    results["failed"].append({
                        "account": account_name,
                        "keyword": kw_text,
                        "reason": f"Status verification failed: {new_status}"
                    })
            else:
                print(f"     ❌ FAILED - Could not pause keyword")
                results["failed"].append({
                    "account": account_name,
                    "keyword": kw_text,
                    "reason": "Mutate operation failed"
                })

            print()

        print()

    # Save rollback file
    rollback_filename = f"rollback_{datetime.now().strftime('%Y%m%d')}.json"
    with open(rollback_filename, "w") as f:
        json.dump(rollback_data, f, indent=2)

    # Print summary
    print("=" * 70)
    print("EXECUTION SUMMARY")
    print("=" * 70)
    print()
    print(f"✅ Successfully Paused: {len(results['success'])}")
    for item in results["success"]:
        print(f"   - {item['account']}: \"{item['keyword']}\" (saved £{item['spend_saved']:.2f}/30d)")

    print()
    print(f"❌ Failed: {len(results['failed'])}")
    for item in results["failed"]:
        print(f"   - {item['account']}: \"{item['keyword']}\" ({item['reason']})")

    print()
    print(f"⏭️ Skipped: {len(results['skipped'])}")
    for item in results["skipped"]:
        print(f"   - {item['account']}: \"{item['keyword']}\" ({item['reason']})")

    print()
    total_saved = sum(item['spend_saved'] for item in results['success'])
    print(f"💰 Estimated Monthly Savings: £{total_saved:.2f}")

    print()
    print(f"📁 Rollback file saved: {rollback_filename}")
    print("   To re-enable keywords, use the resource names in this file")

    print()
    print("=" * 70)
    print("EXECUTION COMPLETE")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
