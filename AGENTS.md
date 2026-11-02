# FreeMoCap polyrepo workspace

## Current layout and publishing

Manifest checkout paths now live under `repos/`, including `repos/utils/`.
References below to original workspace paths are historical: prefix checkout
paths with `repos/`. Core's declaration is `repos/freemocap/pyproject.toml`.
The human runs `poe organize` once to move old checkouts; do not assume this
migration has happened until reported. It preserves local files and Git history.
The outer repository ignores `/repos/` and legacy checkout paths. Publish only
workspace tooling, instructions, manifest, and tests to
`https://github.com/freemocap/project`; never stage child repository contents.
New machines use `poe setup`. Child histories remain independent, without submodules.

## Authority and scope

## Continuity across compaction and handoffs

For substantial ongoing work, follow the portable
[context-continuity protocol](agent-guidance/context-continuity/SKILL.md).
At milestones, preserve the current objective, decisions and reasons, exact
checkout, existing interfaces, validation evidence, and a short reading list for
the next action in a task-specific checkpoint. Use an existing task handoff or
an ignored `.test-artifacts/continuity/<task-id>.md`; name its absolute path in chat.

After compaction or resume, read that checkpoint and the relevant ownership
sections here, then use the [recovery index](agent-guidance/freemocap-recovery.md)
to recover only the ontology, contracts and implementation needed next. Confirm
the checkout against `repos.toml` and Core's source declarations. Continue under
the existing authorization once the next action's meaning and ownership are
clear. Search for existing definitions and interfaces before filling gaps.
Escalate only consequential conflicts about intent that targeted inspection
cannot resolve; continue independent work. Archives and other worktrees provide
historical evidence, not implicit approval to change the current strategy.

## Local work authorization and protected state — explicit owner instruction

Non-mutating commands are always allowed. Run read-only inspection and
information-gathering commands without asking for permission.
This includes reading datasets, logs, diagnostics, and files outside the source
tree whenever the tool sandbox permits access. Do not ask conversationally for
permission to read them; only tool-enforced access approvals may still be needed.

The owner updated this policy on 2026-09-23. Agents may edit source, tests,
documentation, and other task-related files directly on disk without advance
patch previews or one-time permission. Preserve existing user work and leave
changes as unstaged, uncommitted working-tree diffs for human review unless the
owner explicitly authorizes staging, committing, or pushing them.

Tests and diagnostics are authorized on an ongoing basis, including normal
temporary files, caches, reports, screenshots, traces, and test-managed processes
that are cleaned up afterward. Do not request permission for these activities.
Tool-enforced sandbox approvals still apply. Dependency installation and
environment changes are not authorized merely by permission to run tests.

Generated artifacts must be ignored before they are created. Before running
tests, diagnostics, experiments, builds, or temporary scripts, identify their
output paths and verify that the owning repository ignores them with
`git check-ignore`. Add narrowly scoped `.gitignore` rules first when needed,
or use an external temporary directory. Prefer `.test-artifacts/` for local
test reports, screenshots, traces, generated bundles, scratch scripts, and
processed dataset copies. An outer workspace ignore does not apply inside
independent child repositories. Never hide source tests or intentional fixtures
with broad file-extension ignores. Before handoff, inspect untracked files and
check that generated artifacts have not become tracked. Ignore rules do not
untrack existing files; report those for explicit cleanup decisions. Do not delete
user data, untrack files, or rewrite history without the owner's direction and
subject to the Git authorization policy below.

The owner gives standing permission to perform task-related Git operations,
including staging, commits, fetches, branch management, and pushes, within the
repositories and workstreams already discussed. Continue without asking again.
Commit messages must be one sentence or less and describe only the change.
Never include an agent name or AI attribution in commit messages, author or
committer identity, co-author trailers, branch names, or other Git metadata.
Use the existing human-configured Git identity; do not invent an identity.

Repository scope remains a separate boundary: before working in a repository
not previously discussed for the task, pause that portion of the work, identify
the repository and reason, and obtain the owner's direction. Continue independent
work within the agreed repositories. Git permission does not expand task scope.
Preserve unrelated work. Destructive resets, discarding changes, history rewriting,
force-pushes, and release tags require explicit authorization for those actions.
Inspect wrappers before running them so their effects stay within task scope.
This policy supersedes older human-only Git rules and stale copied instructions.

