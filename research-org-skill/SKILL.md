---
name: research-org-skill
description: Comprehensive company and organization research workflow for any industry or sector. Creates Notion database entries with structured research reports following a balanced, objective, and analytical tone. Requires configuration with your Notion database.
allowed-tools: Read, Write, Edit, Agent, Task, TaskCreate, TaskUpdate, TaskGet, TaskList, ToolSearch, WebSearch, WebFetch, Bash, Glob, Grep, mcp__notion__notion-search, mcp__notion__notion-fetch, mcp__notion__notion-create-pages, mcp__notion__notion-update-page, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-create-pages, mcp__claude_ai_Notion__notion-update-page

---

# Research Org Skill

Comprehensive research workflow for creating detailed company intelligence reports and storing them in a Notion database.

## Command

```
research_org: <url> [--model MODEL] [--lite]
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<url>` | Yes | Company website URL to research |
| `--model` | No | Model to use: `sonnet` (default), `opus` (complex), `haiku` (quick) |
| `--lite` | No | Generate a shorter product/market-focused report (omits funding, exec team, SWOT) |

**Examples:**
```
research_org: https://camunda.com
research_org: https://camunda.com --model opus
research_org: https://camunda.com --model haiku
research_org: https://camunda.com --lite
research_org: https://camunda.com --lite --model haiku
```

---

## Workflow

### 1. Load Configuration

1. Read `config.json` from this skill's directory
2. Extract URL from arguments (first `https://` or `http://` match)
3. If `--model` flag present, validate it's `sonnet`, `opus`, or `haiku`
4. Determine final model: `--model` value or `config.research.defaultModel`
5. If `--lite` flag present, set lite mode = true. Use `config.research.liteWordCount` as the word count target instead of `targetWordCount`
6. Use this model in ALL subsequent `Task` tool calls

### 2. Check for Duplicates

Query the Notion database for existing entries with the same URL. If duplicate exists, stop and ask user for guidance.

### 3. Conduct Research

Research the company using web search and fetch tools. Always use `haiku` for the research Task — it's sufficient for web scraping and saves cost. The `--model` flag applies to the main agent only (writing, analysis):

```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: "..."
)
```

Focus on: company background, funding history, products, market position, competition, traction. **Save source URLs** for citations in the report.

For product/pricing research, actively look for `/pricing`, `/plans`, `/products`, and `/features` pages on the company's website. Capture: product names, one-line descriptions, key features (3-5 per product), target users, pricing (exact figures or tiers), and whether the company uses tiered plans vs. distinct products. This structured product data will be used to build a product overview table in the report.

### 4. Review Reference Files

Before writing, read all of these reference files:
1. `references/section_guidelines.md` — Section order and guidance
2. `references/writing_style.md` — Tone, style and approach
3. `references/category_guide.md` — Product categorization
4. `references/valuation_guide.md` — Funding valuation estimation

### 5. Write Report

Follow the section guidelines: `references/section_guidelines.md`

 - match the section structure
 - review the purpose of each section and sub-section
 - follow the section's prompt, examples, and suggested length
 - follow citation guidance

**If lite mode (`--lite`):**

**⚠️ WORD COUNT: Target 1200–1500 words.** Hard max is 2000 words. Write to the LOWER end — aim for 1200–1500 words.

Use the lite structure from `references/section_guidelines.md` (see "Lite Mode Structure" section):

```
# Company Overview
  ## Mission and Vision
# Products and Services
# Notable Partnerships and Customers
# Market
  ## Customer
  ## Market Size and Opportunity
  ## Market Dynamics and Trends
  ## Competitive Landscape Overview
  ## Key Competitors (table)
  ## Competitive Advantages
  ## Traction
```

**If full mode (default):**

**⚠️ WORD COUNT: Target 3000–3500 words.** The hard max is 4000 words. Writing long and then trimming requires many iterations of tedious editing — write tight from the start. Use the LOWER end of each section's expected length range. Do not write elaborate paragraphs where concise ones suffice.

```
# Company Overview
  ## Founding Story
  ## Mission and Vision
  ## Thesis
  ## Business Model
# Executive Team
# Investors, Funding Rounds, and Valuation
  ## Funding Rounds (table)
  ## Valuation Analysis (narrative below table)
# Products and Services
# Notable Partnerships and Customers
# Market
  ## Customer
  ## Market Size and Opportunity
  ## Market Dynamics and Trends
  ## Competitive Landscape Overview
  ## Key Competitors (table)
  ## Competitive Advantages
  ## Traction
# Opportunities and Risks
  ## Key Opportunities
  ## Key Risks
  ## SWOT Analysis
    ### Strengths
    ### Weaknesses
    ### Opportunities
    ### Threats
```

### 6. Prepare Database Fields

Determine values for:
- **Categories** — 1-4 from `references/category_guide.md`
- **Industry** — from `industries` array in config.json
- **Stage** — Seed, Series A, Series B, etc.
- **Revenue** — Estimate or "Not available"
- **FTEs** — Estimate or "Not available"

### 7. Run Quality Checklist

**CRITICAL:** Before creating the database entry, run ALL verification steps in `references/quality_checklist.md` (word count, citation links, structure, database fields, writing quality). Do NOT proceed to step 8 until all checks pass.

**Note:** In lite mode, the word count target is `config.research.liteWordCount` (not `targetWordCount`).

### 8. Create Notion Entry

**Create Page with Overview**

Use `Notion:notion-create-pages` with a brief 2-3 paragraph overview and all properties:

```json
{
  "parent": {"data_source_id": "<from config.json>"},
  "pages": [{
    "content": "# Company Overview\n\nBrief summary...",
    "properties": {
      "Organization": "Company Name",
      "userDefined:URL": "https://company.com",
      "Category": "[\"AI\", \"Workflow Automation\"]",
      "Industry": "[\"Horizontal\"]",
      "Stage": "[\"Series B\"]",
      "Revenue": "[\"$100M+\"]",
      "FTEs": "[\"500+\"]"
    }
  }]
}
```

**Property formatting:** Multi-select fields use JSON array strings with escaped quotes: `"[\"Value1\", \"Value2\"]"`

Store the returned `page_id` for uploading the full report.

**Upload Full Report**

The Notion MCP has payload limits for large content. Use the helper script to upload reliably:

1. **Write report to temp file** using the Write tool (not Bash):
   - File path: `/tmp/research-report-{company}.md`
   - Content: the full report markdown

2. **Run the upload script** using the skill's base directory (shown at the top of this skill when loaded):
```bash
python3 {skill_base_dir}/scripts/upload_to_notion.py \
  --page-id {page_id} \
  --content /tmp/research-report-{company}.md \
  --company-url {url}
```

The script automatically:
- Chunks content by headers
- Converts markdown to Notion blocks
- Uploads in batches with retry logic
- Sets the company favicon icon

**Note:** If re-uploading to an existing page (e.g., after a failure), add `--clear` to remove existing content first.

3. **Clean up:**
```bash
rm /tmp/research-report-{company}.md
```

**Update Properties (if needed)**

If properties weren't set during page creation, use `Notion:notion-update-page` with `command: "update_properties"`.

### 9. Display Summary

```markdown
---
✅ [Company Name] Research Complete

**Company Profile:**
- **URL:** [company URL]
- **Stage:** [stage]
- **Revenue:** [revenue or "Not available"]
- **FTEs:** [FTEs or "Not available"]
- **Industry:** [industry]
- **Categories:** [categories]

**View Entry:** [[Company Name]](notion-page-url)
```

---
