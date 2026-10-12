# research-org-skill

A Claude Code skill that researches a company and writes a structured report into a Notion database.

## Two copies exist. Develop in one, commit from the other.

The skill lives in two independent directories. They are **not** symlinks, and editing one does not touch the other.

| Location | Role |
|---|---|
| `~/.claude/skills/research-org-skill/` | Installed copy. This is what Claude Code actually loads and runs. |
| `~/cc-projects/research-org-skill/research-org-skill/` | Git repo. This is what gets committed. |

**Workflow: develop in the installed copy, then sync back to the repo before committing.** Editing the installed copy is what lets you test a change by invoking the skill. Skipping the sync means the fix works on this machine and exists nowhere else.

```bash
A=~/.claude/skills/research-org-skill
B=~/cc-projects/research-org-skill/research-org-skill
cp "$A/SKILL.md" "$B/SKILL.md"
cp "$A/references/"*.md "$B/references/"
cp "$A/scripts/"* "$B/scripts/"
```

Always verify before committing. Anything other than the expected noise means an unsynced change:

```bash
diff -rq ~/.claude/skills/research-org-skill ~/cc-projects/research-org-skill/research-org-skill
# Expected leftovers only: .DS_Store, .claude/, .cpa-workflow-artifacts/
```

## config.json is gitignored. Edit config.example.json too.

`config.json` holds the Notion API key and is gitignored, so **changes to it never reach git**. The tracked template is `config.example.json` at the repo root.

Any time you add, remove, or rename a config key, change it in three places:
1. `~/.claude/skills/research-org-skill/config.json` (the live copy that runs)
2. `~/cc-projects/research-org-skill/research-org-skill/config.json` (working copy, still untracked)
3. `config.example.json` (repo root, **tracked**, the only one anyone cloning will see)

Miss step 3 and a fresh clone inherits keys the skill no longer reads.

## The skill depends on two agent definitions outside itself

Step 3 dispatches two subagents. Their definitions live in `~/.claude/agents/`, **not** in the skill directory, because Claude Code discovers agents from `.claude/agents/` and the skill runs from any working directory.

| Agent | Model | Job |
|---|---|---|
| `research-scout` | haiku | Retrieval only. Fetch pages, quote figures, cite URLs. No judgment. |
| `research-analyst` | sonnet | Competitive landscape and market sizing. Judgment-heavy. |

Both declare `tools: ["WebSearch", "WebFetch"]`. That restriction is the point: it makes the scope overrun **structurally impossible** rather than merely discouraged. The subagent had been creating Notion pages on its own, and prompting alone did not stop it across two sessions. It cannot now, because it has no tool to do it with.

**This is a real install dependency.** A fresh clone of this repo gets the skill but not the agents, and `Agent(subagent_type: "research-scout")` will fail. Two consequences:

1. Keep repo copies in `agents/` at the repo root and copy them to `~/.claude/agents/` on install (see README).
2. SKILL.md documents a fallback to `general-purpose` with an explicit read-only prompt. That fallback is weaker — the restriction becomes advisory, so the verification step carries the load.

**Don't ask the scout to analyze.** Its observed failures (fabricated customer logos, a garbled `$5.15B` where the source said `$5.1B`) come from being asked to judge rather than retrieve. Facts and URLs go to the scout; anything requiring a decision goes to the analyst or stays with the main agent.

## Testing a change

No session restart is needed. Skill files are read from disk at invocation, and only frontmatter `name`/`description` changes require re-discovery.

One caveat: a conversation that already loaded the skill holds the **old** SKILL.md text in context. Re-invoke through the Skill tool to pull the current version from disk rather than working from the stale copy.

A real test run writes to the live Notion database. Offer a dry run (stop after the quality checklist, before step 8) when the point is to validate report structure or length rather than the upload path.

## Report length: one source of truth

`references/section_guidelines.md` owns report length. `config.json` holds no length settings.

Each section carries a `**Word Budget:**` line. Those budgets sum to the totals and validation bands at the top of the same file. **If you change a section budget, update the totals and bands to match**, or the checklist starts disagreeing with the guidance again.

This replaced paragraph counts, which could not work: summing the old "Expected Length: N paragraphs" guidance at its lower bound came to ~4,800 words against a 4,000 hard max, so every report overshot and needed a long trimming pass.

