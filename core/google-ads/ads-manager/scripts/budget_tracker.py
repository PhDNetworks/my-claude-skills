#!/usr/bin/env python3
"""
Budget Tracker

Tracks spend against monthly budgets for all client accounts.
Alerts at 80%, 95%, and auto-pauses at 100% (if enabled).

Usage:
    python3 budget_tracker.py [--dry-run]
"""

import json
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from pathlib import Path
from google_ads_client import (
    get_client,
    get_account_spend_for_period,
    pause_all_campaigns
)

# Paths
SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"
LOGS_DIR = SCRIPT_DIR.parent / "logs"
BUDGETS_FILE = CONFIG_DIR / "client_budgets.json"

# Alert thresholds
THRESHOLD_WARNING = 0.80   # 80% - log warning
THRESHOLD_CRITICAL = 0.95  # 95% - send email alert
THRESHOLD_PAUSE = 1.00     # 100% - auto-pause if enabled

# Email config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "daniel.doherty@phdnetworks.co.uk"
ALERT_EMAIL = "daniel.doherty@phdnetworks.co.uk"


def load_budgets() -> dict:
    """Load client budget configuration."""
    if not BUDGETS_FILE.exists():
        raise FileNotFoundError(f"Budget config not found: {BUDGETS_FILE}")

    with open(BUDGETS_FILE) as f:
        return json.load(f)


def save_budgets(budgets: dict):
    """Save updated budget configuration."""
    with open(BUDGETS_FILE, "w") as f:
        json.dump(budgets, f, indent=2)


def calculate_cycle_dates(config: dict) -> tuple:
    """
    Calculate the current cycle's start and end dates.

    Returns:
        (cycle_start, cycle_end, days_remaining)
        For one-off budgets (cycle_days=null), returns (cycle_start, today, None)
    """
    cycle_start = datetime.strptime(config["cycle_start"], "%Y-%m-%d").date()
    today = datetime.now().date()

    if config["cycle_days"] is None:
        # One-off budget - track from start to forever
        return cycle_start, today, None

    cycle_days = config["cycle_days"]
    cycle_end = cycle_start + timedelta(days=cycle_days)

    # If we're past the cycle end, the cycle has ended
    if today > cycle_end:
        days_remaining = 0
    else:
        days_remaining = (cycle_end - today).days

    return cycle_start, cycle_end, days_remaining


def track_account(client, customer_id: str, config: dict) -> dict:
    """
    Track budget status for a single account.

    Returns dict with:
        - spend_to_date
        - budget_remaining
        - percent_used
        - days_remaining
        - daily_run_rate
        - projected_total
        - status (OK, WARNING, CRITICAL, EXHAUSTED, OVERDUE)
        - auto_pause (from config)
    """
    cycle_start, cycle_end, days_remaining = calculate_cycle_dates(config)
    today = datetime.now().date()

    # Get spend from cycle start to today
    spend_to_date = get_account_spend_for_period(
        client,
        customer_id,
        cycle_start.isoformat(),
        today.isoformat()
    )

    monthly_budget = config["monthly_budget"]
    budget_remaining = monthly_budget - spend_to_date
    percent_used = spend_to_date / monthly_budget if monthly_budget > 0 else 0

    # Calculate days elapsed in cycle
    days_elapsed = (today - cycle_start).days + 1

    # Daily run rate
    daily_run_rate = spend_to_date / days_elapsed if days_elapsed > 0 else 0

    # Projected total spend
    if config["cycle_days"]:
        projected_total = daily_run_rate * config["cycle_days"]
    else:
        projected_total = spend_to_date  # One-off, no projection

    # Determine status
    if config["status"] == "GOODWILL":
        status = "OVERDUE"
    elif percent_used >= THRESHOLD_PAUSE:
        status = "EXHAUSTED"
    elif percent_used >= THRESHOLD_CRITICAL:
        status = "CRITICAL"
    elif percent_used >= THRESHOLD_WARNING:
        status = "WARNING"
    else:
        status = "OK"

    return {
        "account_id": customer_id,
        "account_name": config["name"],
        "monthly_budget": monthly_budget,
        "spend_to_date": round(spend_to_date, 2),
        "budget_remaining": round(budget_remaining, 2),
        "percent_used": round(percent_used * 100, 1),
        "days_elapsed": days_elapsed,
        "days_remaining": days_remaining,
        "daily_run_rate": round(daily_run_rate, 2),
        "projected_total": round(projected_total, 2),
        "cycle_start": cycle_start.isoformat(),
        "cycle_end": cycle_end.isoformat() if isinstance(cycle_end, datetime) or hasattr(cycle_end, 'isoformat') else str(cycle_end),
        "status": status,
        "auto_pause": config["auto_pause"],
        "config_status": config["status"],
        "note": config.get("note", "")
    }


def send_alert_email(subject: str, body: str):
    """Send alert email via SMTP."""
    import os

    smtp_password = os.environ.get("SMTP_PASSWORD")
    if not smtp_password:
        print("⚠️  SMTP_PASSWORD not set - skipping email")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = ALERT_EMAIL
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, smtp_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False


