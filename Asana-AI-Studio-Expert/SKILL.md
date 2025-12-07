---
name: asana-rules-ai-studio
description: Expert-level guidance for Asana Rules automation and AI Studio smart workflows. Use when building, troubleshooting, or optimizing Asana automation rules, creating AI-powered workflows with AI Studio, designing conditional logic and branching rules, configrating form-to-rule automation, or integrating Asana with third-party apps via rules. Covers triggers, actions, conditions, branching, AI prompting, and all technical limits.
---

# Asana Rules & AI Studio Expert Guide

## Part 1: Asana Rules (Standard Automation)

### Creating Rules

Access: Project → Customize → Rules → Add Rule

**Two creation paths:**
1. **Rules Gallery** - Pre-built templates for common automations
2. **Custom Rule** - Build from scratch with triggers, conditions, actions

### Rule Structure

```
WHEN [Trigger(s)] → CHECK IF [Condition(s)] → DO [Action(s)]
                                           → OTHERWISE IF [Branch] → DO [Actions]
```

### Available Triggers (When)

| Category | Triggers |
|----------|----------|
| **Task Events** | Task added to project, Task moved to section, Task completed/incomplete, Task unblocked |
| **Field Changes** | Assignee changed, Due date changed, Custom field changed, Priority changed |
| **Date Events** | Due date approaching (1,3,7 days), Task overdue, Due date arrived |
| **Approvals** | Approval status changed (pending/approved/rejected/changes_requested) |
| **Other** | Form submitted, Comment added, Attachment added, Task moved from another project |

**Multiple triggers = OR logic** (rule evaluates if ANY trigger fires)

### Available Actions (Do This)

| Category | Actions |
|----------|---------|
| **Assignment** | Assign to person, Clear assignee |
| **Dates** | Set due date, Set start date, Add/subtract days from date |
| **Sections** | Move to section (same project), Add to another project |
| **Fields** | Set custom field value, Clear custom field |
| **Tasks** | Complete task, Mark incomplete, Create subtasks (max 20), Create approval |
| **Communication** | Add comment, Add followers, Send email (via integration) |
| **Integrations** | Send Slack message, Create Jira issue, Create calendar event, Trigger Zapier |

### Conditions & Branching

**Conditions (Check If):** Filter when actions execute
- Field comparisons: equals, not equals, contains, is empty, is set
- Date comparisons: before, after, between
- Assignee checks: assigned to, not assigned to, unassigned

**Branching (Otherwise If):** Multiple conditional paths in one rule
```
WHEN task moved to section
  IF Priority = High → Assign to Sarah, Set due date today
  OTHERWISE IF Priority = Medium → Assign to Team Lead
  OTHERWISE IF Priority = Low → Move to Backlog
```

### Technical Limits (Current as of Dec 2025)

| Limit | Value |
|-------|-------|
| Rules per project/portfolio | 50 |
| Triggers per rule | 20 |
| Actions per branch | 20 |
| Branches per rule | 25 |
| Conditions per branch | 20 |
| Total components per rule | 100 |
| Subtasks in "Create subtasks" action | 20 |
| Manual rule trigger batch | 50 tasks |

### Best Practices

1. **Keep rules simple** - One purpose per rule; easier to debug
2. **Use conditions over multiple rules** - Consolidate with branching when logic overlaps
3. **Test incrementally** - Create rule, test with one task, then scale
4. **Name descriptively** - "Move to Done when completed" not "Rule 1"
5. **Avoid rule conflicts** - Multiple rules on same trigger can cause race conditions
6. **Use custom fields strategically** - Single-select fields are best for rule triggers
7. **Multi-home for complex workflows** - Tasks in multiple projects can trigger rules in each

### Common Patterns

**Auto-assign by form field:**
```
WHEN Form submitted
CHECK IF Department = Marketing → Assign to Marketing Lead
OTHERWISE IF Department = Sales → Assign to Sales Lead
```

**Status-based section movement:**
```
WHEN Status field changes
CHECK IF Status = "In Review" → Move to "Review" section
OTHERWISE IF Status = "Done" → Move to "Complete" section, Complete task
```

**Due date reminders:**
```
WHEN Due date is 3 days away
DO Add comment "@assignee reminder: due in 3 days"
```

