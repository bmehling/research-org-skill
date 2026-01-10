# Notion Integration Reference

---

## ⚠️ QUICK REFERENCE: Two-Step Database Entry Process

### Critical: Creating Page ≠ Populating Fields

When creating a Notion database entry, you MUST perform TWO separate operations:

**Step 1: Create the Page** (`Notion:notion-create-pages`)
- Creates the page with markdown content
- Sets Organization name and URL only
- Multi-select fields (Category, Industry, Stage, Revenue, FTEs) are NOT populated by this call

**Step 2: Update Database Fields** (`Notion:notion-update-page`)
- Populates multi-select properties
- MUST be called after Step 1 completes
- Uses the page_id returned from Step 1

### Working Code Examples

**Step 1: Create Page with Content**

```json
{
  "parent": {
    "data_source_id": "1a55d085-90e9-8063-9687-000b0f07dd0c"
  },
  "pages": [{
    "content": "# Company Overview\n\n[Full markdown report content]...",
    "properties": {
      "Organization": "Company Name",
      "userDefined:URL": "https://www.company.com"
    }
  }]
}
```

**Response from Step 1:**
```json
{
  "page_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "url": "https://notion.so/workspace/Company-Name-a1b2..."
}
```

**Step 2: Update Multi-Select Fields**

```json
{
  "page_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "command": "update_properties",
  "properties": {
    "Category": "[\"Healthcare Analytics\", \"AI\", \"Data Integration\"]",
    "Industry": "[\"Healthcare\"]",
    "Stage": "[\"Series B\"]",
    "Revenue": "[\"$8M-$30M\"]",
    "FTEs": "[\"50-100\"]"
  }
}
```

### Field Formatting Requirements

**Multi-Select Fields** (Category, Industry, Stage, Revenue, FTEs):
- **CRITICAL FORMAT:** Multi-select values must be **JSON-stringified arrays**, not actual JSON arrays
- Format: `"[\"Value1\", \"Value2\"]"` (note the outer quotes and escaped inner quotes)
- ❌ WRONG: `["Value1", "Value2"]` (actual array - this will fail silently)
- ✅ CORRECT: `"[\"Value1\", \"Value2\"]"` (stringified array)
- Use exact values from your config.json categories
- Case-sensitive matching
- Maximum 4-5 categories recommended

**Why Stringified Arrays?**
The Notion MCP tool expects property values as strings. For multi-select fields, this means passing a JSON array that has been converted to a string. When you pass an actual array, it fails without a clear error message.
**Special Field Names:**
- URL field: Use `"userDefined:URL"` in API (not `"URL"`)
- Title field: Use `"Organization"` (or your configured field name)
- Data source ID: UUID only (no `collection://` prefix in create-pages)

### Common Mistakes to Avoid

❌ **WRONG: Trying to set multi-select fields in Step 1**
```json
// This will NOT populate Category, Industry, etc.
{
  "pages": [{
    "properties": {
      "Organization": "Company",
      "userDefined:URL": "https://company.com",
      "Category": ["AI"],  // ← Silently ignored
      "Industry": ["Healthcare"]  // ← Silently ignored
    }
  }]
}
```

❌ **WRONG: Assuming Step 1 populates everything**
```
create-pages → ❌ Expects all fields populated (they're not!)
```

✅ **CORRECT: Two separate, sequential calls**
```
create-pages → (get page_id) → update-page with properties → ✅ All fields populated
```

### Verification After Both Steps

After completing both operations, verify:
- [ ] Page created successfully (Step 1 returned page_id and URL)
- [ ] Content appears in Notion page
- [ ] Organization name and URL properties set
- [ ] Category field shows selected categories
- [ ] Industry field shows selected industries
- [ ] Stage field shows funding stage
- [ ] Revenue field shows revenue range
- [ ] FTEs field shows employee count range

If any multi-select fields are empty after Step 2, check:
1. Field names match your database exactly (case-sensitive)
2. Values exist in your config.json categories array
3. No typos in property names or values

---

[Rest of documentation continues below...]

---

This guide provides technical details for working with your Notion database and understanding the schema and field options for the Research Org Skill.

## Database Configuration

Your database configuration is stored in your local `config.json` file:

```json
{
  "notion": {
    "databaseId": "YOUR_DATABASE_ID",
    "databaseUrl": "https://www.notion.so/YOUR_DATABASE_ID",
    "dataSourceId": "collection://YOUR_DATA_SOURCE_ID",
    "databaseName": "Solutions & Vendors"
  }
}
```

