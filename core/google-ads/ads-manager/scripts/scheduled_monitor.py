#!/usr/bin/env python3
"""
Google Ads Scheduled Monitor - FULL AUTONOMY MODE

Daily workflow (designed to run at 8am):
1. Pull performance data
2. Run conversion_tracking_fixer.py (fix first)
3. Run autonomous_optimizer.py (optimize second)
4. Check budgets
5. Compile all changes made
6. Generate daily summary report
7. Save to JSON for webhooks/email

Usage:
    python3 scheduled_monitor.py [--output-dir /path/to/dir]
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from google_ads_client import (
    get_client,
    get_campaign_performance,
    get_keyword_performance,
    get_account_spend_for_period
)
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


def load_change_history() -> list:
    """Load today's change history."""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            history = json.load(f)
        # Filter to today's changes only
        today = datetime.now().strftime("%Y-%m-%d")
        return [c for c in history if c.get("executed_at", "").startswith(today)]
    return []


def run_conversion_fixer() -> dict:
    """Run the conversion tracking fixer."""
    print("\n" + "="*60)
    print("STEP 1: CONVERSION TRACKING FIXER")
    print("="*60)

    try:
        from conversion_tracking_fixer import ConversionTrackingFixer, load_config
        config = load_config()
        fixer = ConversionTrackingFixer(config)
        results = fixer.run()
        return {
            "success": True,
            "fixes_applied": sum(len(r.get("fixes_applied", [])) for r in results),
            "issues_found": sum(len(r.get("issues", [])) for r in results)
        }
    except Exception as e:
        print(f"  Error running conversion fixer: {e}")
        return {"success": False, "error": str(e)}


def run_optimizer() -> dict:
    """Run the autonomous optimizer."""
    print("\n" + "="*60)
    print("STEP 2: AUTONOMOUS OPTIMIZER")
    print("="*60)

    try:
        from autonomous_optimizer import AutonomousOptimizer, load_config
        config = load_config()
        optimizer = AutonomousOptimizer(config)
        results = optimizer.run()
        return {
            "success": True,
            "changes": len(results.get("changes", [])),
            "alerts": results.get("alerts", [])
        }
    except Exception as e:
        print(f"  Error running optimizer: {e}")
        return {"success": False, "error": str(e)}


def get_account_performance(client, customer_id: str, account_name: str, monthly_budget: float) -> dict:
    """Get performance summary for an account."""
    today = datetime.now()
    start_of_month = today.replace(day=1).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    # Get spend
    try:
        spend = get_account_spend_for_period(client, customer_id, start_of_month, end_date)
    except Exception:
        spend = 0

    # Get 7-day metrics
    try:
        campaigns = get_campaign_performance(client, customer_id, days=7)
        total_conversions = sum(c["conversions"] for c in campaigns)
        total_clicks = sum(c["clicks"] for c in campaigns)
        total_impressions = sum(c["impressions"] for c in campaigns)
    except Exception:
        total_conversions = 0
        total_clicks = 0
        total_impressions = 0

    percent_used = (spend / monthly_budget * 100) if monthly_budget > 0 else 0

    return {
        "account_id": customer_id,
        "account_name": account_name,
        "monthly_budget": monthly_budget,
        "spend_to_date": round(spend, 2),
        "percent_used": round(percent_used, 1),
        "conversions_7d": total_conversions,
        "clicks_7d": total_clicks,
        "impressions_7d": total_impressions
    }


def generate_daily_report(config: dict, conversion_results: dict, optimizer_results: dict) -> dict:
    """Generate the daily summary report."""
    print("\n" + "="*60)
    print("STEP 3: GENERATING DAILY REPORT")
    print("="*60)

    client = get_client()
    accounts = config.get("accounts", {})

    report = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat(),
        "accounts": [],
        "totals": {
            "spend": 0,
            "conversions": 0,
            "clicks": 0
        },
        "changes_made": [],
        "alerts": [],
        "conversion_tracking": conversion_results,
        "optimization": optimizer_results
    }

    # Get performance for each account
    for customer_id, account_info in accounts.items():
        if not account_info.get("enabled", False):
            continue

        monthly_budget = account_info.get("monthly_budget_gbp", 250)
        perf = get_account_performance(client, customer_id, account_info["name"], monthly_budget)
        report["accounts"].append(perf)

        report["totals"]["spend"] += perf["spend_to_date"]
        report["totals"]["conversions"] += perf["conversions_7d"]
        report["totals"]["clicks"] += perf["clicks_7d"]

        print(f"  {perf['account_name']}: £{perf['spend_to_date']:.2f}/{perf['monthly_budget']:.2f} ({perf['percent_used']:.0f}%)")

    # Get today's changes from history
    changes = load_change_history()
    report["changes_made"] = changes

    # Add optimizer alerts
    report["alerts"] = optimizer_results.get("alerts", [])

    return report


