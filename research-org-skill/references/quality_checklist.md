# Quality Checklist - Executable Verification

This checklist provides **executable verification steps** to ensure reports meet quality standards before Notion upload.

---

## Step 1: Verify Word Count

**Validation Band:** 3,200–4,000 words (full mode) or 1,200–2,000 words (lite mode). In update mode the upper bound rises by 200 to absorb the changelog: 3,200–4,200 (full) or 1,200–2,200 (lite). These bands and the per-section and table budgets they derive from live in `references/section_guidelines.md`, which is the single source of truth for report length. config.json holds no length settings.

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

### Step 2b: Check for dead citations

Run the link checker. In **update mode this is required** and runs against the existing page before regenerating, so dead sources are replaced rather than carried forward. In create mode it is a cheap catch for typo'd URLs before upload.

```bash
# update mode: check what is already published
/usr/bin/python3 {skill_base_dir}/scripts/check_links.py --page-id {page_id}

# create mode: check the draft
/usr/bin/python3 {skill_base_dir}/scripts/check_links.py --content {draft_path}
```

**Act only on `DEAD`.** A 404, a 410, or a host that no longer resolves means the citation is gone: find a replacement source or remove the claim it supports.

**Never drop a citation on `BLOCKED`.** A 401, 403, 429, or 999 means the server refused an automated request, which is not evidence the page is gone. This is the same error as treating a JavaScript shell as an empty page: an unreadable response is not a negative finding. Paywalled research firms, LinkedIn, and PitchBook return these routinely.

The block is bot detection, not AI detection. The checker already sends a full browser header set, so what remains is a JavaScript challenge, a TLS fingerprint check, or a login wall — none of which a plain HTTP client can pass.

**Escalate a `BLOCKED` link to Chrome only when both hold:**
1. It is the **sole source for a load-bearing fact** — a funding amount, valuation, certification, or acquisition that no other citation in the report supports. Where a second source exists, cite that instead; it is cheaper than a browser round-trip.
2. The checker did **not** label it `login wall`. LinkedIn, PitchBook, Crunchbase, Gartner, Forrester, and CB Insights load a sign-in page in the browser, which returns 200 and looks like success but is not the cited content — the JavaScript-shell trap again. LinkedIn would also browse as the user's own account.

Use the same browser path as the trust-center escalation in SKILL.md step 3, including the wait-and-retry on an empty first read. If the page shows a CAPTCHA or challenge, stop: do not attempt it, and leave the citation as `BLOCKED`. Every other `BLOCKED` link is left alone without a retry.

`TIMEOUT`, `SERVER_ERR`, and `UNREACHABLE` are usually transient. Re-check before acting.

`REDIRECT` to a different host is worth a look during an update: it is often the first visible sign of a rebrand or an acquisition.

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
- [ ] **Compliance** — 0+ from `compliance` array in config.json, evidenced by trust/security/compliance pages or third-party attestations.

**Every value here must trace to a page that was actually read.** Not a search snippet, not a subagent's summary of a page it could not render, not an inference from the industry served. A trust center returning 200 with only a page shell is unread — escalate to the browser (SKILL.md step 3) or leave the certification out.

Use `None Identified` only when the relevant pages were reached and named nothing. If they could not be reached, that is neither evidence of certification nor of its absence: record only what was read, and state the gap in the report.

*This check exists because a run recorded ISO 27001 and GDPR from a Vanta trust center no fetch could render. The live page listed SOC 2 and HIPAA only.*

---

## Step 4b: Update Mode Only

Skip this step unless `--update` was used.

- [ ] **Metadata line present** directly above the first heading, carrying both `Research completed:` and `Last updated:`
- [ ] **Dead citations resolved.** Step 2b run against the existing page, every `DEAD` link replaced or its claim removed, and no citation dropped merely because it returned `BLOCKED`
- [ ] **`# What Changed — [date]` section** present, at or under 200 words including the report history
- [ ] **"Unchanged" line present.** Silence about what was checked is ambiguous; state it
- [ ] **Report history list** carries every prior entry, each tagged with model and agents, e.g. `[opus-5, scout]`
- [ ] **Competitor cross-links** refreshed: competitors now present in the database are linked to their Notion pages, and the coverage count appears in the run summary
- [ ] **Every substantive change is linked** to its source, same standard as the body
- [ ] **Property diff drafted** (old → new) and shown to the user, with removals flagged
- [ ] **User approved** before any write to Notion
- [ ] **`--clear` included** in the upload command, or the page will hold two reports
- [ ] **`--company-url` is the current URL**, so a rebrand refreshes the favicon

**Terminal events** (shutdown, bankruptcy, absorbed acquisition) are exempt from Steps 1 and 3: the body is frozen by design. Confirm instead that the body was left untouched, the closing changelog entry was added, and Stage was set to `Defunct` or `Acquired`.

*This step exists because the two failure modes of an in-place update are invisible: uploading without `--clear` silently doubles the page, and writing before approval silently overwrites someone's annotations.*

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
