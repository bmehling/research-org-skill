---
name: research-org-skill
description: Comprehensive company and organization research workflow for any industry or sector. Creates Notion database entries with structured research reports following a balanced, objective, and analytical tone. Requires configuration with your Notion database.
allowed-tools: Read, Write, Edit, Agent, Task, TaskCreate, TaskUpdate, TaskGet, TaskList, ToolSearch, WebSearch, WebFetch, Bash, Glob, Grep, mcp__notion__notion-search, mcp__notion__notion-fetch, mcp__notion__notion-create-pages, mcp__notion__notion-update-page, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-create-pages, mcp__claude_ai_Notion__notion-update-page

---

# Research Org Skill

Comprehensive research workflow for creating detailed company intelligence reports and storing them in a Notion database.

## Command

```
research_org: <url> [--model MODEL] [--lite] [--update]
research_org: --stale [--months N]
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<url>` | Yes | Company website URL to research. In update mode, accepts the Notion page URL as well |
| `--model` | No | Model to use: `sonnet` (default), `opus` (complex), `haiku` (quick) |
| `--lite` | No | Generate a shorter product/market-focused report (omits funding, exec team, SWOT) |
| `--update` | No | Refresh an existing entry: regenerate the report, research changes since it was last researched, and rewrite the page in place |
| `--stale` | No | List entries whose research has gone stale, ranked. Takes no URL. Read-only |
| `--months N` | No | Staleness threshold for `--stale` (default 6) |

**Examples:**
```
research_org: https://camunda.com
research_org: https://camunda.com --model opus
research_org: https://camunda.com --model haiku
research_org: https://camunda.com --lite
research_org: https://camunda.com --lite --model haiku
research_org: https://camunda.com --update
research_org: https://app.notion.com/p/abc123 --update
research_org: --stale
research_org: --stale --months 12
```

---

## Stale Sweep Mode (`--stale`)

An update flag nobody remembers to run is a flag that never runs. This mode produces the worklist. It takes **no URL**, writes nothing, and does not follow the workflow below.

```bash
/usr/bin/python3 {skill_base_dir}/scripts/find_stale.py --months {N}
```

The script ranks entries by how long since they were researched, reading each report's metadata line where one exists and falling back to the page's creation date where it does not. Entries staged `Defunct` or `Acquired` are excluded, because their reports are frozen by design and do not go stale.

**Do not just relay the table.** The script ranks by age alone, which is the one thing it can measure and the least interesting input. Add the judgment it cannot:

- **Weight by stage.** A Seed or Series A company at 9 months is more likely to have changed materially than a Public or Bootstrapped one at 18. Early-stage entries should rise above older but slower-moving ones.
- **Flag thin entries for a fresh run, not an update.** An entry with no Stage, no Compliance, and a short report is often a stub. `--update` regenerates against current guidelines, which usually fixes it, but say when a full fresh run is the better call.
- **Read the model tag.** An entry written by a materially weaker model is a re-run candidate rather than an update candidate, because its gaps are as likely to be analysis failures as real absences.
- **Group, do not list.** Ten rows a person will act on beats a hundred they will not. Lead with a handful worth doing now and say how many remain.

Then offer to run the updates, and **run them one at a time**. Each is a full research run with its own approval gate, so batching them without asking would queue up a long series of writes the user has not seen.

If the sweep dates most entries by creation time, say so: those ages are upper bounds, and they will become exact once each entry has been through one update.

---

## Workflow

The steps below cover create mode and update mode. `--stale` does not use them.

### 1. Load Configuration

1. Read `config.json` from this skill's directory
2. Extract URL from arguments (first `https://` or `http://` match)
3. If `--model` flag present, validate it's `sonnet`, `opus`, or `haiku`
4. Determine final model: `--model` value or `config.research.defaultModel`
5. If `--lite` flag present, set lite mode = true (this selects the Lite Mode column of the word budget in `references/section_guidelines.md`)
6. If `--update` flag present, set update mode = true and read `references/update_guide.md` before doing anything else. Update mode changes steps 2, 3, 5, 7, 8, and 9
7. If `--stale` flag present, skip this workflow entirely and follow the Stale Sweep Mode section above. No URL is required in that mode
8. Use this model in ALL subsequent `Task` tool calls

### 2. Resolve the Target Entry

**Create mode (default).** Query the data source for existing entries with the same URL. If a duplicate exists, stop and ask the user for guidance.

**Update mode (`--update`).** The opposite test: you need to *find* the entry, and finding nothing is the failure.

1. If the argument is a Notion page URL or ID, fetch that page directly.
2. Otherwise query the data source on the `URL` property.
3. If that returns nothing, fall back to a title search on `Organization` using the domain's root word. **A rebranded company will not match on URL, and this is the path that finds it.**
4. On a fuzzy or title match, show the candidate's name, URL, and created date, and confirm before proceeding. Never update a row you matched loosely without asking.
5. If nothing is found, stop. Do not fall through to creating a new entry — that is a different action than the one requested.

Then build the fact ledger from the existing page and establish the baseline date, per Steps B and C of `references/update_guide.md`. The ledger is what makes the rest of the run cheap, and the baseline date is what bounds the research.

Also run the link checker against the existing page before researching — it is the cheapest signal available:

```bash
/usr/bin/python3 {skill_base_dir}/scripts/check_links.py --page-id {page_id}
```

Replace every `DEAD` citation during the regeneration. **Never drop a citation that came back `BLOCKED`**: a 403 or 999 means the server refused a bot, not that the page is gone. Retry one in Chrome only when it is the sole source for a load-bearing fact and is not labeled `login wall`; the full rule is in `references/quality_checklist.md`, Step 2b. A `REDIRECT` to a new host is often the first trace of a rebrand.

### 3. Conduct Research