def format_email_summary(report: dict) -> str:
    """Format report as email-friendly text."""
    lines = []
    lines.append("="*60)
    lines.append(f"GOOGLE ADS DAILY REPORT - {report['date']}")
    lines.append("="*60)
    lines.append("")

    # Totals
    lines.append("SUMMARY")
    lines.append("-"*40)
    lines.append(f"Total Spend (MTD): £{report['totals']['spend']:.2f}")
    lines.append(f"Conversions (7d):  {report['totals']['conversions']}")
    lines.append(f"Clicks (7d):       {report['totals']['clicks']}")
    lines.append(f"Changes Made:      {len(report['changes_made'])}")
    lines.append("")

    # Changes applied
    if report["changes_made"]:
        lines.append("CHANGES APPLIED")
        lines.append("-"*40)
        for change in report["changes_made"]:
            account = change.get("account_name", "Unknown")
            change_type = change.get("type", "UNKNOWN")
            if change_type == "PAUSE_KEYWORD":
                lines.append(f"  [{account}] Paused keyword: {change.get('keyword')}")
                lines.append(f"      Reason: {change.get('reason')}")
            elif change_type == "ADD_NEGATIVE_RECOMMENDED":
                lines.append(f"  [{account}] Negative recommended: {change.get('search_term')}")
            elif change_type == "KEYWORD_OPPORTUNITY":
                lines.append(f"  [{account}] Keyword opportunity: {change.get('search_term')}")
            elif change_type == "BID_REDUCTION_RECOMMENDED":
                lines.append(f"  [{account}] Bid reduction: {change.get('keyword')}")
            elif change_type == "BID_INCREASE_RECOMMENDED":
                lines.append(f"  [{account}] Bid increase: {change.get('keyword')}")
            else:
                lines.append(f"  [{account}] {change_type}: {change.get('reason', '')}")
        lines.append("")

    # Conversion tracking fixes
    conv = report.get("conversion_tracking", {})
    if conv.get("fixes_applied", 0) > 0:
        lines.append("CONVERSION TRACKING FIXES")
        lines.append("-"*40)
        lines.append(f"  Issues found:  {conv.get('issues_found', 0)}")
        lines.append(f"  Fixes applied: {conv.get('fixes_applied', 0)}")
        lines.append("")

    # Budget status
    lines.append("BUDGET STATUS")
    lines.append("-"*40)
    for account in report["accounts"]:
        status = "OK"
        if account["percent_used"] >= 100:
            status = "EXHAUSTED"
        elif account["percent_used"] >= 90:
            status = "CRITICAL"
        elif account["percent_used"] >= 80:
            status = "WARNING"

        lines.append(f"  {account['account_name']}:")
        lines.append(f"      £{account['spend_to_date']:.2f} / £{account['monthly_budget']:.2f} ({account['percent_used']:.0f}%) - {status}")
    lines.append("")

    # Alerts requiring human action
    alerts = [a for a in report.get("alerts", []) if a.get("needs_human")]
    if alerts:
        lines.append("ACTION NEEDED (Budget Only)")
        lines.append("-"*40)
        for alert in alerts:
            lines.append(f"  {alert.get('message', alert.get('alert'))}")
        lines.append("")
    else:
        lines.append("ACTION NEEDED: None")
        lines.append("")

    lines.append("-"*60)
    lines.append("PhD Networks Autonomous Google Ads System")
    lines.append("Full Autonomy Mode - Notifies After, Not Before")
    lines.append("="*60)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Google Ads Scheduled Monitor - Full Autonomy")
    parser.add_argument("--output-dir", type=str, default=str(DATA_DIR), help="Directory to save output files")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print()
    print("="*60)
    print("GOOGLE ADS DAILY MONITOR - FULL AUTONOMY MODE")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # Load config
    config = load_config()

    # Step 1: Fix conversion tracking
    conversion_results = run_conversion_fixer()

    # Step 2: Run optimizer
    optimizer_results = run_optimizer()

    # Step 3: Generate report
    report = generate_daily_report(config, conversion_results, optimizer_results)

    # Format email summary
    email_text = format_email_summary(report)

    # Print summary
    print("\n" + email_text)

    # Save outputs
    date_str = datetime.now().strftime("%Y%m%d")
    time_str = datetime.now().strftime("%H%M%S")

    # Full report JSON
    report_file = output_dir / f"daily_report_{date_str}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    # Email text
    email_file = output_dir / f"daily_email_{date_str}.txt"
    with open(email_file, "w") as f:
        f.write(email_text)

    print(f"\n📁 Report saved: {report_file}")
    print(f"📁 Email text saved: {email_file}")

    return report


if __name__ == "__main__":
    main()