Read-only Git and cloud inspection is allowed; prefer Git's --no-optional-locks
for status inspection. Agents must not mutate gCloud configuration or resources.
Historical setup/fetch/pull/align/force notes below are not standing authorization.
Tool-enforced sandbox and approval checks still apply. If an authorized action
is rejected, report the exact action and reason; do not bypass the rejection.


This file governs work across this workspace and its independent repositories.
The project owner established these rules on 2026-09-21. Follow them over older
plans, comments, or scripts that describe conflicting workflows. Read any more
specific repository instructions before editing. Recheck live configuration and
Git state; the dated observations below are an orientation snapshot.

The owner authorized workspace setup/status/fetch tooling after onboarding.
Existing child branches, dependency declarations, environments, and user work
remain untouched unless the task explicitly addresses alignment. The owner
subsequently authorized `poe align` and discarding SkellyCam's tracked local
changes to align it with core. This does not authorize discarding other work.

## Repository ownership and architecture

### Understand established architecture before proposing changes

Before planning or changing a subsystem, recover its purpose, accepted tradeoffs,
owning interfaces, and existing optimization mechanisms from current source,
tests, and strategy documents. Trace the actual path end to end. State those
invariants in the task plan before inventing constraints or proposing alternatives.
Treat missing context as a research obligation, not evidence that the design is
missing. Do not ask the owner to reapprove an established decision because an
agent-authored plan contradicted it; correct the plan and continue authorized work.

**Transport is deliberately fully self-describing.** Every server message carries
the information needed to interpret it independently. The server sends the message;
the client interprets that message without requiring matching prior server/client
state. Repeated metadata and its bandwidth cost are accepted to protect this property.
Preserve the existing handling of repeated data, metadata identity, validation,
buffer ownership, and shared realtime/posthoc rendering paths. Do not propose
delta-only metadata, out-of-band prerequisites, or state-dependent decoding as a
routine bandwidth optimization. Changes to that strategy require an explicit owner
request, not an incidental visualization task.

For transport or visualization work, inspect the composition/encoding path,
connection-owned decoder caches and reconciliation, static-model subscriptions,
and numerical worker-buffer lifecycle before evaluating cost. Distinguish repeated
wire metadata from repeated model construction, validation, renderer preparation,
or worker transfer. Measure the relevant complete path and use existing efficiency
mechanisms; do not label intentional self-description as a newly discovered defect.

### Thin Core and editable local development

The owner updated this policy on 2026-10-31: development uses editable local
checkouts, and agents may implement and validate a task across repositories
without stopping for commits, pushes, or dependency publication between them.
This supersedes older instructions requiring repository-by-repository handoffs.

Keep FreeMoCap Core minimal. Code belongs in Core only when it inherently
requires cooperation between multiple subrepositories. Put every behavior that
can live in an individual subrepository in that repository, including its domain
logic, schemas, configuration, processing, and tests. Being called by Core does
not make a behavior Core-owned. Core connects public interfaces and coordinates
the combined application; it must not reimplement subrepository responsibilities.

Before placing code in Core, identify the subrepositories it must coordinate
and why the behavior cannot belong to one of them. If it can, implement it there
and expose the interface Core needs. Cross-repository editing changes the workflow,
not these ownership boundaries or the requirement for standalone usability.

### Tracking ownership and vocabulary

When changing tracker composition, put detector stage recipes, crop rules,
keypoint schemas/connections, output assembly, and preset-specific mapping
selection in SkellyTracker. Core selects the preset and passes application
settings; it must not reconstruct that recipe or maintain a duplicate schema.
Verify that the same preset works in standalone Tracker without importing Core.
Core owns camera/Tracker/Forge integration and only the lifecycle and transport
coordination that requires multiple subrepositories. Component-specific lifecycle
and transport belong to the component's repository.

