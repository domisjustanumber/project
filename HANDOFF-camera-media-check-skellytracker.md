# Sync the camera recordings and frames check into skellytracker

Prepared 2026-11-17 by the skellycam session, for the session that works in `../skellytracker` and its
worktrees. The owner asked for this hand-off. Nothing in skellytracker was changed.

## The decision

The owner decided on 2026-11-17: do not commit a camera recording (video or audio) or a camera frame (a
still image or a raw frame from a camera) to git. These files are large and can contain private
information. The one exception is a golden reference file. A screenshot that shows a camera image is a
camera frame. A chart, a diagram or a UI screenshot that shows no camera image is not.

The kit has the rule, a check and a skill since commit `6ee0444` on branch `dom/agents-and-adr-kit` of
`../project` (pushed). skellycam adopted them (skellycam ADR-G5S0 is the rule; ADR-NMM1 holds the design
choices of the check, still proposed).

## What skellytracker needs

`python tools/sync_bootstrap_kit.py --check` was reported to show two differences from the kit now:
`AGENTS.md` section 8 (private data) and `.pre-commit-config.yaml`.

1. Add `tools/check_camera_media.py` and `tools/tests/test_camera_media.py` from
   `agents-and-adr-process/bootstrap/tools/`, and add both to `COPIES` in `tools/sync_bootstrap_kit.py`.
   Set `GOLDEN_PATHS` to the folders that hold golden reference recordings in skellytracker, if it has any.
   The kit default is `("golden/",)`. If the list differs from the default, `COPIES` needs an edit for it.
2. Add the `camera-media` hook to the live `.pre-commit-config.yaml`.
3. Add the rule paragraph of the kit `bootstrap/AGENTS.md` section 8, its bullets and the changed
   pre-commit bullet to the live section 8.
4. The skill: adopt the kit skill `commit-files`
   (`agents-and-adr-process/bootstrap/.claude/skills/commit-files/`), or put its rule into the skill
   `stack-commit`. The skellytracker session decides.
5. Write a decision entry in skellytracker for the rule. Its source is the user, 2026-11-17.
6. Run `python tools/sync_bootstrap_kit.py --write`, then `--check`.

The rule text in the kit is inside a block that was synced from skellytracker. If the wording must change,
change it in skellytracker and sync the kit again.

## What was checked from outside

- `python ../project/agents-and-adr-process/bootstrap/tools/check_camera_media.py --all`, run in
  `../skellytracker` on 2026-11-17 with the default golden list: no findings in 937 tracked files. This run
  read the checked-out branch only, not the other worktrees.

## Not checked

- The worktrees `../skellytracker-native-jpeg` and `../skellytracker-node-redesign`.
- Whether the hooks are active in each worktree. In skellycam the hooks are set for each worktree with
  `git config --worktree core.hooksPath .githooks`, because the worktrees share one `.git` directory.
