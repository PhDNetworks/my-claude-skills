#!/usr/bin/env python3
"""
Conversion Tracking Fixer - Full Autonomy Mode

Diagnoses and auto-fixes conversion tracking issues across all accounts.
Executes fixes immediately without approval.

Usage:
    python3 conversion_tracking_fixer.py [--account CUSTOMER_ID]
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

from google_ads_client import get_client
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Paths
SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"
DATA_DIR = SCRIPT_DIR.parent / "data"
CONFIG_FILE = CONFIG_DIR / "optimizer_config.json"


def load_config() -> dict:
    """Load optimizer configuration."""
    with open(CONFIG_FILE) as f:
        return json.load(f)


class ConversionTrackingFixer:
    """Diagnose and fix conversion tracking issues."""

    def __init__(self, config: dict):
        self.config = config
        self.client = get_client()
        self.fixes_applied = []
        self.issues_found = []

    def diagnose_account(self, customer_id: str, account_name: str) -> dict:
        """Diagnose conversion tracking for an account."""
        print(f"\n  Diagnosing: {account_name} ({customer_id})")

        results = {
            "account_id": customer_id,
            "account_name": account_name,
            "conversion_actions": [],
            "issues": [],
            "fixes_applied": []
        }

        # Get all conversion actions
        conversion_actions = self._get_conversion_actions(customer_id)
        results["conversion_actions"] = conversion_actions

        print(f"    Found {len(conversion_actions)} conversion action(s)")

        for action in conversion_actions:
            issues = self._check_action_issues(action)
            if issues:
                results["issues"].extend(issues)
                for issue in issues:
                    print(f"    ⚠️  {issue['issue']}: {action['name']}")

        return results

    def _get_conversion_actions(self, customer_id: str) -> list:
        """Get all conversion actions for an account."""
        ga_service = self.client.get_service("GoogleAdsService")

        query = """
            SELECT
                conversion_action.id,
                conversion_action.name,
                conversion_action.status,
                conversion_action.type,
                conversion_action.category,
                conversion_action.counting_type,
                conversion_action.attribution_model_settings.attribution_model,
                conversion_action.click_through_lookback_window_days,
                conversion_action.include_in_conversions_metric,
                conversion_action.primary_for_goal
            FROM conversion_action
            WHERE conversion_action.status != 'REMOVED'
        """

        actions = []
        try:
            response = ga_service.search(customer_id=customer_id, query=query)
            for row in response:
                ca = row.conversion_action
                actions.append({
                    "id": ca.id,
                    "name": ca.name,
                    "status": ca.status.name,
                    "type": ca.type_.name,
                    "category": ca.category.name,
                    "counting_type": ca.counting_type.name,
                    "attribution_model": ca.attribution_model_settings.attribution_model.name,
                    "lookback_window_days": ca.click_through_lookback_window_days,
                    "include_in_conversions": ca.include_in_conversions_metric,
                    "primary_for_goal": ca.primary_for_goal,
                    "resource_name": f"customers/{customer_id}/conversionActions/{ca.id}"
                })
        except GoogleAdsException as ex:
            print(f"    Error fetching conversion actions: {ex}")

        return actions

    def _check_action_issues(self, action: dict) -> list:
        """Check a conversion action for issues."""
        issues = []
        optimal = self.config.get("conversion_tracking", {}).get("optimal_settings", {})

        # Check if disabled
        if action["status"] != "ENABLED":
            issues.append({
                "action_id": action["id"],
                "action_name": action["name"],
                "issue": "DISABLED",
                "current": action["status"],
                "recommended": "ENABLED",
                "auto_fix": True
            })

        # Check lookback window
        optimal_window = optimal.get("conversion_window_days", 30)
        if action["lookback_window_days"] < optimal_window:
            issues.append({
                "action_id": action["id"],
                "action_name": action["name"],
                "issue": "SHORT_LOOKBACK_WINDOW",
                "current": f"{action['lookback_window_days']} days",
                "recommended": f"{optimal_window} days",
                "auto_fix": True
            })

        # Check counting type for lead gen
        optimal_counting = optimal.get("counting_type", "ONE")
        if action["counting_type"] != optimal_counting and action["category"] in ["LEAD", "CONTACT", "SUBMIT_LEAD_FORM"]:
            issues.append({
                "action_id": action["id"],
                "action_name": action["name"],
                "issue": "WRONG_COUNTING_TYPE",
                "current": action["counting_type"],
                "recommended": optimal_counting,
                "auto_fix": True
            })

        # Check if included in conversions
        if not action["include_in_conversions"]:
            issues.append({
                "action_id": action["id"],
                "action_name": action["name"],
                "issue": "NOT_IN_CONVERSIONS_METRIC",
                "current": "Excluded",
                "recommended": "Included",
                "auto_fix": True
            })

        return issues

    def fix_account(self, customer_id: str, account_name: str) -> dict:
        """Diagnose and fix conversion tracking for an account."""
        results = self.diagnose_account(customer_id, account_name)

        if not results["issues"]:
            print(f"    ✅ No issues found")
            return results

        # Auto-fix if enabled
        if self.config.get("conversion_tracking", {}).get("auto_fix", True):
            print(f"\n    Applying fixes...")
            for issue in results["issues"]:
                if issue.get("auto_fix"):
                    fix_result = self._apply_fix(customer_id, issue)
                    if fix_result["success"]:
                        results["fixes_applied"].append(fix_result)
                        self.fixes_applied.append(fix_result)
                        print(f"    ✅ Fixed: {issue['issue']} on {issue['action_name']}")
                    else:
                        print(f"    ❌ Failed to fix: {issue['issue']} - {fix_result.get('error')}")

        return results

    def _apply_fix(self, customer_id: str, issue: dict) -> dict:
        """Apply a fix for a conversion tracking issue."""
        from google.protobuf import field_mask_pb2

        try:
            conversion_action_service = self.client.get_service("ConversionActionService")
            operation = self.client.get_type("ConversionActionOperation")
            conversion_action = operation.update

            resource_name = f"customers/{customer_id}/conversionActions/{issue['action_id']}"
            conversion_action.resource_name = resource_name

            paths_to_update = []

            if issue["issue"] == "DISABLED":
                conversion_action.status = self.client.enums.ConversionActionStatusEnum.ENABLED
                paths_to_update.append("status")

            elif issue["issue"] == "SHORT_LOOKBACK_WINDOW":
                optimal_window = self.config.get("conversion_tracking", {}).get("optimal_settings", {}).get("conversion_window_days", 30)
                conversion_action.click_through_lookback_window_days = optimal_window
                paths_to_update.append("click_through_lookback_window_days")

            elif issue["issue"] == "WRONG_COUNTING_TYPE":
                conversion_action.counting_type = self.client.enums.ConversionActionCountingTypeEnum.ONE_PER_CLICK
                paths_to_update.append("counting_type")

            elif issue["issue"] == "NOT_IN_CONVERSIONS_METRIC":
                conversion_action.include_in_conversions_metric = True
                paths_to_update.append("include_in_conversions_metric")

            if not paths_to_update:
                return {"success": False, "error": "Unknown issue type"}

            operation.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=paths_to_update))

            response = conversion_action_service.mutate_conversion_actions(
                customer_id=customer_id,
                operations=[operation]
            )

            return {
                "success": True,
                "action_id": issue["action_id"],
                "action_name": issue["action_name"],
                "issue": issue["issue"],
                "fixed_at": datetime.now().isoformat()
            }

        except GoogleAdsException as ex:
            return {
                "success": False,
                "action_id": issue["action_id"],
                "issue": issue["issue"],
                "error": str(ex)
            }

    def run(self, account_filter: str = None) -> list:
        """Run conversion tracking fixer across all accounts."""
        print("\n" + "="*60)
        print("CONVERSION TRACKING FIXER - FULL AUTONOMY")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

        accounts = self.config.get("accounts", {})
        all_results = []

        for customer_id, account_info in accounts.items():
            if not account_info.get("enabled", False):
                continue

            if account_filter and customer_id != account_filter:
                continue

            results = self.fix_account(customer_id, account_info.get("name", customer_id))
            all_results.append(results)

        # Print summary
        total_issues = sum(len(r["issues"]) for r in all_results)
        total_fixes = sum(len(r["fixes_applied"]) for r in all_results)

        print("\n" + "="*60)
        print("CONVERSION TRACKING SUMMARY")
        print("="*60)
        print(f"  Issues found: {total_issues}")
        print(f"  Fixes applied: {total_fixes}")
        print("="*60 + "\n")

        return all_results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Conversion Tracking Fixer")
    parser.add_argument("--account", type=str, help="Only fix specific account ID")
    args = parser.parse_args()

    config = load_config()
    fixer = ConversionTrackingFixer(config)
    fixer.run(account_filter=args.account)


if __name__ == "__main__":
    main()
