# Tracking System & Data Layer Architecture

## Overview
Complete tracking visibility across Google Ads, GTM, GA4, Google Sheets, Make.com automations, and landing page behaviour.

## Primary KPIs to Track
- 60+ second call conversions
- Form submissions
- Landing page engagement
- Conversion rate (CVR)
- Cost per lead (CPL)

---

## Required GA4 Events

### Primary Conversions
| Event Name | Description |
|------------|-------------|
| form_submit | Form submission completed |
| click_to_call | Click on tel: link |
| call_60s | 60-second phone call |

### Micro-Conversions
| Event Name | Description |
|------------|-------------|
| cta_click | CTA button click |
| scroll_50 | 50% scroll depth |

### Diagnostic Events
| Event Name | Description |
|------------|-------------|
| lp_view | Landing page view |
| form_start | Form field focused |
| form_abandon | Form started but not submitted |

---

## GTM Architecture

### Tags Required
1. GA4 Event Tag: form_submit
2. GA4 Event Tag: click_to_call
3. GA4 Event Tag: cta_click
4. GA4 Scroll Depth Tag: 50%
5. Google Ads Call Conversion Tag
6. Google Ads Form Conversion Tag

### Triggers Required
| Trigger Name | Type | Condition |
|--------------|------|-----------|
| Click - tel links | Click - Just Links | Click URL contains "tel:" |
| Form Submission | Form Submission | All forms OR specific form ID |
| Page View - LP | Page View | Page Path matches landing pages |
| Scroll Depth 50% | Scroll Depth | Vertical 50% |
| Timer (optional) | Timer | For time-on-page tracking |

### Variables Required
| Variable Name | Type |
|---------------|------|
| Click URL | Built-in |
| Click Text | Built-in |
| Form ID | Auto-Event Variable |
| Page Path | Built-in |

---

## GTM Tag Templates

### form_submit Tag
```json
{
  "tag_name": "[GA4] Event - form_submit",
  "tag_type": "Google Analytics: GA4 Event",
  "measurement_id": "G-XXXXXXXXXX",
  "event_name": "form_submit",
  "event_parameters": [
    {"name": "form_id", "value": "{{Form ID}}"},
    {"name": "page_path", "value": "{{Page Path}}"}
  ],
  "trigger": "Form Submission - All Forms"
}
```

### click_to_call Tag
```json
{
  "tag_name": "[GA4] Event - click_to_call",
  "tag_type": "Google Analytics: GA4 Event",
  "measurement_id": "G-XXXXXXXXXX",
  "event_name": "click_to_call",
  "event_parameters": [
    {"name": "click_url", "value": "{{Click URL}}"},
    {"name": "page_path", "value": "{{Page Path}}"}
  ],
  "trigger": "Click - tel links"
}
```

### cta_click Tag
```json
{
  "tag_name": "[GA4] Event - cta_click",
  "tag_type": "Google Analytics: GA4 Event",
  "measurement_id": "G-XXXXXXXXXX",
  "event_name": "cta_click",
  "event_parameters": [
    {"name": "click_text", "value": "{{Click Text}}"},
    {"name": "page_path", "value": "{{Page Path}}"}
  ],
  "trigger": "Click - CTA Buttons"
}
```

### scroll_50 Tag
```json
{
  "tag_name": "[GA4] Event - scroll_50",
  "tag_type": "Google Analytics: GA4 Event",
  "measurement_id": "G-XXXXXXXXXX",
  "event_name": "scroll_50",
  "event_parameters": [
    {"name": "page_path", "value": "{{Page Path}}"}
  ],
  "trigger": "Scroll Depth - 50%"
}
```

---

## Google Ads Conversion Setup

### Primary Conversions (Use for Optimisation)
1. Import GA4 event: form_submit
2. Import GA4 event: click_to_call
3. Google Ads call conversion: 60 seconds minimum

### Secondary Conversions (Observational Only)
1. cta_click
2. scroll_50

**Important:** Only mark primary conversions as "Primary" for bidding optimisation.

---

## Google Sheets Data Warehouse

### Schema
| Column | Description |
|--------|-------------|
| Date | Reporting date |
| Campaign | Campaign name |
| Ad Group | Ad group name |
| Keyword | User search term or keyword |
| Match Type | Exact / Phrase |
| Device | Mobile / Desktop |
| Impressions | Visibility |
| Clicks | Engagement |
| CTR | Click-through rate |
| CPC | Cost per click |
| Cost | Total spend |
| Conversions | Combined calls + forms |
| Calls | Phone conversions |
| Forms | Lead forms |
| CPL | Cost / conversions |
| CVR | Conversions / clicks |
| Notes | AI-generated insights |
| Flags | Performance alerts |

---

## Make.com Automation Flows

### Scenario 1: Google Ads → Sheets (Daily Pull)
```
Trigger: Daily @ 08:00
Module 1: Google Ads API - Get Report
Module 2: Iterator - Loop through rows
Module 3: Google Sheets - Append Row
Module 4: Error Handler - Retry 3x, notify on failure
```

### Scenario 2: Sheets → ChatGPT Memory (AI Sync)
```
Trigger: Watch New Rows
Module 1: Summarise performance data
Module 2: Write to ChatGPT Project Memory
Module 3: Log to Notion
Module 4: Alert if CPL > £40
```

### Scenario 3: Weekly Notion Report
```
Trigger: Friday 20:00
Module 1: Query Sheets - Last 7 days
Module 2: ChatGPT - Generate narrative report
Module 3: Notion - Update database
```

### Scenario 4: Performance Alerts
```
Conditions:
- CPL > £40
- Conversions < 3 in last 7 days
- CTR < 3%
- Call conversions = 0

Outputs:
- Slack notification
- Email alert
- Asana urgent task creation
```

---

## QA Checklist

### Pre-Launch Validation
- [ ] GTM container installed on all landing pages
- [ ] form_submit fires in DebugView on test submission
- [ ] click_to_call fires on tel: link click
- [ ] scroll_50 fires at 50% scroll
- [ ] Events appear in GA4 Realtime
- [ ] Conversions imported to Google Ads
- [ ] No duplicate event firing
- [ ] Naming conventions match spec

### Debugging Steps
1. Open GTM Preview mode
2. Navigate to landing page
3. Perform test action (submit form, click phone)
4. Check "Tags Fired" in GTM debugger
5. Verify event parameters in GA4 DebugView
6. Check for duplicate events
7. Validate attribution in Google Ads

---

## End-to-End Data Flow

```
Google Ads → Make.com → Google Sheets → Make.com → ChatGPT Memory → Make.com → Notion → Asana Tasks/Goals
```

### Feedback Loop
```
ChatGPT Project → Recommendations → Asana Optimisation Tasks → Manual Execution → Google Ads Performance → Repeat
```
