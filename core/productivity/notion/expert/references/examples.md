# Examples Reference

Concrete input/output examples for common Notion builds.

## Example 1: Freelance Client Management

**User request:** "I need a system to track my freelance clients, projects, and invoices"

**Database Schema:**

```
CLIENTS DATABASE
├── Name (title)
├── Company (text)
├── Email (email)
├── Phone (phone)
├── Status (select: Lead, Active, Inactive, Past)
├── Source (select: Referral, Website, LinkedIn, Cold)
├── Notes (text)
├── → Projects (relation)
├── Total Revenue (rollup: sum of Project.Value)
└── Project Count (rollup: count of Projects)

PROJECTS DATABASE  
├── Name (title)
├── → Client (relation)
├── Type (select: Website, SEO, Google Ads, Retainer)
├── Status (select: Proposal, Active, Complete, Cancelled)
├── Value (number, £)
├── Start Date (date)
├── Deadline (date)
├── → Tasks (relation)
├── → Invoices (relation)
├── Progress (rollup: % tasks complete)
└── Time Logged (rollup: sum from time entries)

TASKS DATABASE
├── Task (title)
├── → Project (relation)
├── Status (select: To Do, In Progress, Done)
├── Priority (select: Low, Medium, High, Urgent)
├── Due Date (date)
├── Estimated Hours (number)
├── Actual Hours (number)
└── Notes (text)

INVOICES DATABASE
├── Invoice # (title, formula: "INV-" + format(prop("ID")))
├── → Project (relation)
├── → Client (rollup from Project)
├── Amount (number, £)
├── Status (select: Draft, Sent, Paid, Overdue)
├── Date Issued (date)
├── Date Due (date)
├── Date Paid (date)
└── Days Outstanding (formula)
```

**Key Formulas:**

```
// Invoice: Days Outstanding
if(prop("Status") == "Paid", 0,
  dateBetween(now(), prop("Date Due"), "days"))

// Project: Health Status
if(prop("Progress") >= 100, "✅ Complete",
  if(empty(prop("Deadline")), "📋 No deadline",
    if(prop("Deadline") < now(), "🔴 Overdue",
      if(dateBetween(prop("Deadline"), now(), "days") < 7, 
        "🟡 Due soon", "🟢 On track"))))
```

**Views to Create:**

- Clients: Board by Status
- Projects: Board by Status, filtered to Active
- Tasks: Board by Status, grouped by Project
- Invoices: Table sorted by Date Due, filtered to unpaid
- Dashboard: Metrics + embedded filtered views

---

## Example 2: Content Calendar

**User request:** "I need a content calendar for my blog and social media"

**Database Schema:**

```
CONTENT DATABASE
├── Title (title)
├── Status (select: Idea, Outlined, Drafting, Review, Scheduled, Published)
├── Content Type (select: Blog Post, LinkedIn, Instagram, Twitter, Newsletter)
├── Publish Date (date)
├── Author (person)
├── → Campaign (relation, optional)
├── Primary Keyword (text)
├── Word Count Target (number)
├── Featured Image (files)
├── URL (url, for published)
├── AI Summary (AI property)
└── Notes (text)

CAMPAIGNS DATABASE (optional)
├── Campaign Name (title)
├── Theme (text)
├── Start Date (date)
├── End Date (date)
├── → Content (relation)
└── Content Count (rollup)
```

**Views to Create:**

1. **Calendar View:** Group by Publish Date, filtered to Scheduled/Published
2. **Kanban by Status:** Board view for workflow
3. **By Platform:** Board grouped by Content Type
4. **Ideas Backlog:** Table filtered to Status = Idea
5. **This Week:** Table filtered to Publish Date within 7 days

**Dashboard Layout:**

```
# 📅 Content Calendar

## 📊 This Week
| Posts Scheduled | Posts Published | Ideas in Queue |
|       3         |        2        |       12       |

---

## 🗓️ Calendar
[Embedded: Calendar view]

---

## 📝 Pipeline
[Embedded: Kanban by status]

---

## 💡 Quick Capture
[Embedded: Filtered to Idea status, simple table]
```

---

## Example 3: Personal Dashboard

**User request:** "I want a home base dashboard for my daily life and work"

**Database Schema:**