### Word count must strip markup

Never validate length with a plain `wc -w`. It counts HTML table tags and link URLs as words and inflates the total by hundreds, which triggers trimming that isn't needed.

```bash
sed -E 's/<[^>]*>/ /g; s/\]\([^)]*\)/]/g' report.md | wc -w
```

Two details that look like typos but aren't:
- Tags are replaced with a **space**, not deleted. Deleting them glues adjacent cells written on one line (`<td>Eleos</td><td>eleos.health</td>`) into a single word, and tables undercount.
- Link **text** is kept, only the URL is stripped. Link text is prose the reader reads.

## `--update` policy lives in update_guide.md, not config.json

`references/update_guide.md` owns everything about refreshing an existing report: how the entry is located, the fact ledger, the event playbooks, the changelog format, and the approval gate. **config.json holds no update settings**, deliberately, the same way it holds no length settings. The 12-month analyst-staleness threshold is a policy number in that file, so changing it is a one-line edit in one place rather than a three-place config edit.

Update mode **always regenerates the full report** against current guidelines rather than patching sections. A patch-only update preserves prose written against a superseded standard, which would leave the oldest entries permanently the worst ones. Cheapness comes from the fact ledger and date-bounded search, not from writing less.

Three failure modes are invisible and each has a guard:

| Failure | Guard |
|---|---|
| Upload without `--clear` appends, leaving **two reports on one page** | `--clear` is mandatory in update mode |
| Writing before approval silently overwrites someone's annotations | Property diff + changelog shown, then wait for yes |
| No recorded research date means every update re-searches from creation | Metadata line `*Research completed: … Last updated: …*` above the first heading |

**Terminal events do not regenerate.** A company that shut down, went bankrupt, or was absorbed into an acquirer keeps its existing report body as a historical record; only the changelog and properties change. Writing a forward-looking Thesis and Opportunities section for a dead company is wasted effort and reads as an error. Those frozen reports are exempt from the word-count and structure checks.

**`--update` is useless without `--stale`.** Nobody remembers which of 250 entries went stale, so `scripts/find_stale.py` produces the worklist. It dates each row from the report's metadata line, falling back to page creation time, and skips `Defunct` and `Acquired` because those reports are frozen. It reads only rows that could possibly be stale: a page created inside the threshold cannot hold an older report. At a 6-month threshold on 245 rows that was 104 reads, about 48 seconds, and the count drops as entries get updated.

Its ranking is by age, which is the only thing it can measure and the weakest signal available. **Weight by stage when deciding what to actually refresh** — a Seed company at 9 months has usually moved more than a Public one at 18.

