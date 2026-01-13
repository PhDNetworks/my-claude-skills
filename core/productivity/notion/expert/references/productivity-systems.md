# Productivity Systems Reference

## PARA Method

**Creator:** Tiago Forte
**Best for:** Knowledge workers who need to organize both projects and reference material

### Core Concept

Organize everything by actionability:
- **Projects** — Active with deadlines
- **Areas** — Ongoing responsibilities  
- **Resources** — Reference material for future
- **Archives** — Inactive items

### Notion Implementation

**Structure:**
```
🏠 Dashboard
├── 📁 Projects (database)
├── 🎯 Areas (database)
├── 📚 Resources (database)
└── 🗄️ Archives (database)
```

**Projects Database Properties:**
- Name (title)
- Area (relation → Areas)
- Status (select: Active, On Hold, Complete)
- Deadline (date)
- Next Action (text)
- Progress (formula or rollup)

**Areas Database Properties:**
- Name (title)
- Type (select: Work, Personal, Health, Finance, Relationships)
- Description (text)
- → Projects (relation)
- → Resources (relation)
- Review Cycle (select: Weekly, Monthly, Quarterly)

**Resources Database Properties:**
- Name (title)
- Type (select: Article, Book, Course, Template, Reference)
- Area (relation → Areas)
- Tags (multi-select)
- Source URL (url)
- Status (select: To Process, Active, Reference)

**Key Views:**
- Projects: Board by status, filtered to Active
- Areas: Gallery with project counts (rollup)
- Resources: Table searchable by tags

**Weekly Review Template:**
```
# 📅 Weekly Review - [Date]

## 1. Clear Inboxes
- [ ] Email inbox
- [ ] Notes inbox
- [ ] Physical inbox

## 2. Review Projects
[Embedded: Active projects board]

For each project:
- [ ] Is it still active?
- [ ] What's the next action?
- [ ] Any blockers?

## 3. Review Areas
[Embedded: Areas list]

- [ ] Any area being neglected?
- [ ] New project needed?

## 4. Plan Next Week
[Embedded: Calendar view]

Top 3 priorities:
1. 
2. 
3. 
```

---

## GTD (Getting Things Done)

**Creator:** David Allen
**Best for:** People overwhelmed by commitments, managers with high task volume

### Core Concept

Capture everything, clarify meaning, organize by context, reflect regularly, engage confidently.

### Notion Implementation

**Structure:**
```
🏠 GTD Dashboard
├── 📥 Inbox (database)
├── ✅ Next Actions (database)
├── 📁 Projects (database)
├── 📅 Calendar (database or external)
├── 🔮 Someday/Maybe (database)
├── 📚 Reference (database)
└── ⏳ Waiting For (database)
```

**Inbox Database Properties:**
- Item (title)
- Captured (date - auto-set)
- Source (select: Email, Meeting, Idea, Request)

**Next Actions Database Properties:**
- Action (title) — Must start with verb
- Context (multi-select: @computer, @phone, @home, @errands, @office, @anywhere)
- Project (relation → Projects)
- Energy (select: High, Medium, Low)
- Time Required (select: 5min, 15min, 30min, 1hr, 2hr+)
- Due Date (date, optional)
- Status (checkbox)

**Projects Database Properties:**
- Project (title)
- Outcome (text) — What does "done" look like?
- Status (select: Active, On Hold, Complete)
- → Next Actions (relation)
- → Waiting For (relation)
- Area (select or relation)

**Waiting For Database Properties:**
- Item (title)
- Person (text or relation)
- Context (text — why waiting)
- Date Requested (date)
- Follow Up Date (date)
- → Project (relation)

**Key Views:**
- Inbox: Simple list for quick capture
- Next Actions by Context: Board grouped by @context
- Next Actions by Energy: For low-energy days
- Projects: Board by status
- Waiting For: Table sorted by follow-up date

**Processing Workflow:**
```
For each inbox item:
1. What is it?
2. Is it actionable?
   NO → Delete, Reference, or Someday/Maybe
   YES → Continue
3. What's the next action?
4. Will it take <2 minutes?
   YES → Do it now
   NO → Continue
5. Am I the right person?
   NO → Delegate (Waiting For)
   YES → Continue
6. Is it a single action or project?
   Single → Next Actions
   Multi-step → Create Project + Next Action
7. Does it have a hard deadline?
   YES → Add to Calendar
   NO → Just Next Actions
```

---

## Zettelkasten

**Creator:** Niklas Luhmann
**Best for:** Researchers, writers, anyone building a knowledge base over time

