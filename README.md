# Research Org - Claude AI Skill for Company Research

A Claude AI skill that conducts company research and automatically integrates findings into your Notion database. Generates structured research reports with extensive citations and automated Notion database population.

## Key Features

- **Structured Workflow**: 9-step guided process from research planning through Notion integration
- **Quality Assurance**: Built-in checklists ensure all reports meet quality standards before publishing
- **Notion Integration**: Automatic database entry creation with proper field categorization
- **Citation Management**: Markdown-formatted source links distributed throughout reports
- **Duplicate Detection**: Prevents duplicate research by checking existing Notion entries
- **Professional Output**: Reports follow specific structural requirements (Company Overview → Executive Team → Funding → Products → Market → Opportunities/Risks)
- **Configurable**: Customizable Notion database credentials and category definitions

## Project Structure

```
research-org/
├── README.md                          # This file
├── config.example.json                # Configuration template
└── research-org-skill/                # Main skill directory
    ├── .gitignore                     # Git configuration
    ├── config.json                    # Active configuration (credentials & settings)
    ├── SKILL.md                       # Complete workflow documentation
    ├── LICENSE.txt                    # Creative Commons BY-SA license
    ├── scripts/                       # Helper scripts
    │   ├── upload_to_notion.py        # Chunked report upload to Notion
    │   ├── upload_to_notion.py-README.md
    │   └── requirements.txt           # Python dependencies
    └── references/                    # Reference documentation
        ├── section_guidelines.md      # Required report sections and ordering
        ├── writing_style.md           # Tone and analytical approach
        ├── category_guide.md          # Product categorization methodology
        ├── valuation_guide.md         # Funding valuation estimation
        └── quality_checklist.md       # Pre-submission validation
```

## Configuration

### Prerequisites

- Claude Code access with the ability to use skills
- A Notion workspace and database
- Notion API token

### Setup Steps

1. **Create a Notion Database**
   - Set up a Notion database in your workspace for research reports
   - Required fields:
     - Organization / Company Name (Title)
     - Category (Multi-select)
     - URL (URL)
     - Industry (Multi-select)
     - Stage (Multi-select)
     - Revenue (Multi-select)
     - FTEs (Multi-select)
     - Created time
     - Created by
     - Last edited time
   - Add your preferred values to each multi-select property. Some examples:

     **Industry:** Horizontal, Healthcare, Legal, Lab Sciences, Manufacturing, FinTech, Consulting, Energy, EdTech, Education

     **Stage:** Seed, Series A, Series B, Series C, Series D, Series E, Series F, Series G, Growth, Bootstrapped, Acquired, Merger

     **Revenue:** < $1M, $1M-$8M, $8M-$30M, $30M-$100M, $100M-$200M, $200M-$500M, $500M-$750M, > $1B, > $2B, > $5B, > $10B, Not available

     **FTEs:** <10, 10-50, 50-100, 100-250, 250-500, 500-1000, >1000, >5000, Not available

2. **Get Notion Credentials**
   - Create an internal Notion integration in your [Notion settings](https://www.notion.so/my-integrations)
     - Be sure to configure the key with permissions to database (at least)
   - Copy your Internal Integration Token
   - Find your Notion Database ID by
     - opening your database and extracting the ID from the URL
       - Example URL: `https://www.notion.so/workspace/[DATABASE_ID]?v=<DATABASE_ID>`
     - OR databases 3-dot menu: Datasources -> Copy data source ID

3. **Configure the Skill**
   - Copy `config.example.json` to `config.json`
   - Edit `config.json` with your credentials and preferences:
   ```json
   {
     "notion": {
       "databaseId": "<your_database_id>",
       "databaseUrl": "<your_database_url>",
       "dataSourceId": "<your_data_source_id>",
       "databaseName": "<your_database_name>",
       "notion_api": "<your_notion_key>"
     },
     "research": {
       "targetWordCount": "2500-4000",
       "defaultModel": "sonnet"
     }
   }
   ```

## Workflow Overview

Research Org follows a structured 9-step workflow:

1. **Load Configuration** — Read config, parse URL and optional `--model` flag
2. **Check for Duplicates** — Query Notion database to prevent duplicate entries
3. **Conduct Research** — Web search and fetch across company background, funding, products, market, and competition
4. **Review Reference Files** — Load section guidelines, writing style, category guide, and valuation guide
5. **Write Report** — Draft full report following section structure and citation guidelines
6. **Prepare Database Fields** — Determine Categories, Industry, Stage, Revenue, and FTEs
7. **Run Quality Checklist** — Validate report against quality_checklist.md before publishing
8. **Create Notion Entry** — Create page with overview, upload full report via helper script, set all properties
9. **Display Summary** — Show completion summary with link to Notion entry

## Reference Materials

The `research-org-skill/references/` directory contains detailed guides:

- **section_guidelines.md** — Exact section order and formatting requirements
- **writing_style.md** — Tone, voice, and analytical standards
- **quality_checklist.md** — Pre-submission validation requirements
- **valuation_guide.md** — Company valuation estimation methodology
- **category_guide.md** — Product categorization approach

## Quality Standards

All research reports must:

- **Meet target word count** from config.json
- **Include 15-30+ sources** cited throughout the report
- **Include all required sections**: Company Overview, Executive Team, Funding, Products, Market, Opportunities/Risks
- **Maintain professional tone** — balanced, objective, and analytical
- **Use accurate citations** with proper markdown links
- **Avoid duplicates** — existing companies are checked before research begins

## License

This project is licensed under the **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)** license. You are free to:
- Use and modify the project
- Redistribute the project with attribution
- Share modifications with the same license

See `research-org-skill/LICENSE.txt` for details.

## Support

For detailed workflow instructions and best practices, see:
- `research-org-skill/SKILL.md` — Complete workflow documentation
- `research-org-skill/references/` — Reference guides

For configuration troubleshooting:
1. Verify Claude Code has access to the skill using the /skills command
2. Verify Notion API token is valid
3. Ensure database ID is correct (test by viewing in browser)
4. Confirm integration has permission to edit database
5. Check that all required fields exist in your Notion database
6. Verify the python helper script executes successfully

---

**Version**: 1.0
**Last Updated**: 2026-02-04
**License**: CC BY-SA 4.0
