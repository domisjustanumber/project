# FreeMoCap recovery index

Use this index after compaction or handoff to answer the next action's specific
questions. Read the task checkpoint first. It identifies the current goal, latest
owner decisions, exact checkout, approved plan stage and evidence. This index
routes recovery; it does not declare every linked plan active or implemented.

## Locate the working source

[repos.toml](../repos.toml) names canonical checkouts;
[Core's source declarations](../repos/freemocap/pyproject.toml) identify editable
paths and branch targets. Preserve dirty working trees. Alternate cleanup/theme
checkouts and `skellyforge-worktrees/` belong to separate workstreams. Select one
only when the current task explicitly identifies it. This workspace uses
independent repositories, so ignore rules and tests belong to each owner.

Before resuming an edit, review the actual relevant patch hunks in the owning
repository, including staged changes when present, and read relevant untracked
files directly. Status and diff statistics only locate changes. Apply the
context-continuity skill's recovery procedure to distinguish existing user work
from the task's partial implementation without auditing unrelated repositories.

## Recover the relevant meaning

| Next action concerns | Read to answer the ownership or contract question |
| --- | --- |
| Keypoints, mapped observations, landmarks or skeletons | [Ontology](../repos/freemocap/current-work-plans/01-data-model/ontology.md); which layer owns the definition and which data product is being changed? |
| Frames, units, rotations or scaling | [Conventions](../repos/freemocap/current-work-plans/00-foundation/conventions.md), then the owning conversion code; what is authored, measured, or transformed? |
| Array assembly and identities | [Tensor contract](../repos/freemocap/current-work-plans/01-data-model/tensor-contract.md); what axes and identity order must remain aligned? |
| Detector composition or mapping | [Tracker guidance](../repos/skellytracker/AGENTS.md) and [composition](../repos/skellytracker/TRACKER_COMPOSITION.md); what public preset/interface already owns this recipe? |
| Application integration of tracking | [Core integration](../repos/freemocap/TRACKER_COMPOSITION_INTEGRATION.md); which coordination actually requires multiple components? |
| Capture, synchronization or backend selection | [Cam guidance](../repos/skellycam/AGENTS.md); which camera-group abstraction already handles the operation? |
| Reconstruction or authored skeleton geometry | [Forge guidance](../repos/skellyforge/AGENTS.md); which definition and solver own the math? |
| Recording publication, provenance or replay | [Recording contract](../repos/freemocap/RECORDING_CONTRACT.md); which persisted product and identity does the operation consume? |
| Streaming lifecycle or payload ownership | [Connection ownership](../repos/freemocap/current-work-plans/03-transport/connection-ownership.md) and [Cam payload ownership](../repos/freemocap/current-work-plans/03-transport/skellycam-payload-ownership.md); who creates, retains and releases the resource? |
| Blender export/import | [Addon guidance](../repos/freemocap_blender_addon/AGENTS.md); which recorded product and coordinate conversion does the receiver need? |
| Logging, telemetry or documentation tooling | The owning utility's AGENTS.md under `repos/utils/`; distinguish reusable component behavior from application integration. |

For strategy or progress, use the checkpoint's work-plan link and
[current plan index](../repos/freemocap/current-work-plans/README.md). A proposal
does not replace an implemented architecture merely because it appears newer.
Inspect relevant code and tests to distinguish current behavior from intended
changes. Recover only enough to identify the existing interface to extend and
the next validation step; expand reading when a specific contradiction requires it.

If a breadcrumb moved, find its maintained replacement and repair the pointer
within scope. If documentation and code disagree about consequential intent,
record both sources and the smallest decision needing owner input. Continue
independent authorized work. Do not recreate missing context as new architecture.
