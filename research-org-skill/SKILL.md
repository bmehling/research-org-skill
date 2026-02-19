---
name: research-org-skill
description: Comprehensive company and organization research workflow for any industry or sector. Creates Notion database entries with structured research reports following a balanced, objective, and analytical tone. Requires configuration with your Notion database.

---

# Research Org Skill

Comprehensive research workflow for creating detailed company intelligence reports and storing them in a Notion database.

## Command

```
research_org: <url> [--model MODEL]
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<url>` | Yes | Company website URL to research |
| `--model` | No | Model to use: `sonnet` (default), `opus` (complex), `haiku` (quick) |

**Examples:**
```
research_org: https://camunda.com
research_org: https://camunda.com --model opus
research_org: https://camunda.com --model haiku
```

---

## Workflow

### 1. Load Configuration

1. Read `config.json` from this skill's directory
2. Extract URL from arguments (first `https://` or `http://` match)
3. If `--model` flag present, validate it's `sonnet`, `opus`, or `haiku`
4. Determine final model: `--model` value or `config.research.defaultModel`
5. Use this model in ALL subsequent `Task` tool calls

### 2. Check for Duplicates

Query the Notion database for existing entries with the same URL. If duplicate exists, stop and ask user for guidance.

### 3. Conduct Research

Research the company using web search and fetch tools. Pass the determined model to all Task calls:

```
Task(
  subagent_type: "Explore",
  model: <determined_model>,
  prompt: "..."
)
```

Focus on: company background, funding history, products, market position, competition, traction. **Save source URLs** for citations in the report.

### 4. Review Reference Files

Before writing, read these files in order:
1. `references/section_guidelines.md` — Section order and guidance
2. `references/writing_style.md` — Tone, style and approach
3. `references/category_guide.md` — Product categorization
4. `references/valuation_guide.md` — Funding valuation estimation

### 5. Write Report

Follow the section guidlines: `references/section_guidelines.md`

 - match the section structure
 - review the purpose of each section and sub-section
 - follow the section's prompt, examples, and suggested length
 - follow citiation guidance

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
  ## Market Size
  ## Competitive Landscape
  ## Competitors (table)
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

### 5.5. Verify Word Count

**CRITICAL:** Before proceeding, verify the report meets word count requirements.

1. **Count words and check against config target:**
```bash
# Get target range from config.json
TARGET_RANGE=$(grep -o '"targetWordCount"[[:space:]]*:[[:space:]]*"[^"]*"' config.json | cut -d'"' -f4)
MIN_WORDS=$(echo $TARGET_RANGE | cut -d'-' -f1)
MAX_WORDS=$(echo $TARGET_RANGE | cut -d'-' -f2)

# Count words in report
WORD_COUNT=$(wc -w < /tmp/research-report-{company}.md | tr -d ' ')

echo "📊 Word count: $WORD_COUNT"
echo "🎯 Target range: $TARGET_RANGE"

if [ $WORD_COUNT -lt $MIN_WORDS ]; then
    echo "⚠️  Under minimum - expand thin sections"
elif [ $WORD_COUNT -gt $MAX_WORDS ]; then
    echo "❌ OVER LIMIT - MUST revise before proceeding"
else
    echo "✅ Within target range"
fi
```

2. **Revision strategy if over word count:**
   - Review each section against paragraph guidelines in `references/section_guidelines.md`
   - **Paragraph limits are MAXIMUMS, not targets** - aim for lower end of ranges
   - Cut redundant analysis, excessive examples, and repetitive context
   - Combine similar points and consolidate overlapping ideas
   - Keep all citations and data; reduce explanatory prose
   - Each paragraph should be 80-120 words (3-5 sentences maximum)

3. **Common areas to trim:**
   - Competitive Landscape: Often over-written with excessive competitor detail
   - Market sections: Cut verbose market descriptions, keep quantitative data
   - Opportunities/Risks: Be concise - 2-3 sentences per item maximum
   - SWOT: Brief bullets only (1-2 sentences each)

**Do NOT proceed to step 6 until word count is verified within range.**

### 6. Prepare Database Fields

Determine values for:
- **Categories** — 1-4 from `references/category_guide.md`
- **Industry** — Healthcare, Horizontal, Legal, etc.
- **Stage** — Seed, Series A, Series B, etc.
- **Revenue** — Estimate or "Not available"
- **FTEs** — Estimate or "Not available"

### 7. Run Quality Checklist

Before creating the database entry and writing the temporary report.md file, verify the report using the `references/quality_checklist.md`

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

1. **Write report to temp file:**
```bash
cat > /tmp/research-report-{company}.md << 'EOF'
# {Company Name} Research Report
[Full markdown content]
EOF
```

2. **Run the upload script** (from skill directory):
```bash
python3 scripts/upload_to_notion.py \
  --page-id {page_id} \
  --content /tmp/research-report-{company}.md \
  --company-url {url}
```

The script automatically:
- Chunks content by headers
- Converts markdown to Notion blocks
- Uploads in batches with retry logic
- Sets the company favicon icon

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
