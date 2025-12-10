# My Claude Skills

A collection of custom Claude Skills for digital marketing, SEO, PPC, and productivity automation.

## What are Claude Skills?

Claude Skills are reusable instruction sets that give Claude specialized capabilities for specific tasks. Each skill contains a `SKILL.md` file with core instructions and optional reference documents for domain knowledge.

## Skills Library

### Google Ads & PPC
| Skill | Description |
|-------|-------------|
| **google-ads-campaign-architect** | Full campaign structure generation with ad groups, keywords, and RSAs |
| **ossett-dental-ppc-strategist** | Client-specific PPC operating system with tracking, CRO, and automation |

### SEO
| Skill | Description |
|-------|-------------|
| **google-official-seo-guide** | SEO recommendations grounded in Google's official documentation |
| **keyword-strategy** | Keyword research and clustering for content planning |
| **seo-keyword-cluster-builder** | Topic cluster architecture for SEO content |
| **seo-content-optimizer** | On-page optimization and content improvement |
| **technical-seo** | Technical audits, schema, Core Web Vitals |
| **web-performance-audit** | Page speed and performance analysis |

### Content & Creative
| Skill | Description |
|-------|-------------|
| **content-creator** | Blog posts, landing pages, and marketing copy |
| **imageforge-pro** | AI image prompt generation with industry-specific templates |
| **riflebird-cold-email** | Cold outreach sequences and email copywriting |

### Local Business
| Skill | Description |
|-------|-------------|
| **local-business-schema-generator** | LocalBusiness JSON-LD schema markup generator |
| **marketing-demand-acquisition** | Local lead generation strategy and campaigns |

### Productivity & Automation
| Skill | Description |
|-------|-------------|
| **Asana-AI-Studio-Expert** | Asana project setup, task generation, and workflow automation |
| **notion-expert** | Notion workspace design, databases, and systems |
| **notion-knowledge-capture** | Research and knowledge base organization in Notion |
| **notion-research-documentation** | Documentation workflows and templates |

## Usage

### In Claude Projects
1. Zip the skill folder: `zip -r skill-name.skill skill-name/`
2. Upload the `.skill` file to your Claude Project

### In Claude Code / Local
Place the skill folder in `/mnt/skills/user/` or reference via the skills system.

### Triggering a Skill
Most skills activate automatically based on context. Some have explicit triggers documented in their `SKILL.md`.

## Folder Structure

```
skill-name/
├── SKILL.md              # Core instructions (required)
└── references/           # Supporting documents (optional)
    ├── example.md
    └── templates.md
```

## Contributing

These are personal skills for PhD Networks & Systems Ltd. Feel free to fork and adapt for your own use.

## License

MIT
