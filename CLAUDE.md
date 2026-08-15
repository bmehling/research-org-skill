# research-org-skill

A Claude Code skill that researches a company and writes a structured report into a Notion database.

## Two copies exist. Develop in one, commit from the other.

The skill lives in two independent directories. They are **not** symlinks, and editing one does not touch the other.

| Location | Role |
|---|---|
| `~/.claude/skills/research-org-skill/` | Installed copy. This is what Claude Code actually loads and runs. |
| `~/Projects/research-org/research-org-skill/` | Git repo. This is what gets committed. |

**Workflow: develop in the installed copy, then sync back to the repo before committing.** Editing the installed copy is what lets you test a change by invoking the skill. Skipping the sync means the fix works on this machine and exists nowhere else.

```bash
A=~/.claude/skills/research-org-skill
B=~/Projects/research-org/research-org-skill
cp "$A/SKILL.md" "$B/SKILL.md"
cp "$A/references/"*.md "$B/references/"
cp "$A/scripts/"* "$B/scripts/"
```

Always verify before committing. Anything other than the expected noise means an unsynced change:

```bash
diff -rq ~/.claude/skills/research-org-skill ~/Projects/research-org/research-org-skill
# Expected leftovers only: .DS_Store, .claude/, .cpa-workflow-artifacts/
```

## config.json is gitignored. Edit config.example.json too.

`config.json` holds the Notion API key and is gitignored, so **changes to it never reach git**. The tracked template is `config.example.json` at the repo root.

Any time you add, remove, or rename a config key, change it in three places:
1. `~/.claude/skills/research-org-skill/config.json` (the live copy that runs)
2. `~/Projects/research-org/research-org-skill/config.json` (working copy, still untracked)
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
- **Upload via the script, not the MCP tool.** `scripts/upload_to_notion.py` chunks and batches around the MCP payload limit. Add `--clear` when re-uploading to a page that already has content.
