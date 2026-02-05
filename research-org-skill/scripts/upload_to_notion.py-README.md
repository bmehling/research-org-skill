# Research Org Helper Scripts

Helper scripts for the research-org-skill to extend functionality and work around limitations in the Notion MCP tools.

## Scripts

### upload_to_notion.py

Uploads large markdown research reports to Notion pages with custom icons.

**Purpose:** The Notion MCP tools fail when uploading large content blocks (>4000 words). This script reliably uploads reports in chunks while preserving formatting and setting custom company icons.

**Installation:**

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Set up your Notion API key in config.json
#    Edit ~/.claude/skills/research-org-skill/config.json and add:
#    "notion_api": "secret_xxx..."
#    (Get your token from https://www.notion.so/my-integrations)
```

**Usage:**

```bash
python3 upload_to_notion.py \
  --page-id <notion-page-id> \
  --content <path-to-markdown-file> \
  --company-url <company-website-url>
```

**Arguments:**

- `--page-id` (required): Notion page UUID (returned from MCP when creating page)
- `--content` (required): Path to markdown file with full report
- `--company-url` (required): Company website URL (used for favicon)
- `--config` (optional): Path to config.json (auto-finds if omitted)

**Example:**

```bash
python3 upload_to_notion.py \
  --page-id "2f15d568-90e9-81u6-9fac-eff492d320cb" \
  --content "/tmp/company-report.md" \
  --company-url "https://company.com/"
```

**What it does:**

1. **Chunks Content**: Splits markdown by headers (H1, H2) and paragraph boundaries
2. **Converts Formatting**: Preserves headers, bold, links, lists in Notion format
3. **Uploads in Batches**: Uses Notion API to append blocks with retry logic
4. **Sets Icon**: Automatically fetches and sets company favicon on the page

**Output:**

```
📝 Uploading report to Notion (page: 2f15d085-90e9-81b3-9fac-ecc998d320cb)
📄 Content size: 45230 characters

1️⃣ Chunking content by headers...
   → 12 sections found

2️⃣ Converting to Notion blocks...
   → 156 blocks created

3️⃣ Uploading content...
  Batch 1: uploading blocks 1-50... ✓
  Batch 2: uploading blocks 51-100... ✓
  Batch 3: uploading blocks 101-156... ✓

✅ Content uploaded successfully!

4️⃣ Setting page icon...
Setting page icon... ✓

✅ Done! View at: https://notion.so/2f15d085-90e9-81b3-9fac-ecc998d320cb
```

**Error Handling:**

- **Config not found**: Check that config.json exists in `~/.claude/skills/research-org-skill/`
- **API key not set**: Add your Notion integration token to config.json (see README.md)
- **Content file not found**: Verify the markdown file path is correct
- **Upload fails**: Script will retry up to 3 times before giving up

**Integration with research-org-skill:**

The skill calls this script automatically in Step 8 of the workflow:

```bash
python3 upload_to_notion.py \
  --page-id {page_id_from_mcp} \
  --content /tmp/research-report-{timestamp}.md \
  --company-url {company_url}
```

## Configuration 
- (See README.md)

## Requirements

- Python 3.7+
- `requests>=2.31.0` - HTTP client for Notion API
- `markdown-it-py>=3.0.0` - Markdown parsing