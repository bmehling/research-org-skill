# Update Guide (`--update`)

How to refresh an existing report. `--update` regenerates the full report against
current guidelines, carrying forward facts that still hold and researching only
what could have changed since the report was last researched.

**This file owns the update policy.** The staleness thresholds, event playbooks,
and changelog format live here, not in config.json. config.json holds no update
settings, the same way it holds no length settings.

---

## Why a full regeneration, not a patch

Reports drift from the guidelines as the guidelines evolve. A patch-only update
preserves prose written against a superseded standard, so the oldest entries stay
the worst ones forever. Regenerating against `section_guidelines.md` every time
means every refreshed report is a current-standard report.

Regeneration does **not** mean re-researching everything. The fact ledger below
is what makes it cheap: unchanged facts and their citations carry forward
verbatim, and research effort goes only to the delta.

---

## Step 0 — Finding what to update (`--stale`)

`--update` only helps if something tells you which entries need it. The sweep is
that something:

```bash
/usr/bin/python3 {skill_base_dir}/scripts/find_stale.py --months 6
```

It reads every row's research date, preferring the metadata line and falling back
to page creation time, then ranks by age. It is read-only and writes nothing.

**Two properties of the sweep worth knowing:**

- **It only reads pages that could possibly be stale.** A page created inside the
  threshold cannot hold a report older than the threshold, so those are skipped.
  On a 245-row database at a 6-month threshold this cut the per-page reads to 104.
  The saving grows as entries get updated.
- **Terminal entries are excluded.** `Defunct` and `Acquired` reports are frozen by
  design, so listing them as stale would be noise.

**Age is the input the script can measure, not the one that matters most.** Weight
it by stage before deciding what to spend a run on: a Seed company at 9 months has
probably changed more than a Public one at 18. An entry with no Stage and a thin
report is usually a stub that wants a fresh run rather than an update.

---

## Step A — Resolve the target entry

Accept either form of input:

| Input | How to resolve |
|---|---|
| Company URL (`https://acme.com`) | Query the data source on the `URL` property |
| Notion page URL or ID | Fetch the page directly |

**If the URL lookup returns nothing, fall back to a name search** on the
`Organization` title property using the domain's root word. A rebranded company
will not match on URL, and this is the path that finds it.

**Never update on a fuzzy match without confirming.** Show the candidate's
Organization name, URL, and created date, and ask before proceeding. Updating the
wrong row silently corrupts a shared database.

If nothing is found at all, stop and say so. Do not fall through to creating a new
entry — the user asked to update, and a create is a different, unrequested action.

---

## Step B — Build the fact ledger

Fetch the existing page and extract a compact ledger before any research. This is
the baseline the update diffs against, and it is what keeps the run cheap.

Capture:

- **Identity** — organization name, URL, HQ, founding year
- **Metadata line** — research date and report history (Step C)
- **Funding** — every row of the funding table, plus total and valuation
- **Executives** — every named person and title
- **Products** — every row of the product table, plus pricing
- **Customers and partners** — every named logo
- **Compliance** — every certification recorded, and the Compliance property
- **Metrics** — every headline number with its date
- **Competitors** — every row of the competitor table
- **Properties** — Stage, Revenue, FTEs, Category, Industry, Compliance
- **Open questions** — anything the report flagged as unverified

The ledger is working state, not a deliverable. Keep it in context or in the
scratchpad; it never goes to Notion.

**Then check the existing report's citations for rot** — this is the cheapest
signal available and it runs before any research:

```bash
/usr/bin/python3 {skill_base_dir}/scripts/check_links.py --page-id {page_id}
```

Reports carry 25 to 80 links and some die every year. Replace every `DEAD` one
during the regeneration, or drop the claim it supported. **Never drop a citation
that came back `BLOCKED`** — a 403 or a 999 means the server refused a bot, not
that the page is gone, and treating it as gone is the same mistake as reading a
JavaScript shell as an empty page. A browser retry is reserved for a `BLOCKED`
link that is the sole source for a fact the update depends on and is not labeled
`login wall`; see `quality_checklist.md`, Step 2b.

