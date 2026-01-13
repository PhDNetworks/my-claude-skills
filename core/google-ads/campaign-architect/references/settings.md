# Campaign Settings Reference

## Location Targeting

### Leeds & West Yorkshire Setup

**Option 1: Radius Targeting**
```
Centre: Leeds City Centre (LS1)
Radius: 15-20 miles
Covers: Leeds, Bradford, Wakefield, Pudsey, Morley, Horsforth, Wetherby, Otley
```

**Option 2: Location List**
```
Target these areas:
- Leeds (city)
- Bradford (city)
- Wakefield (city)
- Kirklees (Huddersfield area)
- Calderdale (Halifax area)

Or more granular:
- LS postcodes (all)
- BD1-BD18 (Bradford central)
- WF1-WF17 (Wakefield)
```

**Option 3: Postcode Targeting**
```
LS1-LS29 (Leeds)
BD1-BD23 (Bradford)
WF1-WF17 (Wakefield)
HD1-HD9 (Huddersfield)
HX1-HX7 (Halifax)
```

### Location Options Setting
**Always set to: "Presence: People in or regularly in your targeted locations"**

Do NOT use "Presence or Interest" - this shows ads to people searching ABOUT Leeds from anywhere (tourists, researchers, etc.)

### Location Exclusions
Consider excluding:
- Industrial estates (if residential only)
- Airports (transient traffic)
- Universities (if not relevant)

---

## Bidding Strategies

### New Campaigns (No Conversion Data)

**Maximise Clicks**
- Use for first 2-4 weeks
- Set a max CPC limit (e.g., £3-5 for local services)
- Gather data on what converts

**Manual CPC**
- Full control but time-intensive
- Good for small, focused campaigns
- Start with estimated CPCs below

### Estimated CPCs by Industry (Leeds/West Yorkshire)

| Industry | Avg CPC | High-Intent Keywords |
|----------|---------|---------------------|
| Electrician | £2-4 | Emergency: £5-8 |
| Roofer | £3-6 | Emergency: £8-12 |
| Plasterer/Renderer | £1.50-3 | Low competition |
| Flooring | £1-2.50 | Lower than trades |
| Gas Engineer | £3-5 | Boiler install: £6-10 |
| Windows/Doors | £4-8 | High competition |
| Solar | £5-10 | Growing competition |
| Dental | £3-7 | Implants: £10-15 |
| Recruitment | £2-5 | Varies by sector |

*These are estimates - actual CPCs vary by competition, quality score, and seasonality*

### After 30+ Conversions

**Maximise Conversions**
- Let Google optimise for conversions
- No target CPA initially
- Monitor cost per conversion

**Target CPA**
- Set target based on acceptable cost per lead
- Typical local service CPA: £15-50
- Emergency services can justify higher CPA

**Target ROAS**
- Only if you have revenue values
- Requires value tracking per conversion

### Bid Adjustments

**Device**
```
Mobile: +10-20% (most local searches)
Desktop: 0%
Tablet: -10% (usually lower intent)
```

**Schedule (if data supports)**
```
Business hours: +10%
Evenings: -20% (unless emergency service)
Weekends: Depends on business
```

**Audience (observation mode)**
```
Previous visitors: +20-30%
Similar audiences: +10%
In-market audiences: +10-15%
```

---

## Budget Guidelines

### Monthly Budget to Daily Budget
```
Monthly ÷ 30.4 = Daily budget
£500/month = £16.45/day
£1000/month = £32.89/day
£2000/month = £65.79/day
```

### Minimum Viable Budgets by Industry

| Industry | Min Monthly | Recommended |
|----------|-------------|-------------|
| Electrician | £300 | £500-800 |
| Roofer | £400 | £600-1000 |
| Plasterer | £200 | £300-500 |
| Flooring | £250 | £400-600 |
| Gas Engineer | £350 | £500-800 |
| Windows | £500 | £800-1500 |
| Solar | £500 | £800-1200 |
| Dental | £500 | £1000-2000 |

*Below minimum = not enough data to optimise*

### Budget Allocation (Multi-Campaign)
```
Emergency/High-Intent: 40%
Core Services: 40%
Brand/Awareness: 20%
```

### Seasonal Considerations

**Increase Budget:**
- Roofers: Autumn (storm season), Spring
- Gas Engineers: September-November (pre-winter)
- Solar: Spring/Summer
- Windows: Spring, Autumn

**Decrease Budget:**
- Most trades: Christmas-New Year (low search)
- Outdoor trades: Mid-winter

---

## Ad Scheduling

### Standard Trade Business
```
Monday-Friday: 7am - 8pm
Saturday: 8am - 4pm
Sunday: Off or reduced
```

### Emergency Services (24/7)
```
All days: All hours
But consider higher bids during:
- Weekday evenings (6pm-10pm)
- Weekend mornings (emergencies discovered)
```

### Retail/Showroom
```
Monday-Friday: 9am - 6pm
Saturday: 9am - 5pm
Sunday: 10am - 4pm (if open)
```

### B2B/Commercial
```
Monday-Friday: 8am - 6pm
Saturday-Sunday: Off or reduced
```

---

## Audience Settings

### Observation Mode Audiences
Add these for data gathering (don't restrict targeting):

**In-Market Audiences:**
- Home Improvement
- Home Services
- [Industry-specific segments]

**Affinity Audiences:**
- Homeowners
- DIY Enthusiasts (may convert or may be negative)

**Custom Audiences:**
- Competitor websites
- Industry publications
- Related search terms

### Remarketing Audiences
Set up in Google Analytics / Google Ads:
- All website visitors (30, 90, 180 days)
- Specific page visitors (service pages)
- Converters (for exclusion or similar)

---

## Conversion Tracking Setup

### Essential Conversions
```
1. Phone Calls (from ads)
   - Call extension clicks
   - Website call button clicks
   - Call duration threshold: 60+ seconds

2. Form Submissions
   - Contact form completions
   - Quote request forms
   - Callback requests

3. Email Clicks (if applicable)
   - mailto: link clicks
```

### Conversion Values
Set relative values if not tracking revenue:
```
Phone Call: £50 (highest intent)
Form Submission: £30
Email Click: £10
```

### Google Analytics 4 Integration
- Link GA4 to Google Ads
- Import GA4 conversions
- Use for cross-device tracking

---

## Campaign Settings Checklist

### Before Launch
- [ ] Location targeting set to "Presence only"
- [ ] Negative keywords added (campaign + ad group level)
- [ ] Ad schedule matches business hours
- [ ] Daily budget set correctly
- [ ] Bidding strategy appropriate for data level
- [ ] Conversion tracking verified working
- [ ] Extensions all approved
- [ ] Final URLs all working
- [ ] Phone number correct in call extension

### Weekly Checks
- [ ] Search terms reviewed
- [ ] New negatives added
- [ ] Budget pacing on track
- [ ] CPC within targets
- [ ] Quality scores checked
- [ ] Ad performance reviewed

### Monthly Checks
- [ ] Conversion performance analysis
- [ ] Bid strategy evaluation
- [ ] Budget reallocation
- [ ] New keyword opportunities
- [ ] Competitor review
- [ ] Landing page performance