**In update mode, scope the research first.** Classify the change event (Step D of `references/update_guide.md`), then bound the work:

- **Always dispatch the scout**, with a brief that states the baseline date, lists the ledger's current facts, and asks only for what changed since then. Asking it to report "unchanged" against a known fact is far cheaper than asking it to rediscover the fact.
- **Dispatch the analyst only if** the competitor table is more than 12 months old, a listed competitor had an M&A or shutdown event, or the company pivoted or rebranded into a different market. Otherwise carry the competitor table forward with its dates visible.
- **Always re-check the company's own pages yourself** — homepage, `/pricing`, `/security`, `/about`, and the trust portal. They are cheap, high-yield, and where drift shows first.
- **Watch for silent removals.** A dropped certification, a vanished customer logo, or a retired pricing tier announces nothing. The ledger is what makes them visible.

Everything below applies to both modes.

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
5. `references/update_guide.md` — **Update mode only.** Event playbooks, changelog format, approval gate

### 5. Write Report

**In update mode, regenerate the full report against current guidelines**, carrying forward facts that still hold rather than re-deriving them. A patch-only update preserves prose written against a superseded standard, so the oldest entries would stay the worst ones forever.

Open the regenerated report with the metadata line and a `# What Changed — [date]` section, capped at 200 words including the report history list. Each history line records the model and the agents that produced that generation, as `[opus-5, scout]`. Format and rules are in `references/update_guide.md`, Step G. Always include an "Unchanged" line: a reader needs to know what was checked and found stable.

**Terminal events are the exception.** If the company shut down, went bankrupt, or was absorbed into an acquirer, do NOT regenerate. Freeze the existing body as a historical record, add the closing changelog entry, and flip the properties. See the Terminal events playbook.

**Every report opens with a metadata line**, in both modes. Create mode writes `*Research completed: {date} [{model}, {agents}]*` above the first heading. Without it, the next `--update` has no baseline and re-searches from the page's creation date. Format in `references/section_guidelines.md` under Report Preamble.

**Cross-link competitors already in the database.** Before writing the Key Competitors table, fetch the data source's `Organization` and `URL` columns in a single paginated pass, then match each competitor locally by domain and then by name. Link matched names to their Notion pages in the Company cell, keep the website in the URL cell, and report the coverage count in the summary.

Note the property name differs by interface: it is `userDefined:URL` through the Notion MCP tools and plain `URL` through the REST API.

**Rewrite page links to the `/p/` form.** The SQL query's `url` column comes back as `https://app.notion.com/<id>`, which returns 404. The working link is `https://app.notion.com/p/<id>`. `check_links.py` reports the broken form as `DEAD`, which is accurate.

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
- **Stage** — Seed, Series A, Series B, etc. Also available: `Acquired`, `Public` (post-IPO), `Defunct` (shut down or bankrupt), `Merger`, `Bootstrapped`, `Growth`, `Stealth`
- **Revenue** — Estimate or "Not available"
- **FTEs** — Estimate or "Not available"
- **Compliance** — 0+ from `compliance` array in config.json (HIPAA, SOC2, ISO27001, HITRUST, PCI DSS, FedRamp, GDPR, CCPA, CPRA, PIPEDA, PHIPA, CASA, JTC Telehealth, FDA 21 CFR Part 11). Only include items with credible evidence from the company's trust/security/compliance pages or third-party attestations. Use `None Identified` if no evidence is found.

### 7. Run Quality Checklist

**CRITICAL:** Before creating the database entry, run ALL verification steps in `references/quality_checklist.md` (word count, citation links, dead-link check, structure, database fields, writing quality). Do NOT proceed to step 8 until all checks pass.

**Note:** In lite mode, validate against the lite band (1,200–2,000) rather than the full band (3,200–4,000). Both are stated in `references/section_guidelines.md`.

**Note:** In update mode the changelog is measured along with everything else, so the upper bound rises by 200: **3,200–4,200 (full)** and **1,200–2,200 (lite)**. A frozen terminal-event report is exempt from the word-count and structure checks; say so in the summary rather than reporting a failed check.

### 8. Create or Update the Notion Entry

**Update mode: show the diff and wait for approval before writing.**

Never write to Notion before the user says yes. An update overwrites a page that may carry another person's annotations, and a property flip propagates into every filtered view of the database. Show the full "What Changed" section and a property table (old → new, marking changed rows), then stop. Do not show the regenerated prose unless asked. Flag any *removal* explicitly — a dropped certification is the change most likely to be a research miss rather than a real event.

On approval, upload to the existing `page_id` **with `--clear`**, which is mandatory in update mode: without it the new report appends beneath the old one and the page ends up holding two reports. Pass the **current** URL as `--company-url` so a rebrand refreshes the favicon. Then update properties with `notion-update-page`. Full sequence in `references/update_guide.md`, Step I.

Notion page history retains prior versions, so a bad update is recoverable.

---

**Create mode: Create Page with Overview**

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

2. **Run the upload script** using the skill's base directory (shown at the top of this skill when loaded). Invoke it with `/usr/bin/python3`, not bare `python3`: the Homebrew interpreter on PATH has no `requests` module and fails at import, while the system Python has it. The urllib3 LibreSSL warning it prints is harmless.
```bash
/usr/bin/python3 {skill_base_dir}/scripts/upload_to_notion.py \
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

Include the competitor coverage line in both modes, for example "3 of 8 competitors are already in the database; 5 are not." The missing names are a ready-made research backlog of companies already judged relevant.

**In update mode**, report instead: what changed, what was checked and found unchanged, which properties moved, whether the analyst ran, any dead citations replaced, and anything that could not be verified. An update that found nothing is a valid outcome — say "no material changes since [date]" plainly rather than manufacturing significance.

---
