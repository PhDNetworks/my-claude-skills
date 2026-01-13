# My Claude Skills

A curated collection of Claude Skills for digital marketing, SEO, PPC, web development, and productivity automation.

## Repository Structure

```
my-claude-skills/
├── core/                    # Reusable, industry-agnostic skills
│   ├── google-ads/          # PPC campaign management
│   ├── seo/                 # Search engine optimisation
│   ├── content/             # Content creation & image workflows
│   ├── web/                 # Web performance & animation
│   ├── productivity/        # Notion, Asana automation
│   └── marketing/           # Demand generation
│
├── clients/                 # Client-specific configurations
│   ├── jlr-roofing/
│   ├── ossett-dental/
│   ├── riflebird/
│   └── forge-mir/
│
└── _archive/                # Deprecated/backup files (gitignored)
```

## Core Skills

### Google Ads (`core/google-ads/`)

| Skill | Path | Description |
|-------|------|-------------|
| Campaign Architect | `campaign-architect/` | Full campaign structures with ad groups, keywords, negatives, RSAs, and extensions for UK trades |
| Ads Manager | `ads-manager/` | Google Ads API integration with Python scripts for performance analysis and alerts |

### SEO (`core/seo/`)

| Skill | Path | Description |
|-------|------|-------------|
| Official Guide | `official-guide/` | SEO recommendations grounded in Google's official documentation |
| Content Optimizer | `content-optimizer/` | On-page SEO analysis with keyword density, readability, and meta optimization |
| Keyword Strategy | `keyword-strategy/` | Keyword research and prioritization for content planning |
| Keyword Cluster Builder | `keyword-cluster-builder/` | Semantic clustering and pillar-cluster content architecture |
| Technical SEO | `technical-seo/` | Crawling, indexing, Core Web Vitals, structured data audits |
| Local Schema Generator | `local-schema-generator/` | JSON-LD structured data for LocalBusiness, Service, FAQ, Reviews |

### Content (`core/content/`)

| Skill | Path | Description |
|-------|------|-------------|
| Content Creator | `content-creator/` | SEO-optimized blog posts, landing pages, and marketing copy with brand voice |
| ImageForge Pro | `imageforge-pro/` | Batch image renaming, SEO filenames, alt text generation, WordPress upload |

### Web (`core/web/`)

| Skill | Path | Description |
|-------|------|-------------|
| Performance Audit | `performance-audit/` | Page speed analysis, Core Web Vitals, performance bottleneck identification |
| Animation Tools | `animation-tools/` | Web animation guidance for Framer, Motion, GSAP, Lottie, Rive, Spline |

### Productivity (`core/productivity/`)

| Skill | Path | Description |
|-------|------|-------------|
| Asana AI Studio | `asana-ai-studio/` | Asana Rules automation and AI Studio workflow configuration |
| Notion Expert | `notion/expert/` | Workspace design, database architecture, productivity systems |
| Notion Knowledge Capture | `notion/knowledge-capture/` | Transform conversations into structured wiki/FAQ documentation |
| Notion Research | `notion/research-documentation/` | Cross-workspace research synthesis and report generation |

### Marketing (`core/marketing/`)

| Skill | Path | Description |
|-------|------|-------------|
| Demand Acquisition | `demand-acquisition/` | Multi-channel demand gen, paid media optimization, CAC analysis |

## Client Skills

Client-specific skills contain proprietary configurations, account details, and customized workflows.

| Client | Path | Focus |
|--------|------|-------|
| JLR Roofing | `clients/jlr-roofing/` | Leeds roofing PPC on £250/month budget |
| Ossett Dental | `clients/ossett-dental/` | Dental PPC with £49 offer, CRO, GA4/GTM QA |
| Riflebird | `clients/riflebird/` | Cold email sequences for SEO audit outreach |
| FORGE-MIR | `clients/forge-mir/` | B2B WordPress/Elementor website builds |

## Skill Structure

Each skill follows this standard structure:

```
skill-name/
├── SKILL.md              # Core instructions (required)
├── references/           # Supporting documentation (optional)
│   ├── templates.md
│   └── examples.md
├── scripts/              # Automation scripts (optional)
└── assets/               # Templates, images (optional)
```

### SKILL.md Format

Every `SKILL.md` must include YAML frontmatter:

```yaml
---
name: skill-name
description: One-line description with trigger keywords. Use when [context]. Triggers on [keywords].
---

# Skill Title

[Core instructions and workflows]
```

## Usage

### Claude Desktop / Cowork Mode

1. Select this folder as your workspace
2. Skills are automatically available based on context
3. Reference skills explicitly: "Use the campaign-architect skill to..."

### Claude Projects (claude.ai)

1. Zip the skill folder:
   ```bash
   cd core/google-ads
   zip -r campaign-architect.skill campaign-architect/
   ```
2. Upload the `.skill` file to your Claude Project

### Claude Code CLI

Place skills in `~/.claude/skills/` or reference via MCP.

## Contributing

1. Create skill folder with `SKILL.md`
2. Add YAML frontmatter with name and description
3. Include trigger keywords in description
4. Add references/ for supporting docs
5. Test skill activation

## License

MIT — PhD Networks & Systems Ltd
