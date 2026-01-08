# Quality Checklist - MANDATORY REVIEW BEFORE DATABASE ENTRY

## ⚠️ STOP - Complete This Checklist Before Creating Notion Entry

This checklist must be completed BEFORE running `Notion:notion-create-pages`. If any item fails, fix the report first.

---

## Section 1: Structure & Completeness

### Section Order
- [ ] **CRITICAL:** Business Model appears as subsection 1d (after Thesis, before Executive Team)
- [ ] All required sections present in this exact order:
  - [ ] Company Overview
  - [ ] Founding Story (subsection of Overview)
  - [ ] Mission and Vision (subsection of Overview)
  - [ ] Thesis (subsection of Overview)
  - [ ] Business Model (subsection of Overview) ← Must be here, not at end
  - [ ] Executive Team
  - [ ] Investors, Funding Rounds, and Valuation
  - [ ] Products and Services
  - [ ] Notable Partnerships and Customers
  - [ ] Market (with Customer, Market Size, Competitive Landscape, Competitors subsections)
  - [ ] Traction
  - [ ] Key Opportunities
  - [ ] Key Risks
  - [ ] SWOT Analysis (with Strengths, Weaknesses, Opportunities, Threats subsections)

### Section Quality
- [ ] Each section meets minimum length guidelines (see references/section_guidelines.md)
- [ ] Sections flow logically from one to next
- [ ] No duplicate information across sections
- [ ] All subsections properly nested under parent sections

---

## Section 2: Citations & Evidence

### Reference Links Throughout Report

**Critical Check:** Count your links. You should have 15-30+ links distributed throughout.

- [ ] **Company Overview** includes 2-3 links to company website, major announcements, or news articles
- [ ] **Funding amounts** linked to press releases, Crunchbase, or investor announcements
- [ ] **Partnership announcements** linked to PR sources or company blog posts
- [ ] **Market size data** linked to research reports with publication dates (Gartner, Forrester, etc.)
- [ ] **Competitor names** in competitor table linked to their websites
- [ ] **Key metrics** (revenue, customers, growth rates) linked to source articles or filings
- [ ] **Product features** linked to product pages or technical documentation where relevant
- [ ] **Executive backgrounds** linked to LinkedIn profiles where appropriate
- [ ] Links distributed throughout report (not clustered at end or in one section)
- [ ] Estimated 15-30+ total links across all sections

### Evidence Quality
- [ ] All quantitative claims have sources or are marked as estimates
- [ ] Dates provided for all time-sensitive information
- [ ] No unsupported speculation or claims
- [ ] When information unavailable, clearly noted rather than guessed

---

## Section 3: Funding & Valuation

### Funding Table Format
- [ ] All funding rounds in chronological order
- [ ] Each row has: Round name, Date, Amount, Valuation, Lead Investors
- [ ] Valuations marked as "~$XX (estimated)" when using ratio method
- [ ] Valuations marked as "Not available" when insufficient data exists
- [ ] M&A activity included in timeline if applicable (as separate row)
- [ ] Table uses proper markdown table format with header row
- [ ] Lead investors column includes meaningful context (not just names)

### Valuation Summary Position

**Critical Check:** Verify summary is BELOW table, not inside it.

- [ ] **Funding summary appears BELOW the table** as separate narrative prose (not embedded in table footer or final row)
- [ ] Summary includes total funding amount across all rounds
- [ ] Summary mentions key lead investors with their significance explained
- [ ] Summary describes valuation trajectory with growth rates or comparisons
- [ ] Summary is proper narrative prose (2-3 paragraphs minimum, not bullet points)
- [ ] Summary analyzes what funding/valuation reveals about company progress

**Visual Check:**
```
Your markdown should look like this:

</table>

← Blank line here

**Total Funding:** $XXM across N rounds...

The company has attracted... [narrative continues]
```

**NOT like this:**
```
<tr><td colspan="5">Total Funding: $XXM</td></tr>  ← WRONG
</table>
```

---

## Section 4: Database Fields Preparation

