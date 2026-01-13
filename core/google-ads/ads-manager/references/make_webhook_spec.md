# Make.com Webhook Integration Specification

## Overview

This document describes the webhook payload format sent by the Google Ads monitoring system to Make.com for automation workflows.

## Webhook URL Setup

1. In Make.com, create a new scenario
2. Add a "Webhooks" module → "Custom webhook"
3. Copy the generated webhook URL
4. Add the URL to `run_daily_monitor.sh` or call directly:
   ```bash
   python3 alert_system.py --webhook-url "https://hook.eu2.make.com/YOUR_ID"
   ```

## Payload Structure

```json
{
  "timestamp": "2026-01-13T08:00:00.000000",
  "summary": {
    "total_accounts": 3,
    "total_spend": 45.67,
    "total_conversions": 2,
    "high_priority_issues": 1,
    "medium_priority_issues": 3
  },
  "issues": [
    {
      "severity": "high",
      "type": "wasted_keyword_spend",
      "message": "Keyword 'example keyword' spent £25.00 with 0 conversions (1 day)",
      "keyword": "example keyword",
      "spend": 25.00,
      "account_name": "JLR Smith Roofing – Leeds",
      "account_id": "5481658097"
    }
  ],
  "requires_action": true,
  "accounts": {
    "5481658097": {
      "name": "JLR Smith Roofing – Leeds",
      "spend": 20.50,
      "conversions": 0,
      "issue_count": 2
    },
    "6109184488": {
      "name": "Leeds Rendering",
      "spend": 15.00,
      "conversions": 0,
      "issue_count": 1
    },
    "1176290317": {
      "name": "Ossett Dental Care",
      "spend": 10.17,
      "conversions": 2,
      "issue_count": 0
    }
  }
}
```

## Field Descriptions

### Summary Object

| Field | Type | Description |
|-------|------|-------------|
| `total_accounts` | int | Number of accounts monitored |
| `total_spend` | float | Total spend across all accounts (GBP, 1 day) |
| `total_conversions` | float | Total conversions across all accounts |
| `high_priority_issues` | int | Count of high priority issues |
| `medium_priority_issues` | int | Count of medium priority issues |

### Issues Array

Each issue object contains:

| Field | Type | Description |
|-------|------|-------------|
| `severity` | string | `"high"` or `"medium"` |
| `type` | string | Issue type (see below) |
| `message` | string | Human-readable description |
| `account_name` | string | Account display name |
| `account_id` | string | Google Ads customer ID |
| *varies* | *varies* | Additional fields specific to issue type |

### Issue Types

| Type | Severity | Additional Fields |
|------|----------|-------------------|
| `wasted_campaign_spend` | high | `campaign`, `spend` |
| `wasted_keyword_spend` | high | `keyword`, `spend` |
| `low_ctr` | medium | `campaign`, `ctr` |
| `low_quality_score` | medium | `keyword`, `quality_score` |
| `high_cpc` | medium | `keyword`, `cpc` |
| `spend_spike` | medium | `previous`, `current`, `pct_change` |
| `api_error` | high | - |

### Accounts Object

Each account entry contains:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Account display name |
| `spend` | float | Account spend (GBP, 1 day) |
| `conversions` | float | Account conversions |
| `issue_count` | int | Number of issues for this account |

## Example Make.com Scenarios

### 1. Slack Notification

```
Webhook → Router → Slack (Send a Message)

Router condition: summary.high_priority_issues > 0
Message: "🚨 Google Ads Alert: {{summary.high_priority_issues}} high priority issues detected"
```

### 2. Google Sheets Log

```
Webhook → Google Sheets (Add a Row)

Columns:
- timestamp
- total_spend
- total_conversions
- high_priority_issues
- medium_priority_issues
```

### 3. Email Alert (via Make.com)

```
Webhook → Router → Email (Send an Email)

Router condition: requires_action = true
Subject: "Google Ads Alert - Action Required"
Body: Use Iterator to list all issues
```

### 4. Conditional Pause Request

```
Webhook → Router → HTTP (Make a request)

Router condition: issues[].type contains "wasted_keyword_spend"
HTTP: POST to your internal API to flag keywords for review
```

## Testing

To test the webhook integration:

1. Run the monitor manually:
   ```bash
   python3 scheduled_monitor.py --output-dir ./data
   ```

2. Send a test payload:
   ```bash
   python3 alert_system.py --webhook-url "YOUR_URL" --output-dir ./data
   ```

3. Check Make.com scenario history for received data

## Error Handling

The webhook payload will always include `requires_action` boolean:
- `true`: At least one high priority issue exists
- `false`: No high priority issues (may have medium priority)

Use this for conditional routing in Make.com scenarios.

## Rate Limits

- Default: 1 webhook per day (8am daily run)
- Make.com free tier: 1,000 operations/month (sufficient for daily monitoring)

## Security

- Use HTTPS webhook URLs only
- Consider adding a secret token header for verification
- Do not expose sensitive account credentials in webhook payloads
