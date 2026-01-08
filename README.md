# Research Org Skill

A comprehensive Claude skill for conducting in-depth company and organization research, creating structured reports, and storing results in your Notion database.

**Status:** Fully functional, ready for configuration and use.

## Overview

Research Org Skill automates the process of:

1. **Researching companies** - Deep web research with multiple sources
2. **Analyzing products & markets** - Industry positioning, competitive landscape, market sizing
3. **Evaluating funding** - Funding history with valuation estimation methodology
4. **Creating reports** - Professional 14-section intelligence reports in Contrary Research style
5. **Storing in Notion** - Automatic database entry creation with categorization

The skill is domain-agnostic - works for researching any company in any industry (healthcare, SaaS, fintech, enterprise software, etc.).

## Key Features

✅ **Comprehensive Research** - 8,000-12,000 word structured reports with 14 sections
✅ **Smart Categorization** - Intelligent category selection based on product analysis
✅ **Valuation Estimation** - Missing funding valuations estimated using ratio methodology
✅ **Source Attribution** - References and links throughout for verification
✅ **Notion Integration** - Automatic database entry creation with rich field population
✅ **Configurable** - Works with your existing or new Notion database

## Quick Start

### 1. Prerequisites

- Claude with skill support
- Notion account with workspace admin access
- Text editor for JSON configuration

### 2. Setup (5 minutes)

```bash
# 1. Clone or download the skill
git clone research-org-skill

# 2. Copy configuration template
cp config.example.json config.json

# 3. Fill in your Notion database credentials
# Edit config.json with:
#   - Your Notion database ID
#   - Your data source ID
#   - Your database's category options

# 4. Install the skill in Claude
# Package and upload research-org-skill.skill

# 5. Test it!
# In Claude, prompt: research_org: https://www.example.com
```

See `SETUP.md` for detailed step-by-step instructions.

### 3. Usage

Once configured, use the skill by asking Claude:

```
research_org: https://www.example-company.com
```

The skill will:
- Research the company across multiple sources
- Analyze their products, market, competitors, and financials
- Create a comprehensive report
- Store it in your Notion database
- Provide the link for review

## What You Get

### Research Report

1. Company Overview
2. Founding and Background
3. Executive Team
4. Investors, Funding Rounds, and Valuation
5. Mission and Vision
6. Products and Services
7. Notable Partnerships and Customers
8. Market (Customer profiles + sizing)
9. Competition
10. Business Model
11. Traction
12. Key Opportunities
13. Key Risks
14. SWOT Analysis

### Notion Database Entry

Automatically populated fields:
- **Organization** - Company name
- **URL** - Company website
- **Category** - Multi-select (AI, Voice, Analytics, etc.)
- **Industry** - Vertical focus (Healthcare, SaaS, etc.)
- **Stage** - Funding stage
- **Revenue** - Revenue range
- **FTEs** - Employee count

Full research content in Notion page with all 14 sections and links.

## Research Quality

The skill produces research following **Contrary Research standards**:

- **Depth** - Comprehensive analysis across multiple dimensions
- **Accuracy** - Primary sources, verified data, clear citations
- **Balance** - Strengths AND weaknesses, opportunities AND risks
- **Clarity** - Professional prose accessible to broad audience
- **Actionability** - Insights that inform strategic decisions

## Special Features

### Valuation Estimation

When company valuations aren't disclosed, the skill estimates them using:

1. **Raise:Valuation Ratio** - Calculate ratio from disclosed rounds
2. **Median Ratio** - Find median across multiple known rounds
3. **Estimation** - Apply ratio to estimate missing valuations
4. **Transparency** - Mark clearly with methodology documented

Example:
- Series C: $80M raised at $1.6B valuation (5% ratio)
- Series A/B: 20% ratio
- Seed estimate: $2M / 0.20 = ~$10M (estimated)

### Category Selection

The skill systematically selects categories by:

