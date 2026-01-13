#!/usr/bin/env python3
"""
Update Leeds Rendering Daily Budget

Sets daily budget to £8.00 (£250/month ÷ 31 days)
"""

import json
from datetime import datetime
from pathlib import Path
from google_ads_client import (
    get_client,
    get_campaign_budgets,
    update_campaign_budget
)

# Leeds Rendering account
CUSTOMER_ID = "6109184488"
ACCOUNT_NAME = "Leeds Rendering"

# Target budget: £250/month ÷ 31 days = £8.06/day, rounded to £8.00
TARGET_DAILY_BUDGET = 8.00
TARGET_DAILY_BUDGET_MICROS = int(TARGET_DAILY_BUDGET * 1_000_000)


def main():
    print()
    print("=" * 60)
    print("LEEDS RENDERING BUDGET UPDATE")
    print(f"Account: {ACCOUNT_NAME} ({CUSTOMER_ID})")
    print(f"Target Daily Budget: £{TARGET_DAILY_BUDGET:.2f}")
    print("=" * 60)
    print()

    # Initialize client
    client = get_client()

    # Get current budgets (ENABLED campaigns only to avoid updating paused campaigns)
    print("📊 Querying current campaign budgets (ENABLED only)...")
    budgets = get_campaign_budgets(client, CUSTOMER_ID, enabled_only=True)

    if not budgets:
        print("❌ No campaigns found!")
        return

    print(f"   Found {len(budgets)} campaign(s)")
    print()

    # Track rollback data
    rollback_data = {
        "timestamp": datetime.now().isoformat(),
        "account_id": CUSTOMER_ID,
        "account_name": ACCOUNT_NAME,
        "reason": f"Set daily budget to £{TARGET_DAILY_BUDGET:.2f} (£250/month over 31 days)",
        "changes": []
    }

    # Process each unique budget (campaigns may share budgets)
    processed_budgets = set()
    results = []

    for b in budgets:
        budget_id = b["budget_id"]
        if budget_id in processed_budgets:
            continue
        processed_budgets.add(budget_id)

        current_budget = b["daily_budget"]
        resource_name = b["resource_name"]

        print(f"Campaign: {b['campaign_name']}")
        print(f"   Current daily budget: £{current_budget:.2f}")
        print(f"   Budget resource: {resource_name}")

        # Store rollback data
        rollback_data["changes"].append({
            "budget_id": budget_id,
            "resource_name": resource_name,
            "campaign_name": b["campaign_name"],
            "previous_budget": current_budget,
            "previous_budget_micros": b["daily_budget_micros"]
        })

        if current_budget == TARGET_DAILY_BUDGET:
            print(f"   ✅ Already at target budget")
            results.append({"campaign": b["campaign_name"], "status": "already_correct"})
            continue

        # Update budget
        print(f"   🔄 Updating to £{TARGET_DAILY_BUDGET:.2f}...")
        result = update_campaign_budget(
            client,
            CUSTOMER_ID,
            resource_name,
            TARGET_DAILY_BUDGET_MICROS
        )

        if result["success"]:
            print(f"   ✅ Updated successfully")
            results.append({
                "campaign": b["campaign_name"],
                "status": "updated",
                "previous": current_budget,
                "new": TARGET_DAILY_BUDGET
            })
        else:
            print(f"   ❌ Error: {result['error']}")
            results.append({
                "campaign": b["campaign_name"],
                "status": "error",
                "error": result["error"]
            })

        print()

    # Save rollback file
    rollback_file = Path(__file__).parent / f"rollback_budget_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(rollback_file, "w") as f:
        json.dump(rollback_data, f, indent=2)

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    updated = len([r for r in results if r["status"] == "updated"])
    already_correct = len([r for r in results if r["status"] == "already_correct"])
    errors = len([r for r in results if r["status"] == "error"])

    print(f"Updated: {updated}")
    print(f"Already correct: {already_correct}")
    print(f"Errors: {errors}")
    print()
    print(f"📁 Rollback file: {rollback_file}")
    print()

    # Verify the change
    print("🔍 Verifying changes...")
    updated_budgets = get_campaign_budgets(client, CUSTOMER_ID, enabled_only=True)
    for b in updated_budgets:
        print(f"   {b['campaign_name']}: £{b['daily_budget']:.2f}/day")

    print()
    print("=" * 60)

    return results


if __name__ == "__main__":
    main()