**Subtask auto-creation:**
```
WHEN Task moved to "In Progress"
DO Create subtasks: "Initial review", "Draft response", "Final approval"
```

---

## Part 2: AI Studio (Smart Workflows)

AI Studio is a no-code builder for AI-powered workflows that go beyond simple if-then automation.

### Key Capabilities

- **Natural language instructions** - Tell AI what to do in plain English
- **Context-aware processing** - AI reads task data, descriptions, custom fields
- **Web search** - AI can search the web for enrichment
- **Dynamic outputs** - AI generates comments, field values, task names based on content
- **Human-in-the-loop** - Optional approval steps before AI actions execute

### AI Studio Structure

```
WHEN [Trigger] → AI STEP [Instructions + Context] → DO [AI-generated output]
```

### Building AI Studio Workflows

1. **Access:** Project → Customize → Rules → Create with AI Studio
2. **Select trigger** (same triggers as standard rules)
3. **Add AI step** with:
   - **Instructions** (prompt) - What you want AI to do
   - **Context sources** - Projects, portfolios, goals, web, attached files
4. **Define output action** - Comment, rename task, set field value (using AI)

### Writing Effective AI Instructions

**Structure your prompts:**
```
**Context:**
[Who you are, what this workflow is for]

**Instructions:**
[Step-by-step what AI should do]

**Output format:**
[How to structure the response]
```

**Example - Lead Enrichment:**
```
**Context:**
We are a consulting agency. When leads submit our form, we need to qualify them.

**Instructions:**
1. Extract the domain from the email address
2. Search the web for company information
3. Identify: Industry, Company Size, Recent News
4. Based on company size >100 employees, recommend Enterprise plan

**Output:**
Post a comment with:
🏥 Industry: {findings}
📊 Size: {findings}
📰 News: {findings}
💡 Recommended Plan: {recommendation}
```

### AI-Compatible Actions

| Action | AI Capability |
|--------|---------------|
| **Add comment** | AI writes contextual comment based on task data |
| **Rename task** | AI generates descriptive task name from description |
| **Set custom field** | AI determines appropriate field value |
| **Set description** | AI rewrites or enhances task description |

### Pre-Built Smart Workflows

- **Smart Task Naming** - Renames form submissions with clear titles
- **Missing Info Checker** - Flags incomplete task submissions
- **Duplicate Detection** - Identifies similar existing tasks
- **Priority Assessment** - AI assigns priority based on content

### AI Studio Prompting Best Practices

1. **Be specific about output format** - "Post a comment following this exact format..."
2. **Provide context** - Include who you are, what your business does
3. **Use structured data** - Reference specific custom fields by name
4. **Include examples** - Show AI what good output looks like
5. **Set constraints** - "Only recommend Enterprise if >100 employees"
6. **Enable web search** - For enrichment workflows, allow AI to search
7. **Attach reference documents** - Upload PDFs with scoring criteria, guidelines

### Multi-Step AI Workflows

Chain multiple AI steps for complex processes:

```
Step 1: Data Enrichment (AI researches lead)
Step 2: Lead Scoring (AI scores based on criteria PDF)
Step 3: Sales Assignment (AI matches to best salesperson)
Step 4: Email Draft (AI writes personalized follow-up)
Step 5: Human Review (Approval before sending)
Step 6: Send Email (Integration action)
```

### AI Studio Plans & Credits

| Plan | Access |
|------|--------|
| AI Studio Basic | Included with Starter+ (rate-limited credits) |
| AI Studio Plus | Paid add-on, higher limits |
| AI Studio Pro | Advanced controls, AI Teammates beta |

### Troubleshooting

**Rule not triggering:**
- Verify trigger matches actual action (exact field name, section name)
- Check if another rule completed the task first
- Confirm rule is enabled (not paused)

**AI producing poor output:**
- Add more context to instructions
- Provide example outputs
- Specify format explicitly
- Test prompt in Smart Chat first

**Actions not executing:**
- Check conditions aren't excluding the task
- Verify you have required permissions
- Check integration authentication (Slack, Gmail, etc.)

---

## Quick Reference

See `references/triggers-actions.md` for complete trigger/action matrix.
See `references/ai-prompts.md` for production-ready AI Studio prompt templates.
See `references/integrations.md` for third-party app rule configurations.
