# Continuity validation — 2026-11-01

## Results

- 12 workspace tests pass: eight bibliography tests and four installer tests.
  Installer cases cover preservation, idempotence, malformed block rejection and
  conflicting skill rejection before any destination changes.
- Workspace bibliography: four entries, zero errors. Core bibliography: 58 entries,
  zero errors; Core's eight validator tests also pass after the ontology edit.
- The continuity skill and updated workspace checklist skill pass the bundled
  skill validator using Core's existing environment. No packages were installed.
- Every local link in the new recovery index and canonical AGENTS files resolves.
- Installed personal continuity skill matches its reviewed workspace source.
- Changed tracked guidance passes `git diff --check`. All nine repositories have
  no staged changes and no tracked `.test-artifacts` files. New test output is
  under the already-ignored workspace `.test-artifacts/compaction-audit/`.
- Hashes of previously dirty files match the baseline except workspace AGENTS.md,
  which this task intentionally extends. Existing Core/Tracker implementation,
  bibliography and untracked test changes are preserved.

The first installer-test attempt hit Windows sandbox permissions in its default
temporary directory. Rerunning with temporary storage inside the verified ignored
artifact directory passed. The system Python lacked PyYAML for skill validation;
Core's existing Python supplied it without changing an environment.

## Source-based recovery walkthroughs

These are manual checks of the instructions and their destinations against current
code, not independent model evaluations or a forced-compaction experiment.

| Continuation scenario | Recovery route and checked evidence | Result |
| --- | --- | --- |
| Summary omits the combined tracker recipe | Tracker AGENTS → TRACKER_COMPOSITION → `human_tracker_config` and `combined_tracker_config` in `tracker_presets.py` | Existing recipe found in Tracker; Core need not recreate it |
| Summary conflates mapped observations with reconstructed landmarks | Ontology dynamic trajectory products → addon AGENTS → `read_recording` in `parquet_recording.py` | Reader explicitly distinguishes LANDMARKS_3D and MAPPED_KEYPOINTS_3D |
| Old note implies all geometry is +X forward in mm | Recovery index → foundation conventions → Forge coordinate definitions and human YAML | Authored reference-unit geometry, measured units and Blender authoring frame are distinguished |
| Summary proposes an exposure task separately for each backend | Cam AGENTS → camera-group tasks → `CameraBackendManager.create_or_update_camera_group` | Existing manager invokes shared `recommend_exposure`; recovery finds the abstraction |
| Ontology says posthoc is deferred | Corrected pointer → posthoc plan → `mocap_pipeline.py` | Implemented pipeline is discoverable; the ontology no longer supplies obsolete progress status |
| Checkpoint names a different worktree | Manifest/source-declaration check before inspecting or editing | Instructions require matching the task's explicit checkout; no automatic worktree switch |
| Maintained plan and current code disagree about an unrecorded owner decision | Protocol's gap-resolution branch | Gather evidence, ask the smallest consequential question, continue independent work; no guessed architecture |
| Compaction occurs halfway through an approved checklist item | Continuation section → checkpoint approval, partial operations and current diff | Existing approval survives; only verified completed items are checked off |

## Change ownership

| Location | Changes |
| --- | --- |
| Personal Codex | New AGENTS continuity section and context-continuity skill; appended continuation section in personal checklist skill |
| Workspace | Protocol sources, recovery index, audit, installation helper and preservation tests, source registry/validator; targeted AGENTS fixes and local checklist-skill section |
| Core | AGENTS recovery routes; stale posthoc paragraph replaced by maintained status pointer |
| Tracker | AGENTS recovery routes; CLAUDE points to current ownership/composition guidance |
| Cam | New AGENTS with backend, camera-group, recording and timing routes |
| Forge | New AGENTS; repaired CLAUDE ownership/ontology links and obsolete test setup advice |
| Blender addon | New AGENTS with recording products, transform, packaging and validation routes |
| Logs | New AGENTS with handler/queue versus consumer relay boundary |
| Pings | New AGENTS with client/server and live telemetry/cloud boundaries |
| Docs | New AGENTS with browser-theme versus Node CLI and consumer-site ownership |

## Limits

No application code changed, so hardware, inference and application regression
suites were not run. No unrelated projects or alternate worktrees were modified.
The isolated runtime check proves configuration acceptance/readback only.
The subsequent UI trial below verifies one manual compaction and continuation;
Hook context injection remains untested. The passive real-work observation below
adds evidence of an in-turn boundary, without instrumented trigger telemetry.
The deployed behavior relies on instructions and checkpoints; it is not a
runtime-enforced editing barrier. No global hooks, thresholds or prompt overrides
were enabled. See [audit](AUDIT.md) for the evidence behind that choice.

## UI follow-up — 2026-11-01

Trial 01 (chat `01a1976b-616e-7100-a7d5-6683a3e0efa9`) recorded a real compaction
before its analysis continuation. The agent first read its checkpoint and skill,
recovered ownership and existing interfaces, and completed without domain reminders.
It distinguished inspected tests from executed tests. Its diff review was limited
to statistics. This is a bounded behavioral pass, not a controlled comparison or
evidence of automatic mid-turn reliability.

The protocol now requires actual relevant patch hunks, separate staged/unstaged
review when applicable, direct reads of untracked files, and baseline comparisons
outside Git. Review stays scoped to the next edit and dependencies. The installed
global skill matches the workspace source; skill validation and all 12 workspace
guidance-tooling tests pass after this change.

Trial 02 (chat `01a19795-b1ea-7031-bc10-3bfe8068667c`) uses disposable stdlib code
under ignored `.test-artifacts/continuity-implementation-02/`, immutable baseline
copies, pre-existing local edits, and a requirement correction with rationale.
It paused after component implementation while application integration remained
unfinished. The app recorded a completed contextCompaction before the user's
minimal continuation. Before its first resumed edit, the agent read its checkpoint,
instructions, implementation and actual baseline patches. It retained the corrected
absence semantics and rationale, reused the component interface, and preserved
the seeded local edits. Reviewer reruns passed all 9 fixture tests and all 5
independent acceptance checks, including baseline/user-file hashes and nested
result ownership. This is a bounded implementation-recovery pass, not evidence
of automatic mid-turn reliability or improvement over an untreated baseline.
Detailed local evidence and the independent evaluator are in
`.test-artifacts/compaction-audit/` and are intentionally untracked.

## Natural mid-turn observation

A read-only review of the active **hands and stuff** chat found a compaction
inside an ongoing implementation turn at 2026-11-01 14:58:25.927 UTC, followed by
continuation without user prompting. The agent read logs and targeted sources,
but edited before re-reading its checkpoint or reviewing the relevant patch.
Timing audit subsequently established that the chat had read the older skill
before the revision was installed during its ongoing turn. Receipt of the new
actual-patch paragraph was not demonstrated. This is not a fair failure verdict
for the revised skill, nor an independently established code defect.
The trigger was not explicitly labeled in the inspected record and the task
was still active; do not report a completed automatic-recovery pass.
See [investigation and next test design](mid-turn-testing.md).
The active **Investigate real-time skeleton blinking** chat demonstrably read the
revised skill at 15:03:46.890 UTC; its next natural compaction is an eligible
candidate, with no event yet observed at the timing audit.
