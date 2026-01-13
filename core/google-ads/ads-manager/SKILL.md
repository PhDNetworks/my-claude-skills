---
name: google-ads-manager
description: Google Ads API integration for PhD Networks client campaign management. Use when analyzing Google Ads performance, pulling campaign/keyword metrics, identifying optimization opportunities, generating reports, or making bid/budget adjustments across client accounts (JLR Smith Roofing, Leeds Rendering, Ossett Dental Care). Triggers on requests involving Google Ads data, PPC analysis, campaign optimization, or ad performance reporting.
---

# Google Ads Manager

Manage and optimize Google Ads campaigns for PhD Networks client accounts via the Google Ads API.

## Credentials

```yaml
developer_token: QEbSx8y0DWbQPKeR635KDg
client_id: 1093467682273-mbbq6mpeoegnnehnisahv3mcouqgoemg.apps.googleusercontent.com
client_secret: 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
login_customer_id: 4906637401
refresh_token: <GENERATE USING scripts/generate_refresh_token.py>
```

## Client Accounts

| Account | Customer ID | Status |
|---------|-------------|--------|
| JLR Smith Roofing - Leeds | 548-165-8097 | Active |
| Leeds Rendering | 610-918-4488 | Active |
| Ossett Dental Care | 117-629-0317 | Active |

## Quick Start

### 1. Install Dependencies

```bash
pip install google-ads requests
```

### 2. Generate Refresh Token (One-time)

```bash
cd scripts/
python3 generate_refresh_token.py
```

This opens a browser for OAuth authentication. Save the refresh token securely.

### 3. Run Analysis

```bash
python3 analyze_performance.py --days 30 --output markdown
```

## Available Scripts

### `google_ads_client.py`
Core API client with functions:
- `get_client()` - Initialize authenticated client
- `get_campaign_performance()` - Fetch campaign metrics
- `get_keyword_performance()` - Fetch keyword metrics  
- `get_search_terms_report()` - Fetch search query data

### `analyze_performance.py`
Automated analysis that:
- Pulls data from all client accounts
- Identifies issues (wasted spend, low CTR, low quality scores)
- Generates markdown or JSON reports
- Flags high/medium priority actions

### `generate_refresh_token.py`
OAuth flow to generate the refresh token needed for API access.

### `send_alerts.py`
Email notification system for high-priority issues.

## Analysis Rules

The analyzer flags these issues:

**High Priority (🔴)**
- Enabled campaigns with 0 impressions
- Spend > £50 with 0 conversions
- Keywords spending > £20 with 0 conversions

**Medium Priority (🟡)**
- CTR below 1%
- Average CPC above £5
- Quality Score below 5/10

## API Query Examples

### Get Campaign Performance
```python
from google_ads_client import get_client, get_campaign_performance

client = get_client()
campaigns = get_campaign_performance(client, "5481658097", days=30)
for c in campaigns:
    print(f"{c['name']}: £{c['cost']:.2f} spend, {c['conversions']} conversions")
```

### Get Keyword Data
```python
from google_ads_client import get_client, get_keyword_performance

client = get_client()
keywords = get_keyword_performance(client, "5481658097", days=30)
for kw in keywords:
    print(f"{kw['keyword']}: QS={kw['quality_score']}, CTR={kw['ctr']:.2f}%")
```

## Automation Options

### Option 1: Cron Job (Linux/Mac)
```bash
# Run daily at 8am
0 8 * * * cd /path/to/skills/google-ads-manager/scripts && python3 analyze_performance.py --output markdown >> /var/log/google-ads.log 2>&1
```

### Option 2: Make.com Webhook
Create a Make.com scenario that:
1. Triggers on schedule (daily/hourly)
2. Calls a webhook endpoint
3. Receives JSON analysis
4. Sends email/Slack notification

### Option 3: Claude Code Scheduled Task
Run analysis directly in Claude conversations when needed.

## Optimization Actions

The API supports these modifications (use with caution):

**Safe Actions (auto-executable)**
- Pause keywords with >£50 spend and 0 conversions
- Add obvious negative keywords
- Adjust bids within 20% of current

**Requires Approval**
- Budget changes
- Pausing campaigns
- Bid changes >20%
- Adding new keywords

## Troubleshooting

**"Invalid refresh token"**
- Re-run `generate_refresh_token.py` to get a new token

**"Quota exceeded"**
- Explorer access allows 15,000 operations/day
- Reduce query frequency or apply for Basic access

**"Customer not accessible"**
- Ensure account is linked to MCC 490-663-7401
- Check customer ID format (no dashes in API calls)
