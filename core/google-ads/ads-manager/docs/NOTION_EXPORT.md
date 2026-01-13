# Google Ads API Automation System

## System Overview

Google Ads API automation system for PhD Networks & Systems Ltd.

**Purpose:** Automated performance analysis, issue detection, and keyword management for Google Ads client accounts.

**Scope:**
- Manages 3 client accounts under MCC 490-663-7401
- Daily performance monitoring and reporting
- Automated issue detection with actionable recommendations
- Keyword pausing for wasted spend elimination
- Match type optimization

### Architecture

```
                    +------------------------+
                    |    MCC Account         |
                    |    490-663-7401        |
                    |    (PhD Networks)      |
                    +------------------------+
                              |
          +-------------------+-------------------+
          |                   |                   |
+---------v--------+ +--------v---------+ +------v-----------+
| JLR Smith        | | Leeds Rendering  | | Ossett Dental    |
| Roofing          | |                  | | Care             |
| 5481658097       | | 6109184488       | | 1176290317       |
+---------+--------+ +--------+---------+ +------+-----------+
          |                   |                   |
          +-------------------+-------------------+
                              |
                    +---------v---------+
                    |     Scripts       |
                    | analyze_performance|
                    | get_urgent_issues |
                    | execute_fixes     |
                    +-------------------+
                              |
          +-------------------+-------------------+
          |                   |                   |
    +-----v-----+       +-----v-----+       +----v-----+
    | Reports   |       | Alerts    |       | Rollback |
    | (Markdown)|       | (Email/   |       | (JSON)   |
    |           |       | Webhook)  |       |          |
    +-----------+       +-----------+       +----------+
```

---

## Credentials

| Credential | Value |
|------------|-------|
| Developer Token | `QEbSx8y0DWbQPKeR635KDg` |
| Client ID | `1093467682273-mbbq6mpeoegnnehnisahv3mcouqgoemg.apps.googleusercontent.com` |
| Client Secret | [STORED IN CODE] |
| Refresh Token | [STORED SECURELY] |
| MCC ID | `4906637401` |

**Environment Variables (Optional):**
```
GOOGLE_ADS_DEVELOPER_TOKEN
GOOGLE_ADS_CLIENT_ID
GOOGLE_ADS_CLIENT_SECRET
GOOGLE_ADS_REFRESH_TOKEN
GOOGLE_ADS_LOGIN_CUSTOMER_ID
```

---

## Client Accounts

| Account | ID | Status |
|---------|-----|--------|
| JLR Smith Roofing - Leeds | 5481658097 | Active |
| Leeds Rendering | 6109184488 | Active |
| Ossett Dental Care | 1176290317 | Active |

---

## Scripts Reference

### google_ads_client.py
**Purpose:** Core API client - handles authentication and basic API operations

**Key Functions:**
- `get_client()` - Initialize Google Ads API client
- `get_accessible_accounts()` - List all ENABLED client accounts under MCC
- `get_account_details()` - Get basic account info (currency, timezone)
- `get_campaign_performance()` - Fetch campaign metrics for N days
- `get_keyword_performance()` - Fetch keyword metrics and quality scores
- `get_search_terms_report()` - Identify new keyword opportunities

**Usage:**
```python
from google_ads_client import get_client, get_campaign_performance

client = get_client()
campaigns = get_campaign_performance(client, "5481658097", days=30)
```

---

### analyze_performance.py
**Purpose:** Performance analysis - pulls data from all client accounts and generates analysis/recommendations

**Features:**
- Analyzes campaign and keyword performance
- Identifies issues by severity (high/medium)
- Generates markdown or JSON reports
- Calculates account totals and trends

**Usage:**
```bash
python3 analyze_performance.py --days 30 --output markdown
python3 analyze_performance.py --account 5481658097 --output json
```

**Arguments:**
- `--days` - Days of data to analyze (default: 30)
- `--output` - Output format: markdown or json
- `--account` - Single account ID to analyze
- `--config` - Path to config file

---

### get_urgent_issues.py
**Purpose:** Issue detection - identifies keywords and search terms needing immediate attention

**Detection Criteria:**
- High spend with zero conversions
- Low quality scores (< 5)
- Irrelevant search terms
- Missing conversion tracking

**Usage:**
```bash
python3 get_urgent_issues.py
```

**Output:** Read-only report with action plan including:
- Recommended pauses
- Bid reduction suggestions
- Negative keyword candidates

---

### execute_urgent_fixes.py
**Purpose:** Keyword pausing - pauses high-spend, zero-conversion keywords

**Features:**
- Fetches current keyword details and resource names
- Executes pause operations via mutate API
- Verifies changes after execution
- Creates rollback file for recovery
- Generates execution summary with savings estimate

**Usage:**
```bash
python3 execute_urgent_fixes.py
```

**Output:**
- Execution summary with success/fail/skipped counts
- Estimated monthly savings
- Rollback JSON file

---