**Important:** See `SETUP.md` for instructions on finding your database credentials.

## Database Fields and Schema

The Research Org Skill expects your Notion database to have the following fields. You can customize the field names and options to match your existing database.

### Title Property (Required)

**Field Name:** Organization  
**Type:** Title (required - this is your primary key)  
**Description:** Company or organization name  
**Example:** "TailorCare", "Cresta", "Salesforce"  

This is the primary identifying field and appears as the page title in Notion.

### URL Field

**Field Name:** URL (or `userDefined:URL` in API)  
**Type:** URL  
**Description:** Company website URL  
**Example:** "https://www.example-company.com"  
**Notes:**
- Used to check for duplicates before creating new entries
- Should be the primary domain (e.g., www.example.com not www.example.com/careers)
- Helps with verification and follow-up research

### Category Field

**Field Name:** Category  
**Type:** Multi-select  
**Description:** Product/solution categories describing what the company does  

**Example Options** (customize to your database):
- AI / Machine Learning
- Voice / Communication
- Agentic / Autonomous
- Real-time / Live
- Analytics / Data
- Automation / Workflow
- Data Integration
- Security / Compliance
- Healthcare (specific vertical)
- SaaS Platform
- Enterprise Software

**Notes:**
- The skill uses the category options from your `config.json`
- You can add new categories if a company doesn't fit existing options
- Typically 2-4 categories per company
- Categories describe WHAT the company does, not WHO uses it

**Custom Categories:** Add domain-specific options for your research focus:
- For healthcare: Patient Engagement, Care Navigation, RCM, EHR integration
- For enterprise: Workforce Management, Customer Experience, Compliance
- For fintech: Payment Processing, Risk Management, Trading

### Industry Field

**Field Name:** Industry  
**Type:** Multi-select  
**Description:** Vertical market focus or industry served  

**Example Options:**
- Horizontal (serves all industries)
- Healthcare
- Financial Services / Banking
- Insurance
- Legal
- Real Estate
- Retail / E-commerce
- Manufacturing
- Telecommunications
- Education
- Government

**Notes:**
- Describes WHO the company primarily serves
- Different from Category (which describes WHAT)
- Many companies serve multiple verticals
- "Horizontal" for companies serving all industries

### Stage Field

**Field Name:** Stage  
**Type:** Multi-select  
**Description:** Company funding stage or maturity level  

**Example Options:**
- Stealth / Private
- Seed
- Series A
- Series B
- Series C
- Series D+
- Late Stage (Series D+)
- Pre-IPO
- Public / IPO
- Acquired
- Defunct / Shutdown

**Notes:**
- Based on latest known funding round
- "Acquired" for companies that were acquired by another
- "Public" for companies that completed IPO
- Update as new information becomes available

### Revenue Field

**Field Name:** Revenue  
**Type:** Multi-select  
**Description:** Estimated or known annual revenue range  

**Example Options:**
- < $1M
- $1M - $5M
- $5M - $10M
- $10M - $50M
- $50M - $100M
- $100M - $500M
- $500M - $1B
- $1B+
- Unknown / Private

**Notes:**
- For public companies, use latest annual revenue
- For private companies, estimate from disclosures or industry sources
- ARR (Annual Recurring Revenue) for SaaS companies
- "Unknown / Private" for companies that don't disclose

### FTEs Field

**Field Name:** FTEs (or Employee Count)  
**Type:** Multi-select  
**Description:** Estimated or known number of full-time employees  

**Example Options:**
- 1 - 10
- 10 - 50
- 50 - 100
- 100 - 250
- 250 - 500
- 500 - 1000
- 1000 - 5000
- 5000+
- Unknown

**Notes:**
- FTE = Full-Time Equivalent
- Use Crunchbase, LinkedIn, or company disclosure if available
- For very large companies, this is last known size
- "Unknown" if not disclosed

---

## Field Management Best Practices

### Adding Custom Fields

You can add additional fields to track information important to your research:

**Recommended Optional Fields:**
- **Founder/CEO** - Text field with primary leader
- **Founded Year** - Date or number field
- **Last Updated** - Date field tracking when research was last updated
- **Notes** - Rich text for additional context
- **Investors** - Text or relation field
- **Market Focus** - Additional multi-select for market segment

### Renaming Fields

If you prefer different field names:

1. Create the fields in your Notion database
2. Update `config.json` to use your field names
3. Update `references/notion_integration.md` to reflect your schema