Use **keypoint** for detector output, **mapping** for the rules converting
keypoints into observations of named anatomical landmarks, and **landmark** for
the anatomical model point defined in SkellyForge. Tracker owns mapping definitions
and numerical evaluation; Forge owns anatomical geometry and reconstruction.
Core may connect those interfaces but must not duplicate their domain algorithms.
Tracker's `Observation` container is not interchangeable terminology with mapped
observations of anatomical landmarks. State code ownership separately from which
application calls it. Keep numerical assembly in dense arrays with prepared indices;
do not introduce per-keypoint dictionaries or scalar loops on frame paths.

| Directory | Responsibility | Useful entry points |
| --- | --- | --- |
| `freemocap/` | Core application: composes the subprojects into the motion capture pipeline | `freemocap/core/pipeline/{realtime,posthoc}/`, `freemocap/core/tasks/`, `freemocap/core/tracking/`, `freemocap/core/streaming/`, `freemocap/api/`, `freemocap/app/` |
| `skellycam/` | Standalone camera capture, synchronization, recording, and streaming | `skellycam/core/`, `skellycam/api/`, `skellycam-ui/` |
| `skellytracker/` | Standalone image analysis and detection | `skellytracker/core/`, detector implementations, mapping definitions in `core/io/` |
| `skellyforge/` | Standalone 3D geometry, skeleton reconstruction, and kinematics | `skellyforge/core/math/`, `skellyforge/core/skeleton/`, `skellyforge/core/biomechanics/`, `skellyforge/definitions/` |
| `freemocap_blender_addon/` | Downstream receiver for visualization and animation in Blender | `freemocap_blender_addon/freemocap_data_handler/`, `core_functions/`, `blender_ui/` |
| `utils/skellylogs/` | Shared logging library | `skellylogs/`, `tests/` |
| `utils/skellypings/` | Telemetry client and separately configured server | `skellypings/`, `server/`, `infra/` |
| `utils/skellydocs/` | Shared Docusaurus theme and documentation CLI | `README.md`, `package.json` |

Entry points in the last column are relative to their repository.

- SkellyCam, SkellyTracker, and SkellyForge must remain independently usable.
  They must never import one another, including in tests or type-only imports.
  They must not depend on FreeMoCap core to operate.
- FreeMoCap core owns only composition, adapters, and integration contracts that
  require multiple subrepositories. Put checks that need multiple subskellies in
  Core; keep component behavior and its tests in the owning repository.
- Shared utilities remain independent packages with their own change lifecycle.
- Work across repositories as needed to complete the authorized task. Keep each
  repository's changes independently reviewable and validate both the owning
  components and their integration through the configured editable checkouts.
- Use the configured editable local dependencies through normal package imports.
  Do not bypass ownership boundaries or package interfaces with sibling-path
  imports or `PYTHONPATH` manipulation. Editable installation does not authorize
  imports between SkellyCam, SkellyTracker, and SkellyForge.

## Cross-repository workflow and Git authorization

The owner controls Git authorization under the policy above. Agents may perform
explicitly authorized commits and pushes; publication is not a prerequisite for
working across editable local checkouts.

Commit messages, including suggested messages, must be one sentence or less and
describe only the change. Never mention the agent, its name, or AI assistance;
never include agent attribution or a `Co-authored-by` trailer for an agent.

1. Before editing each affected repository, inspect its branch, status, diff,
   dependency declarations, and relevant instructions. Preserve existing work.
2. Assign each behavior to its owning repository before implementation. Keep
   Core changes limited to necessary coordination between subrepositories.
3. Implement the component interfaces and consumer integration across the local
   checkouts. Continue across repository boundaries without commit/push gates.
4. Validate component behavior in its owning repository and cross-repository
   integration in Core. Verify that the consumer uses the intended local sources.
5. Present a per-repository diff summary, validation results, and limitations.
   Leave changes unstaged and uncommitted unless publication is explicitly
   authorized. When authorized, inspect the intended diff, stage only the approved
   changes, commit and push within scope, and verify and report the result.

## Branch and dependency policy

- `repos/freemocap/pyproject.toml` is authoritative for dependency configuration.
  Read `[tool.uv.sources]` for installed sources and
  `[tool.freemocap.workspace.sources]` for editable checkouts' Git URLs and branch
  targets. For Git UV sources, use their declared branch. Do not infer targets
  from Core's branch name or an old README.
