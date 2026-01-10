---
name: research-org-skill
description: Comprehensive company and organization research workflow for any industry or sector. Creates Notion database entries with structured research reports following a balanced, objective, and analytical tone. Requires configuration with your Notion database.

---

# Research Org Skill

Comprehensive research workflow for creating detailed company and organization intelligence reports and storing them in a Notion database.

## Overview

This skill enables in-depth research of any company or organization and the creation of comprehensive database entries with a single command. It follows a structured reporting format proven effective for organization analysis and strategic intelligence gathering.

The workflow combines web research, critical analysis, and Notion database integration to produce professional-grade research reports that serve as reference materials for strategic decision-making, competitive analysis, and organization evaluation.

## ⚠️ CRITICAL: Always Read config.json First

**Before executing any research_org command, you must:**

1. Read the `config.json` file located in the same directory as this skill's SKILL.md file
2. Use `research.targetWordCount` as the canonical source of the overall report word count requirements
3. Load the Notion database credentials from config.json and use them as the canonical source for all Notion API/Tool calls:
   - `notion.databaseId` - The Notion database ID
   - `notion.dataSourceId` - The data source ID
   - `notion.databaseName` - Name of the target database
   - `categories` - Array of valid category options for multi-select fields

## Command: research_org: <url> [--model MODEL]

**Purpose:** Research a company or organization and create a comprehensive database entry in your configured Notion database

**Parameters:**
- `<url>` (required): Company/organization website URL to research
- `--model MODEL` (optional): Specify Claude model to use (sonnet, opus, haiku). Defaults to value in config.json.
  - `sonnet` - Best for comprehensive research and complex analysis (recommended for most companies)
  - `opus` - Frontier model for extremely complex organizations or research tasks
  - `haiku` - Fast, lightweight research for simple companies or quick analysis

**Examples:**
- `research_org: https://camunda.com`  - Uses config default (typically sonnet)
- `research_org: https://camunda.com --model opus` - Uses Opus for complex research
- `research_org: https://camunda.com --model haiku` - Uses Haiku for quick research

**⚠️ CRITICAL WORKFLOW - Follow Phases in Exact Order:**

### Phase 1: Configuration & Research (Steps 0-2)

**Step 0: [REQUIRED] Load Configuration & Parse Arguments**

1. **Parse Command Arguments:**
   - Extract the URL from arguments (first non-flag argument)
   - Check for `--model` flag to determine which Claude model to use
   - If `--model` present: use specified model (sonnet, opus, or haiku)
   - If `--model` not present: use `research.defaultModel` from config.json (typically sonnet)
   - Store the determined model and use it for ALL subsequent Task tool calls

2. **Load Configuration File:**
   Read `config.json` from this skill's directory to load:
   - Notion database credentials (databaseId, dataSourceId)
   - Valid category options for multi-select fields
   - Database name and URL for reference
   - Default model setting from `research.defaultModel`

**Step 1: [REQUIRED] Check for Duplicates**

Check the database to ensure no duplicate entry exists (use the company URL as the unique identifier):
- If duplicate exists: **STOP**, inform user, ask for next steps
- If no duplicate: Proceed to Step 2

**Step 2: [REQUIRED] Conduct Comprehensive Research**

Research the company using web search and fetch tools. **Use the determined model from Step 0 for all research Task calls:**
- Use `Task` tool with `subagent_type: Explore` for comprehensive codebase/market research with `model: <determined_model>`
- Use `WebSearch` and `WebFetch` tools for gathering information from authoritative sources
- **Collect and save URLs for ALL key sources** (you will link these in the report)
- Focus on: company background, funding, products, market, competition, traction
- Save URLs for: press releases, news articles, company blog posts, investor announcements, analyst reports

---

### Phase 2: Report Structure & Writing (Steps 3-4)

**Step 3: [REQUIRED] Review ALL Reference Files Before Writing**

Before writing a single word, read these reference files in order:

1. **references/section_guidelines.md** - For EXACT section order and detailed writing requirements
2. **references/writing_style.md** - For tone, voice, and approach
3. **references/category_guide.md** - For product categorization methodology
4. **references/valuation_guide.md** - For funding round valuation estimation

**Step 4: [REQUIRED] Write Report Following Exact Section Order**

Write the report following the EXACT structure from references/section_guidelines.md (lines 44-71):

**🔴 CRITICAL: Use This Exact Section Sequence:**

```
# Company Overview
## Founding Story
## Mission and Vision
## Thesis
## Business Model

# Executive Team

# Investors, Funding Rounds, and Valuation
## Funding Rounds (table)
## Valuation Analysis (narrative BELOW table, not inside table)

# Products and Services

# Notable Partnerships and Customers

# Market
## Customer
## Market Size
## Competitive Landscape
## Competitors (table)
## Traction

# Opportunities and Risks
## Key Opportunities
## Key Risks
## SWOT Analysis
```

**🔴 CRITICAL: Add Reference Links Throughout Report**

As you write each section, include source links using markdown syntax `[description](URL)`. If the description is meant to be bolded, use `**[CompanyName](URL)**` (bold wraps the entire link).

- Link funding amounts to press releases or Crunchbase
- Link partnerships to announcement URLs
- Link market data to research reports
- Link competitor names to their websites
- Link key metrics to source articles
- **Target: 15-30+ links distributed throughout the report**

See references/section_guidelines.md lines 14-36 for detailed citation guidelines.

**🔴 CRITICAL: Funding Summary Positioning**

The funding/valuation summary MUST appear BELOW the funding table as separate narrative prose:
- ❌ WRONG: Summary embedded in table footer
- ✅ CORRECT: Table ends, then summary begins as separate paragraphs below

