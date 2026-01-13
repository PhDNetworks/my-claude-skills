---
name: notion-expert
description: World-class Notion workspace design, database architecture, and productivity system creation. Use when users want to build Notion pages, dashboards, databases, or productivity systems. Triggers include requests for Notion templates, database setup, visual dashboard design, relation/rollup/formula help, automation configuration, AI property setup, or implementing productivity frameworks (PARA, GTD, Zettelkasten). Also use for optimizing existing Notion workspaces, creating client management systems, project trackers, content calendars, CRMs, or any interconnected database architecture.
---

# Notion Expert Skill

Transform Notion from a simple note-taking tool into a powerful, visually aesthetic productivity system with interconnected databases, intelligent automation, and AI-powered workflows.

## Core Design Philosophy

**Function before form** — Build robust database architecture first, then layer visual design on top.

**Progressive complexity** — Start with the simplest structure that works. Add relations, rollups, and formulas only when they solve real problems.

**Single source of truth** — Every piece of data lives in exactly one database. Other views reference it via relations, never duplicate it.

## Workflow Selection

Determine the task type:

**Building from scratch?** → Follow "New Workspace Workflow" below
**Optimizing existing setup?** → Follow "Optimization Workflow" below
**Specific feature request?** → Consult appropriate reference file

### New Workspace Workflow

1. **Clarify requirements** — What are you tracking? What decisions will this help you make?
2. **Design database schema** — See references/database-patterns.md
3. **Build core databases** — Essential properties first
4. **Add interconnections** — Relations, rollups, formulas as needed
5. **Create views** — Filtered/sorted views for different contexts
6. **Design dashboard** — See references/visual-design.md
7. **Configure automation** — See references/automation.md
8. **Document and handoff**

### Optimization Workflow

1. **Audit current setup** — Identify redundancy, missing relations, unused properties
2. **Map data flow** — How does information move through the workspace?
3. **Identify friction** — What requires manual work that could be automated?
4. **Propose improvements** — Prioritize by impact vs. effort
5. **Implement incrementally**

## Database Architecture Principles

### Property Types

| Type | Best For | Avoid When |
|------|----------|------------|
| Select | Fixed categories <10 options | Options change frequently |
| Multi-select | Tags, labels | Need metadata per tag |
| Relation | Connecting databases | Simple categorization suffices |
| Rollup | Aggregating related data | Formula works instead |
| Formula | Calculated values, status logic | Simple text suffices |

### Relation Strategies

**One-to-many** — Tasks → Project (many tasks belong to one project)
**Many-to-many** — Tasks ↔ Tags (tasks have many tags, tags apply to many tasks)
**Self-relation** — Tasks → Parent Task (subtasks)

See references/database-patterns.md for hub databases, junction tables, and inheritance patterns.

## Visual Design Quick Reference

**Spacing** — Use dividers sparingly. Empty space is a divider. Max 3 columns.

**Icons** — Use consistently within a database. Match icon style. Don't over-icon.

**Color** — Limit to 3-4 accent colors. Use callout backgrounds for hierarchy.

**Elevating components:** Callouts, toggle lists, synced blocks, gallery views, board views

See references/visual-design.md for comprehensive aesthetic guidelines.

## Automation & AI

### Native Automations

Triggers: Property changes, page added, specific date
Actions: Edit property, add page, send notification, Slack message

**High-value automations:**
- Auto-set "Created" date on new entries
- Move to "Archive" when status = "Done" for 7 days
- Notify on deadline approaching

### Notion AI Properties

| AI Property | Use Case |
|-------------|----------|
| AI Summary | Condense meeting notes, long documents |
| AI Key Info | Extract action items, decisions |
| AI Custom Autofill | Generate content based on page data |
| AI Translation | Multi-language workspaces |

See references/automation.md for setup guides.

## Productivity Frameworks

| Framework | Best For | Core Principle |
|-----------|----------|----------------|
| PARA | Knowledge workers | Organize by actionability |
| GTD | Task-heavy roles | Capture everything, process weekly |
| Zettelkasten | Writers, researchers | Atomic notes, emergent connections |
| OKRs | Teams | Measurable outcomes |

See references/productivity-systems.md for implementation guides.

## Formula Quick Reference

```
// Status based on dates
if(empty(prop("Due Date")), "No date",
  if(prop("Due Date") < now(), "Overdue",
    if(prop("Due Date") < dateAdd(now(), 7, "days"), "Due soon", "On track")))

// Progress percentage
round(prop("Completed") / prop("Total") * 100)

// Days until due
dateBetween(prop("Due Date"), now(), "days")
```

## Output Standards

When delivering Notion builds:
1. List all databases, their purpose, and key properties
2. Explain how databases connect (diagram or description)
3. Specify views with filters/sorts
4. Document formula logic
5. Suggest evolution path