def generate_alert_email(accounts: list) -> str:
    """Generate HTML email body for budget alerts."""
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
            .ok { background-color: #c8e6c9; }
            .warning { background-color: #fff9c4; }
            .critical { background-color: #ffccbc; }
            .exhausted { background-color: #ef9a9a; }
            .overdue { background-color: #ce93d8; }
        </style>
    </head>
    <body>
        <h2>Google Ads Budget Alert</h2>
        <table>
            <tr>
                <th>Account</th>
                <th>Budget</th>
                <th>Spent</th>
                <th>Remaining</th>
                <th>% Used</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
    """

    for acc in accounts:
        status_class = acc["status"].lower()
        action = ""
        if acc["status"] == "EXHAUSTED" and acc["auto_pause"]:
            action = "AUTO-PAUSED"
        elif acc["status"] == "EXHAUSTED" and not acc["auto_pause"]:
            action = "NEEDS REVIEW"
        elif acc["status"] == "OVERDUE":
            action = "⚠️ CHASE PAYMENT"
        elif acc["status"] == "CRITICAL":
            action = "MONITOR CLOSELY"

        html += f"""
            <tr class="{status_class}">
                <td>{acc['account_name']}</td>
                <td>£{acc['monthly_budget']:.2f}</td>
                <td>£{acc['spend_to_date']:.2f}</td>
                <td>£{acc['budget_remaining']:.2f}</td>
                <td>{acc['percent_used']:.1f}%</td>
                <td>{acc['status']}</td>
                <td>{action}</td>
            </tr>
        """

    html += """
        </table>
        <p><small>Generated by PhD Networks Google Ads Budget Tracker</small></p>
    </body>
    </html>
    """

    return html


def main():
    parser = argparse.ArgumentParser(description="Track Google Ads budgets")
    parser.add_argument("--dry-run", action="store_true", help="Don't pause campaigns, just report")
    args = parser.parse_args()

    print()
    print("=" * 70)
    print("GOOGLE ADS BUDGET TRACKER")
    print(f"Timestamp: {datetime.now().isoformat()}")
    if args.dry_run:
        print("MODE: DRY RUN (no changes will be made)")
    print("=" * 70)
    print()

    # Ensure logs directory exists
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Load budget config
    budgets = load_budgets()
    print(f"📋 Loaded {len(budgets)} account configurations")
    print()

    # Initialize API client
    client = get_client()

    # Track each account
    results = []
    alerts_needed = []
    pauses_needed = []

    for customer_id, config in budgets.items():
        print(f"📊 Tracking: {config['name']} ({customer_id})")

        try:
            status = track_account(client, customer_id, config)
            results.append(status)

            # Print status
            icon = {
                "OK": "✅",
                "WARNING": "⚠️",
                "CRITICAL": "🔶",
                "EXHAUSTED": "🛑",
                "OVERDUE": "💸"
            }.get(status["status"], "❓")

            print(f"   {icon} {status['status']}: £{status['spend_to_date']:.2f} / £{status['monthly_budget']:.2f} ({status['percent_used']:.1f}%)")

            if status["note"]:
                print(f"   📝 {status['note']}")

            # Check if alerts/pauses needed
            if status["status"] in ["CRITICAL", "EXHAUSTED", "OVERDUE"]:
                alerts_needed.append(status)

            if status["status"] == "EXHAUSTED" and status["auto_pause"]:
                pauses_needed.append(status)

        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                "account_id": customer_id,
                "account_name": config["name"],
                "status": "ERROR",
                "error": str(e)
            })

        print()

    # Handle auto-pauses
    if pauses_needed and not args.dry_run:
        print("=" * 70)
        print("AUTO-PAUSE ACTIONS")
        print("=" * 70)

        for acc in pauses_needed:
            print(f"🛑 Pausing all campaigns for {acc['account_name']}...")
            pause_results = pause_all_campaigns(client, acc["account_id"])

            for r in pause_results:
                if r["success"]:
                    print(f"   ✅ Paused: {r.get('campaign_name', r['campaign_id'])}")
                else:
                    print(f"   ❌ Failed: {r.get('error', 'Unknown error')}")

            # Update config status
            budgets[acc["account_id"]]["status"] = "PAUSED"

        # Save updated config
        save_budgets(budgets)
        print()

    # Send alerts
    if alerts_needed:
        print("=" * 70)
        print("SENDING ALERTS")
        print("=" * 70)

        subject = f"🚨 Google Ads Budget Alert - {len(alerts_needed)} account(s) need attention"
        body = generate_alert_email(alerts_needed)

        if args.dry_run:
            print("   [DRY RUN] Would send email alert")
        else:
            if send_alert_email(subject, body):
                print("   ✅ Alert email sent")
            else:
                print("   ⚠️  Email not sent (check SMTP config)")
        print()

    # Save log file
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "dry_run": args.dry_run,
        "accounts": results,
        "alerts_sent": len(alerts_needed) > 0,
        "pauses_executed": len(pauses_needed) if not args.dry_run else 0
    }

    log_file = LOGS_DIR / f"budget_{datetime.now().strftime('%Y%m%d')}.json"
    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=2)

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    ok_count = len([r for r in results if r.get("status") == "OK"])
    warning_count = len([r for r in results if r.get("status") == "WARNING"])
    critical_count = len([r for r in results if r.get("status") == "CRITICAL"])
    exhausted_count = len([r for r in results if r.get("status") == "EXHAUSTED"])
    overdue_count = len([r for r in results if r.get("status") == "OVERDUE"])

    print(f"OK: {ok_count}")
    print(f"Warning (80%+): {warning_count}")
    print(f"Critical (95%+): {critical_count}")
    print(f"Exhausted (100%): {exhausted_count}")
    print(f"Overdue (GOODWILL): {overdue_count}")
    print()
    print(f"📁 Log saved: {log_file}")
    print()

    return log_data


if __name__ == "__main__":
    main()
