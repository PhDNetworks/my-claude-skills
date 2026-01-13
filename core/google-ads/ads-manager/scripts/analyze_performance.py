#!/usr/bin/env python3
"""
Google Ads Performance Analyzer

Pulls data from all client accounts and generates analysis/recommendations.
Can be run manually or scheduled via cron/Make.com.

Usage:
    python3 analyze_performance.py [--days 30] [--output json|markdown]
"""

import json
import argparse
from datetime import datetime
from typing import Optional
from google_ads_client import (
    get_client,
    get_accessible_accounts,
    get_account_details,
    get_campaign_performance,
    get_keyword_performance,
    get_search_terms_report
)


# Client accounts under PhD Networks MCC (490-663-7401)
# Only ENABLED client accounts (excludes MCC and draft/test accounts)
CLIENT_ACCOUNTS = {
    "5481658097": "JLR Smith Roofing – Leeds",
    "6109184488": "Leeds Rendering",
    "1176290317": "Ossett Dental Care"
}


def analyze_campaign(campaign: dict) -> list:
    """Analyze a single campaign and return issues/recommendations."""
    issues = []
    
    # No impressions
    if campaign['impressions'] == 0 and campaign['status'] == 'ENABLED':
        issues.append({
            "severity": "high",
            "type": "no_impressions",
            "message": f"Campaign '{campaign['name']}' is enabled but has 0 impressions",
            "recommendation": "Check targeting, bids, and budget"
        })
    
    # Low CTR
    if campaign['impressions'] > 100 and campaign['ctr'] < 1.0:
        issues.append({
            "severity": "medium",
            "type": "low_ctr",
            "message": f"Campaign '{campaign['name']}' has low CTR ({campaign['ctr']:.2f}%)",
            "recommendation": "Review ad copy and keyword relevance"
        })
    
    # High cost, no conversions
    if campaign['cost'] > 50 and campaign['conversions'] == 0:
        issues.append({
            "severity": "high",
            "type": "wasted_spend",
            "message": f"Campaign '{campaign['name']}' spent £{campaign['cost']:.2f} with 0 conversions",
            "recommendation": "Review conversion tracking, pause underperforming keywords"
        })
    
    # High CPC
    if campaign['avg_cpc'] > 5.0 and campaign['clicks'] > 10:
        issues.append({
            "severity": "medium",
            "type": "high_cpc",
            "message": f"Campaign '{campaign['name']}' has high avg CPC (£{campaign['avg_cpc']:.2f})",
            "recommendation": "Review bid strategy, consider adding negative keywords"
        })
    
    return issues


def analyze_keyword(keyword: dict) -> list:
    """Analyze a single keyword and return issues/recommendations."""
    issues = []
    
    # Low quality score
    if keyword['quality_score'] and keyword['quality_score'] < 5:
        issues.append({
            "severity": "medium",
            "type": "low_quality_score",
            "message": f"Keyword '{keyword['keyword']}' has low quality score ({keyword['quality_score']}/10)",
            "recommendation": "Improve ad relevance, landing page, expected CTR"
        })
    
    # High cost, no conversions
    if keyword['cost'] > 20 and keyword['conversions'] == 0:
        issues.append({
            "severity": "high",
            "type": "wasted_keyword_spend",
            "message": f"Keyword '{keyword['keyword']}' spent £{keyword['cost']:.2f} with 0 conversions",
            "recommendation": "Consider pausing or adding as negative keyword"
        })
    
    return issues


def get_all_client_data(client, days: int = 30, account_filter: str = None) -> dict:
    """Fetch performance data for client accounts."""
    all_data = {}

    # Filter to single account if specified
    accounts = CLIENT_ACCOUNTS
    if account_filter:
        if account_filter in CLIENT_ACCOUNTS:
            accounts = {account_filter: CLIENT_ACCOUNTS[account_filter]}
        else:
            accounts = {account_filter: f"Account {account_filter}"}

    for customer_id, name in accounts.items():
        print(f"  Fetching data for {name} ({customer_id})...")
        
        try:
            account_data = {
                "name": name,
                "customer_id": customer_id,
                "campaigns": get_campaign_performance(client, customer_id, days),
                "keywords": get_keyword_performance(client, customer_id, days),
                "search_terms": get_search_terms_report(client, customer_id, days)
            }
            
            # Calculate totals
            account_data["totals"] = {
                "impressions": sum(c['impressions'] for c in account_data['campaigns']),
                "clicks": sum(c['clicks'] for c in account_data['campaigns']),
                "cost": sum(c['cost'] for c in account_data['campaigns']),
                "conversions": sum(c['conversions'] for c in account_data['campaigns'])
            }
            
            all_data[customer_id] = account_data
            
        except Exception as e:
            print(f"    Error: {e}")
            all_data[customer_id] = {"name": name, "error": str(e)}
    
    return all_data