Example:
```json
// If your field is named "Company" instead of "Organization"
{
  "fieldMapping": {
    "title": "Company",
    "url": "Website",
    "category": "Categories"
  }
}
```

### Managing Category Options

**Adding New Categories:**

1. Add to your Notion database's Category field in Notion UI
2. Add to the `categories` array in your `config.json`:

```json
"categories": [
  "AI",
  "Voice",
  "Agentic",
  "Real-time",
  "Analytics",
  "MyCustomCategory"  // ← Add here
]
```

**Removing Unused Categories:**

1. Remove from `config.json` categories array
2. Optionally remove from Notion UI (won't affect existing entries)

---

## Content Structure in Notion

Each research entry creates a Notion page with:

### Page Properties (top of page)
- Organization (title)
- URL
- Category (multi-select tags)
- Industry (multi-select tags)
- Stage (multi-select tags)
- Revenue (multi-select tags)
- FTEs (multi-select tags)

### Page Content (14 sections)

Markdown-formatted sections including:
1. Company Overview
2. Founding and Background
3. Executive Team
4. Investors, Funding Rounds, and Valuation (includes table)
5. Mission and Vision
6. Products and Services
7. Notable Partnerships and Customers
8. Market (with subsections)
9. Competition
10. Business Model
11. Traction
12. Key Opportunities
13. Key Risks
14. SWOT Analysis

### Formatting in Notion

Research uses **Notion-flavored Markdown** for:
- **Headers** - Section titles (#, ##, ###)
- **Bold** - Key terms and emphasis (**bold**)
- **Lists** - Bullet points and numbered lists
- **Links** - Source citations and references
- **Tables** - Funding rounds, competitors, comparisons
- **Blockquotes** - Important quotes or callouts

All markdown automatically renders in Notion.

---

## Notion API Integration

If you need to programmatically interact with your database:

### Database ID vs Data Source ID

- **Database ID:** The main database identifier in your URL
  - Example: `1a55d08590e9805997ecd7d0b2bda1c4`
  - Used in: `https://www.notion.so/{DATABASE_ID}`

- **Data Source ID:** The collection identifier (for multi-source databases)
  - Example: `collection://1a55d085-90e9-8063-9687-000b0f07dd0c`
  - Used by: Notion API and advanced integrations
  - Get from: Notion API docs or database settings

### Using the Notion API

## Database Field Formats

### Critical: Multi-select Fields Use Array Format

When populating Notion database fields via the API, multi-select fields **must** use array format:

**✓ Correct Format:**
```json
{
  "properties": {
    "Organization": "Function Health",
    "userDefined:URL": "https://www.functionhealth.com",
    "Category": ["Functional Medicine", "Labs", "Healthcare Analytics", "AI", "PHR"],
    "Industry": ["Healthcare"],
    "Stage": ["Series B"],
    "Revenue": ["$30M-$100M"],
    "FTEs": ["250-500"]
  }
}
```

**✗ Incorrect Format:**
```json
{
  "properties": {
    "Category": "Functional Medicine, Labs, Healthcare Analytics, AI, PHR",  // WRONG!
    "Industry": "Healthcare",  // WRONG!
  }
}
```

If building additional integrations:

```
API Endpoint: https://api.notion.com/v1/databases/{database_id}
Authentication: Bearer token with read/write access to your database
Scope: Must have permission to your database
```

Reference: [Notion API Documentation](https://developers.notion.com)

### Creating Pages with Large Content

When creating research pages with comprehensive reports (8,000-12,000+ words), the Notion API has practical limits on single-request content size. To ensure reliable page creation with full research content, use a **chunked content approach**.

#### The Problem

Attempting to create a page with 10,000+ words of content in a single `notion-create-pages` call may fail or timeout due to:
- API payload size limits (~50-100KB)
- Request timeout thresholds
- Markdown processing overhead

#### The Solution: Chunked Content Upload

**Step 1: Create Page with Properties and Brief Overview**

Create the page with all properties populated and a brief 2-3 paragraph overview (200-500 words):

```json
{
  "pages": [{
    "properties": {
      "Organization": "Company Name",
      "userDefined:URL": "https://www.company.com/",
      "Category": "[\"AI\", \"Healthcare\", \"Analytics\"]",
      "Industry": "[\"Healthcare\"]",
      "Stage": "[\"Series B\"]",
      "Revenue": "[\"$30M-$100M\"]",
      "FTEs": "[\"100-250\"]"
    },
    "content": "# Company Overview\n\nBrief 2-3 paragraph summary with key metrics and highlights.\n\nThis provides context while the full research is added in subsequent steps."
  }],
  "parent": {
    "type": "data_source_id",
    "data_source_id": "YOUR_DATA_SOURCE_UUID"
  }
}
```

**Important Property Formatting:**
- Multi-select fields MUST be JSON array strings: `"[\"Value1\", \"Value2\"]"`
- Title field must match your schema exactly (typically `"Organization"`)
- URL field is `"userDefined:URL"` in the API (even if shown as "URL" in Notion)
- Data source ID is UUID only, not prefixed with `collection://`

**Step 2: Split Full Research into Manageable Sections**

Divide your complete research into 6-8 sections, each containing ~2,000-3,000 words:

```
Section 1: Company Overview + Founding & Background
Section 2: Executive Team + Investors/Funding
Section 3: Mission/Vision + Products/Services
Section 4: Partnerships + Market Analysis
Section 5: Competition + Business Model
Section 6: Traction + Key Opportunities
Section 7: Key Risks + SWOT Analysis
```

**Step 3: Add Sections Sequentially with `insert_content_after`**

For each section after the first, use `notion-update-page` with the `insert_content_after` command:

```json
{
  "command": "insert_content_after",
  "page_id": "PAGE_ID_FROM_STEP_1",
  "selection_with_ellipsis": "end of previous section...last few words",
  "new_str": "\n\n# New Section Title\n\nFull section content here..."
}
```

**Key Implementation Details:**

1. **Selection Snippets:** Use the last 20-30 characters of the previous section as your `selection_with_ellipsis` to identify the insertion point. Make it unique enough to avoid ambiguity.

   Example: `"selection_with_ellipsis": "supporting evidence...comprehensive analysis."`

2. **Spacing:** Always include `\n\n` at the start of `new_str` to ensure proper section separation

3. **Sequential Order:** Add sections in order from top to bottom of the research

4. **Error Handling:** If a section fails to insert, you can retry without losing previous sections

#### Example Workflow

```python
# Pseudocode for chunked content approach

# 1. Create page with properties and brief overview
page = create_page(
    properties=formatted_properties,
    content=brief_overview  # 200-500 words
)

# 2. Split full research into sections
sections = [
    founding_and_background,
    executive_team_and_funding,
    mission_products_partnerships,
    market_and_competition,
    business_model_and_traction,
    opportunities_and_risks,
    swot_analysis
]

# 3. Add each section sequentially
for i, section in enumerate(sections):
    # Get unique text from end of previous section
    if i == 0:
        # First section appends after initial overview
        selection = get_last_chars(brief_overview, 30)
    else:
        selection = get_last_chars(sections[i-1], 30)
    
    # Insert section
    update_page(
        page_id=page.id,
        command="insert_content_after",
        selection_with_ellipsis=selection,
        new_str=f"\n\n{section}"
    )
```

#### Benefits of Chunked Approach

1. **Reliability:** Works consistently with reports up to 15,000+ words
2. **Progress Visibility:** Can track which sections have been added
3. **Error Recovery:** Failed section insertions can be retried without restarting
4. **API Limits:** Stays well within Notion API payload and timeout limits
5. **Flexibility:** Easy to adjust section boundaries based on content structure

#### Troubleshooting Chunked Content

**Issue: "Could not find page" error during section insertion**

**Causes:**
- Page creation succeeded but there's a brief propagation delay
- Page ID copied incorrectly

**Solutions:**
1. Add 1-2 second delay after page creation before first insert
2. Verify page ID is exact UUID from creation response
3. Test with `notion-fetch` to confirm page exists before inserting

**Issue: Section inserted in wrong location**

**Causes:**
- `selection_with_ellipsis` text appears multiple times in document
- Not enough characters in selection to be unique

**Solutions:**
1. Use longer selection snippet (30-50 characters instead of 20)
2. Include distinctive words or punctuation from end of previous section
3. If section has a unique table or heading, use that as selection point

**Issue: Formatting lost between sections**

**Causes:**
- Missing `\n\n` spacing between sections
- Markdown syntax issues at section boundaries

**Solutions:**
1. Always include `\n\n` at start of `new_str`
2. Ensure previous section ends with complete markdown (no open tables/lists)
3. Test section boundaries individually if formatting issues appear

#### ❌ What NOT to Do (Common Failures)

**WRONG: Attempting to create page with full 10,000-word report in single call**
```json
{
  "pages": [{
    "content": "# Full Report\n\n[10,000+ words of markdown content here]",
    "properties": {"Organization": "Company"}
  }]
}
```
**Result:** Request timeout, payload limit exceeded, or silently truncated content

**WRONG: Creating page without properties, then trying to add properties later**
```json
// Step 1: Create without properties
{"pages": [{"content": "...", "properties": {"Organization": "Name"}}]}

// Step 2: Try to add properties separately
{"page_id": "xxx", "properties": {"Category": ["AI"]}}
// Result: Fields not updated if not done correctly
```

**WRONG: Using actual JSON arrays instead of JSON strings for multi-select**
```json
{
  "properties": {
    "Category": ["AI", "Healthcare"]  // ← WRONG: actual array
  }
}
```
**Result:** Fields silently ignored, no error message

**RIGHT: Using JSON-stringified arrays**
```json
{
  "properties": {
    "Category": "[\"AI\", \"Healthcare\"]"  // ← CORRECT: stringified
  }
}
```

**WRONG: Inserting sections out of order or with duplicate selections**
```json
// Insert section 3 before section 2
{"selection_with_ellipsis": "section 2 content", "new_str": "section 3..."}
{"selection_with_ellipsis": "section 2 content", "new_str": "section 2..."}
// Result: Section 3 appears before section 2
```

**RIGHT: Insert sequentially, use unique selection points**
```json
// First insert section 2 at known location
{"selection_with_ellipsis": "end of section 1", "new_str": "section 2..."}
// Then insert section 3 at new location
{"selection_with_ellipsis": "end of section 2", "new_str": "section 3..."}
```

---

## Troubleshooting Common Issues

### Issue: "Field not found" error

**Causes:**
- Field name doesn't match your Notion database
- Field type is wrong (e.g., text instead of multi-select)
- Typo in field name

**Solutions:**
1. Verify field exists in Notion database
2. Check exact field name (case-sensitive)
3. Ensure field type matches expectations
4. Check config.json for typos

### Issue: Categories not appearing in Notion

**Causes:**
- Category not in `config.json` categories array
- Typo in category name
- Category field doesn't exist in Notion database

**Solutions:**
1. Add category to `config.json` categories array
2. Verify spelling matches Notion field options exactly
3. Check that Category field exists in your database
4. Clear browser cache and reload Notion

### Issue: Research page created but properties empty

**Causes:**
- Field names don't match your database schema
- Multi-select fields don't have the options being selected
- Database fields are read-only or restricted

**Solutions:**
1. Check field names exactly match your database
2. Verify multi-select options exist in Notion
3. Check database permissions and access
4. Test creating entry manually to verify database accepts data

### Issue: Can't find database ID or data source ID

**Solutions:**
1. See `SETUP.md` Step 2 for detailed instructions
2. Database URL in browser: `https://www.notion.so/{DATABASE_ID}`
3. Data Source ID: Check Notion API docs or contact Notion support
4. Try copying from database view settings (more options → share)

---

## Performance Considerations

### Large Databases

If your Solutions & Vendors database grows large:

**Optimization Tips:**
1. Use database filters to reduce page loads (e.g., filter by date)
2. Archive old entries if needed
3. Create separate views for different analyses
4. Use multi-select filtering for easier browsing

**Database Maintenance:**
1. Periodically review and update outdated research
2. Clean up duplicate entries
3. Archive acquired or defunct companies
4. Keep field options manageable (don't proliferate categories)

### Best Practices

1. **Naming** - Use consistent naming (TitleCase for Company, lowercase for fields)
2. **Dates** - Include date research was conducted or last updated
3. **Archival** - Mark outdated research as archived, don't delete
4. **Relations** - Consider linking related companies (competitors, partners, acquirers)
5. **Backups** - Periodically export your database for backup

---

## Advanced: Custom Database Schema

If you want to customize the database schema significantly:

### Alternative Field Organization

Some users prefer:
```
Company Name (title)
Website URL
Category Tags (multi-select)
Vertical Market (multi-select)
Stage
ARR Estimate
Team Size
Last Research Date
Key Contacts
Notes
```

### Adding Relations

You can add relation fields to link:
- Competitors (relation to other companies)
- Parent/Acquired By (relation to acquirer)
- Investors (relation to investor records)
- Technologies Used (relation to technology database)

### Creating Rollups

Combine with rollups to aggregate data:
- Count of research entries by category
- Latest funding by vertical
- Average team size by stage

---

## Questions?

**For setup help:** See `SETUP.md`

**For database schema:** Check this file

**For Notion-specific questions:** Visit [Notion Help](https://notion.so/help)

**For skill usage:** See `SKILL.md` and `references/section_guidelines.md`

