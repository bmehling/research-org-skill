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

**1. PARSE COMMAND ARGUMENTS:**

Parse the ARGUMENTS string to extract the URL and optional `--model` flag:

```
Example ARGUMENTS formats:
- "https://camunda.com" → URL only, use default model
- "https://camunda.com --model sonnet" → URL + explicit model
- "https://camunda.com --model opus" → URL + explicit model
- "https://camunda.com --model haiku" → URL + explicit model
```

**Parsing Logic:**
- Regex: Extract URL (first argument that starts with https:// or http://)
- Regex: Check if `--model` flag is present
- If `--model` present: extract the model name (next word after `--model`)
- If invalid model name (not sonnet/opus/haiku): Report error and stop
- If `--model` not present: Will use default from config.json

**PSEUDOCODE:**
```
arguments = <ARGUMENTS string from command>
url = extract_url_from_arguments(arguments)  # First http(s):// URL
model_flag_present = "--model" in arguments

if model_flag_present:
    model_name = extract_after_flag(arguments, "--model")
    if model_name not in ["sonnet", "opus", "haiku"]:
        ERROR: "Invalid model. Must be sonnet, opus, or haiku. Got: {model_name}"
        STOP
    determined_model = model_name
else:
    determined_model = <will get from config.json in step below>
```

**2. LOAD CONFIGURATION FILE:**

Read `config.json` from this skill's directory to load:
- Notion database credentials (databaseId, dataSourceId)
- Valid category options for multi-select fields
- Database name and URL for reference
- Default model setting from `research.defaultModel`

**3. DETERMINE FINAL MODEL:**

```
if determined_model is already set from --model flag:
    use determined_model
else:
    determined_model = config.json["research"]["defaultModel"]

Output confirmation: "Using {determined_model} model for research"
```

**4. VALIDATE URL:**

Confirm the extracted URL is valid:
- Starts with https:// or http://
- Contains a domain name
- If invalid: Report error and stop

**5. STORE DETERMINED MODEL FOR ALL SUBSEQUENT STEPS:**

🔴 **CRITICAL:** The `determined_model` value MUST be used in:
- ALL `Task` tool calls (WebSearch agent, Explore agent, general-purpose agent, etc.)
- Pass as `model: "<determined_model>"` parameter to Task tool
- Document which model is being used in your initial output to user

**Step 1: [REQUIRED] Check for Duplicates**

Check the database to ensure no duplicate entry exists (use the company URL as the unique identifier):
- If duplicate exists: **STOP**, inform user, ask for next steps
- If no duplicate: Proceed to Step 2

**Step 2: [REQUIRED] Conduct Comprehensive Research**

Research the company using web search and fetch tools. **ALWAYS use the determined model from Step 0:**

**Task Tool Calls - ALWAYS include `model` parameter:**
```
Task(
  description: "Research description",
  subagent_type: "Explore|general-purpose|<other>",
  prompt: "...",
  model: "<determined_model>"  ← CRITICAL: Use determined model here
)
```

**Research approach:**
- For complex research: Use `Task` tool with `subagent_type: Explore` and `model: <determined_model>`
- For quick facts: Use `WebSearch` and `WebFetch` tools (these don't require model selection)
- **Collect and save URLs for ALL key sources** (you will link these in the report)
- Focus on: company background, funding, products, market, competition, traction
- Save URLs for: press releases, news articles, company blog posts, investor announcements, analyst reports

**IMPORTANT:** Every Task tool call in this workflow should have `model: "<determined_model>"` to ensure consistent analysis quality throughout the research

---

### Phase 2: Report Structure & Writing (Steps 3-4)

**Step 3: [REQUIRED] Review ALL Reference Files Before Writing**

Before writing a single word, read these reference files in order:

1. **references/section_guidelines.md** - For EXACT section order and detailed writing requirements
2. **references/writing_style.md** - For tone, voice, and approach
3. **references/category_guide.md** - For product categorization methodology
4. **references/valuation_guide.md** - For funding round valuation estimation

**Step 4: [REQUIRED] Write Report Following Exact Section Order**

**BEFORE WRITING:** Confirm you have the `determined_model` from Step 0. You will write the report directly (not using Task tool) with your built-in intelligence enhanced by the model quality specified by the user.

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

**Step 7: [REQUIRED] Create Notion Page with Properties and Overview (Chunked Content Strategy)**

🔴 **CRITICAL:** The full comprehensive report (4,000-5,000+ words) MUST be added using chunked content approach to stay within Notion API payload limits. Do NOT attempt to add the entire report in a single API call.

**7A: Create Page with Brief Overview**

Use `Notion:notion-create-pages` with:
- All database properties (Category, Industry, Stage, Revenue, FTEs) already populated in Step 5
- Only a 2-3 paragraph overview (200-500 words) as initial content
- Set parent to `data_source_id` from config.json
- Organization name and URL

Example:
```json
{
  "parent": {"data_source_id": "1a55d085-90e9-8063-9687-000b0f07dd0c"},
  "pages": [{
    "content": "# Company Overview\n\nBrief 2-3 paragraph summary with key metrics and highlights.\n\nThis provides context while the full research is added in subsequent steps.",
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

**CRITICAL PROPERTY FORMATTING:**
- Multi-select fields MUST be JSON array strings: `"[\"Value1\", \"Value2\"]"` (with escaped quotes)
- URL field is `"userDefined:URL"` in the API
- Data source ID is UUID only (no `collection://` prefix)
- Store the `page_id` returned from this call for Step 7B

**7B: Add Full Report in Sections**

Split the comprehensive report into 6-8 sections (~2,000-3,000 words each):

```
Section 1: Founding Story + Mission and Vision
Section 2: Thesis + Business Model
Section 3: Executive Team + Investors/Funding
Section 4: Products and Services + Partnerships
Section 5: Market Analysis + Competitors
Section 6: Traction + Opportunities and Risks
Section 7: SWOT Analysis
```

For each section, use `Notion:notion-update-page` with `insert_content_after` command:

```json
{
  "page_id": "<page_id_from_7a>",
  "command": "insert_content_after",
  "selection_with_ellipsis": "context while the full research is added in subsequent steps.",
  "new_str": "\n\n## Founding Story\n\nFull section content here (2,000-3,000 words)..."
}
```

**For subsequent sections, use the last unique phrase from the previous section:**

```json
{
  "page_id": "<page_id_from_7a>",
  "command": "insert_content_after",
  "selection_with_ellipsis": "...previous section's last unique phrase",
  "new_str": "\n\n## Next Section Title\n\nNext section content..."
}
```

**Implementation Guidelines:**
- Process sections sequentially (don't insert out of order)
- Use last 20-30 characters of previous section as `selection_with_ellipsis`
- Always start `new_str` with `\n\n` for proper spacing
- If a section fails to insert, the page still contains previous sections
- Retry failed sections without losing progress

See `references/notion_integration.md` "Creating Pages with Large Content" section for detailed examples.

**Step 8: [REQUIRED] Update Database Fields (If Not Done in Step 7A)**

If you haven't already populated all fields in Step 7A, use `Notion:notion-update-page`:

```json
{
  "page_id": "<page_id_from_step_7a>",
  "command": "update_properties",
  "properties": {
    "Category": "[\"AI\", \"Healthcare\"]",
    "Industry": "[\"Healthcare\"]",
    "Stage": "[\"Series B\"]",
    "Revenue": "[\"$8M-$30M\"]",
    "FTEs": "[\"50-100\"]"
  }
}
```

**Verify Success:**
- Page created successfully (Step 7A)
- All sections added successfully (Step 7B)
- All properties populated (Step 8)
- Note the final page URL for user summary

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
- `[actual Notion page URL]` → the Notion page URL from Step 7A
- All field values populated in Steps 7A/8

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

---

## Implementation Reference: Argument Parsing

When executing this skill, follow this pattern to parse arguments and determine the model:

**Step 1: Extract URL**
```javascript
// Match first https:// or http:// URL
const url_match = arguments.match(/https?:\/\/[^\s]+/);
if (!url_match) {
  console.error("ERROR: No valid URL found in arguments");
  return;
}
const url = url_match[0];
```

**Step 2: Check for --model flag**
```javascript
const model_match = arguments.match(/--model\s+(\w+)/);
const specified_model = model_match ? model_match[1] : null;
```

**Step 3: Validate model if specified**
```javascript
const valid_models = ["sonnet", "opus", "haiku"];
if (specified_model && !valid_models.includes(specified_model)) {
  console.error(`ERROR: Invalid model '${specified_model}'. Must be: ${valid_models.join(", ")}`);
  return;
}
```

**Step 4: Load config and determine final model**
```javascript
const config = load_json("./config.json");
const default_model = config.research.defaultModel;
const determined_model = specified_model || default_model;
console.log(`Using ${determined_model} model for research`);
```

**Step 5: Use in Task calls**
```javascript
// All Task calls must include the model parameter
Task({
  description: "...",
  subagent_type: "Explore",
  prompt: "...",
  model: determined_model  // ← CRITICAL: Always use determined model
})
```

---

## ARGUMENTS

This skill receives arguments in the following format:

**Single URL (uses default model from config):**
```
https://camunda.com
```

**URL with explicit model:**
```
https://camunda.com --model opus
```

**ARGUMENT PARSING:**

When invoked, the ARGUMENTS string will contain:
1. The company/organization URL (always present)
2. Optional `--model` flag followed by model name

**Valid Models:**
- `sonnet` - Recommended for most comprehensive research
- `opus` - Frontier model for complex analysis
- `haiku` - Fast, lightweight research

**Parsing Implementation:**
1. Extract URL using regex: `https?://[^\s]+`
2. Check if `--model` flag exists: `--model\s+(\w+)`
3. Validate model is one of: sonnet, opus, haiku
4. If invalid: Report error and stop
5. If no model specified: Use config.json `research.defaultModel`
6. Store determined model and use in ALL Task calls

**Examples of ARGUMENTS:**
- `https://camunda.com` → URL only
- `https://camunda.com --model sonnet` → URL + sonnet model
- `https://camunda.com --model opus` → URL + opus model
- `https://camunda.com --model haiku` → URL + haiku model
- `https://www.example.com --model invalid` → ERROR (invalid model)
