# Database Patterns Reference

## Advanced Relation Patterns

### Hub Database Pattern

Central database that connects multiple related databases. Example: A "Projects" hub connects Tasks, Notes, Files, Meetings.

```
Projects (Hub)
├── → Tasks (one-to-many)
├── → Notes (one-to-many)  
├── → Meetings (one-to-many)
└── → Team Members (many-to-many)
```

**Implementation:**
- Create Projects database first
- Add Relation property in each satellite database pointing to Projects
- In Projects, create rollup properties to aggregate data from satellites

### Junction Table Pattern

For many-to-many with metadata. Example: Team assignments with roles.

```
Team Members ←→ Project Assignments ←→ Projects
                (junction table)
                - Role
                - Hours allocated
                - Start date
```

**When to use:** Need to store data about the relationship itself, not just the connection.

### Self-Referential Pattern

Tasks with subtasks, categories with subcategories.

```
Tasks
├── Parent Task (relation to same database)
└── Subtasks (rollup counting children)
```

**Formula for depth:**
```
if(empty(prop("Parent")), "Root", 
  if(empty(prop("Parent").prop("Parent")), "Level 1", "Level 2+"))
```

### Inheritance Pattern

Child items inherit properties from parent via rollups.

```
Projects → Tasks
- Project Status (select)
- Tasks inherit "Project Status" via rollup
- Formula checks: if project is "On Hold", task shows "Blocked"
```

## Common Database Schemas

### Client Management

**Clients Database:**
- Name (title)
- Company (text)
- Email (email)
- Phone (phone)
- Status (select: Lead, Active, Inactive)
- Source (select: Referral, Web, Cold)
- → Projects (relation)
- Total Revenue (rollup: sum of Project values)

**Projects Database:**
- Name (title)
- → Client (relation)
- Status (select: Proposal, Active, Completed, Cancelled)
- Value (number, GBP)
- Start Date (date)
- Deadline (date)
- → Tasks (relation)
- Progress (rollup: % tasks complete)

**Tasks Database:**
- Name (title)
- → Project (relation)
- Status (select: To Do, In Progress, Done)
- Due Date (date)
- Priority (select: Low, Medium, High, Urgent)
- Assignee (person)

### Content Calendar

**Content Database:**
- Title (title)
- Status (select: Idea, Drafting, Review, Scheduled, Published)
- Content Type (select: Blog, Social, Email, Video)
- Platform (multi-select: Website, LinkedIn, Instagram, YouTube)
- Publish Date (date)
- Author (person)
- → Campaign (relation)
- AI Summary (AI property)

**Views to create:**
- Calendar: By Publish Date
- Board: By Status
- Gallery: By Content Type (shows featured image)
- Table: Master view with all filters

### Personal Productivity

**Areas Database:**
- Name (title)
- Type (select: Work, Personal, Health, Finance)
- → Projects (relation)
- → Resources (relation)

**Projects Database:**
- Name (title)
- → Area (relation)
- Status (select: Active, On Hold, Completed, Someday)
- → Tasks (relation)
- Due Date (date)
- Progress (formula based on task completion)

**Tasks Database:**
- Name (title)
- → Project (relation)
- Status (checkbox)
- Due Date (date)
- Energy (select: High, Medium, Low)
- Time Estimate (number, minutes)
- Context (multi-select: @computer, @phone, @errands, @home)

## Advanced Formulas

### Status Logic

```
// Multi-condition status
if(prop("Completed"), "✅ Done",
  if(empty(prop("Due Date")), "📋 No date",
    if(prop("Due Date") < now(), "🔴 Overdue",
      if(prop("Due Date") < dateAdd(now(), 3, "days"), "🟡 Due soon",
        if(prop("Due Date") < dateAdd(now(), 7, "days"), "🟢 This week", "⚪ Scheduled")))))
```

### Progress Calculations

```
// Percentage with null handling
if(prop("Total Tasks") == 0, 0, 
  round(prop("Completed Tasks") / prop("Total Tasks") * 100))

// Progress bar (visual)
slice("██████████", 0, round(prop("Progress") / 10)) + 
slice("░░░░░░░░░░", 0, 10 - round(prop("Progress") / 10)) + 
" " + format(prop("Progress")) + "%"
```

### Date Calculations

```
// Working days remaining (excludes weekends)
let(total, dateBetween(prop("Due Date"), now(), "days"),
let(weeks, floor(total / 7),
total - (weeks * 2)))

// Time since created
if(dateBetween(now(), prop("Created"), "days") < 1, "Today",
  if(dateBetween(now(), prop("Created"), "days") < 7, 
    format(dateBetween(now(), prop("Created"), "days")) + " days ago",
    if(dateBetween(now(), prop("Created"), "weeks") < 4,
      format(dateBetween(now(), prop("Created"), "weeks")) + " weeks ago",
      format(dateBetween(now(), prop("Created"), "months")) + " months ago")))
```

### Conditional Formatting Helpers

```
// Priority score for sorting
if(prop("Priority") == "Urgent", 4,
  if(prop("Priority") == "High", 3,
    if(prop("Priority") == "Medium", 2, 1)))

// Combined sort score (priority + due date proximity)
prop("Priority Score") * 100 + (100 - min(dateBetween(prop("Due Date"), now(), "days"), 100))
```

## Database Design Checklist

Before building:
- [ ] What's the primary entity? (tasks, projects, clients, content)
- [ ] What questions will this answer? (affects which views/rollups needed)
- [ ] What's the minimum viable property set?
- [ ] Which properties might need relations vs. selects?
- [ ] What views will users need daily?

After building:
- [ ] Can you find any item in <3 clicks?
- [ ] Is there a clear inbox/capture point?
- [ ] Are status options mutually exclusive and exhaustive?
- [ ] Do relations flow in the logical direction?
- [ ] Are rollups aggregating useful information?
