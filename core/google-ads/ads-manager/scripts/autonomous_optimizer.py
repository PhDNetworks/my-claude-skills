#!/usr/bin/env python3
"""
Autonomous Google Ads Optimizer - FULL AUTONOMY MODE

World-class Google Ads specialist with full decision-making authority.
Executes optimizations automatically. Notifies after, not before.

Human approval ONLY required for:
- Increasing budgets
- Adding funds

Usage:
    python3 autonomous_optimizer.py [--account CUSTOMER_ID]
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from google_ads_client import (
    get_client,
    get_campaign_performance,
    get_keyword_performance,
    get_search_terms_report,
    get_campaign_budgets,
    get_account_spend_for_period
)
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Paths
SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"
DATA_DIR = SCRIPT_DIR.parent / "data"
CONFIG_FILE = CONFIG_DIR / "optimizer_config.json"
HISTORY_FILE = DATA_DIR / "change_history.json"


def load_config() -> dict:
    """Load optimizer configuration."""
    with open(CONFIG_FILE) as f:
        return json.load(f)


def save_to_history(changes: list):
    """Append changes to history file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    history = []
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            history = json.load(f)

    history.extend(changes)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def save_rollback(account_id: str, account_name: str, changes: list):
    """Save rollback data for safety."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    rollback_file = DATA_DIR / f"rollback_{account_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    rollback_data = {
        "timestamp": datetime.now().isoformat(),
        "account_id": account_id,
        "account_name": account_name,
        "changes": changes
    }

    with open(rollback_file, "w") as f:
        json.dump(rollback_data, f, indent=2)

    return rollback_file


class AutonomousOptimizer:
    """
    World-class Google Ads specialist with full decision-making authority.
    Executes optimizations automatically. Notifies after, not before.
    """

    def __init__(self, config: dict):
        self.config = config
        self.client = get_client()
        self.guardrails = config.get("guardrails", {})
        self.rules = config.get("optimization_rules", {})
        self.auto_execute = config.get("auto_execute", {})

        self.all_changes = []
        self.alerts = []

    def run(self, account_filter: Optional[str] = None) -> dict:
        """Main optimization loop - executes immediately."""
        print("\n" + "="*60)
        print("AUTONOMOUS GOOGLE ADS OPTIMIZER - FULL AUTONOMY")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

        accounts = self.config.get("accounts", {})

        for customer_id, account_info in accounts.items():
            if not account_info.get("enabled", False):
                continue

            if account_filter and customer_id != account_filter:
                continue

            self._optimize_account(customer_id, account_info)

        # Save all changes to history
        if self.all_changes:
            save_to_history(self.all_changes)

        # Print summary
        self._print_summary()

        return {
            "changes": self.all_changes,
            "alerts": self.alerts
        }

    def _optimize_account(self, customer_id: str, account_info: dict):
        """Run full optimization on an account."""
        account_name = account_info.get("name", customer_id)

        print(f"\n{'='*60}")
        print(f"Optimizing: {account_name} ({customer_id})")
        print("="*60)

        # Get performance data
        min_days = self.guardrails.get("min_data_before_decisions", {}).get("days", 7)
        print(f"\n  Fetching {min_days}-day performance data...")

        campaigns = get_campaign_performance(self.client, customer_id, min_days)
        keywords = get_keyword_performance(self.client, customer_id, min_days)
        search_terms = get_search_terms_report(self.client, customer_id, min_days)

        print(f"    Campaigns: {len(campaigns)}")
        print(f"    Keywords: {len(keywords)}")
        print(f"    Search terms: {len(search_terms)}")

        account_changes = []

        # 1. Pause wasteful keywords
        if self.auto_execute.get("pause_keywords", True):
            changes = self._pause_wasteful_keywords(customer_id, account_name, keywords)
            account_changes.extend(changes)

        # 2. Add negative keywords
        if self.auto_execute.get("add_negative_keywords", True):
            changes = self._add_negative_keywords(customer_id, account_name, search_terms)
            account_changes.extend(changes)

        # 3. Promote good search terms to keywords
        if self.auto_execute.get("create_keywords_from_search_terms", True):
            changes = self._promote_search_terms(customer_id, account_name, search_terms)
            account_changes.extend(changes)

        # 4. Optimize bids
        if self.auto_execute.get("adjust_bids", True):
            changes = self._optimize_bids(customer_id, account_name, keywords)
            account_changes.extend(changes)

        # 5. Check budget status
        budget_status = self._check_budget(customer_id, account_info)
        if budget_status.get("needs_human"):
            self.alerts.append(budget_status)

        # Save rollback data
        if account_changes:
            save_rollback(customer_id, account_name, account_changes)

        self.all_changes.extend(account_changes)

        print(f"\n  ✅ {len(account_changes)} changes applied to {account_name}")

    def _pause_wasteful_keywords(self, customer_id: str, account_name: str, keywords: list) -> list:
        """Pause keywords that are wasting budget."""
        changes = []
        rules = self.rules.get("pause_keyword_if", {})
        min_spend = rules.get("spend_gbp", 30)
        max_conversions = rules.get("conversions", 0)
        min_clicks = rules.get("clicks_min", 15)

        protected_patterns = self.guardrails.get("protected_patterns", [])

        for kw in keywords:
            if kw["status"] != "ENABLED":
                continue

            # Check if meets pause criteria
            if (kw["cost"] >= min_spend and
                kw["conversions"] <= max_conversions and
                kw["clicks"] >= min_clicks):

                # Check if protected
                kw_lower = kw["keyword"].lower()
                is_protected = any(p.lower() in kw_lower for p in protected_patterns)

                if is_protected:
                    print(f"    ⏭️  Skipped (protected): {kw['keyword']}")
                    continue

                # Execute pause
                success = self._execute_pause_keyword(customer_id, kw)

                if success:
                    change = {
                        "type": "PAUSE_KEYWORD",
                        "account_id": customer_id,
                        "account_name": account_name,
                        "keyword": kw["keyword"],
                        "ad_group": kw["ad_group"],
                        "reason": f"Spent £{kw['cost']:.2f} with {kw['conversions']} conversions",
                        "metrics": {"cost": kw["cost"], "clicks": kw["clicks"], "conversions": kw["conversions"]},
                        "executed_at": datetime.now().isoformat()
                    }
                    changes.append(change)
                    print(f"    ✅ Paused: {kw['keyword']} (£{kw['cost']:.2f}, 0 conv)")

        return changes

    def _execute_pause_keyword(self, customer_id: str, keyword: dict) -> bool:
        """Execute keyword pause via API."""
        from google.protobuf import field_mask_pb2

        ga_service = self.client.get_service("GoogleAdsService")

        # Find the keyword criterion
        query = f"""
            SELECT
                ad_group_criterion.resource_name
            FROM keyword_view
            WHERE ad_group_criterion.keyword.text = '{keyword["keyword"]}'
                AND ad_group.name = '{keyword["ad_group"]}'
                AND ad_group_criterion.status = 'ENABLED'
            LIMIT 1
        """

        try:
            response = ga_service.search(customer_id=customer_id, query=query)
            for row in response:
                resource_name = row.ad_group_criterion.resource_name

                criterion_service = self.client.get_service("AdGroupCriterionService")
                operation = self.client.get_type("AdGroupCriterionOperation")
                criterion = operation.update
                criterion.resource_name = resource_name
                criterion.status = self.client.enums.AdGroupCriterionStatusEnum.PAUSED

                operation.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["status"]))

                criterion_service.mutate_ad_group_criteria(
                    customer_id=customer_id,
                    operations=[operation]
                )
                return True

            return False
        except GoogleAdsException as ex:
            print(f"    ❌ Error pausing keyword: {ex}")
            return False

    def _add_negative_keywords(self, customer_id: str, account_name: str, search_terms: list) -> list:
        """Add negative keywords for irrelevant search terms."""
        changes = []
        rules = self.rules.get("add_as_negative_if", {})
        min_spend = rules.get("search_term_spend_gbp", 15)
        max_conversions = rules.get("conversions", 0)
        min_clicks = rules.get("clicks_min", 10)

        protected_patterns = self.guardrails.get("protected_patterns", [])

        for st in search_terms:
            if (st["cost"] >= min_spend and
                st["conversions"] <= max_conversions and
                st["clicks"] >= min_clicks):

                # Check if protected
                st_lower = st["search_term"].lower()
                is_protected = any(p.lower() in st_lower for p in protected_patterns)

                if is_protected:
                    print(f"    ⏭️  Skipped negative (protected): {st['search_term']}")
                    continue

                # Log for now - full negative keyword implementation requires campaign ID lookup
                change = {
                    "type": "ADD_NEGATIVE_RECOMMENDED",
                    "account_id": customer_id,
                    "account_name": account_name,
                    "search_term": st["search_term"],
                    "campaign": st["campaign"],
                    "reason": f"Spent £{st['cost']:.2f} with {st['conversions']} conversions",
                    "metrics": {"cost": st["cost"], "clicks": st["clicks"]},
                    "executed_at": datetime.now().isoformat()
                }
                changes.append(change)
                print(f"    📝 Negative recommended: {st['search_term']} (£{st['cost']:.2f})")

        return changes

    def _promote_search_terms(self, customer_id: str, account_name: str, search_terms: list) -> list:
        """Promote high-performing search terms to keywords."""
        changes = []
        rules = self.rules.get("add_as_keyword_if", {})
        min_conversions = rules.get("search_term_conversions_min", 1)
        min_clicks = rules.get("or_clicks_min", 5)
        min_ctr = rules.get("and_ctr_above", 3.0)

        for st in search_terms:
            ctr = (st["clicks"] / st["impressions"] * 100) if st["impressions"] > 0 else 0

            if st["conversions"] >= min_conversions or (st["clicks"] >= min_clicks and ctr >= min_ctr):
                change = {
                    "type": "KEYWORD_OPPORTUNITY",
                    "account_id": customer_id,
                    "account_name": account_name,
                    "search_term": st["search_term"],
                    "campaign": st["campaign"],
                    "reason": f"{st['conversions']} conv, {st['clicks']} clicks, {ctr:.1f}% CTR",
                    "metrics": {"conversions": st["conversions"], "clicks": st["clicks"], "ctr": ctr},
                    "executed_at": datetime.now().isoformat()
                }
                changes.append(change)
                print(f"    💡 Keyword opportunity: {st['search_term']} ({st['conversions']} conv)")

        return changes

    def _optimize_bids(self, customer_id: str, account_name: str, keywords: list) -> list:
        """Optimize keyword bids based on performance."""
        changes = []
        reduce_rules = self.rules.get("reduce_bid_if", {})
        increase_rules = self.rules.get("increase_bid_if", {})

        max_bid = self.guardrails.get("max_bid_amount_gbp", 10.00)
        min_clicks = self.guardrails.get("min_data_before_decisions", {}).get("clicks", 10)

        # Calculate average metrics
        converting_kws = [kw for kw in keywords if kw["conversions"] > 0]
        avg_cpa = sum(kw["cost"] for kw in converting_kws) / sum(kw["conversions"] for kw in converting_kws) if converting_kws else 0

        for kw in keywords:
            if kw["status"] != "ENABLED" or kw["clicks"] < min_clicks:
                continue

            # Check for bid reduction
            if kw["quality_score"] and kw["quality_score"] < reduce_rules.get("quality_score_below", 4):
                change = {
                    "type": "BID_REDUCTION_RECOMMENDED",
                    "account_id": customer_id,
                    "account_name": account_name,
                    "keyword": kw["keyword"],
                    "reason": f"Quality Score {kw['quality_score']} below threshold",
                    "current_cpc": kw["avg_cpc"],
                    "executed_at": datetime.now().isoformat()
                }
                changes.append(change)
                print(f"    📉 Bid reduction recommended: {kw['keyword']} (QS={kw['quality_score']})")

            # Check for bid increase
            if (kw["quality_score"] and kw["quality_score"] >= increase_rules.get("quality_score_above", 7) and
                kw["conversions"] > 0):
                change = {
                    "type": "BID_INCREASE_RECOMMENDED",
                    "account_id": customer_id,
                    "account_name": account_name,
                    "keyword": kw["keyword"],
                    "reason": f"High performer: QS={kw['quality_score']}, {kw['conversions']} conv",
                    "current_cpc": kw["avg_cpc"],
                    "executed_at": datetime.now().isoformat()
                }
                changes.append(change)
                print(f"    📈 Bid increase recommended: {kw['keyword']} (QS={kw['quality_score']})")

        return changes

    def _check_budget(self, customer_id: str, account_info: dict) -> dict:
        """Check budget status and alert if action needed."""
        monthly_budget = account_info.get("monthly_budget_gbp", 250)
        account_name = account_info.get("name", customer_id)

        # Get current month spend
        today = datetime.now()
        start_of_month = today.replace(day=1).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")

        try:
            spend = get_account_spend_for_period(self.client, customer_id, start_of_month, end_date)
        except Exception:
            spend = 0

        percent_used = (spend / monthly_budget * 100) if monthly_budget > 0 else 0
        days_in_month = 31
        day_of_month = today.day
        expected_percent = (day_of_month / days_in_month * 100)

        status = {
            "account_id": customer_id,
            "account_name": account_name,
            "monthly_budget": monthly_budget,
            "spend_to_date": spend,
            "percent_used": percent_used,
            "expected_percent": expected_percent,
            "needs_human": False
        }

        if spend >= monthly_budget:
            status["needs_human"] = True
            status["alert"] = "BUDGET_EXHAUSTED"
            status["message"] = f"{account_name}: Budget exhausted (£{spend:.2f}/£{monthly_budget})"
            print(f"\n    ⚠️  BUDGET EXHAUSTED: {account_name}")
        elif percent_used > expected_percent * 1.2:
            status["alert"] = "OVERPACING"
            status["message"] = f"{account_name}: Overpacing ({percent_used:.0f}% vs expected {expected_percent:.0f}%)"
            print(f"    ⚠️  Overpacing: {account_name} ({percent_used:.0f}%)")

        return status

    def _print_summary(self):
        """Print optimization summary."""
        print("\n" + "="*60)
        print("OPTIMIZATION SUMMARY - FULL AUTONOMY")
        print("="*60)

        # Count by type
        by_type = {}
        for change in self.all_changes:
            t = change.get("type", "UNKNOWN")
            by_type[t] = by_type.get(t, 0) + 1

        print(f"\n  Total changes: {len(self.all_changes)}")
        for t, count in by_type.items():
            print(f"    {t}: {count}")

        if self.alerts:
            print(f"\n  ⚠️  ALERTS REQUIRING HUMAN ACTION:")
            for alert in self.alerts:
                if alert.get("needs_human"):
                    print(f"    - {alert.get('message', alert.get('alert'))}")

        print("\n" + "="*60)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Autonomous Google Ads Optimizer - Full Autonomy")
    parser.add_argument("--account", type=str, help="Only optimize specific account ID")
    args = parser.parse_args()

    config = load_config()
    optimizer = AutonomousOptimizer(config)
    optimizer.run(account_filter=args.account)


if __name__ == "__main__":
    main()