**An unreadable link is not a dead link.** `scripts/check_links.py` runs at the start of every update. It splits `DEAD` (404, 410, DNS failure) from `BLOCKED` (401, 403, 429, and LinkedIn's 999), and only `DEAD` justifies dropping a citation. This is the same epistemics as the JavaScript-shell rule below: a response you could not read is not evidence in either direction. Paywalled analyst firms, LinkedIn, PitchBook, and Cloudflare-fronted sites return `BLOCKED` constantly and their pages are almost always fine. A run against the Eluve report returned 40 ok, 1 genuinely dead, and 10 blocked — acting on the blocked ones would have stripped ten good citations.

**Blocks are bot detection, not AI detection, and the browser is a narrow fallback.** The checker sends a full browser header set; on the Lumos report that alone cleared Grand View's 403. What still blocks is a JavaScript challenge or a login wall. Chrome retries a `BLOCKED` link only when it is the sole source for a load-bearing fact, and never on a host the checker labels `login wall` (LinkedIn, PitchBook, Crunchbase, Gartner, Forrester, CB Insights): those render a 200 sign-in page, which is the JavaScript-shell false positive in a new place. The host list lives in `LOGIN_WALLED` in `check_links.py`.

**A rebrand is the case that breaks lookups.** The stored URL no longer matches, so resolution falls back to a title search on `Organization`, and the new URL must be passed to the upload script as `--company-url` or the favicon stays stale. Mission, target market, and Category all need re-examination on a rebrand — the name is rarely the only thing that moved.

## The JavaScript shell: a 200 that isn't a page

WebFetch does not run JavaScript. A client-side-rendered page returns HTTP 200 with only its static shell — a title and header — and **no error**. It looks like a real page that happens to say nothing, which is the shape that manufactures false readings in both directions.

Compare the failure modes seen across runs:

| Response | Announces itself? |
|---|---|
| 403, 402, timeout | Yes — obviously go find another route |
| **200 + shell** | **No** |

**Trust centers are the standing case.** `trust.<company>.com` is nearly always Vanta, Drata, or SafeBase, all JS apps. So compliance — the one field most dependent on reading a specific page — is exactly where this bites.

**Find the portal first — it's a subdomain.** It lives at `trust.<domain>` (`trust.hash.ai`, `trust.reducto.ai`); `<domain>/trust` usually 404s and proves nothing either way. `/security` is normally the only page linking to it.

When a compliance page returns a shell, load it in Chrome (`tabs_context_mcp` → `navigate` → `get_page_text` → `tabs_close_mcp`), and **wait-and-retry on an empty first read**: `get_page_text` often returns `No text content found` before the app renders. On `trust.hash.ai` the first read returned nothing and a 4-second wait returned the full certification list. Treating that first empty read as "no content" reproduces the exact false negative the escalation exists to prevent.

That step belongs to the **main agent**, never the subagents: their `WebSearch`/`WebFetch` restriction is what closed the scope-overrun problem, and browser automation would hand a haiku agent a general-purpose click-and-type surface. Do not relax it to solve this.

**The backstop matters more than the escalation:** never write a certification into the Compliance field from a page nobody read. An unreadable page supports neither recording the certification nor `None Identified`.

Reducto is the worked example. The scout reported SOC 2, ISO 27001, GDPR, and HIPAA from the trust center; those went into Notion. Loading the page in Chrome showed **SOC 2 and HIPAA only** — plus a SOC 2 Type 2 report, a penetration test, and the subprocessor list (AWS, Google Cloud, OpenAI, Anthropic), none of which any fetch had surfaced.

## Subagent output is leads, not facts

The tool restriction above closes the scope-overrun failure. It does **not** close the accuracy ones — a restricted agent can still misreport what it read. Verify directly with WebFetch before writing:

- Every named customer, against the company's own customers or case study page
- Every headline metric and funding figure, against the primary announcement
- Compliance claims, against `/security`, `/trust`, or `/legal`

When a claim only exists in the company's own marketing, attribute it as such in the report rather than stating it as fact. Both agent definitions require a `## Could not verify` section — read it. Gaps reported honestly are the point; an empty one is a signal to check, not reassurance.

## Notion specifics

- **Check for duplicates first** (step 2). Query the data source by URL before creating anything.
- **Multi-select values must already exist in the database schema.** `Stage`, `Revenue`, `FTEs`, `Category`, `Industry`, and `Compliance` are constrained option lists. Fetch the data source (`collection://<dataSourceId>`) to read the allowed values; a value not in the list will not stick.
- **Tables must be HTML**, not pipe tables. Pipe tables do not render in Notion. Use `<table header-row="true">`.
- **`Linked Org` is not a self-relation.** Both it and `Projects` point at a *different* database (`0f60f56f-…`), so neither can link one organization to another. Competitor cross-linking therefore works by putting a Notion page URL in the competitor table's Company cell, which needs no schema change at all. If you ever want real relations, add a self-relation property by hand; the skill will populate one if it exists but will never create it.
- **Match competitors in one paginated pass, not N queries.** Fetch the whole `Organization` + `URL` column set and match locally by domain then name. The database was 254 rows in 3 round-trips when this was built, and that cost is flat no matter how many competitors a report names.
- **Page links from SQL are missing `/p/`.** The `url` column of a SQL query returns `https://app.notion.com/<id>`, which 404s. Competitor cross-links must use `https://app.notion.com/p/<id>`. The Concurrence update caught this when `check_links.py` reported three cross-links `DEAD`; any earlier report with cross-links likely carries the broken form.
- **The URL property has two names.** It is `userDefined:URL` through the Notion MCP tools and plain `URL` through the REST API. Code that works in one will silently return nothing in the other.
- **Upload via the script, not the MCP tool.** `scripts/upload_to_notion.py` chunks and batches around the MCP payload limit. Add `--clear` when re-uploading to a page that already has content.
