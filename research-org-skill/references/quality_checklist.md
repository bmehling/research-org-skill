# Quality Checklist - Executable Verification

This checklist provides **executable verification steps** to ensure reports meet quality standards before Notion upload.

---

## Step 1: Verify Word Count

**Validation Band:** 3,200–4,000 words (full mode) or 1,200–2,000 words (lite mode). These bands and the per-section and table budgets they derive from live in `references/section_guidelines.md`, which is the single source of truth for report length. config.json holds no length settings.

**Run this mid-draft, not just at the end.** After finishing the Market section — past all three tables — measure the partial draft with the same command below. Expect roughly **2,850 words (full)** or **1,300 (lite)**. Materially over means the remaining sections will not fit, and fixing it then costs one edit instead of four. Catching overrun only at Step 1 is what produces multi-pass trimming.

**Verification:**

Count PROSE only. A plain `wc -w` counts HTML table markup (`<tr>`, `</tr>`, `<table header-row="true">`) and link URLs as words, which inflates the total by several hundred and triggers unnecessary trimming. Strip both first.

Note the space in `s/<[^>]*>/ /g`. Tags must be replaced with a space, not deleted, or adjacent cells written on one line (`<td>Eleos</td><td>eleos.health</td>`) get glued into a single word and the table undercounts.

Link URLs are stripped but link TEXT is kept, since it is prose the reader reads. `[$53M in Series A](url)` counts as four words.

```bash
sed -E 's/<[^>]*>/ /g; s/\]\([^)]*\)/]/g' /tmp/research-report-{company}.md | wc -w
```

Check the output against the validation band above. If over the maximum, trim before proceeding. If under the minimum, sections were likely skipped or underdeveloped; compare against the per-section budgets to find which.

To see how much of the total is markup rather than prose, compare against the raw count:
```bash
wc -w < /tmp/research-report-{company}.md
```

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
- [ ] Products and Services (with product overview table)
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
- [ ] **Compliance** — 0+ from `compliance` array in config.json, evidenced by trust/security/compliance pages or third-party attestations. Use `None Identified` if no evidence found.

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