def generate_analysis(data: dict) -> dict:
    """Generate analysis and recommendations from performance data."""
    analysis = {
        "generated_at": datetime.now().isoformat(),
        "accounts": {},
        "summary": {
            "total_accounts": 0,
            "total_spend": 0,
            "total_conversions": 0,
            "high_priority_issues": 0,
            "medium_priority_issues": 0
        }
    }
    
    for customer_id, account_data in data.items():
        if "error" in account_data:
            continue
            
        account_analysis = {
            "name": account_data["name"],
            "totals": account_data.get("totals", {}),
            "issues": [],
            "recommendations": []
        }
        
        # Analyze campaigns
        for campaign in account_data.get("campaigns", []):
            issues = analyze_campaign(campaign)
            account_analysis["issues"].extend(issues)
        
        # Analyze keywords
        for keyword in account_data.get("keywords", []):
            issues = analyze_keyword(keyword)
            account_analysis["issues"].extend(issues)
        
        # Count issues by severity
        high = len([i for i in account_analysis["issues"] if i["severity"] == "high"])
        medium = len([i for i in account_analysis["issues"] if i["severity"] == "medium"])
        
        account_analysis["issue_counts"] = {"high": high, "medium": medium}
        
        analysis["accounts"][customer_id] = account_analysis
        
        # Update summary
        analysis["summary"]["total_accounts"] += 1
        analysis["summary"]["total_spend"] += account_data.get("totals", {}).get("cost", 0)
        analysis["summary"]["total_conversions"] += account_data.get("totals", {}).get("conversions", 0)
        analysis["summary"]["high_priority_issues"] += high
        analysis["summary"]["medium_priority_issues"] += medium
    
    return analysis


def format_markdown_report(analysis: dict) -> str:
    """Format analysis as a markdown report."""
    lines = []
    
    lines.append("# Google Ads Performance Report")
    lines.append(f"\nGenerated: {analysis['generated_at']}")
    lines.append("")
    
    # Summary
    s = analysis["summary"]
    lines.append("## Summary")
    lines.append(f"- **Accounts Analyzed:** {s['total_accounts']}")
    lines.append(f"- **Total Spend:** £{s['total_spend']:.2f}")
    lines.append(f"- **Total Conversions:** {s['total_conversions']}")
    lines.append(f"- **High Priority Issues:** {s['high_priority_issues']}")
    lines.append(f"- **Medium Priority Issues:** {s['medium_priority_issues']}")
    lines.append("")
    
    # Per-account details
    for customer_id, account in analysis["accounts"].items():
        lines.append(f"## {account['name']}")
        lines.append(f"*Customer ID: {customer_id}*")
        lines.append("")
        
        totals = account.get("totals", {})
        if totals:
            lines.append("### Performance")
            lines.append(f"- Impressions: {totals.get('impressions', 0):,}")
            lines.append(f"- Clicks: {totals.get('clicks', 0):,}")
            lines.append(f"- Cost: £{totals.get('cost', 0):.2f}")
            lines.append(f"- Conversions: {totals.get('conversions', 0)}")
            lines.append("")
        
        if account["issues"]:
            lines.append("### Issues")
            for issue in account["issues"]:
                severity_emoji = "🔴" if issue["severity"] == "high" else "🟡"
                lines.append(f"- {severity_emoji} **{issue['type']}**: {issue['message']}")
                lines.append(f"  - *Recommendation:* {issue['recommendation']}")
            lines.append("")
        else:
            lines.append("### Issues")
            lines.append("✅ No issues detected")
            lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze Google Ads performance")
    parser.add_argument("--days", type=int, default=30, help="Days of data to analyze")
    parser.add_argument("--output", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--config", type=str, help="Path to config file")
    parser.add_argument("--account", type=str, help="Single account ID to analyze")
    args = parser.parse_args()
    
    print("=" * 60)
    print("Google Ads Performance Analyzer")
    print("PhD Networks & Systems Ltd")
    print("=" * 60)
    print()
    
    # Load config if provided
    config = None
    if args.config:
        with open(args.config) as f:
            config = json.load(f)
    
    print(f"Analyzing last {args.days} days of data...")
    print()
    
    # Initialize client
    try:
        client = get_client(config)
    except Exception as e:
        print(f"Error initializing client: {e}")
        print("\nMake sure you have generated a refresh token by running:")
        print("  python3 generate_refresh_token.py")
        return
    
    # Fetch all data
    print("Fetching account data...")
    data = get_all_client_data(client, args.days, args.account)
    
    # Generate analysis
    print("\nAnalyzing performance...")
    analysis = generate_analysis(data)
    
    # Output results
    print()
    if args.output == "json":
        print(json.dumps(analysis, indent=2))
    else:
        report = format_markdown_report(analysis)
        print(report)
        
        # Save to file
        filename = f"google_ads_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, "w") as f:
            f.write(report)
        print(f"\nReport saved to: {filename}")


if __name__ == "__main__":
    main()
