# Decision log

This log records the technical decisions of {{PROJECT}}, with their reasons and evidence. Read this
file and [open-work.md](open-work.md) before you change {{AREAS}} or the agent instructions. The
[Rules](#rules) tell you which entries to read
([ADR-0001](entries/0001-decision-log-agents-md-and-private-data.md)).

Each entry gives the decision, its reason, the evidence (when there is evidence), the alternatives
rejected and a "Not repeated" section for pitfalls already found. When a decision changes, add a new
entry that supersedes the old entry in full. The body of a decided entry changes only by the edits
that the skill [`change-decision-log`](../.claude/skills/change-decision-log/SKILL.md) allows. To write an entry,
load that skill and use [template.md](template.md).

## Index

### Active

These entries are `accepted`.

| # | Decision | Status |
|---|----------|--------|
| [0001](entries/0001-decision-log-agents-md-and-private-data.md) | Decision log and its rules; `AGENTS.md` files hold the instructions; `plans/` is local; no private data | accepted |

### Proposed

These entries wait for a decision of the user. Section is the section or area of the change, or
`none`.

| # | Decision | Section | Status |
|---|----------|---------|--------|

The entries that are `rejected`, `superseded by XXXX`, `absorbed into <path>#<anchor>`,
`evidence; used by XXXX`, `evidence; replaced by XXXX` or `done` are in [historical.md](historical.md).
The entries that are `evidence` are in [evidence.md](evidence.md).

## Open work

The open work is in [open-work.md](open-work.md).

## Rules

- Read the Active entries that apply to your task. Then you do not repeat a settled question. Before
  you make a measurement, scan the rows of `evidence.md` of each log, and read the entries that
  apply. Then you do not repeat a completed measurement. `evidence.md` and its entries are not in
  the read path. Read a Proposed entry only for work in its section, or when a skill
  tells you to. Read an entry of [historical.md](historical.md) only to find the reason for a
  decision.
- A decision that a document or code refers to must be in an entry. "This log" in an older entry or
  in the Rules means all logs.
- Delete an open-work item when the work is done. Put a dated fact in `open-work.md` or in an
  entry, not in `AGENTS.md`.
- Before you add or change an entry, a status or a row of a table, load the skill
  [`change-decision-log`](../.claude/skills/change-decision-log/SKILL.md). It gives the rules for
  each change to a log.