- Before implementation in a dependency repository, compare its active branch
  to the branch declared by core. Report a mismatch and resolve it with the
  human before editing. Do not alter core's source declaration merely to fit
  an existing checkout.
- Preserve dirty checkouts. Do not automatically stash, reset, discard, or move
  existing work. The owner explicitly requested that the initial mismatched
  checkouts below remain untouched for now.
- Sources without an explicit branch target do not establish a named branch
  policy; preserve the current branch unless the task explicitly addresses it.
- For editable dependencies, verify the configured path, installed editable
  metadata, and actual import location. The working-tree source, including
  uncommitted edits, is what the consumer must exercise; a commit SHA alone does
  not identify that code. Ordinary source edits need no publication or Git refresh.
- For Git-pinned dependencies, verify the declared source, locked commit, and
  installed revision when investigating integration problems. Cached remote refs
  are not proof of current remote state. Dependency installation, lock refreshes,
  and environment changes still require task authorization; crossing repository
  boundaries does not itself require them.
- Do not delete lockfiles as routine setup. The owner explicitly authorized
  `poe align` to delete root uv.lock files and run uv sync across the workspace's
  Python repositories after Git updates, including core. This is a deliberate
  full refresh; regenerated lockfiles remain subject to human review/commit/push.

## Development and validation

### References and intellectual provenance

When research, external documentation, tutorials or source repositories inform
scientific claims, architecture or implementation, register the sources in the
owning independent repository's root `references.bib` and cite stable keys beside
the supported claims. Create that file on first use, not preemptively in every
checkout. Prefer preserving useful references and verified metadata as an
intellectual paper trail, including sources beyond formal academic publications.
Use Better BibTeX-compatible BibTeX, explicit `url`, access date, `review` scope
and `claim` fields; record limited access honestly and never invent metadata.
Add bibliography/citation validation with the first adoption, and run it when
citations change. Follow the owning repository's `CITATIONS.md` for exact format
and checks. Core's policy is in its root `CITATIONS.md`; other repositories adopt
their own policy and tests when citation-bearing work reaches them. Keep those
changes within their normal independent review boundaries.

- Run Git and environment commands inside the relevant repository (or use
  `git -C <repo>`). The workspace parent is its own Git repository for tooling
  and guidance; child checkouts are ignored by that repository.
- Each Python repository owns its `pyproject.toml`, `uv.lock`, and environment.
  Inspect its actual dev groups/extras before installing or running tests.
  SkellyForge and SkellyTracker currently require Python >=3.11,<3.13.
- Core's Python entry point is `freemocap.__main__:run_main`; its backend serves
  the React/TypeScript/Electron UI in `freemocap/freemocap-ui/`.
  The documented development backend port is 8005; frontend starts with
  `npm run dev` from the UI directory.
- Core defaults to the `tracker-default` group: CUDA on Windows/Linux and CPU
  on macOS. CPU-only Windows/Linux uses `--no-default-groups --group cpu`;
  include `--group dev` when development tools are needed. Do not combine CPU
  and CUDA groups: their onnxruntime installations conflict.
- Python tests live in `freemocap/freemocap/tests/`,
  `skellycam/skellycam/tests/`, `skellytracker/skellytracker/tests/`, and
  `skellyforge/skellyforge/tests/`. Run focused relevant tests first.
  Core calibration/pipeline tests can require `FREEMOCAP_TEST_DATA_PATH`, real
  recordings, model assets, or hardware. Report skips and missing prerequisites.
- Core's `poe_tasks.toml` provides test and lint tasks, but verify their paths:
  several named test tasks reference files absent from this checkout.
  The UI currently has no `npm test` script despite `test-ui` calling it.
  Streaming/renderer TypeScript tests document esbuild + Node invocation in
  their file headers; `npm run e2e` invokes Playwright.