### fix_rendering_keyword.py
**Purpose:** Match type changes - specifically handles match type optimization

**Current Target:** Leeds Rendering "rendering near me" keyword
- Changes BROAD match to PHRASE match
- Creates new PHRASE match keyword
- Keeps old BROAD match PAUSED
- Verifies creation

**Usage:**
```bash
python3 fix_rendering_keyword.py
```

---

### generate_refresh_token.py
**Purpose:** OAuth token generation - generates the refresh token needed for API authentication

**Process:**
1. Opens browser for Google OAuth authorization
2. Starts local server on port 8080 to receive callback
3. Exchanges authorization code for tokens
4. Outputs refresh token and config format
5. Saves config to `google-ads-config.json`

**Usage:**
```bash
python3 generate_refresh_token.py
```

---

## Analysis Rules

### High Priority Issues

| Condition | Threshold | Recommendation |
|-----------|-----------|----------------|
| Campaign wasted spend | Spend > 50 GBP with 0 conversions | Review conversion tracking, pause underperforming keywords |
| Keyword wasted spend | Spend > 20 GBP with 0 conversions | Consider pausing or adding as negative keyword |
| No impressions | ENABLED campaign with 0 impressions | Check targeting, bids, and budget |

### Medium Priority Issues

| Condition | Threshold | Recommendation |
|-----------|-----------|----------------|
| Low CTR | CTR < 1% with > 100 impressions | Review ad copy and keyword relevance |
| Low Quality Score | Quality Score < 5 | Improve ad relevance, landing page, expected CTR |
| High CPC | Avg CPC > 5 GBP with > 10 clicks | Review bid strategy, consider adding negative keywords |

---

## Actions Log

### 2026-01-13

**Paused 5 keywords saving approximately 318.96 GBP/month:**

**JLR Smith Roofing - Leeds (5481658097):**
| Keyword | Match Type | Ad Group | Campaign |
|---------|------------|----------|----------|
| roof repair leeds | PHRASE | Roof Repairs Leeds | JLR - Roof Repairs Leeds - Search |
| fascias soffits guttering leeds | PHRASE | Roof Repairs Leeds | JLR - Roof Repairs Leeds - Search |
| roofing company leeds | EXACT | Roof Repairs Leeds | JLR - Roof Repairs Leeds - Search |
| chimney repair leeds | PHRASE | Roof Repairs Leeds | JLR - Roof Repairs Leeds - Search |

**Leeds Rendering (6109184488):**
| Keyword | Match Type | Ad Group | Campaign |
|---------|------------|----------|----------|
| rendering near me | BROAD | Full House Rendering - Leeds | Leeds Rendering - Search - Nov-Dec 2025 |

**Additional Actions:**
- Created "rendering near me" as PHRASE match for Leeds Rendering (to replace paused BROAD match)

**Budget Management Actions:**
- Updated Leeds Rendering daily budget to £8.00 (£250/month ÷ 31 days)
- Created `config/client_budgets.json` with all 3 client budget configurations
- JLR Smith set to GOODWILL status (payment overdue, £290/£250 spent)
- Ossett Dental set as one-off budget (no cycle reset)

---

## Automation Setup

### launchd (macOS)

Daily execution at 8am via launchd plist:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.phdnetworks.google-ads-analyzer</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/scripts/analyze_performance.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>/path/to/scripts</string>
</dict>
</plist>
```

### Make.com Integration

Webhook integration for automated alerts:
- Trigger: Daily schedule or on-demand
- Action: Run analysis script
- Output: Send results to webhook endpoint
- Alert destination: daniel.doherty@phdnetworks.co.uk

---

## Budget Management

### Client Budget Configuration

Budget settings are stored in `config/client_budgets.json`:

```json
{
  "6109184488": {
    "name": "Leeds Rendering",
    "monthly_budget": 250,
    "currency": "GBP",
    "cycle_start": "2026-01-08",
    "cycle_days": 31,
    "auto_pause": true,
    "status": "ACTIVE"
  }
}
```

**Status Values:**
| Status | Meaning |
|--------|---------|
| `ACTIVE` | Normal operation, auto-pause enabled |
| `GOODWILL` | Payment overdue, tracking only (no auto-pause) |
| `PAUSED` | Campaigns paused due to budget exhaustion |

### Budget Tracker

Run daily budget tracking:

```bash
python3 budget_tracker.py           # Normal run (may auto-pause)
python3 budget_tracker.py --dry-run # Report only, no changes
```

**Alert Thresholds:**
| Threshold | Action |
|-----------|--------|
| 80% | Warning logged |
| 95% | Email alert sent |
| 100% | Auto-pause campaigns (if enabled) |

**GOODWILL Mode:**
When `auto_pause: false` and `status: GOODWILL`:
- Tracks spend but does NOT pause campaigns
- Flags account as "⚠️ OVERDUE" in reports
- Use when client payment is pending

### Update Billing Cycle

When payment is received:

```bash
python3 update_billing_cycle.py \
  --account 6109184488 \
  --payment-date 2026-01-08 \
  --amount 250 \
  --enable-campaigns
