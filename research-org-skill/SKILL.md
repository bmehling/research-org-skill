---
name: research-org-skill
description: Comprehensive company and organization research workflow for any industry or sector. Creates Notion database entries with structured research following Contrary Research depth and analytical style. Requires configuration with your Notion database.

---

# Research Org Skill

Comprehensive research workflow for creating detailed, [Contrary Research-style](https://research.contrary.com/company) company and organization intelligence reports and storing them in a Notion database.

## Overview

This skill enables in-depth research of any company or organization and the creation of comprehensive database entries with a single command. It follows a structured reporting format proven effective for organization analysis and strategic intelligence gathering.

The workflow combines web research, critical analysis, and Notion database integration to produce professional-grade research reports that serve as reference materials for strategic decision-making, competitive analysis, and organization evaluation.

## ⚠️ CRITICAL: Always Read config.json First

**Before executing any research_org command, you must:**

1. Read the `config.json` file located in the same directory as this skill's SKILL.md file
2. Load the Notion database credentials from config.json:
   - `notion.databaseId` - The Notion database ID
   - `notion.dataSourceId` - The data source ID
   - `categories` - Array of valid category options for multi-select fields
   - `notion.databaseName` - Name of the target database
3. Use these values as the canonical source for all Notion API/Tool calls

## Command: research_org: <url>

**Purpose:** Research a company or organization and create a comprehensive database entry in your configured Notion database

**What it does:**

0. **Load configuration:** Read `config.json` from the same directory as this SKILL.md to get:
   - Notion database credentials (databaseId, dataSourceId)
   - Valid category options for multi-select fields
   - Database name and URL for reference
1. Check the database to ensure no duplicate entry exists (use the company URL as the unique identifier) to prevent duplicates
2. Research the company using web search and information fetching from multiple sources
3. Review and follow the reference guidelines:
   - (see references/writing_style.md)
   - (see references/section_guidelines.md)
   - (see references/category_guide.md)
   - (see references/valuation_guide.md)
   - (see references/quality_checklist.md)
4. Compile comprehensive findings following the structured section format (see references/section_guidelines.md)
5. Select appropriate database Categories based on product analysis (see references/category_guide.md)
6. Estimate missing funding valuations using ratio methodology where applicable (see references/valuation_guide.md)
7. Perform final review of the the completed research using the Quality Checklist (see references/quality_checklist.md) before finalizing the entry
8. Create a new entry in the configured Notion database
9. Populate database fields with research findings (Category, Industry, Stage, Revenue, FTEs)
10. Provide a summary of the research and the Notion URL for final review and manual icon/favicon addition (see Final Step below)

**Usage:**

```
research_org: <url>
```

**Example:**

```
research_org: https://www.example-company.com
```

## Research Quality Standards

- Follow Contrary Research's depth and analytical style (see references/writing_style.md)
- Provide specific details, data points, and concrete examples **with source links** throughout
- Include quantitative metrics and financial data wherever available with citations
- Cite sources and dates for all key claims; link to primary sources (press releases, analyst reports, news articles)
- Present balanced analysis with both strengths and challenges
- Use clear, professional prose without excessive formatting
- Ground all competitive claims in specific evidence
- When information is unavailable, clearly note this rather than speculating

## Report Structure Overview

The research report follows this section organization (closely follow the detailed guidance in references/section_guidelines.md):

1. **Company Overview** - Clear description of what the company does, who they serve, value proposition
2. **Founding Story** - Origin story, founding team, key pivots
3. **Executive Team** - Key leaders with background and expertise
4. **Investors, Funding Rounds, and Valuation** - Funding history with table including estimated valuations, key investors, valuation trends
5. **Products and Services** - Detailed breakdown of offerings, features, use cases
6. **Notable Partnerships and Customers** - Market validation and go-to-market strength
7. **Market** - Customer profiles and Market Size subsections
8. **Competition** - Competitive landscape overview and competitor comparison table
9. **Business Model** - Revenue streams, pricing, unit economics, sales motion
10. **Traction** - Growth metrics, milestones, partnerships, team growth
11. **Key Opportunities** - major growth opportunities with strategic analysis
12. **Key Risks** - major risks with mitigation considerations
13. **SWOT Analysis** - Strengths, Weaknesses, Opportunities, Threats assessment per section

## Final Step: Summary of work, suggestions, and URL to add the company's favico (logo)

After the Notion page is created and populated with research content, display a summary of the research and generate* the URL to add the company's favico (logo) following this template:

--- 
Company Profile:

* URL: <Organization URL>
* Stage: <Organization Stage>
* Revenue: <Organization revenue (if known)>
* FTEs: <Company employees>
* Industry: <Organization Industries>
* Categories: <Organization Categories>
   * Suggested additional categories: <Suggested additional categories>

View the entry: [Organization Name](URL to Notion entry) in Notion

Use this URL to add the companies logo to their Notion entry: 
   https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=<company_url>
---

* Example of how to generate the URL: `https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://www.example-company.com`
