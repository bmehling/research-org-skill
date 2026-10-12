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
    "defaultModel": "sonnet"
  },
  "categories": ["AI", "Voice", "Analytics", "..."],
  "industries": ["Healthcare", "Horizontal", "Fintech", "..."]
}
```

Customize the `categories` and `industries` arrays to match the multi-select values in your Notion database.

Report length is **not** configured here. Per-section word budgets and validation bands live in `references/section_guidelines.md`, which is the single source of truth for length.

### 4. Install the Skill

```bash
# Copy the skill to Claude Code's skills directory
cp -r research-org-skill ~/.claude/skills/research-org-skill

# Install the research subagents (REQUIRED — see below)
mkdir -p ~/.claude/agents
cp agents/*.md ~/.claude/agents/

# Install Python dependencies (used by the Notion upload script)
pip install -r ~/.claude/skills/research-org-skill/scripts/requirements.txt
```

Restart Claude Code if needed, then verify with `/skills`.

**The agents step is not optional.** The research workflow dispatches two subagents that Claude Code discovers from `~/.claude/agents/`, outside the skill directory:

| Agent | Model | Job |
|---|---|---|
| `research-scout` | haiku | Web retrieval — fetch pages, quote figures, cite URLs |
| `research-analyst` | sonnet | Competitive landscape and market sizing |

Both are restricted to `WebSearch` and `WebFetch`, so they cannot write files or reach your Notion database. That restriction is deliberate: it makes the research step structurally read-only instead of relying on the prompt to ask nicely.

Skip this step and the workflow falls back to a general-purpose agent with a read-only instruction in its prompt. It still runs, but the restriction becomes advisory rather than enforced.

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
| `--update` | Refresh an existing entry in place (see below) | `/research-org-skill --update https://example.com` |
| `--stale` | List entries whose research has gone stale. Takes no URL | `/research-org-skill --stale --months 12` |

Flags can be combined:

```
/research-org-skill --lite --model haiku https://example.com
```

### Updating an existing report

`--update` refreshes an entry that already exists in the database. It reads the
existing report, researches only what changed since it was last researched, and
rewrites the page in place with a dated changelog on top.

```
/research-org-skill --update https://example.com
/research-org-skill --update https://app.notion.com/p/<page-id>
```

Pass the Notion page URL instead of the company URL when the company has
rebranded — the new domain will not match the stored one.

What it does differently:

- **Regenerates the whole report** against current guidelines, carrying forward
  facts that still hold. Old reports are brought up to the current standard rather
  than left in whatever format they were written in.
- **Bounds research by date.** It reads the `Research completed:` line from the
  existing report and searches only the window since then.
- **Runs the analyst only when needed** — when the competitor table is over 12
  months old, a competitor had an M&A event, or the company changed markets.
  Routine refreshes run scout-only and cost a fraction of a fresh report.
- **Handles structural events** with dedicated playbooks: rebrand, pivot,
  acquisition, IPO, and shutdown. A company that shut down or was absorbed has its
  report frozen as a historical record rather than regenerated.
- **Asks before writing.** It shows the changelog and a property diff (old → new)
  and waits for approval, because an update overwrites a page other people may
  have annotated.

Prior versions remain available through Notion's page history.

### Workflow

The skill follows a 9-step process:

1. **Load Configuration** — Read config, parse URL, flags
2. **Resolve the Target Entry** — Query Notion to prevent duplicate entries, or in update mode, locate the existing one
3. **Conduct Research** — Web search and fetch (uses haiku for cost efficiency)
4. **Review Reference Files** — Load section guidelines, writing style, and category guides
5. **Write Report** — Draft report following section structure and citation guidelines
6. **Prepare Database Fields** — Determine Categories, Industry, Stage, Revenue, FTEs
7. **Run Quality Checklist** — Validate word count, citations, structure, and writing quality
8. **Create or Update the Notion Entry** — Create or rewrite the page, upload report, set properties and icon
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
    │   ├── check_links.py                 # Dead-citation checker
    │   ├── find_stale.py                  # Lists entries needing a refresh
    │   └── requirements.txt              # Python dependencies
    └── references/
        ├── section_guidelines.md          # Report section order, structure, and length
        ├── writing_style.md               # Tone, citation standards, and examples
        ├── category_guide.md              # Product categorization methodology
        ├── valuation_guide.md             # Funding valuation estimation
        ├── update_guide.md                 # --update playbooks and changelog format
        └── quality_checklist.md           # Pre-publish validation steps
```

## 📖 How It Works

**`SKILL.md`** is the core skill definition. It contains YAML frontmatter (name, description, allowed tools) and the full 9-step workflow that Claude follows when the skill is invoked.

**`references/`** contains the editorial guidelines that shape report quality:

- **section_guidelines.md** — Defines the exact section order, expected content, table formats (including product overview tables with Pattern A/B), and length targets for both full and lite modes
- **writing_style.md** — Sets the professional, analytical tone; citation density targets (25-40+ links per report); and examples of good vs. poor writing
- **category_guide.md** — Guides selection of product categories and industry tags for Notion database fields
- **valuation_guide.md** — Methodology for estimating company valuations when not publicly available
- **update_guide.md** — Governs `--update`: how to locate the existing entry, build a fact ledger from it, bound research by date, and handle rebrands, acquisitions, IPOs, and shutdowns. Also owns the changelog format and the approval gate
- **quality_checklist.md** — Executable verification steps (word count, link count, structure, field completeness) run before every Notion upload

**`scripts/find_stale.py`** lists entries whose research has gone stale, ranked oldest first. It reads each report's `Research completed` / `Last updated` metadata line and falls back to the page's creation date for reports written before that line existed. Entries staged `Defunct` or `Acquired` are excluded, since their reports are frozen by design. Read-only.

```bash
/usr/bin/python3 research-org-skill/scripts/find_stale.py --months 6 --limit 10
/usr/bin/python3 research-org-skill/scripts/find_stale.py --fast --json
```

Only pages that could possibly be stale are read individually, so the scan cost stays well below one request per row, and it drops further as entries get updated.

**`scripts/check_links.py`** checks a report's citations for rot, reading either a local markdown draft or a published Notion page. It classifies each link and, importantly, separates **DEAD** (404, 410, or a host that no longer resolves) from **BLOCKED** (401, 403, 429, 999 — the server refused an automated request). Only DEAD is actionable; paywalled research firms, LinkedIn, and PitchBook return BLOCKED routinely and their pages are usually fine. Runs automatically during `--update`; useful standalone at any time.

```bash
/usr/bin/python3 research-org-skill/scripts/check_links.py --page-id <notion-page-id>
/usr/bin/python3 research-org-skill/scripts/check_links.py --content report.md --all --strict
```

**`scripts/upload_to_notion.py`** handles the Notion upload. It chunks reports by header, converts markdown to Notion blocks (including HTML tables, inline formatting, and links), and uploads in batches with retry logic. It also sets the company's favicon as the page icon.

## ↖ Dependencies

- **Python 3.9+** with `requests` library (for the Notion upload script)
- **Notion MCP server** — provides `notion-search`, `notion-fetch`, `notion-create-pages`, `notion-update-page` tools
- **Claude Code** with skills support and web search/fetch capabilities

## License

This project is licensed under **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. See [`LICENSE.txt`](research-org-skill/LICENSE.txt) for details.
