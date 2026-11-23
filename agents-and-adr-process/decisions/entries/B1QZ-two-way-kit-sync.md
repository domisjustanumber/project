# B1QZ — The kit is a two-way hub: kit_sync.py, manifest.toml and a repo-owned kit.toml

**Status:** accepted, 2026-11-23 (user, decisions Q635 to Q639, Q655 and Q656 given in the skellycam session; backfilled).

## Decision

1. **Two ways.** Each repo that uses the kit takes the changes of the kit, and gives its own changes
   of the kit text back to the kit. One tool does both: `bootstrap/tools/kit_sync.py`, the same file
   in each repo, with `check`, `pull` and `propose`. Standard library and the git CLI only. Python
   3.13 or later.
2. **Kit text.** [`manifest.toml`](../../manifest.toml) lists the units: kit-owned files, and kit-owned
   blocks between marker lines in a repo file. All other text is repo text. A value of a repo in a
   unit is a placeholder in the kit.
3. **`kit.toml`.** Each repo owns one `kit.toml` with its values: `[sync]`, `[values]`, and a table
   for each check tool. The tools read their tables through `tools/kit_config.py`, which fails
   closed: a missing table, an unknown key or a value of the wrong type stops the tool. The table
   `[kit]` at its end holds the kit commit, the SHA-256 of `[values]` and of the filled text of each
   unit, and each proposed local change that waits for the kit.
4. **CI.** CI runs only the offline `check`, through the doc test. A note that a newer kit exists is
   only for a local run (Q639).
5. **Path of a rule.** A rule comes up in a repo and gets an entry there. `propose` writes it into
   the kit with the values changed back to placeholders. A PR to freemocap/project cites that entry.
   Each repo then runs `pull`. The kit text cites only the kit entry 0001.
6. **Pilot.** skellycam is the pilot (Q635). Its rows won where the table of the brief says so
   (Q638). skellytracker then removes its one-way tool `tools/sync_bootstrap_kit.py`.
7. **Values.** The skill takes the branch as Markdown text, `DEFAULT_BRANCH_TEXT`, so that a repo
   can write "upstream `development`" (Q655). The uv of the doc checks is kit text, the same in each
   repo (Q656).

## Reason

- The user, in words: "any repo using the kit must be able to sync back to it, and pick up changes
  from the kit into it's version. Not just skellytracker."
- Before, only skellytracker wrote to the kit, one way. No repo recorded the kit state that it took,
  and four repos copied the kit by hand and drifted.
- The hash of the filled text lets `check` run with no kit checkout and no reverse fill.
- A waiting local change keeps the repo of the rule green until the kit takes the change.
- The pilot review found that a misspelt table gave a default that allowed media. Thus the reader
  fails closed, and `golden_paths` allows none by default.

## Consequences

- The kit tools are the same file in each repo. A repo value is in `kit.toml`, not in the code.
- A repo with a new rule needs one entry there and one kit PR.
- The section "Keep the kit current" of the kit README stays until skellytracker takes `kit_sync.py`.

## Evidence

- The skellycam pilot on kit 05a3d2d: `check` passes on 39 units, a second `pull` changes
  nothing, 442 tool tests pass (reported by the skellycam session, 2026-11-23).
- `tests/test_kit_sync.py` of this repo tests `pull`, `propose`, the refusals and the manifest.

## Alternatives rejected

- **The edit lists of `sync_bootstrap_kit.py` for each repo.** They hold the values of one repo in
  code, and they work one way only.
- **Unfill the local text in `check`.** A short value such as `main` is ambiguous. The hash of the
  filled text needs no unfill.

## Not repeated

- An older `kit_sync.py` runs the first `pull` of a newer kit. The new tool now runs the pull once
  more after it replaces itself.
