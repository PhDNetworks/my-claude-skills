# Automation & AI Reference

## Database Automations

Native automations within Notion databases.

### Trigger Types

| Trigger | Use Case |
|---------|----------|
| Page added | Auto-set created date, default status, assign owner |
| Property changed | Status workflows, notifications, cascading updates |
| Specific date | Deadline reminders, scheduled archiving |

### Action Types

| Action | Capabilities |
|--------|--------------|
| Edit property | Set select, date, person, text, number, checkbox |
| Add page | Create linked page in another database |
| Send notification | Notify specific people |
| Send to Slack | Post to Slack channel (requires integration) |

### High-Value Automation Recipes

**Auto-timestamp:**
- Trigger: Page added
- Action: Set "Created" property to now

**Status-based assignment:**
- Trigger: Status changed to "Ready for Review"
- Action: Set "Reviewer" to specific person

**Deadline notification:**
- Trigger: Due Date is 2 days from now
- Action: Send notification to assignee

**Auto-archive:**
- Trigger: Status changed to "Done"
- Action: Set "Archived Date" to 7 days from now

**Project cascade:**
- Trigger: Project status changed to "On Hold"
- Action: (Use with caution) Can notify, but can't bulk-update related tasks

### Automation Limitations

- Cannot trigger on rollup changes
- Cannot perform bulk operations
- Cannot run complex conditional logic
- Cannot modify multiple properties in one automation
- Cannot trigger cross-database updates directly

**Workarounds:**
- Use Notion API + Make/Zapier for complex workflows
- Use formulas for conditional display (not actual automation)
- Manual weekly reviews for bulk status updates

## Notion AI Features

### AI Properties (Database)

Configure in database property settings.

**AI Summary**
- Generates: Concise summary of page content
- Best for: Meeting notes, research, long documents
- Updates: On page edit (with delay)

**AI Key Info**
- Generates: Structured extraction (action items, decisions, contacts)
- Best for: Meeting notes, emails, project briefs
- Customisable: Can specify what to extract

**AI Custom Autofill**
- Generates: Content based on custom prompt + page data
- Best for: Meta descriptions, categorisation, response drafts
- Examples:
  - "Generate a 2-sentence project summary based on the title and description"
  - "Suggest 3 relevant tags based on the content"
  - "Draft a follow-up email based on meeting notes"

**AI Translation**
- Generates: Translated version of specified property
- Best for: Multi-language teams, localised content

### AI Blocks (In-page)

Available anywhere via `/ai` command.

**Use cases:**
- Summarise selection
- Explain technical content
- Generate ideas/brainstorm
- Improve writing
- Translate text
- Continue writing

**Best practices:**
- Be specific in prompts
- Select relevant content before invoking
- Use for first drafts, then edit

### AI in Templates

Pre-configure AI prompts in templates for consistency.

**Example: Meeting Note Template**
```
# Meeting Notes

## AI Summary
[AI Summary property - auto-generates after content added]

## Key Decisions
[AI Key Info property - extracts decisions]

## Action Items
[AI Key Info property - extracts action items]
```

## External Integrations

### Make (formerly Integromat)

Best for: Complex multi-step workflows, scheduled operations, cross-platform sync

**Common scenarios:**
- New Notion page → Create Google Calendar event
- Gmail with label → Create Notion task
- Notion status change → Update CRM
- Scheduled: Weekly report generation

### Zapier

Best for: Simple trigger-action pairs, quick setup, wide app support

**Common scenarios:**
- Form submission → Notion database entry
- Notion page added → Slack notification
- Calendar event → Notion task

### Notion API Direct

Best for: Custom applications, bulk operations, advanced logic

**Capabilities:**
- CRUD operations on databases and pages
- Query with complex filters
- Bulk updates
- Webhook triggers (via third-party)

**Limitations:**
- No native webhooks (need polling or third-party)
- Rate limits apply
- Some property types have quirks

## Automation Patterns

### Inbox Zero Pattern

```
Trigger: Email arrives (via Zapier/Make)
Action: Create page in Inbox database
  - Title: Email subject
  - Status: "Unprocessed"
  - Source: "Email"
  - Content: Email body

Manual: Weekly review to process inbox
  - Move to appropriate project
  - Convert to task
  - Archive/delete
```

### Client Onboarding Pattern

```
Trigger: New page added to Clients database
Actions (sequence via Make):
  1. Create Project page (linked to Client)
  2. Create Task template pages (linked to Project)
  3. Send welcome email (via email service)
  4. Notify team on Slack
  5. Create Google Drive folder
  6. Add calendar kickoff meeting
```

### Content Pipeline Pattern

```
Database: Content Calendar

Automation 1:
- Trigger: Status → "Drafting"
- Action: Set "Draft Due" to +3 days

Automation 2:
- Trigger: Status → "Review"
- Action: Notify editor

Automation 3:
- Trigger: Status → "Scheduled"
- Action: (via Make) Create social posts in Buffer
```

### Status Sync Pattern

For keeping related items in sync.

```
Scenario: Project status should reflect task status

Option 1: Rollup + Formula (display only)
- Rollup: Count tasks where status ≠ "Done"
- Formula: if(prop("Open Tasks") == 0, "Complete", "In Progress")

Option 2: Make automation (actual status change)
- Trigger: Task status changed
- Filter: All sibling tasks are "Done"
- Action: Update parent project status to "Complete"
```

## Automation Checklist

Before building:
- [ ] What manual action are you eliminating?
- [ ] How often does this trigger occur?
- [ ] What could go wrong? (edge cases)
- [ ] Is native Notion automation sufficient?
- [ ] Do you need external integration?

After building:
- [ ] Test with realistic data
- [ ] Document the automation (for future you)
- [ ] Monitor for failures
- [ ] Review quarterly — still needed?
