#!/usr/bin/env python3
"""
Fix Leeds Rendering "rendering near me" keyword

Changes BROAD match to PHRASE match by:
1. Creating new PHRASE match keyword in same ad group
2. Keeping old BROAD match PAUSED

Account: Leeds Rendering (6109184488)
"""

import json
from datetime import datetime
from google_ads_client import get_client
from google.ads.googleads.errors import GoogleAdsException

CUSTOMER_ID = "6109184488"
ACCOUNT_NAME = "Leeds Rendering"
KEYWORD_TEXT = "rendering near me"


def get_ad_group_info(client, customer_id: str) -> dict:
    """Get the ad group ID where the keyword exists."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group.resource_name,
            campaign.id,
            campaign.name
        FROM ad_group_criterion
        WHERE ad_group_criterion.keyword.text = "{KEYWORD_TEXT}"
        LIMIT 1
    """

    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            return {
                "ad_group_id": row.ad_group.id,
                "ad_group_name": row.ad_group.name,
                "ad_group_resource": row.ad_group.resource_name,
                "campaign_id": row.campaign.id,
                "campaign_name": row.campaign.name
            }
    except GoogleAdsException as ex:
        print(f"Error: {ex}")
    return None


def create_phrase_match_keyword(client, customer_id: str, ad_group_id: int) -> dict:
    """Create the keyword with PHRASE match type."""
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    # Create the operation
    operation = client.get_type("AdGroupCriterionOperation")
    criterion = operation.create

    # Set the ad group resource name
    criterion.ad_group = f"customers/{customer_id}/adGroups/{ad_group_id}"

    # Set keyword details
    criterion.keyword.text = KEYWORD_TEXT
    criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE

    # Set status to ENABLED
    criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED

    try:
        response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id,
            operations=[operation]
        )
        result = response.results[0]
        return {
            "success": True,
            "resource_name": result.resource_name
        }
    except GoogleAdsException as ex:
        return {
            "success": False,
            "error": str(ex)
        }


def verify_keyword_exists(client, customer_id: str, match_type: str) -> dict:
    """Verify the keyword exists with specified match type."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            ad_group_criterion.resource_name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.status,
            ad_group.name
        FROM ad_group_criterion
        WHERE ad_group_criterion.keyword.text = "{KEYWORD_TEXT}"
            AND ad_group_criterion.keyword.match_type = '{match_type}'
    """

    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            return {
                "exists": True,
                "resource_name": row.ad_group_criterion.resource_name,
                "status": row.ad_group_criterion.status.name,
                "match_type": row.ad_group_criterion.keyword.match_type.name,
                "ad_group": row.ad_group.name
            }
    except GoogleAdsException as ex:
        print(f"Error verifying: {ex}")

    return {"exists": False}


def main():
    timestamp = datetime.now()
    log_data = {
        "timestamp": timestamp.isoformat(),
        "account_id": CUSTOMER_ID,
        "account_name": ACCOUNT_NAME,
        "action": "Create PHRASE match keyword",
        "keyword": KEYWORD_TEXT,
        "changes": []
    }

    print()
    print("=" * 70)
    print("LEEDS RENDERING KEYWORD FIX")
    print(f"Timestamp: {timestamp.isoformat()}")
    print("=" * 70)
    print()

    # Initialize client
    try:
        client = get_client()
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return

    # Step 1: Get ad group info
    print("📋 Step 1: Getting ad group information...")
    ad_group_info = get_ad_group_info(client, CUSTOMER_ID)

    if not ad_group_info:
        print("❌ Could not find ad group for keyword")
        return

    print(f"   Ad Group: {ad_group_info['ad_group_name']} (ID: {ad_group_info['ad_group_id']})")
    print(f"   Campaign: {ad_group_info['campaign_name']}")
    print()

    # Step 2: Check current state - BROAD should be PAUSED
    print("📋 Step 2: Verifying BROAD match is PAUSED...")
    broad_status = verify_keyword_exists(client, CUSTOMER_ID, "BROAD")

    if broad_status["exists"]:
        print(f"   BROAD match: {broad_status['status']}")
        if broad_status["status"] != "PAUSED":
            print("   ⚠️ Warning: BROAD match is not PAUSED")
        else:
            print("   ✅ BROAD match correctly PAUSED")
    else:
        print("   ⚠️ BROAD match not found (may have been removed)")
    print()

    # Step 3: Check if PHRASE match already exists
    print("📋 Step 3: Checking if PHRASE match already exists...")
    phrase_status = verify_keyword_exists(client, CUSTOMER_ID, "PHRASE")

    if phrase_status["exists"]:
        print(f"   ✅ PHRASE match already exists: {phrase_status['status']}")
        log_data["changes"].append({
            "action": "SKIPPED",
            "reason": "PHRASE match keyword already exists",
            "status": phrase_status["status"]
        })
    else:
        print("   PHRASE match does not exist - creating...")
        print()

        # Step 4: Create PHRASE match keyword
        print("📋 Step 4: Creating PHRASE match keyword...")
        result = create_phrase_match_keyword(client, CUSTOMER_ID, ad_group_info["ad_group_id"])

        if result["success"]:
            print(f"   ✅ Created successfully!")
            print(f"   Resource: {result['resource_name']}")

            log_data["changes"].append({
                "action": "CREATED",
                "keyword": KEYWORD_TEXT,
                "match_type": "PHRASE",
                "status": "ENABLED",
                "resource_name": result["resource_name"],
                "ad_group_id": ad_group_info["ad_group_id"],
                "ad_group_name": ad_group_info["ad_group_name"]
            })

            # Step 5: Verify creation
            print()
            print("📋 Step 5: Verifying creation...")
            verify = verify_keyword_exists(client, CUSTOMER_ID, "PHRASE")
            if verify["exists"] and verify["status"] == "ENABLED":
                print(f"   ✅ Verified: PHRASE match is {verify['status']}")
            else:
                print(f"   ⚠️ Verification issue: {verify}")
        else:
            print(f"   ❌ Failed to create: {result['error']}")
            log_data["changes"].append({
                "action": "FAILED",
                "error": result["error"]
            })

    print()

    # Save log file
    log_filename = f"keyword_fix_log_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_filename, "w") as f:
        json.dump(log_data, f, indent=2)

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Account: {ACCOUNT_NAME} ({CUSTOMER_ID})")
    print(f"Keyword: \"{KEYWORD_TEXT}\"")
    print()
    print("Current state:")

    # Final verification
    broad_final = verify_keyword_exists(client, CUSTOMER_ID, "BROAD")
    phrase_final = verify_keyword_exists(client, CUSTOMER_ID, "PHRASE")

    if broad_final["exists"]:
        print(f"  • BROAD match: {broad_final['status']}")
    if phrase_final["exists"]:
        print(f"  • PHRASE match: {phrase_final['status']}")

    print()
    print(f"📁 Log saved: {log_filename}")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
