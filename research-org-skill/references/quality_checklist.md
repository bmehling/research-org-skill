# Quality Checklist - Executable Verification

This checklist provides **executable verification steps** to ensure reports meet quality standards before Notion upload.

---

## Step 1: Verify Word Count

**Target Range:** Defined in `config.json` under `research.targetWordCount` (you read this in Step 1 of the workflow)

**Verification:**
```bash
wc -w < /tmp/research-report-{company}.md
```

Check the output against the `targetWordCount` range from config.json. If over the maximum, trim before proceeding.

**Revision strategy if over limit:**
- Paragraph limits in section_guidelines.md are MAXIMUMS, not targets — aim for lower end
- Cut redundant analysis, excessive examples, and repetitive context
- Keep all citations and data; reduce explanatory prose
- Common areas to trim: Competitive Landscape, Market sections, Opportunities/Risks, SWOT

---

## Step 2: Verify Citation Links

**Target:** 25-40+ links distributed throughout report (from writing_style.md)

**Verification:**
```bash
grep -o '\[[^]]*\](http' /tmp/research-report-{company}.md | wc -l
```

If under 25, add more source links before proceeding.

**Action if under minimum:**
- Review writing_style.md citation guidelines
- Add links to funding announcements, partnerships, market data, competitors
- Ensure major claims have source attribution

---

## Step 3: Verify Report Structure

**Required Sections:**
- [ ] Company Overview (with Founding Story, Mission/Vision, Thesis, Business Model)
- [ ] Executive Team
- [ ] Investors, Funding Rounds, and Valuation
- [ ] Products and Services
- [ ] Notable Partnerships and Customers
- [ ] Market (with Customer, Market Size and Opportunity, Market Dynamics and Trends, Competitive Landscape Overview, Key Competitors table, Competitive Advantages, Traction)
- [ ] Opportunities and Risks (with Key Opportunities, Key Risks, SWOT Analysis)

**Verification:**
```bash
grep "^# " /tmp/research-report-{company}.md
grep "^## SWOT Analysis" /tmp/research-report-{company}.md
grep "^### " /tmp/research-report-{company}.md
```

Confirm all top-level (`#`) sections are present, `## SWOT Analysis` exists, and all four SWOT `###` subsections (Strengths, Weaknesses, Opportunities, Threats) appear.

---

## Step 4: Database Fields Prepared

Verify values determined for:
- [ ] **Categories** — 1-4 from category_guide.md based on explicit product features
- [ ] **Industry** — Selected from `industries` array in config.json
- [ ] **Stage** — Determined from funding or "Not available"
- [ ] **Revenue** — Estimated from research or "Not available"
- [ ] **FTEs** — Estimated from research or "Not available"

---

## Step 5: Writing Quality Manual Review

Quick manual checks (from writing_style.md and section_guidelines.md):
- [ ] Professional, analytical tone (not promotional)
- [ ] Balanced analysis (both strengths and weaknesses presented)
- [ ] No speculation without marking as estimates
- [ ] Tables use HTML `<table>` format (not pipe tables) for proper Notion rendering
- [ ] All markdown syntax valid (no broken links or malformed headers)

---

## VERIFICATION COMPLETE

**All checks must pass before proceeding to Notion upload (step 8 in SKILL.md).**

If any checks fail:
- Word count over max: Revise using trimming strategy above
- Link count under 25: Add more citations inline
- Missing sections: Complete required sections
- Database fields incomplete: Determine all required values

---