---

### Phase 3: Quality Review & Database Preparation (Steps 5-6)

**Step 5: [REQUIRED] Prepare Database Field Values**

Based on your research, determine:
- **Categories** - Review references/category_guide.md and select 1-4 categories based on explicit product features
- **Industry** - Select from: Healthcare, Horizontal, Legal, etc.
- **Stage** - Determine from funding history: Seed, Series A, Series B, etc.
- **Revenue** - Estimate range or mark "Not available"
- **FTEs** - Estimate employee count range or mark "Not available"

**Step 6: [REQUIRED] Run Quality Checklist - DO NOT SKIP THIS STEP**

⛔ **STOP HERE - Complete This Checklist Before Creating Database Entry**

Read references/quality_checklist.md and verify EACH item below:

**Structure Checks:**
- [ ] Business Model appears as subsection 1d (after Thesis, before Executive Team)
- [ ] All required sections present in correct order
- [ ] No sections missing or out of sequence

**Citation Checks:**
- [ ] Reference links included throughout report (not clustered at end)
- [ ] Funding amounts linked to sources
- [ ] Partnership announcements linked
- [ ] Market data linked to reports with dates
- [ ] Competitor names linked to websites
- [ ] Estimated 15-30+ links total distributed across sections

**Funding/Valuation Checks:**
- [ ] Funding table complete with all known rounds
- [ ] Each round has: Round, Date, Amount, Valuation, Lead Investors
- [ ] Estimated valuations marked with "~$XX (estimated)"
- [ ] Unavailable valuations marked "Not available"
- [ ] **Funding summary appears BELOW table as narrative (not in table)**

**Database Fields Checks:**
- [ ] At least 1 category selected (no more than 4-5)
- [ ] Categories based on explicit product features from research
- [ ] Industry, Stage, Revenue, FTEs determined

**Writing Quality Checks:**
- [ ] Professional, analytical tone throughout
- [ ] Balanced perspective (not promotional)
- [ ] Clear, accessible language
- [ ] No typos or grammatical errors

**✅ If ALL items checked:** Proceed to Phase 4
**❌ If ANY items unchecked:** Fix the report, then re-run this checklist

---

### Phase 4: Notion Database Entry Creation (Steps 7-8)

**Step 7: [REQUIRED] Create Notion Page with Report Content**

Use `Notion:notion-create-pages` to create the page:
- Set parent to `data_source_id` from config.json
- Include full report content in markdown format
- Set page properties: Organization name and URL

Example:
```json
{
  "parent": {"data_source_id": "1a55d085-90e9-8063-9687-000b0f07dd0c"},
  "pages": [{
    "content": "# Company Overview\n\n[full report markdown]...",
    "properties": {
      "Organization": "Company Name",
      "userDefined:URL": "https://company.com"
    }
  }]
}
```

**Step 8: [REQUIRED] Update Database Fields**

Use `Notion:notion-update-page` to populate the multi-select fields:

Example:
```json
{
  "page_id": "<page_id_from_step_7>",
  "command": "update_properties",
  "properties": {
    "Category": ["Healthcare Analytics", "AI"],
    "Industry": ["Healthcare"],
    "Stage": ["Series B"],
    "Revenue": ["$8M-$30M"],
    "FTEs": ["50-100"]
  }
}
```

**IMPORTANT:** Creating the page (Step 7) does NOT automatically populate these fields. You MUST separately update them in Step 8.

See references/notion_integration.md for detailed examples and field formatting.

**Verify Success:**
- Confirm both tool calls succeeded without errors
- Note the page URL returned from Step 7
- Note the field values you set in Step 8

---

### Phase 5: Final Summary (Step 9)

**Step 9: [REQUIRED] Display Research Summary with Favicon URL**

Provide the user with a complete summary following this exact format:

```markdown
---
✅ [Company Name] Research Complete

**Company Profile:**
- **URL:** [actual company URL]
- **Stage:** [actual stage value]
- **Revenue:** [actual revenue value or "Not available"]
- **FTEs:** [actual FTE value or "Not available"]
- **Industry:** [actual industry values]
- **Categories:** [actual category values]
  - Suggested additions: [any suggested new categories, if applicable]

**View Entry:** [[Company Name]]([actual Notion page URL])

**Add Company Logo/Favicon:**

Use this URL to add the company's logo to their Notion entry:

https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=[ACTUAL_COMPANY_URL]

Example: https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://www.functionhealth.com
---
```

**Important:** Replace ALL placeholders with actual values:
- `[Company Name]` → actual company name
- `[actual company URL]` → the actual URL (e.g., https://www.functionhealth.com)
- `[actual Notion page URL]` → the Notion page URL from Step 7
- All field values from Step 8

No further summary is required.

---

## Research Quality Standards

- Provide specific details, data points, and concrete examples **with source links** throughout
- Include quantitative metrics and financial data wherever available with citations
- Cite sources and dates for all key claims; link to primary sources (press releases, analyst reports, news articles)
- Present balanced analysis with both strengths and challenges
- Use clear, professional prose without excessive formatting
- Ground all competitive claims in specific evidence
- When information is unavailable, clearly note this rather than speculating

---

## Usage

```
research_org: <url> [--model MODEL]
```

**Examples:**

```
research_org: https://www.example-company.com
```
Uses the default model specified in config.json (typically sonnet).

```
research_org: https://www.example-company.com --model opus
```
Uses Opus model for complex organizations requiring deeper analysis.

```
research_org: https://www.example-company.com --model haiku
```
Uses Haiku model for quick, lightweight research on straightforward companies.
