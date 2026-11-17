# Sync the camera recordings and frames check into skellyfileformat

Prepared 2026-11-17 by the skellycam session, for the session that works in `../skellyfileformat`.
The owner asked for this hand-off. Nothing in skellyfileformat was changed.

## The decision

The owner decided on 2026-11-17: do not commit a camera recording (video or audio) or a camera frame (a
still image or a raw frame from a camera) to git. These files are large and can contain private
information. The one exception is a golden reference file. A screenshot that shows a camera image is a
camera frame. A chart, a diagram or a UI screenshot that shows no camera image is not.

The kit has the rule, a check and a skill since commit `6ee0444` on branch `dom/agents-and-adr-kit` of
`../project` (pushed). skellycam adopted them (skellycam ADR-G5S0 is the rule; ADR-NMM1 holds the design
choices of the check, still proposed).

## What skellyfileformat needs

1. Copy `agents-and-adr-process/bootstrap/tools/check_camera_media.py` to `tools/`. Keep
   `GOLDEN_PATHS = ("golden/",)`, the kit default.
2. Copy `agents-and-adr-process/bootstrap/tools/tests/test_camera_media.py` to `tools/tests/`.
3. Add the `camera-media` hook to `.pre-commit-config.yaml`, as in the kit file
   `agents-and-adr-process/bootstrap/.pre-commit-config.yaml`.
4. Copy the skill `agents-and-adr-process/bootstrap/.claude/skills/commit-files/` to `.claude/skills/`, and
   add its row to the skill table of `AGENTS.md`. `AGENTS.md` now says "This repository has no skills yet".
5. Add the rule text of the kit `bootstrap/AGENTS.md` section 8 (the paragraph that starts "Do not commit a
   camera recording", its bullets, and the changed pre-commit bullet) to the private-data section of
   `AGENTS.md`.
6. Record the rule under the Rules of the decision log of skellyfileformat. Entry 0001 is absorbed there, so
   the rule needs a new entry. Its source is the user, 2026-11-17.
7. Add the check to the CI doc checks, if the other checks run there.

## What was checked from outside

- A whole-repository run of the kit tool with the default golden list was reported clean: each tracked media
  file of skellyfileformat (92 MKV, 37 M4A, 15 MP4 and the others) is under `golden/`. Run
  `uv run python tools/check_camera_media.py --all` after the copy to confirm.
- The only known difference between the tools of skellyfileformat and the kit is `ALLOWED_EMAILS` in
  `check_private_data.py`.

## Not checked

- Whether the hook needs a change for the way skellyfileformat runs pre-commit.
- CI was not run.