### Categories
- [ ] At least 1 category selected from references/category_guide.md
- [ ] No more than 4-5 categories (more becomes less useful)
- [ ] Categories based on EXPLICIT product features mentioned in research (not assumptions)
- [ ] Categories consistent with similar companies already in database (if known)
- [ ] Primary category clearly reflects main offering/core business

### Other Fields Determined
- [ ] **Industry** selected: Healthcare, Horizontal, Legal, or other (from config.json)
- [ ] **Stage** determined from funding history: Seed, Series A, Series B, Growth, etc.
- [ ] **Revenue** range estimated from research or marked "Not available"
- [ ] **FTEs** (employee count) range estimated from research or marked "Not available"

**Preparation Check:**
Before proceeding, you should have prepared these exact values ready to populate:
- Category: [list specific values]
- Industry: [list specific values]
- Stage: [list specific values]
- Revenue: [specific range or "Not available"]
- FTEs: [specific range or "Not available"]

---

## Section 5: Writing Quality

### Professional Standards
- [ ] Professional, analytical tone throughout (not promotional or marketing-like)
- [ ] Balanced perspective showing both strengths/opportunities AND weaknesses/risks
- [ ] Clear, accessible language (jargon explained when necessary)
- [ ] Consistent formatting and style across all sections
- [ ] No typos or grammatical errors
- [ ] Proper capitalization of company names, products, and proper nouns

### Markdown Formatting
- [ ] Headers properly formatted using # ## ### syntax
- [ ] Tables render correctly with proper header rows
- [ ] Links formatted correctly as [text](url)
- [ ] No broken markdown syntax (mismatched tags, unclosed elements)
- [ ] Proper use of bold, italics, code blocks where appropriate
- [ ] Consistent indentation and spacing

---

## Section 6: Final Verification

### Content Completeness
- [ ] Report word count 7,000-10,000 words (comprehensive depth)
- [ ] Each major section substantive (not placeholder text)
- [ ] Thesis section articulates clear investment case
- [ ] SWOT analysis synthesizes earlier findings (not introducing new information)
- [ ] Opportunities and Risks sections identify 3-5 items each with substance

### Accuracy Check
- [ ] Company name spelled correctly throughout
- [ ] Founding year correct
- [ ] Executive names and titles accurate
- [ ] Funding amounts match source materials
- [ ] Competitor information factually accurate
- [ ] No contradictions between sections

---

## ✅ CHECKLIST COMPLETE - READY TO CREATE DATABASE ENTRY

**If ALL items above are checked:**
✅ Proceed to create Notion page with `Notion:notion-create-pages`
✅ Then update database fields with `Notion:notion-update-page`
✅ Then provide final summary with favicon URL

**If ANY items are unchecked:**
❌ FIX the report before creating database entry
❌ Re-run this checklist after fixes
❌ Do NOT proceed to database creation with unchecked items

---

## After Database Entry Creation

After creating the Notion page and updating fields, verify:

- [ ] Notion page created successfully (no errors)
- [ ] Full report content appears in Notion page
- [ ] Database fields populated correctly:
  - [ ] Category field shows selected categories
  - [ ] Industry field shows selected industries
  - [ ] Stage field shows funding stage
  - [ ] Revenue field shows revenue range
  - [ ] FTEs field shows employee count range
- [ ] Organization name and URL properties set correctly
- [ ] Page appears in correct database/data source

If any verification fails, use `Notion:notion-update-page` to correct the fields.

---

## Common Issues and Solutions

**Issue:** Business Model appears at end of report instead of after Thesis
**Solution:** Restructure report following section_guidelines.md lines 45-70 exactly

**Issue:** Funding summary embedded in table footer
**Solution:** Remove from table, add as separate narrative paragraphs below table

**Issue:** Fewer than 15 links in report
**Solution:** Review each section and add links to key claims, metrics, partnerships, competitors

**Issue:** Categories based on assumptions rather than explicit features
**Solution:** Re-read product section and select categories only for explicitly mentioned capabilities

**Issue:** Database fields not populated after page creation
**Solution:** Use separate `Notion:notion-update-page` call to update multi-select properties

---
