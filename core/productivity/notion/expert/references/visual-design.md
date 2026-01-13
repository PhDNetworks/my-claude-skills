# Visual Design Reference

## Design Principles

### Hierarchy Through Space

White space is your primary design tool. Don't fill every pixel.

**Spacing guidelines:**
- Add blank lines between sections (3 empty blocks = section break)
- Use horizontal dividers sparingly (max 2-3 per page)
- Columns should breathe — don't pack them full

### The 3-Column Maximum

More than 3 columns creates visual chaos and mobile breakage.

**Column usage:**
- 2 columns: Primary content + sidebar (70/30 or 60/40)
- 3 columns: Equal cards or metrics (33/33/33)
- Never: 4+ columns

### Consistent Icon Language

Choose ONE icon style and stick to it:

**Emoji style** — Friendly, casual, colourful
- ✅ Tasks, 📁 Projects, 📅 Calendar, 💰 Finance

**Minimal style** — Clean, professional
- ▫️ or • for bullets, → for links, ○ for incomplete

**Custom icons** — Brand-aligned (requires upload)
- Consistent size, style, and colour palette

### Colour Strategy

**Limit palette to 3-4 colours:**
- Primary: Main brand/accent colour
- Secondary: Complementary colour for variety
- Neutral: Greys for backgrounds and dividers
- Alert: Red/orange for urgent items only

**Callout colours for hierarchy:**
- Grey: Standard information
- Blue: Tips, notes, references
- Yellow: Warnings, attention needed
- Red: Critical, urgent, errors
- Green: Success, completed, positive

## Component Patterns

### Hero Section

Opening section that orients the user.

```
[Cover Image - full width, 200-300px height]

# Page Title

> Brief description or current status in a quote block

---
```

### Metrics Dashboard

Quick-glance numbers using callouts in columns.

```
|  📊 Active Projects  |  ✅ Tasks Due Today  |  💰 Monthly Revenue  |
|        12            |          5           |       £4,200         |
```

**Implementation:**
- Use 3-column layout
- Each metric in a coloured callout
- Large number, small label below
- Link callout to filtered database view

### Quick Actions Section

Buttons/links for common actions.

```
| ➕ New Task | 📝 New Note | 📅 Schedule | 🔍 Search |
```

**Implementation:**
- Row of linked callouts or button-style text
- Use consistent emoji prefix
- Link to templates or filtered views

### Database Views Section

Embedded databases with toggle visibility.

```
▶ 📋 Today's Tasks
  [Embedded database - filtered to today, sorted by priority]

▶ 📁 Active Projects  
  [Embedded database - gallery view, filtered to active]

▶ 📅 This Week
  [Embedded database - calendar view]
```

**Implementation:**
- Wrap each database in a toggle for clean collapsed view
- Use descriptive toggle title with emoji
- Default to collapsed unless user needs daily visibility

### Sidebar Pattern

Persistent navigation or reference content.

```
| Main Content (70%)        | Sidebar (30%)           |
| [Primary database/content]| 📌 Pinned               |
|                           | - Link 1                |
|                           | - Link 2                |
|                           | 📚 Resources            |
|                           | - Doc link              |
|                           | ⚡ Quick Add            |
|                           | [Template button]       |
```

### Card Layout

For visual databases or grouped information.

**Gallery view settings:**
- Card size: Medium or Large
- Card preview: Page content or specific property
- Fit image: Enable for consistent sizing
- Properties: Show 2-3 max on card face

### Progress Indicators

Visual status representation.

**Option 1: Formula-based progress bar**
```
████████░░ 80%
```

**Option 2: Status callouts**
- 🔴 Not started
- 🟡 In progress  
- 🟢 Complete

**Option 3: Checkbox visual**
```
[x] Phase 1: Research
[x] Phase 2: Design
[ ] Phase 3: Build
[ ] Phase 4: Launch
```

## Page Templates

### Dashboard Template

```
[Cover: Abstract or branded image]

# 🏠 Dashboard

> Quick overview of everything that matters

---

## ⚡ Quick Actions

| ➕ New Task | 📝 Capture | 📅 Schedule |

---

## 📊 This Week

|  Tasks Due  |  Meetings  |  Focus Hours  |
|     7       |     4      |      12       |

---

## 🎯 Today's Focus

[Embedded filtered task view - due today or priority:high]

---

## 📁 Active Projects

[Embedded gallery view - status:active, limit 6]

---

## 📌 Quick Reference

| Resources | Contacts | Templates |
```

### Project Page Template

```
[Cover: Project-specific or category image]

# [Project Name]

| Status | Deadline | Client | Value |
|--------|----------|--------|-------|

---

## 📋 Overview

[Project description, goals, key deliverables]

---

## ✅ Tasks

[Embedded task database - filtered to this project]

---

## 📝 Notes & Docs

[Embedded notes database or linked pages]

---

## 📅 Timeline

[Embedded calendar or timeline view]

---

## 📎 Resources

[Links, files, references]
```

### Meeting Notes Template

```
# 📅 [Meeting Title]

**Date:** @today
**Attendees:** 
**Duration:** 

---

## 📋 Agenda

1. 
2. 
3. 

---

## 📝 Notes

[Main discussion points]

---

## ✅ Action Items

[ ] Action 1 - @person - due date
[ ] Action 2 - @person - due date

---

## 🔗 Related

- [[Link to project]]
- [[Link to previous meeting]]
```

## Mobile Considerations

Notion mobile renders differently. Design for it:

- **Columns stack vertically** — Don't rely on side-by-side layout for meaning
- **Tables scroll horizontally** — Keep key columns on the left
- **Toggles are your friend** — Collapse by default for mobile scannability
- **Large tap targets** — Callouts and buttons work better than small links
- **Test on phone** — Always check your dashboard on mobile

## Anti-Patterns to Avoid

❌ **Over-decoration** — Every heading doesn't need an emoji
❌ **Rainbow callouts** — Pick 2-3 colours, not all of them
❌ **Deep nesting** — If you're 4 toggles deep, restructure
❌ **Horizontal scroll** — Tables wider than viewport frustrate users
❌ **Orphaned databases** — Every database needs a home and a purpose
❌ **Status overload** — 10 status options means nobody knows the real status