```
TASKS DATABASE
├── Task (title)
├── Status (checkbox)
├── Due Date (date)
├── Priority (select: Low, Medium, High, Urgent)
├── Area (select: Work, Personal, Health, Admin)
├── Project (relation → Projects, optional)
├── Energy (select: High, Medium, Low)
└── Time Estimate (select: 5min, 15min, 30min, 1hr, 2hr+)

PROJECTS DATABASE
├── Name (title)
├── Status (select: Active, On Hold, Complete, Someday)
├── Area (select: Work, Personal, Health, Admin)
├── Deadline (date)
├── → Tasks (relation)
├── Progress (rollup: % tasks complete)
└── Next Action (text)

HABITS DATABASE
├── Habit (title)
├── Frequency (select: Daily, Weekly)
├── Current Streak (number)
├── → Habit Log (relation)
└── Last Completed (rollup: max date from log)

HABIT LOG DATABASE
├── Date (date, title)
├── → Habit (relation)
└── Completed (checkbox)
```

**Dashboard Layout:**

```
# 🏠 Home Base

> Good morning! Today is [formula: current date]

---

## ⚡ Quick Actions

| ➕ New Task | 📝 Journal | 📅 Calendar |

---

## 🎯 Today's Focus

**Top 3 Priorities:**
[Embedded: Tasks filtered to Due = Today AND Priority = High/Urgent, limit 3]

**Other Tasks:**
[Embedded: Tasks filtered to Due = Today, excluding above]

---

## 📁 Active Projects

[Embedded: Projects gallery, Status = Active, limit 6]

---

## 🔥 Habits

| Habit | Streak | Today |
[Embedded: Habits table with today's status]

---

## 📅 This Week

[Embedded: Calendar or task list for next 7 days]
```

---

## Example 4: Meeting Notes System

**User request:** "I need a system for meeting notes that tracks action items"

**Database Schema:**

```
MEETINGS DATABASE
├── Title (title)
├── Date (date)
├── Type (select: 1:1, Team, Client, External)
├── Attendees (multi-select or people)
├── → Project (relation, optional)
├── → Client (relation, optional)
├── Status (select: Scheduled, Complete, Cancelled)
├── Recording Link (url)
├── AI Summary (AI property)
├── AI Action Items (AI Key Info property)
└── Notes (text, in page body)

ACTION ITEMS DATABASE
├── Action (title)
├── → Meeting (relation)
├── Owner (person)
├── Due Date (date)
├── Status (checkbox)
└── → Project (relation, optional)
```

**Meeting Template:**

```
# 📅 {{Title}}

| Date | Type | Attendees |
|------|------|-----------|

---

## 📋 Agenda

1. 
2. 
3. 

---

## 📝 Discussion Notes



---

## ✅ Action Items

[Embedded: Action Items filtered to this meeting]

---

## 🔗 Related

- Project: 
- Previous meeting: 
- Documents: 

---

## 🤖 AI Summary

[AI Summary property - auto-generates after content added]
```

**Automations:**

1. **On meeting created:** Set Date to today if empty
2. **On meeting complete:** Notify attendees of action items (via integration)

---

## Example 5: Simple CRM for Service Business

**User request:** "I run a trades business and need to track leads and jobs"

**Database Schema:**

```
CONTACTS DATABASE
├── Name (title)
├── Phone (phone)
├── Email (email)
├── Address (text)
├── Source (select: Website, Google, Referral, Repeat)
├── → Jobs (relation)
├── Total Spent (rollup: sum of Job values)
└── Last Job Date (rollup: max date)

JOBS DATABASE
├── Job Name (title)
├── → Contact (relation)
├── Status (select: Enquiry, Quoted, Booked, In Progress, Complete, Lost)
├── Quote Amount (number, £)
├── Final Amount (number, £)
├── Quote Date (date)
├── Job Date (date)
├── Job Type (select: based on services offered)
├── Notes (text)
└── Photos (files)

FOLLOW-UPS DATABASE
├── Task (title)
├── → Contact (relation)
├── → Job (relation)
├── Due Date (date)
├── Status (checkbox)
└── Type (select: Quote Follow-up, Review Request, Check-in)
```

**Key Views:**

- **Pipeline Board:** Jobs by Status
- **Today's Follow-ups:** Follow-ups due today
- **Jobs This Week:** Calendar view by Job Date
- **Hot Leads:** Jobs where Status = Enquiry/Quoted, sorted by Quote Date

**Automations:**

1. **Job status → Quoted:** Create Follow-up task for 3 days later
2. **Job status → Complete:** Create Follow-up for review request 7 days later

---

## Quick Reference: Common Property Patterns

**Date tracking:**
- Created (date, auto-set by automation)
- Modified (date, manual or API)
- Due Date (date)
- Completed Date (date)

**Status progression:**
- Lead → Proposal → Active → Complete (projects)
- To Do → In Progress → Done (tasks)
- Idea → Draft → Review → Published (content)

**Financial tracking:**
- Amount (number)
- Currency (usually implied, don't need property)
- Paid (checkbox or Status select)
- Payment Date (date)

**People tracking:**
- Owner/Assignee (person for team, text for external)
- Created By (person)
- Related Contact (relation)
