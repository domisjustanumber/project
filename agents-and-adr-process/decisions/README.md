# Decision log of the kit

This log records the decisions about the agents and ADR kit itself: the sync, the tools and the
rules that the kit gives to each repo. Read this file and [open-work.md](open-work.md) before you
change the kit. The decisions of a repo that uses the kit stay in the log of that repo.

This log uses the rules of the kit: the [Rules](../bootstrap/decisions/README.md#rules) of the kit
index, and the skill [`change-decision-log`](../bootstrap/.claude/skills/change-decision-log/SKILL.md)
for each change of the log. Write each entry from the kit
[template.md](../bootstrap/decisions/template.md). The place of this log can change
([ADR-KAX0](entries/KAX0-the-kit-decision-log.md)).

## Index

### Active

These entries are `accepted`.

| # | Decision | Status |
|---|----------|--------|
| [B1QZ](entries/B1QZ-two-way-kit-sync.md) | The kit is a two-way hub: `kit_sync.py`, `manifest.toml` and a repo-owned `kit.toml` | accepted |
| [W045](entries/W045-lf-line-ends-in-each-repo.md) | LF line ends in each repo, set by `.gitattributes` and checked by `check_line_ends.py` | accepted |
| [KAX0](entries/KAX0-the-kit-decision-log.md) | The decisions of the kit are in `agents-and-adr-process/decisions/` | accepted |

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