A `REDIRECT` to a different host is a useful early signal here: it is often the
first visible trace of a rebrand or an acquisition, before any announcement
surfaces in search.

---

## Step C — Establish the baseline date

Every report carries a metadata line directly under the title area, before the
first `#` heading:

```
*Research completed: 2026-09-17. Last updated: 2027-03-04.*
```

On a first-generation report there is only `Research completed:`, carrying the
bracket tag that records which model and which agents produced it:

```
*Research completed: 2026-09-17 [fable-5.1, scout+analyst]*
```

`--update` rewrites this into the two-date form and moves the tags down into the
report history, one line per generation (Step G). Full format in
`section_guidelines.md` under Report Preamble.

**Read the model tag before deciding scope.** A report written by a materially
weaker model than the one running now is a candidate for a full fresh run rather
than an update — its gaps are as likely to be analysis failures as genuine
absences of information. Say so rather than silently inheriting them.

**Baseline date = the most recent date on that line.** Bound all searches to the
window from that date to today.

**Legacy pages with no metadata line:** fall back to the Notion page's created
time, and note in the changelog that the baseline was inferred. Add the metadata
line as part of the regeneration so the next update is deterministic.

---

## Step D — Classify the event

Before researching, decide which playbook applies. Check the company's homepage
and a single date-bounded news search first — that is usually enough to classify.

| Event | Signals | Playbook |
|---|---|---|
| **Routine drift** | Nothing structural; new dates, numbers, people | Standard |
| **Funding round** | New raise announced | Standard + funding table row |
| **Rebrand** | New name, domain redirect, new logo | Rebrand |
| **Pivot** | Products or target market materially changed | Pivot |
| **Acquisition (brand lives on)** | Acquired, product still sold under its name | Acquisition |
| **Acquisition (brand absorbed)** | Product folded into buyer, site redirects | **Terminal** |
| **Merger** | Combined into a new entity | Acquisition or Terminal, by which brand survives |
| **IPO** | Listed, ticker assigned | IPO |
| **Bankruptcy / shutdown** | Chapter 7/11, wind-down notice, site dark | **Terminal** |
| **Take-private / PE buyout** | Delisted, PE owner | Acquisition |
| **Layoffs / contraction** | Headcount cut, offices closed | Standard + revised FTEs and risks |

More than one can apply. A rebrand often accompanies a pivot; an acquisition often
triggers a rebrand. Run both playbooks.

---

## Event playbooks

### Rebrand

The hardest case, because the identity itself moved and the old report's
assumptions are embedded everywhere.

1. **Confirm the new identity** from the company's own site or announcement, not a
   directory. Capture old name, new name, old domain, new domain, and the date.
2. **Rewrite the `URL` property** to the new domain and log the old one in the
   changelog. The old URL is how anyone searching the database will look for it.
3. **Re-examine mission and positioning.** A rebrand usually signals an expanded or
   narrowed mission. Do not carry forward the old Mission and Vision section on the
   assumption that only the name changed — re-read the new site's about and
   homepage copy and rewrite it.
4. **Re-examine target market and category.** Rebrands frequently accompany a move
   upmarket or into a new vertical. Re-check the Category and Industry properties.
5. **Pass the new URL to the upload script** as `--company-url` so the favicon
   refreshes. A stale favicon is the most visible sign of a half-done update.
6. **Use the new name in the `Organization` title**, with the old name in the
   changelog. Consider `New Name (formerly Old Name)` for one update cycle if the
   old name is how people still search.

### Pivot

1. Rewrite Thesis, Business Model, Products, and Customer from the current site.
2. Re-run the Category selection against `category_guide.md`; the old categories
   are probably wrong.
3. The competitor set has likely changed — this triggers the analyst regardless of
   the 12-month rule.
4. Say plainly in the changelog what the company moved from and to.

### Acquisition (brand lives on)

1. Add an M&A row to the funding table per `section_guidelines.md`: acquirer,
   date, price, rationale.
2. Set Stage to `Acquired`.
3. Rewrite Business Model and Key Risks — distribution, pricing, and roadmap
   control now sit with the parent.
4. Check whether the acquirer is its own entry in the database and mention the
   relationship in the report.