- Inspect task bodies before execution. Core's `bump-*` tasks invoke bumpver
  configured with `commit = true`, `tag = true`, and `push = true`; running them
  requires explicit authorization for all those actions. `poe update` pulls multiple repos and deletes
  `uv.lock`; `poe go` invokes it. Do not use them as routine agent commands.
- For reconstruction/streaming work, use
  `repos/freemocap/current-work-plans/01-data-model/ontology.md` and the relevant
  layer selected through `repos/freemocap/current-work-plans/README.md`.
  Read the current task's named handoff, not an assumed root `HANDOFF.md`.
  Archived plans are historical; dated test claims are not fresh verification.
- Before changing geometry or transport, read
  `repos/freemocap/current-work-plans/00-foundation/conventions.md` and the owning
  boundary conversion. Distinguish dimensionless authored geometry from measured
  millimeters and name the coordinate frame at each boundary; older +X-forward
  notes do not describe Forge's Blender authoring frame. Use the maintained
  conventions rather than copying an abbreviated rule into a new implementation.

## Initial observations — 2026-09-21

| Repository | Active branch | Core source branch | Observation |
| --- | --- | --- | --- |
| freemocap | development-streaming | n/a | Clean |
| skellycam | development | main | Mismatch; modified UI package.json, package-lock.json, and uv.lock |
| skellytracker | development-streaming | development-streaming | Match; clean |
| skellyforge | development-streaming | development-streaming | Match; clean |
| freemocap_blender_addon | development | development-streaming | Mismatch; clean |
| utils/skellylogs | main | Unspecified Git branch | Clean |
| utils/skellypings | main | Unspecified Git branch | Untracked `env copy.example`; preserve it |
| utils/skellydocs | main | Not a core Python dependency | Clean |

Historical architectural debt observed on 2026-09-21: SkellyForge declared SkellyTracker as a dependency
and imported it in `skellyforge/skellymodels/standard_human/tracker_contract.py`,
`skellyforge/tests/test_tracker_contract.py`, and
`skellyforge/tests/test_face_mapping_consistency.py`. Older comments and handoff
notes call this a sanctioned exception. The owner's current no-cross-import
rule supersedes those notes. Do not extend this coupling. Plan its removal and
relocation of cross-repository validation to core as a separate staged change;
this orientation task does not authorize an incidental refactor. These paths and
the dependency are absent from the audited 2026-11-01 canonical Forge checkout;
inspect current sources before treating this historical note as unfinished work.

This workspace-level file is local guidance, outside the independent Git
repositories. If these instructions need to travel with separate clones,
coordinate repository-level copies or a shared maintained policy with the owner.

## Workspace management tooling

The initial upper-level tools are implemented in `scripts/workspace.py` with
`poe setup`, `poe status`, `poe fetch`, `poe pull`, and `poe align` entry points. Use the name `setup` in
commands and documentation. Read README.md for usage and limits. Tests in
`tests/` create disposable Git repositories and synthetic history only.
`poe align` fetches origin, follows explicit core source branches, and pulls
the selected dependencies with fast-forward only, then deletes root uv.lock
files and runs uv sync in each selected Python repository. With no names,
environment refresh includes core and all manifest repositories with root
pyproject.toml files. Report alignment complete only when pulls and syncs succeed. Without
repository names it handles all core dependencies. `--force` discards tracked
changes even when already on the target branch; unpinned dependencies keep their
current branch. Untracked files are preserved and do not by themselves block pull.
Only run force where the human has authorized discarding that repository's work.
Batch commits/pushes require explicit owner authorization for the batch scope.

`poe pull` fetches and fast-forwards manifest repositories, core first, with
source declarations re-read after core updates. It blocks dirty/mismatched
checkouts and never creates commits or refreshes environments. A core failure
stops the batch; other blocked repositories are reported while the rest proceed.

Prefer an inventory that identifies independent repository paths while deriving
dependency branch targets from core's pyproject.toml, avoiding a duplicate branch
source of truth. A read-only status/preflight command could show expected and
actual branches, dirty files, upstream state, and core's locked dependency SHAs.
Later batch mutations should preview their plan, preserve local work, and report
partial completion clearly. Helpers follow the same explicit Git authorization
policy. Commits and pushes are not prerequisites for local cross-repository work.
