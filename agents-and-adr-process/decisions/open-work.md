# Open work

This file holds the open work of the [decision log](README.md) of the kit. Read the items that
apply to your task. Delete an item when its work is done. The PR that closes an item records the
result.

- **The merge branch of the kit.** For now the kit work merges into `dom/agents-and-adr-kit`
  (user, 2026-11-23: "everything gets merged into dom/agents-and-adr-kit for now"). The branch
  of freemocap/project that `dom/agents-and-adr-kit` merges to is not chosen
  ([ADR-B1QZ](entries/B1QZ-two-way-kit-sync.md)).
- **The adoption of the other repos.** skellycam is the pilot. skellytracker removes
  `tools/sync_bootstrap_kit.py` and takes `kit_sync.py`. skellyspecs, freemocap and skellycertify
  take the kit when they choose. Then the section "Keep the kit current" of the kit README goes
  ([ADR-B1QZ](entries/B1QZ-two-way-kit-sync.md)).
- **The module templates.** `module/` is not in `manifest.toml`. A repo copies it one time
  ([ADR-B1QZ](entries/B1QZ-two-way-kit-sync.md)).
- **The kit tests in CI.** The workflow of this repo runs the unittest tests in `tests/`. It does not
  run the pytest tests of `bootstrap/tools/tests/`. One of them, the `.gitignore` test of
  `test_private_data.py`, cannot pass in the kit folder, because the kit is not a repo.
