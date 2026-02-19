# Quality Checklist - Executable Verification

This checklist provides **executable verification steps** to ensure reports meet quality standards before Notion upload.

---

## Step 1: Verify Word Count

**Target Range:** Defined in `config.json` under `research.targetWordCount`

**Verification:**
```bash
# Read target range from config.json
TARGET_RANGE=$(grep -o '"targetWordCount"[[:space:]]*:[[:space:]]*"[^"]*"' config.json | cut -d'"' -f4)
MIN_WORDS=$(echo $TARGET_RANGE | cut -d'-' -f1)
MAX_WORDS=$(echo $TARGET_RANGE | cut -d'-' -f2)

# Count words in report
WORD_COUNT=$(wc -w < /tmp/research-report-{company}.md | tr -d ' ')

echo "📊 Word count: $WORD_COUNT"
echo "🎯 Target range: $TARGET_RANGE (from config.json)"

if [ $WORD_COUNT -lt $MIN_WORDS ]; then
    echo "⚠️  WARNING: Under minimum ($MIN_WORDS). Consider expanding thin sections."
elif [ $WORD_COUNT -gt $MAX_WORDS ]; then
    echo "❌ OVER LIMIT: Exceeds maximum ($MAX_WORDS). MUST revise before proceeding."
    echo "   Review section_guidelines.md paragraph limits and trim accordingly."
else
    echo "✅ Word count within target range"
fi
```

**Action if over limit:**
- DO NOT proceed to Notion upload
- Return to step 5.5 in SKILL.md for revision guidance
- Trim sections to paragraph maximums in section_guidelines.md

---

## Step 2: Verify Citation Links

**Target:** 15-30+ links distributed throughout report (from writing_style.md)

**Verification:**
```bash
LINK_COUNT=$(grep -o '\[.*\](http' /tmp/research-report-{company}.md | wc -l | tr -d ' ')
echo "🔗 Link count: $LINK_COUNT"
echo "🎯 Target: 15-30+ (from writing_style.md)"

if [ $LINK_COUNT -lt 15 ]; then
    echo "⚠️  WARNING: Below minimum citations (15). Add more source links."
else
    echo "✅ Link count meets target"
fi
```

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
- [ ] Market (with Customer, Market Size, Competitive Landscape, Competitors table, Traction)
- [ ] Opportunities and Risks (with Key Opportunities, Key Risks, SWOT Analysis)

**Verification:**
```bash
# Check for required headers
for section in "# Company Overview" "# Executive Team" "# Investors, Funding Rounds, and Valuation" "# Products and Services" "# Notable Partnerships and Customers" "# Market" "# Opportunities and Risks"; do
    if grep -q "^$section" /tmp/research-report-{company}.md; then
        echo "✅ Found: $section"
    else
        echo "❌ Missing: $section"
    fi
done
```

**SWOT Structure:**
- [ ] ## SWOT Analysis exists
- [ ] ### Strengths subsection
- [ ] ### Weaknesses subsection
- [ ] ### Opportunities subsection
- [ ] ### Threats subsection

---

## Step 4: Database Fields Prepared

Verify values determined for (defined in category_guide.md and config.json):
- [ ] **Categories** — 1-4 from category_guide.md based on explicit product features
- [ ] **Industry** — Selected from available options (from config.json categories)
- [ ] **Stage** — Determined from funding or "Not available"
- [ ] **Revenue** — Estimated from research or "Not available"
- [ ] **FTEs** — Estimated from research or "Not available"

---

## Step 5: Writing Quality Manual Review

Quick manual checks (from writing_style.md and section_guidelines.md):
- [ ] Professional, analytical tone (not promotional)
- [ ] Balanced analysis (both strengths and weaknesses presented)
- [ ] No speculation without marking as estimates
- [ ] Tables formatted correctly with header rows
- [ ] All markdown syntax valid (no broken links or malformed headers)

---

## ✅ VERIFICATION COMPLETE

**All checks must pass before proceeding to Notion upload (step 8 in SKILL.md).**

If any checks fail:
- Word count over max: Return to step 5.5 for revision
- Link count under 15: Add more citations inline
- Missing sections: Complete required sections
- Database fields incomplete: Determine all required values

---
