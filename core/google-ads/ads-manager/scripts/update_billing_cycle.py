#!/usr/bin/env python3
"""
Update Billing Cycle

Utility to update client budgets when payment is received.
- Updates cycle_start in client_budgets.json
- Resets status to ACTIVE
- Sets auto_pause to true
- Optionally re-enables campaigns if they were budget-paused

Usage:
    python3 update_billing_cycle.py --account 6109184488 --payment-date 2026-01-08 --amount 250
    python3 update_billing_cycle.py --account 5481658097 --payment-date 2026-01-13 --amount 250 --enable-campaigns
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from google_ads_client import get_client, enable_all_campaigns, get_campaign_budgets

# Paths
SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"
LOGS_DIR = SCRIPT_DIR.parent / "logs"
BUDGETS_FILE = CONFIG_DIR / "client_budgets.json"


def load_budgets() -> dict:
    """Load client budget configuration."""
    with open(BUDGETS_FILE) as f:
        return json.load(f)


def save_budgets(budgets: dict):
    """Save updated budget configuration."""
    with open(BUDGETS_FILE, "w") as f:
        json.dump(budgets, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Update billing cycle after payment")
    parser.add_argument("--account", required=True, help="Account ID to update")
    parser.add_argument("--payment-date", required=True, help="Payment date (YYYY-MM-DD)")
    parser.add_argument("--amount", type=float, required=True, help="Payment amount in GBP")
    parser.add_argument("--cycle-days", type=int, default=31, help="Cycle length in days (default: 31)")
    parser.add_argument("--enable-campaigns", action="store_true", help="Re-enable paused campaigns")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying")
    args = parser.parse_args()

    print()
    print("=" * 60)
    print("UPDATE BILLING CYCLE")
    print(f"Timestamp: {datetime.now().isoformat()}")
    if args.dry_run:
        print("MODE: DRY RUN")
    print("=" * 60)
    print()

    # Load current config
    budgets = load_budgets()

    if args.account not in budgets:
        print(f"❌ Account {args.account} not found in config")
        print(f"   Available accounts: {list(budgets.keys())}")
        return

    config = budgets[args.account]
    print(f"Account: {config['name']} ({args.account})")
    print()

    # Show current state
    print("CURRENT STATE:")
    print(f"   Cycle Start: {config['cycle_start']}")
    print(f"   Cycle Days: {config['cycle_days']}")
    print(f"   Monthly Budget: £{config['monthly_budget']:.2f}")
    print(f"   Status: {config['status']}")
    print(f"   Auto-pause: {config['auto_pause']}")
    if config.get("note"):
        print(f"   Note: {config['note']}")
    print()

    # Validate payment date
    try:
        payment_date = datetime.strptime(args.payment_date, "%Y-%m-%d").date()
    except ValueError:
        print(f"❌ Invalid date format: {args.payment_date}")
        print("   Use YYYY-MM-DD format")
        return

    # Calculate new values
    new_config = {
        "cycle_start": args.payment_date,
        "cycle_days": args.cycle_days,
        "monthly_budget": args.amount,
        "status": "ACTIVE",
        "auto_pause": True
    }

    print("NEW STATE:")
    print(f"   Cycle Start: {new_config['cycle_start']}")
    print(f"   Cycle Days: {new_config['cycle_days']}")
    print(f"   Monthly Budget: £{new_config['monthly_budget']:.2f}")
    print(f"   Status: {new_config['status']}")
    print(f"   Auto-pause: {new_config['auto_pause']}")
    print()

    if args.dry_run:
        print("[DRY RUN] No changes made")
        return

    # Update config
    budgets[args.account].update(new_config)

    # Remove old note if status changed
    if "note" in budgets[args.account] and config["status"] != "ACTIVE":
        del budgets[args.account]["note"]

    save_budgets(budgets)
    print("✅ Configuration updated")
    print()

    # Re-enable campaigns if requested
    if args.enable_campaigns:
        print("ENABLING CAMPAIGNS:")
        client = get_client()

        # Get current campaign states
        campaign_budgets = get_campaign_budgets(client, args.account)
        paused_campaigns = [b for b in campaign_budgets if b["campaign_status"] == "PAUSED"]

        if not paused_campaigns:
            print("   No paused campaigns found")
        else:
            results = enable_all_campaigns(client, args.account)
            for r in results:
                if r["success"]:
                    print(f"   ✅ Enabled campaign {r['campaign_id']}")
                else:
                    print(f"   ❌ Failed: {r.get('error', 'Unknown error')}")
        print()

    # Log the change
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": "billing_cycle_update",
        "account_id": args.account,
        "account_name": config["name"],
        "payment_date": args.payment_date,
        "amount": args.amount,
        "previous_status": config["status"],
        "new_status": "ACTIVE",
        "campaigns_enabled": args.enable_campaigns
    }

    log_file = LOGS_DIR / f"billing_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, "w") as f:
        json.dump(log_entry, f, indent=2)

    print(f"📁 Log saved: {log_file}")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