5. Revenue and FTEs are often no longer separately reported. Say so rather than
   carrying forward a stale figure.

### IPO

1. Set Stage to `Public`.
2. Replace estimated figures with reported ones. Revenue, headcount, and margins
   are now primary-source facts from the S-1, 10-K, or quarterly filings — cite the
   filing, not a market estimate.
3. Replace the valuation analysis with market capitalization, noting the as-of
   date, and keep the pre-IPO round history in the funding table.
4. Add the risk factors that matter from the filing's own risk section, filtered to
   the material ones. Do not transcribe the whole list.
5. Set Revenue from the reported figure, not a band estimate.

### Terminal events (shutdown, bankruptcy, absorbed acquisition)

**Do not regenerate the prose.** A forward-looking Thesis and an Opportunities
section for a company that no longer operates is wasted effort and reads as an
error.

1. Leave the existing report body exactly as it is. It becomes the historical
   record of what the company was.
2. Add the changelog at the top with a closing entry: what happened, when, the
   source, and where the product or team went.
3. Update the metadata line to `Last updated:` today.
4. Flip properties: Stage to `Defunct` or `Acquired`; update `URL` if the domain
   now redirects or is dark; leave Revenue and FTEs at their last known values.
5. State the freeze explicitly in the changelog, so a later reader knows the body
   is intentionally historical: *"Report body frozen as of [original date]; the
   company ceased operations [date]."*

The word-count and structure checks do not apply to a frozen report. Note that in
the run summary rather than reporting a failed check.

---

## Step E — Research scope

**Always dispatch the scout**, with a date-bounded brief. Always re-check the
company's own pages directly yourself — homepage, `/pricing`, `/security`,
`/about`, and the trust portal — because they are cheap, high-yield, and where
most drift shows up first.

The scout brief must:

- State the baseline date and ask only for changes since it
- List the ledger's current facts so the scout can report *unchanged* rather than
  re-deriving from scratch
- Ask explicitly for: new funding, exec changes, new or lost customers, pricing
  changes, new certifications, layoffs, M&A, litigation, and name or domain changes
- Keep the standing "Could not verify" requirement

**Dispatch the analyst only when one of these is true:**

- The competitor table was last refreshed more than **12 months** ago
- A competitor in the table had an M&A, shutdown, or major funding event
- The company pivoted or rebranded into a different market
- The report is terminal-adjacent in the other direction — the company grew into a
  new tier and now meets different competitors

Otherwise carry the competitor table forward unchanged and leave its funding
figures dated as they were. A competitor row that says a rival raised $30M in 2025
is not wrong in 2027; it is dated, and the dates are visible.

**Record which agents ran** in the report history line (Step G) so the next update
knows how old the competitor data is.

**Refresh the competitor cross-links either way.** Even when the analyst does not
run and the competitor set is unchanged, other companies may have been added to
the database since the last update, so a competitor that was plain text last time
may now have its own entry. Re-run the match described in
`section_guidelines.md` under Key Competitors and report the coverage count.

---

## Step F — Carry forward vs. re-verify

Anything returning `DEAD` from the link check is re-verified regardless of which
column it falls in — a fact whose only citation is gone needs a new source or it
needs to leave the report.

| Carry forward verbatim | Re-verify every time |
|---|---|
| Founding story and history | Anything on the company's own site |
| Closed funding rounds and their dates | Current pricing |
| Historical metrics with as-of dates | Compliance certifications |
| Prior executives' backgrounds | Current executive roster |
| Market sizing under 18 months old | Named customers still displayed |

**Certifications expire.** SOC 2 Type II is an annual report and HITRUST e1 is a
one-year certification. A certification recorded two years ago is not evidence
today. Re-read the security page; if it no longer lists a cert the report claims,
that is a change worth logging and a property worth removing.

**Watch for silent removals.** A customer logo that disappeared, a certification
no longer listed, a pricing tier that vanished — these are real signals and are
easy to miss because nothing announces them. The ledger is what makes them
visible: anything in the ledger that is no longer on the site gets checked.

---

## Step G — Changelog and metadata format

The regenerated report opens with the metadata line and a changelog, above the
first content heading.

