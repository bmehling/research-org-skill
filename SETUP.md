# Setup Guide for Research Org Skill

This guide walks you through configuring the Research Org Skill for your Notion database.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Prepare Your Notion Database](#step-1-prepare-your-notion-database)
3. [Step 2: Find Your Database Credentials](#step-2-find-your-database-credentials)
4. [Step 3: Configure the Skill](#step-3-configure-the-skill)
5. [Step 4: Install the Skill](#step-4-install-the-skill)
6. [Step 5: Test the Skill](#step-5-test-the-skill)
7. [Security Considerations](#security-considerations)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- **Notion Account** - With a workspace you control
- **Notion Workspace Admin Access** - To create/modify databases and get API credentials
- **Claude Access** - Claude Haiku 4.5 or later (with skill installation capability)
- **Text Editor** - To edit `config.json`

---

## Step 1: Prepare Your Notion Database

### Option A: Create a New Database (Recommended for Testing)

1. Open [Notion](https://notion.so)
2. Click "Add a page" → Select "Database" → Choose "Table"
3. Name your database "Solutions & Vendors" (or your preferred name)
4. Create the following fields:

| Field Name | Type | Description |
|------------|------|-------------|
| Organization | Title | Company/organization name (primary field) |
| URL | URL | Company website URL |
| Category | Multi-select | Product/service categories (e.g., AI, Voice, Data) |
| Industry | Multi-select | Vertical focus (e.g., Healthcare, SaaS, Financial) |
| Stage | Multi-select | Funding stage (e.g., Seed, Series A, Series B) |
| Revenue | Multi-select | Revenue range (e.g., $1M-$10M, $10M-$50M) |
| FTEs | Multi-select | Employee count range (e.g., 10-50, 50-200) |

5. Configure your **Category** field options:
   - Click on "Category" column header → "Edit property"
   - Add your desired categories (see `config.example.json` for suggestions)
   - Common options: AI, Voice, Agentic, Real-time, Analytics, Automation, Data, Security

### Option B: Use Your Existing Database

If you already have a research database, ensure it has at minimum:
- A **Title field** for the organization name
- A **URL field** for the company website
- **Multi-select fields** for Category, Industry, Stage, Revenue, and FTEs

You can add missing fields later.

---

## Step 2: Find Your Database Credentials

You need three pieces of information to configure the skill:

### A. Database URL

1. Open your database in Notion
2. Look at your browser address bar
3. Copy the URL structure:
   ```
   https://www.notion.so/WORKSPACE_NAME/DATABASE_ID?v=VIEW_ID
   ```
4. Extract the **DATABASE_ID** (long alphanumeric string before `?v=`)
   - Example: `1as455d08930e98053847ecd7d0b2bdl1c4`

### B. Data Source ID (Collection ID)

The data source ID identifies the specific collection within your database.

**Method 1: Via Notion API Documentation (Most Reliable)**

1. Go to [Notion Developers](https://developers.notion.com)
2. Create an integration (or use existing one)
3. Go to your database in Notion
4. Share the database with your integration
5. Visit [Notion API Reference](https://developers.notion.com/reference/get-database)
6. Test your connection and look at the response
7. Find the `id` field - this is your **data source ID**
8. Format it as: `collection://{id}`

**Method 2: Via Notion UI (View Settings)**

1. Open your database
2. Click the "..." (more options) near database name
3. Select "Copy link to database"
4. The database ID is in the URL
5. From Notion's internal data, the collection ID is typically the same or similar

**Method 3: Contact Notion Support**

If you have difficulty finding your data source ID, Notion support can provide it.

### C. Verify Your Credentials

Create a test to ensure you have the right information:

```
Database URL: https://www.notion.so/1as455d08930e98053847ecd7d0b2bdl1c4
Database ID: 1as455d08930e98053847ecd7d0b2bdl1c4
Data Source ID: collection://1a77d085-91e9-8563-9697-000b0f07rr0c
```

---

## Step 3: Configure the Skill

### A. Create Your config.json

1. Navigate to the research-org-skill directory
2. Copy the template file:
   ```bash
   cp config.example.json config.json
   ```
3. Open `config.json` in your text editor

### B. Fill In Your Credentials

Edit `config.json` with your information:

```json
{
  "notion": {
    "databaseId": "1as455d08930e98053847ecd7d0b2bdl1c4",
    "databaseUrl": "https://www.notion.so/1as455d08930e98053847ecd7d0b2bdl1c4",
    "dataSourceId": "collection://1a77d085-91e9-8563-9697-000b0f07rr0c",
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
    "Automation",
    "Data",
    "Security",
    "Compliance"
  ]
}
```

### C. Customize Categories

Update the `categories` array to match your Notion database's Category field options:

```json
"categories": [
  "AI",
  "Voice",
  "Agentic",
  "Real-time",
  "Analytics",
  "Automation",
  "Data",
  "Security",
  "Compliance",
  "Healthcare",
  "Financial Services",
  "Legal"
]
```

### D. Verify the Configuration

- [ ] `databaseId` is 32 characters (alphanumeric)
- [ ] `databaseUrl` matches your actual Notion database URL
- [ ] `dataSourceId` starts with `collection://`
- [ ] `categories` array matches your Notion field options
- [ ] `config.json` is valid JSON (use an online JSON validator if unsure)

### E. Secure Your Configuration

**IMPORTANT:** `config.json` contains your database credentials and should be kept private.

✅ **DO:**
- Keep `config.json` in `.gitignore` (it already is)
- Never commit `config.json` to version control
- Treat it like a password or API key
- Back it up securely if you want a copy

❌ **DON'T:**
- Share `config.json` publicly
- Commit it to GitHub or other public repositories
- Email it unencrypted
- Paste it in chat or forums

---

## Step 4: Install the Skill

### For Claude.ai

**Upload to Claude**
   - Open Claude.ai
   - Go to Settings → Custom Skills (or appropriate menu)
   - Upload the `.skill` file
   - Confirm the skill is installed

### For Other Environments

Refer to your specific Claude integration's documentation for skill installation.

---

## Step 5: Test the Skill

### A. Run a Test Research

1. Open Claude (same chat where you installed the skill)
2. Run the command:
   ```
   research_org: https://www.example-company.com
   ```
   (Use a real company URL, not literally "example-company.com")

3. The skill should:
   - Research the company using web search
   - Compile research findings
   - Create a new entry in your Notion database
   - Display the Notion URL of the created entry

### B. Verify the Result

1. Open your Notion database
2. Look for a new entry with the company name
3. Verify that:
   - [ ] Organization name is populated
   - [ ] URL field has the company website
   - [ ] Category field has appropriate categories selected
   - [ ] Industry field has been populated
   - [ ] Stage field reflects the company's funding stage
   - [ ] All 14 sections of the research report are present

### C. Troubleshoot Issues

If the research doesn't appear in Notion:
- Check your `config.json` credentials
- Verify the database URL matches your actual database
- Ensure the data source ID is correctly formatted
- Check that categories in `config.json` match your Notion field options

See [Troubleshooting](#troubleshooting) below for more help.

---

## Security Considerations

### Protecting Your Credentials

Your `config.json` contains:
- Notion database ID
- Data source/collection ID
- Your database name

While these aren't passwords, they do identify your personal Notion workspace.

**Best Practices:**

1. **Version Control Security**
   - `config.json` is in `.gitignore` (don't remove it!)
   - Never commit credentials to any repository
   - If you accidentally commit, remove it from history

2. **Access Control**
   - Only install the skill on trusted Claude instances
   - Don't share your `config.json` with others
   - If installing on shared systems, use separate configs per user

3. **Least Privilege**
   - If using Notion API tokens, create one with minimal permissions
   - Grant read/write only to the necessary database
   - Consider using separate workspaces for sensitive research

4. **Backup & Recovery**
   - Safely back up your `config.json` if you value this configuration
   - Store backup separately from your main system
   - Test recovery to ensure backups work

### If Credentials Are Compromised

1. Remove or rename your `config.json`
2. Change your Notion workspace security settings if needed
3. Create new database credentials/IDs if your Notion workspace includes sensitive data
4. Reinstall the skill with new credentials

---

## Troubleshooting

### Issue: "Database not found" or "Invalid credentials"

**Solutions:**
1. Verify `databaseId` matches the URL (no extra characters, correct case)
2. Verify `dataSourceId` format: `collection://...` (no extra characters)
3. Test by opening your Notion database URL in browser - does it load?
4. Check that config.json is valid JSON (no missing commas, quotes)

### Issue: Research created but missing fields

**Solutions:**
1. Check that your Notion database has all expected fields (Organization, URL, Category, etc.)
2. Verify field names exactly match your Notion database
3. Ensure multi-select fields (Category, Industry, Stage) have the expected options
4. Check that `categories` array in config.json matches your Notion Category options

### Issue: Skill doesn't appear in Claude

**Solutions:**
1. Confirm you packaged the skill correctly with the skill-creator script
2. Check that `.skill` file was created
3. Try re-uploading the skill file
4. Ensure Claude version supports custom skills (Haiku 4.5+)
5. Check Claude documentation for your specific platform

### Issue: Research quality is poor or incomplete

**Solutions:**
1. Check that all 14 sections appear (see references/section_guidelines.md)
2. Verify research includes citations and reference links
3. For funding rounds, check that valuation estimation methodology was applied
4. Review the company's actual website and investor announcements for missing data
5. Consider running research_org again with additional search context

### Issue: Categories not being selected appropriately

**Solutions:**
1. Review references/category_and_valuation_guide.md for category selection methodology
2. Verify your `categories` array in config.json matches Notion field options
3. Check that categories are being selected based on product keywords
4. Compare against similar companies in your database for consistency
5. Consider expanding the `categories` array with additional relevant options

### Issue: Valuation estimation seems off

**Solutions:**
1. Review the "Valuation Estimation Methodology" section in the research
2. Check that all disclosed valuations were identified correctly
3. Verify the raise:valuation ratio calculation (Amount / Valuation)
4. Ensure estimated valuations are marked with "~" and methodology noted
5. See references/category_and_valuation_guide.md Part 2 for estimation details

### Getting Help

1. **For Skill Issues**
   - Review SKILL.md and SETUP.md in the research-org-skill directory
   - Check references/notion_integration.md for Notion-specific guidance
   - Consult references/section_guidelines.md for research quality standards

2. **For Notion Issues**
   - Visit [Notion Support](https://notion.so/help)
   - Check Notion database settings and field configuration
   - Verify your workspace has necessary permissions

3. **For Claude Issues**
   - Check Claude documentation for skill installation
   - Verify you're using supported Claude version
   - Consult Claude support channels

---

## Next Steps

Once your skill is configured and tested:

1. **Customize Categories** - Add domain-specific categories for your research
2. **Run Research** - Start researching companies of interest
3. **Build Database** - Create comprehensive database of Solutions & Vendors
4. **Refine Methodology** - Adjust category selection and research focus as needed
5. **Share Insights** - Use your research database for strategic decisions

---

## Configuration Reference

For detailed information on each configuration option, see:
- `config.example.json` - Template with all available options
- `references/notion_integration.md` - Notion-specific field guidance
- `references/category_and_valuation_guide.md` - Category selection and valuation strategies
- `references/section_guidelines.md` - Research section requirements

