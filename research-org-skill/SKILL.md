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
5. If `--lite` flag present, set lite mode = true (this selects the Lite Mode column of the word budget in `references/section_guidelines.md`)
6. Use this model in ALL subsequent `Task` tool calls

### 2. Check for Duplicates

Query the Notion database for existing entries with the same URL. If duplicate exists, stop and ask user for guidance.

### 3. Conduct Research

Dispatch **two subagents in parallel**, split by whether the work needs judgment. Both are read-only (`WebSearch` and `WebFetch` only) and cannot write files or touch Notion. The `--model` flag applies to the main agent only; each subagent's model comes from its own definition.

```
Agent(subagent_type: "research-scout",   prompt: "...")   # haiku  — retrieval
Agent(subagent_type: "research-analyst", prompt: "...")   # sonnet — judgment
```

| Agent | Model | Scope |
|---|---|---|
| `research-scout` | haiku | Company background, founders, funding rounds, products and pricing, compliance, customers, traction. Mechanical extraction — fetch the page, quote the figure, cite the URL. |
| `research-analyst` | sonnet | Competitive landscape and market sizing. Deciding who actually competes and which market figures are defensible needs judgment that retrieval-grade models get wrong. |

**Do not ask the scout to analyze.** Its failures come from being asked to judge credibility, decide what counts as a customer, or assemble competitor sets. Ask it for facts and URLs; do the analysis yourself or route it to the analyst.

**If either agent type is unavailable** (the definitions live in `~/.claude/agents/`, outside this skill — see README), fall back to `subagent_type: "general-purpose"` with an explicit read-only instruction in the prompt: no file writes, no Notion tools, WebSearch and WebFetch only, return text. The tool restriction is then advisory rather than enforced, so verification in the next step matters more.

**Verify before writing — subagent output is leads, not facts.** Observed failures across runs: fabricated customer logos that appeared nowhere on the company's site, a garbled figure ($5.15B where the source said $5.1B), and two certifications reported from a trust center the scout could not actually read. Before drafting, confirm with your own WebFetch:

- Every named customer, against the company's own customers or case study page
- Every headline metric and funding figure, against the primary announcement
- Every compliance claim, against `/security`, `/legal`, and the `trust.<domain>` portal

When a claim exists only in the company's own marketing, attribute it as such in the report rather than stating it as fact.

**Escalate to the browser when a page is JavaScript-rendered.** A fetch that returns 200 with only a page title and header has not failed loudly — it has handed you a shell while the real content waits on scripts that never ran. Trust centers are the common case: `trust.<company>.com` is nearly always a Vanta, Drata, or SafeBase application, and WebFetch will return a header every time.

When a compliance-bearing page returns a shell, load it in Chrome instead. Load the tools in one call:

```
ToolSearch("select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__tabs_close_mcp")
```

Then `tabs_context_mcp{createIfEmpty:true}` → `navigate` → `get_page_text` → `tabs_close_mcp`. Close the tab when done. This is a main-agent step: the scout and analyst are restricted to WebSearch and WebFetch on purpose, and that restriction should not be relaxed to solve this.

**Wait and retry before concluding the page is empty.** `get_page_text` frequently returns `No text content found` on the first call because the app has not finished rendering. That is the same false negative the escalation exists to prevent, one layer deeper. When it happens, `computer{action:"wait", duration:4}` then read again. On `trust.hash.ai` the first read returned nothing and the retry returned the full certification list. Treat an empty first read as "not yet rendered," never as "no content."

**The backstop, whether or not the browser is available:** never write a certification into the Compliance database field that came from a page nobody could read. If Chrome is unavailable or permission is declined, record only what was actually read and state the rest as unverified in the report. An unreadable page is not evidence in either direction — it does not support recording a certification, and it does not support `None Identified` either.

Focus on: company background, funding history, products, market position, competition, traction, and **compliance posture** (regulatory controls like HIPAA, compliance frameworks like SOC2, and 3rd-party accreditations like The Joint Commission). **Save source URLs** for citations in the report.

For compliance, check `/security`, `/compliance`, `/legal`, and footer links on the company's website, plus the **`trust.<domain>` subdomain** — that is where trust portals live (`trust.hash.ai`, `trust.reducto.ai`), while `<domain>/trust` usually 404s and proves nothing. `/security` is normally the only page that links to it. Look for badges/attestations on the homepage. **Third-party trust portals (Vanta, Drata, SafeBase) are JavaScript applications and cannot be read by fetch** — reaching one means switching to the browser path above, not treating the shell as the answer. Quote the exact wording, since "SOC 2 Type 2 certified", "follows the criteria set forth by the SOC 2 Framework", and "SOC 2 aligned" are three different claims. Only record certifications with credible evidence — do not assume HIPAA compliance just because a vendor sells to healthcare. Use `None Identified` only when the relevant pages were actually read and named nothing, never when they could not be reached.

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

**⚠️ WORD BUDGET: use the Lite Mode column of the word budget table in `references/section_guidelines.md`.** Section prose sums to ~1,340 words, tables add ~400, so the finished report should measure ~1,740. Validation band is 1,200–2,000 words. Respect the table row and cell caps in `section_guidelines.md`, and write each section to its stated budget rather than drafting long and trimming.

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

**⚠️ WORD BUDGET: use the Full Mode column of the word budget table in `references/section_guidelines.md`.** Each section carries its own `**Word Budget:**` line. Section prose sums to ~3,120 words, tables add ~550, so the finished report should measure ~3,670. Validation band is 3,200–4,000 words.

**Budget the tables too.** Table cell text escapes the section budgets but still counts toward the total, and it is the most common cause of overrun. `references/section_guidelines.md` sets row caps and per-cell word limits for the Funding, Product Overview, and Key Competitors tables. Respect them: more rows than the cap means rank and cut, not extend.

Write each section to its stated budget as you draft it. Drafting long and trimming afterward costs many iterations of tedious editing. Run the mid-draft checkpoint after the Market section, when all three tables are written.

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
- **Compliance** — 0+ from `compliance` array in config.json (HIPAA, SOC2, ISO27001, HITRUST, PCI DSS, FedRamp, GDPR, CCPA, CPRA, PIPEDA, PHIPA, CASA, JTC Telehealth, FDA 21 CFR Part 11). Only include items with credible evidence from the company's trust/security/compliance pages or third-party attestations. Use `None Identified` if no evidence is found.

### 7. Run Quality Checklist

**CRITICAL:** Before creating the database entry, run ALL verification steps in `references/quality_checklist.md` (word count, citation links, structure, database fields, writing quality). Do NOT proceed to step 8 until all checks pass.

**Note:** In lite mode, validate against the lite band (1,200–2,000) rather than the full band (3,200–4,000). Both are stated in `references/section_guidelines.md`.

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
      "FTEs": "[\"500+\"]",
      "Compliance": "[\"SOC2\", \"HIPAA\"]"
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
- **Compliance:** [compliance items, or "None Identified"]

**View Entry:** [[Company Name]](notion-page-url)
```

---