```markdown
*Research completed: 2026-09-17. Last updated: 2027-03-04.*

# What Changed — March 4, 2027

**Funding.** Raised a $22M Series A led by Bessemer in January 2027, the first
priced round and first arm's-length valuation. [source](https://example.com)

**Leadership.** Hired a Chief Medical Officer; the CRO listed previously no longer
appears on the site.

**Compliance.** Added ISO 27001. SOC 2 Type II renewed; HITRUST e1 no longer
listed on the security page.

**Unchanged.** Products, pricing, and the competitor set are materially as
reported in September 2026.

**Report history**
- 2026-09-17 — initial report [fable-5.1, scout+analyst]
- 2027-03-04 — updated [opus-5, scout]

# Company Overview
...
```

Rules:

- **Cap the changelog at 200 words**, report history included. It is a summary, not
  a second report. Detail belongs in the sections it affects.
- **Bold lead-in per change**, one short paragraph each. Group by theme, not by
  source.
- **Always include an "Unchanged" line.** A reader needs to know what was checked
  and found stable, otherwise silence is ambiguous.
- **Link every substantive change** to its source, same standard as the body.
- **Keep prior changelog entries out of the body.** Only the report history list
  carries forward; superseded "What Changed" sections are replaced, because the
  current changelog covers the window since the last update and the history line
  preserves the timeline.
- **Tag each history line** with the model and the agents that ran, comma
  separated, as `[opus-5, scout]`. The agents half lets the next update compute
  competitor-table age; the model half lets it judge whether the prose is worth
  updating or worth replacing. Legacy entries get `[model unknown, agents
  unknown]` rather than a guess.

**Word budget effect:** the changelog is measured with everything else, so in
update mode the validation band's upper bound rises by 200 words:
**3,200–4,200 (full)** and **1,200–2,200 (lite)**. Lower bounds are unchanged.

---

## Step H — Property diff and approval gate

**Never write to Notion before showing the diff and getting a yes.** An update
overwrites a page that may carry another person's annotations, and a property flip
propagates into every filtered view of the database.

Show:

1. The full "What Changed" section as drafted
2. A property table, old to new, marking rows that change

```
Property     Current            Proposed
Stage        Seed               Series A          ← change
Revenue      $1M-$8M, Est       $8M-$30M, Est     ← change
FTEs         10-50              50-100            ← change
Category     AI, Ambient Notes  unchanged
Compliance   SOC2, HIPAA,       SOC2, HIPAA,      ← change
             HITRUST, PIPEDA    ISO27001, PIPEDA
URL          https://old.com    https://new.com   ← change
```

Then wait. Do not show the regenerated prose unless asked — it is long, and the
changelog plus property diff is the part worth a human's attention.

**Flag removals explicitly.** Dropping a certification or a customer is a bigger
deal than adding one, and it is the change most likely to be a research miss
rather than a real event. If a removal is based on absence of evidence rather than
positive evidence of loss, say so and keep the property until confirmed.

---

## Step I — Write back

1. Write the regenerated report to the scratchpad.
2. Run the quality checklist, using the update-mode bands above.
3. Upload with `--clear`, which removes the existing body first:

```bash
/usr/bin/python3 {skill_base_dir}/scripts/upload_to_notion.py \
  --page-id {existing_page_id} \
  --content {scratchpad}/research-report-{company}.md \
  --company-url {current_url} \
  --clear
```

`--clear` is mandatory in update mode. Without it the new report appends beneath
the old one and the page ends up with two reports.

Pass the **current** URL as `--company-url` so a rebrand refreshes the favicon.

4. Update properties with `notion-update-page` using `command: "update_properties"`.
5. Delete the scratchpad file.

**Recovery:** Notion page history retains prior versions, so a bad update is
recoverable through the page's version history. Say so if an update looks wrong.

---

## Step J — Run summary

Report, in this order: what changed, what was checked and found unchanged, which
properties moved, whether the analyst ran, and anything that could not be
verified. Link the page.

An update that found nothing is a valid and useful outcome. Say "no material
changes since [date]" plainly rather than manufacturing significance, and still
write the refreshed report so the metadata line and guideline conformance advance.
