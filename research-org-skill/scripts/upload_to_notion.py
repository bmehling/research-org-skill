#!/usr/bin/env python3
"""
upload_to_notion.py - Upload research report content to Notion page

Uploads large markdown research reports to Notion pages in chunks,
preserving formatting and setting custom company icons.

Usage:
    python upload_to_notion.py --page-id <id> --content <file> --company-url <url>
    python upload_to_notion.py --page-id <id> --content <file> --company-url <url> --config /path/to/config.json
"""

import argparse
import json
import sys
import time
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import requests


NOTION_API_VERSION = "2022-06-28"
NOTION_BASE_URL = "https://api.notion.com/v1"
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds


class NotionUploader:
    """Handles uploading markdown content to Notion pages via API"""

    def __init__(self, api_key: str, page_id: str):
        """Initialize uploader with API credentials

        Args:
            api_key: Notion integration token (secret_xxx format)
            page_id: Notion page UUID
        """
        self.api_key = api_key
        self.page_id = page_id
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_API_VERSION
        }

    def chunk_markdown_by_headers(self, content: str) -> List[Dict]:
        """Split markdown into chunks by headers

        Splits on # (H1) and ## (H2) headers. If a section exceeds
        2000 characters, splits at paragraph boundaries.

        Args:
            content: Full markdown report content

        Returns:
            List of {header_level, title, content} dicts
        """
        chunks = []

        # Split on H1 and H2 headers (capturing group)
        # Result alternates: [preamble, header1, body1, header2, body2, ...]
        sections = re.split(r'^(#{1,2}\s+.+?)$', content, flags=re.MULTILINE)

        # Handle any preamble text before the first header
        if sections[0].strip():
            chunks.append({
                "header_level": 1,
                "title": "",
                "content": sections[0].strip()
            })

        # Walk header-body pairs starting at index 1, stepping by 2
        i = 1
        while i < len(sections):
            header_line = sections[i]
            body = sections[i + 1] if i + 1 < len(sections) else ""

            header_level = len(header_line) - len(header_line.lstrip('#'))
            title = header_line.lstrip('#').strip()

            # If body is too large, split at paragraph boundaries.
            # Only the first sub-chunk gets the title; subsequent ones omit it
            # to avoid duplicate headers in Notion.
            if len(body) > 2000:
                paragraphs = body.split('\n\n')
                current_chunk = ""
                first_chunk = True
                for para in paragraphs:
                    if len(current_chunk) + len(para) > 2000:
                        if current_chunk:
                            chunks.append({
                                "header_level": header_level,
                                "title": title if first_chunk else "",
                                "content": current_chunk.strip()
                            })
                            first_chunk = False
                        current_chunk = para
                    else:
                        current_chunk += "\n\n" + para if current_chunk else para
                if current_chunk:
                    chunks.append({
                        "header_level": header_level,
                        "title": title if first_chunk else "",
                        "content": current_chunk.strip()
                    })
            else:
                chunks.append({
                    "header_level": header_level,
                    "title": title,
                    "content": body.strip()
                })
            i += 2

        return chunks

    def markdown_to_notion_blocks(self, chunk: Dict) -> List[Dict]:
        """Convert markdown chunk to Notion block format

        Handles: headers, paragraphs, links, bold, lists, tables

        Args:
            chunk: {header_level, title, content} dict

        Returns:
            List of Notion block dicts
        """
        blocks = []

        # Add header for this section
        if chunk["title"]:
            header_level = chunk["header_level"]
            block_type = f"heading_{header_level}"
            blocks.append({
                "object": "block",
                "type": block_type,
                block_type: {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": chunk["title"]}
                        }
                    ]
                }
            })

        # Process content
        content = chunk["content"]

        # Pre-process: ensure sub-headers (### and deeper) are their own
        # paragraphs.  Without this, a ### heading followed immediately by
        # bullets (no blank line) collapses into a single paragraph and the
        # entire block is emitted as a heading in Notion.
        content = re.sub(r'(?m)^(#{3,}\s+.+)$', r'\n\n\1\n\n', content)
        content = re.sub(r'\n{3,}', '\n\n', content)  # collapse triple+ newlines

        # Split into paragraphs
        paragraphs = content.split('\n\n')

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # Sub-headers (### or deeper within body content)
            if re.match(r'^#{1,6}\s+', para):
                level = len(para) - len(para.lstrip('#'))
                level = min(level, 3)  # Notion only supports heading_1 through heading_3
                heading_text = para.lstrip('#').strip()
                block_type = f"heading_{level}"
                blocks.append({
                    "object": "block",
                    "type": block_type,
                    block_type: {
                        "rich_text": [{"type": "text", "text": {"content": heading_text}}]
                    }
                })

            # Bulleted lists
            elif para.startswith('- ') or para.startswith('* '):
                list_items = [re.sub(r'^[-*]\s+', '', line.strip()) for line in para.split('\n') if line.strip().startswith(('- ', '* '))]
                for item in list_items:
                    blocks.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": self._parse_inline_formatting(item)
                        }
                    })

            # Numbered lists
            elif re.match(r'^\d+[\.\)]\s+', para):
                for line in para.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                    item_text = re.sub(r'^\d+[\.\)]\s+', '', line)
                    blocks.append({
                        "object": "block",
                        "type": "numbered_list_item",
                        "numbered_list_item": {
                            "rich_text": self._parse_inline_formatting(item_text)
                        }
                    })

            # Markdown tables — convert rows to paragraphs (Notion table API is complex)
            elif para.startswith('|'):
                for line in para.split('\n'):
                    line = line.strip()
                    if not line or re.match(r'^\|[\s\-|:]+\|$', line):
                        continue  # skip separator rows
                    # Strip outer pipes and join cells with " | "
                    cells = [c.strip() for c in line.strip('|').split('|')]
                    row_text = ' | '.join(cells)
                    blocks.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": self._parse_inline_formatting(row_text)
                        }
                    })

            # HTML tables — parse <table> tags and convert to Notion table blocks
            elif para.strip().startswith('<table'):
                table_blocks = self._parse_html_table(para)
                blocks.extend(table_blocks)

            # Regular paragraph
            else:
                rich_text = self._parse_inline_formatting(para)
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": rich_text
                    }
                })

        return blocks

    def _parse_inline_formatting(self, text: str) -> List[Dict]:
        """Parse inline markdown formatting (bold, links, etc)

        Handles nested formatting like **[link](url) more bold text**

        Args:
            text: Text with markdown formatting

        Returns:
            List of Notion rich text dicts (segments with different formatting)
        """
        segments = []

        # Step 1: Split by bold markers ** to identify bold vs non-bold regions
        # Example: "Hello **[link](url) world** bye"
        #   -> ["Hello ", "[link](url) world", " bye"]
        #   -> is_bold: [False, True, False]
        parts = re.split(r'\*\*', text)

        for i, part in enumerate(parts):
            if not part:
                continue

            is_bold = (i % 2 == 1)  # Odd indices are inside ** markers

            # Step 2: Within each part, parse links
            link_segments = self._parse_links_in_segment(part, is_bold)
            segments.extend(link_segments)

        # If no segments created, return whole text as plain
        if not segments:
            segments.append({
                "type": "text",
                "text": {"content": text}
            })

        return segments

    def _parse_links_in_segment(self, text: str, is_bold: bool) -> List[Dict]:
        """Parse links within a text segment, applying bold if specified

        Args:
            text: Text that may contain [link](url) patterns
            is_bold: Whether this segment is inside ** markers

        Returns:
            List of Notion rich text dicts
        """
        segments = []
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'

        last_end = 0
        for match in re.finditer(link_pattern, text):
            # Add plain text before this link
            if match.start() > last_end:
                plain_text = text[last_end:match.start()]
                if plain_text:
                    segment = {
                        "type": "text",
                        "text": {"content": plain_text}
                    }
                    if is_bold:
                        segment["annotations"] = {"bold": True}
                    segments.append(segment)

            # Add the link
            link_text = match.group(1)
            link_url = match.group(2)
            segment = {
                "type": "text",
                "text": {
                    "content": link_text,
                    "link": {"url": link_url}
                }
            }
            if is_bold:
                segment["annotations"] = {"bold": True}
            segments.append(segment)

            last_end = match.end()

        # Add remaining text after last link
        if last_end < len(text):
            remaining = text[last_end:]
            if remaining:
                segment = {
                    "type": "text",
                    "text": {"content": remaining}
                }
                if is_bold:
                    segment["annotations"] = {"bold": True}
                segments.append(segment)

        # If no links found, return whole text as one segment
        if not segments and text:
            segment = {
                "type": "text",
                "text": {"content": text}
            }
            if is_bold:
                segment["annotations"] = {"bold": True}
            segments.append(segment)

        return segments

    def _parse_html_table(self, html: str) -> List[Dict]:
        """Parse HTML table and convert to Notion table block

        Handles <table header-row="true"> format used in skill templates.

        Args:
            html: HTML table string

        Returns:
            List of Notion blocks (table block with rows)
        """
        blocks = []

        # Extract rows from <tr>...</tr> tags
        row_pattern = r'<tr[^>]*>(.*?)</tr>'
        rows = re.findall(row_pattern, html, re.DOTALL | re.IGNORECASE)

        if not rows:
            # Fallback: return as plain text if parsing fails
            clean_text = re.sub(r'<[^>]+>', ' ', html)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            return [{
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": clean_text}}]
                }
            }]

        # Check if first row is header
        has_header = 'header-row="true"' in html.lower() or 'header-row=true' in html.lower()

        # Parse each row into cells
        table_rows = []
        for row_html in rows:
            # Extract cells from <td>...</td> tags
            cell_pattern = r'<td[^>]*>(.*?)</td>'
            cells = re.findall(cell_pattern, row_html, re.DOTALL | re.IGNORECASE)

            if cells:
                # Clean up cell contents and parse inline formatting
                row_cells = []
                for cell in cells:
                    # Remove any nested HTML tags, preserve text
                    cell_text = re.sub(r'<[^>]+>', '', cell).strip()
                    row_cells.append(cell_text)
                table_rows.append(row_cells)

        if not table_rows:
            return blocks

        # Determine table width (max columns in any row)
        table_width = max(len(row) for row in table_rows)

        # Build Notion table block
        table_children = []
        for i, row_cells in enumerate(table_rows):
            # Pad row to table width if needed
            while len(row_cells) < table_width:
                row_cells.append("")

            # Build cells with rich_text
            cells_rich_text = []
            for cell_text in row_cells:
                cells_rich_text.append(self._parse_inline_formatting(cell_text))

            table_children.append({
                "object": "block",
                "type": "table_row",
                "table_row": {
                    "cells": cells_rich_text
                }
            })

        # Create table block with children
        table_block = {
            "object": "block",
            "type": "table",
            "table": {
                "table_width": table_width,
                "has_column_header": has_header,
                "has_row_header": False,
                "children": table_children
            }
        }

        blocks.append(table_block)
        return blocks

    def clear_page_content(self) -> bool:
        """Delete all existing blocks from the page

        Returns:
            True if successful, False otherwise
        """
        print("Clearing existing page content...", end=" ", flush=True)

        try:
            # Get all block children
            url = f"{NOTION_BASE_URL}/blocks/{self.page_id}/children"
            response = requests.get(url, headers=self.headers, timeout=30)

            if response.status_code != 200:
                print(f"✗ (failed to get blocks: HTTP {response.status_code})")
                return False

            blocks = response.json().get("results", [])

            if not blocks:
                print("(no content to clear) ✓")
                return True

            # Delete each block
            deleted = 0
            for block in blocks:
                block_id = block.get("id")
                if block_id:
                    delete_url = f"{NOTION_BASE_URL}/blocks/{block_id}"
                    del_response = requests.delete(delete_url, headers=self.headers, timeout=10)
                    if del_response.status_code == 200:
                        deleted += 1

            print(f"({deleted} blocks removed) ✓")
            return True

        except Exception as e:
            print(f"✗ ({str(e)})")
            return False

    def upload_content(self, blocks: List[Dict]) -> Tuple[bool, List[str]]:
        """Upload content blocks to Notion page

        Uploads blocks in batches with retry logic. Batches are limited
        to 100 blocks per API call (Notion limit).

        Args:
            blocks: List of Notion block dicts

        Returns:
            (success: bool, failed_indices: list of failed block indices)
        """
        if not blocks:
            print("No blocks to upload")
            return True, []

        failed_indices = []
        total_blocks = len(blocks)
        batch_size = 50  # Conservative batch size

        print(f"Uploading {total_blocks} blocks in batches of {batch_size}...")

        for batch_num, i in enumerate(range(0, total_blocks, batch_size)):
            batch = blocks[i:i + batch_size]
            batch_end = min(i + batch_size, total_blocks)

            print(f"  Batch {batch_num + 1}: uploading blocks {i + 1}-{batch_end}...", end=" ", flush=True)

            success = False
            for attempt in range(MAX_RETRIES):
                try:
                    url = f"{NOTION_BASE_URL}/blocks/{self.page_id}/children"

                    payload = {"children": batch}

                    response = requests.patch(
                        url,
                        headers=self.headers,
                        json=payload,
                        timeout=30
                    )

                    if response.status_code == 200:
                        print("✓")
                        success = True
                        break
                    else:
                        error_msg = response.json().get("message", f"HTTP {response.status_code}")
                        if attempt < MAX_RETRIES - 1:
                            print(f"(retry {attempt + 1}/{MAX_RETRIES}) ", end="", flush=True)
                            time.sleep(RETRY_DELAY * (attempt + 1))
                        else:
                            print(f"✗ {error_msg}")
                            for block_idx in range(i, batch_end):
                                failed_indices.append(block_idx)

                except requests.exceptions.RequestException as e:
                    if attempt < MAX_RETRIES - 1:
                        print(f"(retry {attempt + 1}/{MAX_RETRIES}) ", end="", flush=True)
                        time.sleep(RETRY_DELAY * (attempt + 1))
                    else:
                        print(f"✗ {str(e)}")
                        for block_idx in range(i, batch_end):
                            failed_indices.append(block_idx)

        success = len(failed_indices) == 0
        return success, failed_indices

    def set_icon(self, company_url: str) -> bool:
        """Set page icon using company favicon

        Uses Google's favicon service to fetch company logo.

        Args:
            company_url: Company website URL

        Returns:
            True if successful, False otherwise
        """
        # Generate favicon URL
        favicon_url = f"https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url={company_url}"

        try:
            print("Setting page icon...", end=" ", flush=True)

            url = f"{NOTION_BASE_URL}/pages/{self.page_id}"

            payload = {
                "icon": {
                    "type": "external",
                    "external": {"url": favicon_url}
                }
            }

            response = requests.patch(
                url,
                headers=self.headers,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                print("✓")
                return True
            else:
                print(f"✗ (HTTP {response.status_code})")
                return False

        except Exception as e:
            print(f"✗ ({str(e)})")
            return False


def load_config(config_path: Optional[Path]) -> Dict:
    """Load configuration from config.json

    Args:
        config_path: Path to config.json (None = auto-find)

    Returns:
        Configuration dict

    Raises:
        SystemExit if config not found or API key missing
    """
    if config_path:
        config_file = Path(config_path)
    else:
        # Auto-find: one level up from scripts/ into research-org-skill/
        script_dir = Path(__file__).parent
        config_file = script_dir.parent / "config.json"

    if not config_file.exists():
        print(f"ERROR: config.json not found at {config_file}", file=sys.stderr)
        print(f"Try: python upload_to_notion.py --config /path/to/config.json", file=sys.stderr)
        sys.exit(1)

    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {config_file}: {str(e)}", file=sys.stderr)
        sys.exit(1)

    api_key = config.get("notion", {}).get("notion_api", "").strip()
    if not api_key or api_key.startswith("<") or api_key.startswith("ntn_your"):
        print("ERROR: notion.notion_api not set in config.json", file=sys.stderr)
        print("Steps to fix:", file=sys.stderr)
        print("  1. Go to https://www.notion.so/my-integrations", file=sys.stderr)
        print("  2. Create new integration: 'Research Org Upload Helper'", file=sys.stderr)
        print("  3. Copy the 'Internal Integration Token' (starts with 'ntn_')", file=sys.stderr)
        print("  4. Add to config.json: {\"notion\": {\"notion_api\": \"ntn_xxx...\"}}", file=sys.stderr)
        sys.exit(1)

    return config


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Upload research report to Notion page",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python upload_to_notion.py --page-id abc123def456 --content report.md --company-url https://example.com
  python upload_to_notion.py --page-id abc123def456 --content report.md --company-url https://example.com --clear
  python upload_to_notion.py --page-id abc123def456 --content report.md --company-url https://example.com --config /path/to/config.json
        """
    )

    parser.add_argument("--page-id", required=True, help="Notion page UUID")
    parser.add_argument("--content", required=True, help="Path to markdown file with report content")
    parser.add_argument("--company-url", required=True, help="Company website URL (for favicon)")
    parser.add_argument("--config", help="Path to config.json (default: auto-find in skill directory)")
    parser.add_argument("--clear", action="store_true", help="Clear existing page content before uploading")

    args = parser.parse_args()

    # Validate inputs
    content_file = Path(args.content)
    if not content_file.exists():
        print(f"ERROR: Content file not found: {args.content}", file=sys.stderr)
        sys.exit(1)

    # Load config and get API key
    config = load_config(Path(args.config) if args.config else None)
    api_key = config["notion"]["notion_api"]

    # Read content
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Could not read content file: {str(e)}", file=sys.stderr)
        sys.exit(1)

    if not content.strip():
        print("ERROR: Content file is empty", file=sys.stderr)
        sys.exit(1)

    # Create uploader and process
    print(f"\n📝 Uploading report to Notion (page: {args.page_id})")
    print(f"📄 Content size: {len(content)} characters")

    uploader = NotionUploader(api_key, args.page_id)

    # Clear existing content if requested
    if args.clear:
        print("\n0️⃣ Clearing existing content...")
        uploader.clear_page_content()

    # Chunk the content
    print("\n1️⃣ Chunking content by headers...")
    chunks = uploader.chunk_markdown_by_headers(content)
    print(f"   → {len(chunks)} sections found")

    # Convert to Notion blocks
    print("\n2️⃣ Converting to Notion blocks...")
    all_blocks = []
    for chunk in chunks:
        blocks = uploader.markdown_to_notion_blocks(chunk)
        all_blocks.extend(blocks)
    print(f"   → {len(all_blocks)} blocks created")

    # Upload blocks
    print("\n3️⃣ Uploading content...")
    success, failed_indices = uploader.upload_content(all_blocks)

    if not success:
        print(f"\n⚠️ Upload completed with errors ({len(failed_indices)} blocks failed)")
        print(f"Failed block indices: {failed_indices}")
    else:
        print("\n✅ Content uploaded successfully!")

    # Set icon
    print("\n4️⃣ Setting page icon...")
    uploader.set_icon(args.company_url)

    # Final summary
    print(f"\n{'✅' if success else '⚠️'} Done! View at: https://notion.so/{args.page_id}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