1. **Extracting Keywords** - AI, Voice, Real-time, Automation, etc.
2. **Mapping to Categories** - Converting keywords to database options
3. **Validating** - Checking consistency with similar companies
4. **Multi-Select** - Typically 2-4 relevant categories

### Source Attribution

Research includes reference links throughout:

- Company website, press releases, news coverage
- Analyst reports and market research
- Funding announcements and investor profiles
- Product pages, demos, and case studies
- Competitive products and comparisons

## Configuration

### Getting Started

See `SETUP.md` for complete configuration guide, including:

- Creating or preparing your Notion database
- Finding your database ID and data source ID
- Creating and securing `config.json`
- Installing and testing the skill

### Configuration File

`config.json` (created from `config.example.json`):

```json
{
  "notion": {
    "databaseId": "YOUR_DATABASE_ID",
    "databaseUrl": "https://www.notion.so/YOUR_DATABASE_ID",
    "dataSourceId": "collection://YOUR_DATA_SOURCE_ID",
    "databaseName": "Solutions & Vendors"
  },
  "research": {
    "sections": 14,
    "targetWordCount": "8000-12000",
    "reportStyle": "contrary-research"
  },
  "categories": [
    "AI",
    "Voice",
    "Agentic",
    "Real-time",
    "Analytics",
    "Automation"
  ]
}
```

**Security:** `config.json` is in `.gitignore` - never share or commit to version control.

## Documentation

- **SETUP.md** - Complete configuration and installation guide
- **SKILL.md** - Skill definition and usage documentation
- **references/section_guidelines.md** - Detailed guidance for each research section
- **references/category_and_valuation_guide.md** - Category selection and valuation methodology
- **references/writing_style.md** - Writing standards and best practices
- **references/notion_integration.md** - Notion database field reference
- **config.example.json** - Configuration template with all options

## Architecture

**Code (Public):**
- SKILL.md - Skill logic and workflow
- references/ - Guidelines and best practices
- Documentation - Setup, usage, and quality standards

**Configuration (Private, Local):**
- config.json - Your Notion credentials
- Not in repository, in .gitignore

**Data (Private, Yours):**
- Notion database - Your research entries
- Your workspace, your control

## File Structure

```
research-org-skill/
├── README.md                         ← You are here
├── SETUP.md                          ← Start here for setup
├── SKILL.md                          ← Skill definition
├── config.example.json               ← Configuration template (shared)
├── config.json                       ← Your configuration (NOT shared, .gitignore)
├── .gitignore                        ← Protects config.json
├── LICENSE                           ← MIT or similar
└── references/
    ├── section_guidelines.md         ← Research section guidance
    ├── category_and_valuation_guide.md ← Category & valuation methodology
    ├── writing_style.md              ← Writing standards
    └── notion_integration.md         ← Notion field reference
```

## Getting Help

### Setup Issues

1. Review `SETUP.md` - Step-by-step instructions
2. Check Troubleshooting section in `SETUP.md`
3. Verify config.json is valid JSON

### Research Quality Issues

1. See `references/section_guidelines.md` for quality standards
2. Check that all 14 sections are present
3. Verify citations and links are included

### Category & Valuation Issues

1. See `references/category_and_valuation_guide.md`
2. Review similar companies for consistency
3. Verify valuation methodology documented

### Notion Issues

1. Check database field names match exactly
2. Verify category options match config.json
3. See Notion support for workspace issues

## Contributing

Found improvements? Have suggestions?

This is a shared skill - improvements benefit everyone:

1. **Improve documentation** - Clearer setup, better examples
2. **Add category mappings** - New industries or domains
3. **Enhance research methodology** - Better analysis or data extraction
4. **Fix issues** - Bug fixes, edge cases

Contributions are welcome while maintaining:
- ✅ No hardcoded private data
- ✅ Generic, domain-agnostic approach
- ✅ Clear separation of code and configuration
- ✅ Comprehensive documentation

## License

MIT License - See LICENSE file for details.

Free to use, modify, and share.