```

**Arguments:**
- `--account` - Account ID to update
- `--payment-date` - Payment date (YYYY-MM-DD)
- `--amount` - Payment amount in GBP
- `--cycle-days` - Cycle length (default: 31)
- `--enable-campaigns` - Re-enable paused campaigns
- `--dry-run` - Preview changes only

### Google Ads Script (Hourly Monitoring)

For more responsive monitoring, install `google_ads_scripts/budget_monitor.js` in Google Ads:

1. Go to Tools & Settings > Bulk Actions > Scripts
2. Create new script and paste `budget_monitor.js`
3. Update CONFIG section with account details
4. Set frequency to "Hourly"

**Features:**
- Runs every hour (vs daily Python check)
- Email alerts at 95%
- Auto-pause at 100%
- Sends notification emails

### Budget API Functions

New functions added to `google_ads_client.py`:

| Function | Purpose |
|----------|---------|
| `get_campaign_budgets(client, customer_id)` | Get all campaign budgets |
| `update_campaign_budget(client, customer_id, resource_name, amount_micros)` | Update a budget |
| `pause_campaign(client, customer_id, campaign_id)` | Pause single campaign |
| `enable_campaign(client, customer_id, campaign_id)` | Enable single campaign |
| `pause_all_campaigns(client, customer_id)` | Pause all ENABLED campaigns |
| `enable_all_campaigns(client, customer_id)` | Enable all PAUSED campaigns |
| `get_account_spend_for_period(client, customer_id, start, end)` | Get spend for date range |

**Example: Update budget to £8/day:**
```python
from google_ads_client import get_client, get_campaign_budgets, update_campaign_budget

client = get_client()
budgets = get_campaign_budgets(client, "6109184488")

for b in budgets:
    update_campaign_budget(
        client,
        "6109184488",
        b["resource_name"],
        8_000_000  # £8.00 in micros
    )
```

---

## Rollback Procedures

### Rollback File Location
Rollback files are stored in the `scripts/` directory with naming convention:
```
rollback_YYYYMMDD.json
```

### Rollback File Structure
```json
{
  "timestamp": "2026-01-13T20:11:43.477512",
  "description": "Rollback data for urgent keyword pauses",
  "changes": [
    {
      "account_id": "5481658097",
      "account_name": "JLR Smith Roofing - Leeds",
      "resource_name": "customers/5481658097/adGroupCriteria/188059510997~326119294485",
      "keyword_text": "roof repair leeds",
      "match_type": "PHRASE",
      "previous_status": "ENABLED",
      "ad_group": "Roof Repairs Leeds",
      "campaign": "JLR - Roof Repairs Leeds - Search"
    }
  ]
}
```

### Rollback Script (Manual)

To re-enable paused keywords, use the resource names from the rollback JSON:

```python
from google_ads_client import get_client
from google.ads.googleads.errors import GoogleAdsException
from google.protobuf import field_mask_pb2

def enable_keyword(client, customer_id: str, resource_name: str) -> bool:
    """Re-enable a paused keyword."""
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operation = client.get_type("AdGroupCriterionOperation")
    criterion = operation.update
    criterion.resource_name = resource_name
    criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED

    operation.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["status"]))

    try:
        response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id,
            operations=[operation]
        )
        return True
    except GoogleAdsException as ex:
        print(f"Error: {ex}")
        return False

# Usage
client = get_client()
enable_keyword(client, "5481658097", "customers/5481658097/adGroupCriteria/188059510997~326119294485")
```

---

## Troubleshooting

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `CUSTOMER_NOT_ENABLED` | Account is deactivated or suspended | Verify account status in Google Ads UI |
| `AuthenticationError` | Invalid or expired tokens | Regenerate refresh token using `generate_refresh_token.py` |
| `RATE_LIMIT_EXCEEDED` | Too many API requests | Add delays between API calls |
| `INVALID_CUSTOMER_ID` | Wrong customer ID format | Use ID without dashes (e.g., 5481658097 not 548-165-8097) |
| `PERMISSION_DENIED` | MCC doesn't have access | Verify account is linked under MCC 490-663-7401 |

### Token Regeneration Steps

1. Run the token generator:
   ```bash
   python3 generate_refresh_token.py
   ```

2. Sign in with the Google account that has MCC access

3. Grant the requested permissions

4. Copy the refresh token from output

5. Update in `google_ads_client.py` or environment variable

### Debugging API Queries

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Test connection:
```python
from google_ads_client import get_client, get_accessible_accounts

client = get_client()
accounts = get_accessible_accounts(client)
print(accounts)
```

---

## Contact

**Owner:** Danny Doherty
**Company:** PhD Networks & Systems Ltd
**Location:** Leeds, UK
**Email:** daniel.doherty@phdnetworks.co.uk
