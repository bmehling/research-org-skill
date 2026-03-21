# Research Org Skill

> A Claude Code skill that conducts comprehensive company research and automatically publishes structured reports to your Notion database. Generates cited, analyst-quality intelligence reports with product tables, competitive landscapes, and market analysis — all from a single command.

## Overview

Research Org automates the end-to-end workflow of company research: web scraping, data synthesis, report writing, quality validation, and Notion publishing. It produces structured reports following a consistent format (Company Overview, Products & Services, Market Analysis, Competitive Landscape, etc.) with inline citations throughout. Reports can be generated in full mode (3,000-3,500 words) or lite mode (1,200-1,500 words) depending on the depth needed.

## 🏗️ Setup & Configuration

### Prerequisites

- [Claude Code](https://claude.ai/claude-code) with skills support
- A [Notion](https://www.notion.so/) workspace and database
- A Notion MCP server ([Notion MCP](https://www.npmjs.com/package/@anthropic-ai/notion-mcp-server) or equivalent)
- Python 3.9+

### 1. Create a Notion Database

Set up a database in your Notion workspace with the following fields:

| Field | Type | Notes |
|-------|------|-------|
| Organization | Title | Company name (primary field) |
| URL | URL | Company website |
| Category | Multi-select | Product categories (e.g., AI, Voice, Analytics) |
| Industry | Multi-select | Vertical focus (e.g., Healthcare, Horizontal, Fintech) |
| Stage | Multi-select | Funding stage (e.g., Seed, Series A, Series B) |
| Revenue | Multi-select | Revenue range (e.g., $1M-$8M, $30M-$100M, Not available) |
| FTEs | Multi-select | Employee count range (e.g., 10-50, 100-250, Not available) |

Populate each multi-select field with the values that make sense for your research focus.

### 2. Get Notion Credentials

1. Create an internal integration at [Notion Integrations](https://www.notion.so/my-integrations)
   - Grant it database read/write permissions at minimum
2. Copy your **Internal Integration Token**
3. Find your **Database ID** from the database URL: `https://www.notion.so/workspace/{DATABASE_ID}?v=...`
4. Find your **Data Source ID** via the database's 3-dot menu → Data sources → Copy data source ID

### 3. Configure the Skill

Copy the example config and fill in your credentials:

```bash
cp config.example.json research-org-skill/config.json
```

Edit `research-org-skill/config.json`:

```json
{
  "notion": {
    "databaseId": "<your_database_id>",
    "databaseUrl": "https://www.notion.so/<your_database_id>",
    "dataSourceId": "<your_data_source_id>",
    "databaseName": "<your_database_name>",
    "notion_api": "<your_integration_token>"
  },
  "research": {
    "targetWordCount": "2500-4000",
    "liteWordCount": "1200-2000",
    "defaultModel": "sonnet"
  },
  "categories": ["AI", "Voice", "Analytics", "..."],
  "industries": ["Healthcare", "Horizontal", "Fintech", "..."]
}
```

Customize the `categories` and `industries` arrays to match the multi-select values in your Notion database.

### 4. Install the Skill

```bash
# Copy the skill to Claude Code's skills directory
cp -r research-org-skill ~/.claude/skills/research-org-skill

# Install Python dependencies (used by the Notion upload script)
pip install -r ~/.claude/skills/research-org-skill/scripts/requirements.txt
```

Restart Claude Code if needed, then verify with `/skills`.

### 5. Set Up Notion MCP

The skill requires a Notion MCP server for database operations. Follow the setup instructions for your Notion MCP provider to connect it to Claude Code.

## 🛠️ Usage

Trigger the skill with `/research-org-skill` followed by a company URL:

```
/research-org-skill https://example.com
```

### Options

| Flag | Description | Example |
|------|-------------|---------|
| `--lite` | Shorter report (1,200-1,500 words), omits funding, exec team, SWOT | `/research-org-skill --lite https://example.com` |
| `--model MODEL` | Override the default model (`sonnet`, `opus`, `haiku`) | `/research-org-skill --model opus https://example.com` |

Flags can be combined:

```
/research-org-skill --lite --model haiku https://example.com
```

### Workflow

The skill follows a 9-step process:

1. **Load Configuration** — Read config, parse URL, flags
2. **Check for Duplicates** — Query Notion to prevent duplicate entries
3. **Conduct Research** — Web search and fetch (uses haiku for cost efficiency)
4. **Review Reference Files** — Load section guidelines, writing style, and category guides
5. **Write Report** — Draft report following section structure and citation guidelines
6. **Prepare Database Fields** — Determine Categories, Industry, Stage, Revenue, FTEs
7. **Run Quality Checklist** — Validate word count, citations, structure, and writing quality
8. **Create Notion Entry** — Create page, upload report, set properties and icon
9. **Display Summary** — Show completion summary with Notion link

## 📂 Project Structure

```
research-org/
├── README.md                              # This file
├── config.example.json                    # Configuration template
└── research-org-skill/                    # Main skill directory
    ├── SKILL.md                           # Skill definition and workflow
    ├── config.json                        # Active configuration (gitignored)
    ├── LICENSE.txt                        # CC BY-SA 4.0
    ├── scripts/
    │   ├── upload_to_notion.py            # Chunked report upload to Notion
    │   ├── upload_to_notion.py-README.md  # Upload script documentation
    │   └── requirements.txt              # Python dependencies
    └── references/
        ├── section_guidelines.md          # Report section order, structure, and length
        ├── writing_style.md               # Tone, citation standards, and examples
        ├── category_guide.md              # Product categorization methodology
        ├── valuation_guide.md             # Funding valuation estimation
        └── quality_checklist.md           # Pre-publish validation steps
```

## 📖 How It Works

**`SKILL.md`** is the core skill definition. It contains YAML frontmatter (name, description, allowed tools) and the full 9-step workflow that Claude follows when the skill is invoked.

**`references/`** contains the editorial guidelines that shape report quality:

- **section_guidelines.md** — Defines the exact section order, expected content, table formats (including product overview tables with Pattern A/B), and length targets for both full and lite modes
- **writing_style.md** — Sets the professional, analytical tone; citation density targets (25-40+ links per report); and examples of good vs. poor writing
- **category_guide.md** — Guides selection of product categories and industry tags for Notion database fields
- **valuation_guide.md** — Methodology for estimating company valuations when not publicly available
- **quality_checklist.md** — Executable verification steps (word count, link count, structure, field completeness) run before every Notion upload

**`scripts/upload_to_notion.py`** handles the Notion upload. It chunks reports by header, converts markdown to Notion blocks (including HTML tables, inline formatting, and links), and uploads in batches with retry logic. It also sets the company's favicon as the page icon.

## ↖ Dependencies

- **Python 3.9+** with `requests` library (for the Notion upload script)
- **Notion MCP server** — provides `notion-search`, `notion-fetch`, `notion-create-pages`, `notion-update-page` tools
- **Claude Code** with skills support and web search/fetch capabilities

## License

This project is licensed under **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. See [`LICENSE.txt`](research-org-skill/LICENSE.txt) for details.
