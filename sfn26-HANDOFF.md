# sfn26 development workspace

The five application repositories have local `sfn26` branches published to
`origin/sfn26`: FreeMoCap, SkellyCam, SkellyTracker, SkellyForge, and the Blender
add-on. FreeMoCap's initial commit includes the previously pending tensor and
pipeline work. Utilities retain their existing branches.

## Editable dependencies

FreeMoCap's `tool.uv.sources` now points to the four sibling application
checkouts with `editable = true`, plus SkellyLogs and SkellyPings under
`../utils/`. The installed core environment uses those local copies.
`skelly_synchronize` remains a Git dependency because there is no managed local
checkout for it.

SkellyCam uses editable utility checkouts. SkellyTracker uses the local
SkellyForge checkout, and SkellyForge uses the local tracker for its existing
development dependency. Their existing architecture is unchanged.

Core's `tool.freemocap.workspace.sources` table retains clone URLs and branch
targets. The workspace commands use this table for editable dependencies and
continue reading Git UV sources on older branches. Local paths must match the
checkout paths in `repos.toml`.

## Development commands

From `repos/freemocap`, run `uv sync --locked --group dev` to install the core
application and editable dependencies. The default tracker group selects CUDA
on Windows/Linux and CPU on macOS. For CPU-only Windows/Linux use
`uv sync --locked --no-default-groups --group cpu --group dev`.

From the workspace root, `poe status` inspects branches. With clean checkouts,
`poe switch BRANCH --dry-run` previews selection of a core branch and its declared
dependency branches. `poe switch BRANCH` applies that selection using local refs.
Fetch, pull, and environment refresh remain separate operations.

GitHub default-branch settings have not been changed. Creating and pushing
`sfn26` does not change those settings.