### Core Concept

Atomic notes that connect to form emergent knowledge structures. Each note captures one idea and links to related notes.

### Notion Implementation

**Structure:**
```
🏠 Zettelkasten
├── 📥 Fleeting Notes (database)
├── 📝 Permanent Notes (database)
├── 📚 Literature Notes (database)
├── 🗂️ Index (page with manual links)
└── 📁 Projects (database)
```

**Fleeting Notes Database:**
Quick captures, unprocessed. Properties:
- Note (title)
- Content (text)
- Source (text)
- Captured (date)
- Processed (checkbox)

**Literature Notes Database:**
Notes about sources. Properties:
- Title (title)
- Author (text)
- Source Type (select: Book, Article, Video, Podcast)
- Key Ideas (text)
- Quotes (text)
- → Permanent Notes (relation)

**Permanent Notes Database:**
Processed, atomic ideas. Properties:
- Title (title) — Clear, specific
- Content (text) — One idea, your own words
- → Related Notes (self-relation)
- → Source (relation → Literature Notes)
- Tags (multi-select) — Sparse, emergent
- Created (date)
- Modified (date)

**Index Page:**
Manual structure of major topics with linked permanent notes.

```
# 🗂️ Index

## Productivity
- [[Note: Atomic habits compound]]
- [[Note: Context switching costs]]
- [[Note: Energy management > time management]]

## Business
- [[Note: Value-based pricing principles]]
- [[Note: Client red flags]]
...
```

**Workflow:**
1. Capture fleeting notes (quick, unprocessed)
2. Process into literature notes (if from source) or permanent notes
3. Each permanent note: one idea, own words, linked to related notes
4. Update index when new cluster emerges
5. Review connections during writing projects

**Linking Best Practices:**
- Link to related ideas, not just categories
- Ask: "What does this remind me of?"
- Prefer specific links over tag proliferation
- Let structure emerge, don't force hierarchy

---

## OKRs (Objectives & Key Results)

**Best for:** Teams, goal-oriented individuals, quarterly planning

### Core Concept

Objectives = Qualitative goals (inspiring, ambitious)
Key Results = Quantitative measures (specific, measurable)

### Notion Implementation

**Structure:**
```
🎯 OKRs
├── 🏢 Company OKRs (database)
├── 👥 Team OKRs (database)
├── 👤 Personal OKRs (database)
└── 📊 Dashboard
```

**OKRs Database Properties:**
- Objective (title)
- Level (select: Company, Team, Personal)
- Quarter (select: Q1, Q2, Q3, Q4)
- Year (select or number)
- Status (formula based on KR progress)
- Parent OKR (relation - for cascade)
- Key Results (relation → Key Results database)

**Key Results Database Properties:**
- Key Result (title)
- Objective (relation → OKRs)
- Target (number)
- Current (number)
- Unit (text: %, £, #)
- Progress (formula: Current/Target * 100)
- Status (formula based on progress thresholds)
- Owner (person)
- Updates (relation → Updates database or text)

**Progress Formula:**
```
if(prop("Progress") >= 100, "🟢 Complete",
  if(prop("Progress") >= 70, "🟢 On Track",
    if(prop("Progress") >= 40, "🟡 At Risk", "🔴 Off Track")))
```

**Dashboard View:**
- Grouped by Objective
- Progress bars for each KR
- Overall health indicator
- Weekly update log

**Check-in Template:**
```
# 📊 Weekly OKR Check-in - [Date]

## Key Results Update
[Embedded: KRs filtered to current quarter, grouped by objective]

For each KR:
- Current value: 
- Confidence (1-10):
- Blockers:
- Next actions:

## Wins This Week


## Challenges


## Focus for Next Week

```

---

## Hybrid Systems

Often the best system combines elements:

**PARA + GTD:**
- Use PARA for knowledge organization
- Use GTD for task management within Projects

**Zettelkasten + PARA:**
- Zettelkasten for research/writing
- PARA for active project management
- Link permanent notes to project pages

**OKRs + GTD:**
- OKRs for quarterly/annual goals
- GTD for daily/weekly execution
- Key Results inform Project outcomes

## Choosing the Right System

| If you... | Consider... |
|-----------|-------------|
| Manage many active projects | PARA |
| Feel overwhelmed by tasks | GTD |
| Do research or writing | Zettelkasten |
| Set quarterly goals | OKRs |
| Need simple task tracking | Basic task database |
| Run a business | Custom (Client + Project + Task) |

**Start simple.** Add complexity only when you hit friction.
