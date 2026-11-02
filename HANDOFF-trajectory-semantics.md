# Separate keypoint observations from reconstructed landmarks

Prepared 2026-10-05 for a secondary agent that the workspace owner will start. This is an implementation handoff, not a report of a completed fix. The originating chat is designing Blender integration and has made no pipeline changes.

## Follow up review and Blender restart

Reviewed later on 2026-10-05 against FreeMoCap `c8c458f3` and Forge `8a28aab`. The original investigation and implementation instructions below are historical. The upstream separation has now been implemented; do not repeat that work from this handoff.

Core now preserves `mapped_keypoints`, synthesized rigid `landmarks`, and explicit `segment_origins`. Recording and streaming expose `MAPPED_KEYPOINTS_3D`, `LANDMARKS_3D`, and segment pose channels separately. The optional solver input reader uses mapped observations. Core's locked and installed Forge commit both match `8a28aab7f57a6d7e268e5e67baca026bccaf6bcd`. Core, Forge, and the Blender add-on checkouts were clean and on `development-streaming` at inspection. No remote freshness claim is implied.

Forge now supplies `synthesize_anchored_pose`: it preserves measured world orientations and connects the observed component through declared joint attachments from a selected anchor. The anchor can be the skull or a hand, not only the anatomical root. Its absence prevents connected output; missing intermediate poses break the component. The anchor does not redefine the world coordinate frame or anatomical parent tree. Core persists anchor selection in the recorded model.

### Current Blender design

The three paths remain required:

| Input | Construction | Purpose |
| --- | --- | --- |
| Legacy NPY recording | Existing Blender reconstruction | Preserve old recording support |
| New Parquet mapped keypoints | Compatibility projection, then Blender reconstruction | Compare Blender reconstruction with upstream reconstruction |
| New Parquet rigid landmarks and segment poses | Import saved geometry and transforms | Native Blender skeleton without reconstructing again |

Use the native result's `SEGMENT_ORIGINS` and `ROTATIONS_WORLD` as authoritative segment transforms. Use recorded skeleton/rest geometry and segment scales for dimensions. Never reconstruct origins from mapped observations. The earlier concern about preserving independently placed segments is superseded by connected anchored synthesis, but Blender bone-axis and rest-space conversion still requires explicit validation. Parent-relative rotations may be absent when an anatomical parent is outside the visible anchored component; world-transform import must support that case.

Keep tracker keypoints, mapped keypoints, rigid landmarks, and Blender objects distinct. Call the resulting representation a **Blender skeleton**. Optional connected solver/fitted-skeleton sources remain out of scope. Recording-wide scale estimation remains in scope. A naming compatibility option does not implicitly select a reconstruction method.

The current upstream policy explicitly does not support older mixed-landmark Parquet files and has no semantic version field. Preserve old NPY support independently. Require the new mapped/landmark/segment channel set and validate definitions for native Parquet input; reject unsupported older Parquet clearly rather than silently interpreting it as new data. Channel presence is a capability gate, not a general proof of numerical correctness.

The recording contract has stale root-only wording below its newer anchor description. The implementation and anchor tests permit a connected observed component that excludes the anatomical root. Blender must follow that implemented behavior; do not require the pelvis or every anatomical ancestor merely to load a valid skull-anchored component.

### Next implementation stage

Work only in the Blender add-on for its first independently reviewable stage:

1. Define a pure-data recording input with explicit source/run/group selection, model definitions, mapped observations, rigid landmarks, segment world transforms, scales, timestamps, and missingness. Keep legacy loading isolated. Settle how the Parquet reader dependency reaches Blender without importing FreeMoCap or detector runtimes.
2. Implement and test native landmark/segment scene playback before adapting the old rig builder. Verify transformed model geometry against saved landmarks, including non-root anchors, missing segments, millimeter-to-meter conversion, and time mapping.
3. Build the Blender skeleton from recorded model structure. Validate bone basis/rest-space conversion rather than assigning Forge quaternions directly to pose-bone channels without conversion.
4. Add the explicit canonical-to-legacy projection and Parquet-to-Blender-reconstruction path. Inventory required old names and derived points; do not duplicate MediaPipe/RTMPose mappings or silently equate distinct anatomical points.
5. Compare native and Blender-reconstructed outputs from the same recording/run, timing, coordinate reference, and mapped input. Report differences instead of promising numerical identity between different algorithms. Preserve legacy-file regression coverage.

No Blender source changes have been made in this chat. Complete the input contract and dependency decision before beginning scene implementation. Source changes remain subject to the workspace's human commit/push handoff.

Fixture prerequisite: metadata inspection of both canonical prepared recordings under `~/freemocap_data/testing/prepared/*/current/recordings/` found no `MAPPED_KEYPOINTS_3D` channel. They predate this contract. The acceptance test refreshes reconstruction on temporary copies, not these originals. Use a newly reconstructed copy for Blender integration; do not mistake a passing rebuild test for evidence that the canonical files were migrated.

Validation in this review: 16 focused core tests passed for trajectory separation, Parquet/export round trips, anchors, hand completeness, and missing observations. Both real-recording acceptance cases also passed (test and sample, 169.99 seconds total), rebuilding reconstruction on copies and verifying geometry, preserved evidence, channel grids, and optional solver input semantics. Seven dependency deprecation warnings were reported by each test invocation. Blender rendering, animation export, and UI behavior have not been tested.

## Objective and owner decisions

Preserve three distinct trajectory products throughout reconstruction, recording, and consumption:

1. **Keypoint trajectories:** tracker-named measurements, including existing raw and filtered stages. Preserve their existing identities and processing provenance.
2. **Mapped keypoint trajectories:** the observations produced by the SkellyTracker mapping rules, keyed by the model landmark identities they observe. These include direct correspondences, means, weighted combinations, and anatomical offsets. They are inputs to reconstruction; they are not rigidified model output and are not additional independent detector measurements.
3. **Landmark trajectories:** model-local landmark geometry transformed into world coordinates by the solved segment pose and the corresponding segment scale. These represent the reconstructed rigid bodies.

The static AnatomicalLandmark definition remains the model's anatomical point and segment ownership. This change separates dynamic observations of that point from reconstructed positions of that point; it does not require duplicating static landmark definitions or redefining tracker keypoints.

The owner explicitly wants all three products retained. The optional connected/fitted skeleton is currently bypassed and is not the reconstruction method to implement here. Existing recording-wide model/segment scale estimation remains necessary and is distinct from that optional solver.

## Confirmed implementation evidence

Paths below are relative to this workspace. Recheck them before editing; these observations describe the inspected checkout, not installed-package or remote state.

- `repos/freemocap/freemocap/core/skeletons/reconstruct_skeleton.py`: `reconstruct_skeleton()` applies `bundle.landmark_mapping` to filtered keypoints, hydrates the skeleton, and resolves roll. It then creates `landmarks = dict(mapped_landmarks)` and replaces entries corresponding to solved segment origins. This is a mixed observation/result collection, not a complete rigidified landmark product.
- The same function calls Forge's `landmark_world_positions()` only inside the center-of-mass branch, when a scale fit exists. Its returned world positions feed biomechanics but do not replace the published landmark collection.
- `repos/skellyforge/skellyforge/core/biomechanics/center_of_mass.py`: `landmark_world_positions()` already applies segment scale, orientation, and origin to model-local landmarks. It omits absent segments and rejects missing scale for hydrated segments. Inspect ownership and coordinate conventions before reusing it; avoid duplicating its math in FreeMoCap.
- `repos/freemocap/freemocap/core/skeletons/skeleton_reconstruction.py`: the result currently has one `landmarks` dictionary and segment rotations, but no separate mapped-observation product or explicit segment-origin dictionary.
- `repos/freemocap/freemocap/core/recording/sample_encoding/reconstruction_samples.py`: `LANDMARKS_3D` uses `frame.landmarks`. `SEGMENT_ORIGINS` also reads that dictionary through the source definition's segment-to-origin-landmark mapping.
- `repos/freemocap/freemocap/core/streaming/producers/keypoints_producer.py` publishes that collection as `LANDMARKS_3D`; `segment_producer.py` likewise derives origins from it. The semantic problem therefore affects both posthoc and realtime consumers.
- `repos/freemocap/freemocap/core/recording/result_processing/skeleton_fitting.py`: `read_fit_inputs()` loads `LANDMARKS_3D` into observation/prior input `points`. Changing the channel meaning without auditing this consumer would change optional solver inputs. Preserve mapped observations for consumers that need observations; inspect each use instead of blindly replacing channel names.
- The optional solver separately publishes predicted `LANDMARKS_3D` under a solver source. Keep its source distinct; do not substitute it for ordinary segment reconstruction.

The confirmed defect relative to the owner's requested semantics is the conflation above. It does not establish a defect in segment solving itself. Existing docs call mapping output landmark observations; update them to distinguish the three dynamic products explicitly rather than claim every historical use of the word landmark was wrong.

Inspected commits:

| Repository | HEAD |
| --- | --- |
| freemocap | `4e88663bebab8bb216241fe300e8574f19a241d4` |
| skellyforge | `cbae21e48824a562cd4ea859a03900d66ce515fe` |
| skellytracker | `51c9934d371cfad231e72744fce4cc3a43befb9f` |
| freemocap_blender_addon | `127482b1a722cd441411f2c3e7411697f6c78024` |

## Read before implementation

- Workspace `AGENTS.md` and applicable repository instructions.
- `repos/freemocap/current-work-plans/01-data-model/ontology.md`
- `repos/freemocap/current-work-plans/00-foundation/glossary.md` and `conventions.md`
- `repos/freemocap/current-work-plans/01-data-model/tracker-mapping.md`
- `repos/freemocap/RECORDING_CONTRACT.md`
- `repos/freemocap/freemocap/core/recording/data_descriptors/recording_model.py` and `recording_descriptor.py`
- `repos/skellyforge/skellyforge/core/skeleton/components/anatomical_landmark.py` and the existing world-position helper.

Follow current code and the owner's clarification together. Dated plans contain stale implementation claims. RecordedModel already stores skeleton/rest-pose/mapping snapshots: replay must use recorded definitions, not today's YAML defaults.

## Implementation plan

Start with FreeMoCap core as the proposed owning repository. It owns composition, result representation, Parquet publication, and streaming. Forge already provides the geometry operation. Determine whether that operation is sufficient before proposing any dependency change.

1. Define separate typed result fields for mapped observations and rigidified landmarks. Prefer explicit per-segment origins from the solved pose rather than recovering segment transforms from a shared landmark dictionary. Inspect shared origin references and partial hydration before selecting the exact representation.
2. Preserve the mapping result without mutating it. Continue using it for hydration, scale evidence, and consumers needing observations. Generate landmark output from resolved segment poses and the same scale field used for model geometry, independently of whether COM is enabled.
3. Specify missingness: absent segment poses cannot produce rigidified landmarks. Missing scale cannot become unit scale or mapped-observation fallback. Preserve available observations even when reconstruction cannot produce a pose; inspect the current early `None` returns, which otherwise discard them. Do not fill absent results with zeros, previous frames, or invented points.
4. Carry the separate products through posthoc and realtime. Add the appropriate channel identity and descriptors for mapped observations. `MAPPED_KEYPOINTS_3D` is a proposed spelling, not an existing or finalized API. Its values must retain model, tracker/mapping provenance, run, sensor group, reference frame, units, and sample grid.
5. Audit publication, checkpoint retention/invalidation, input signatures, saved-stage reprocessing, tall exports, playback, frontend channel declarations, and streaming. A file that preserves only the new rigidified output has not met the requirement to retain all three products.
6. Audit optional fitting inputs without enabling or redesigning fitting. Mapped targets and reconstruction pose seeds have different roles. Changing `LANDMARKS_3D` must not silently feed reconstructed predictions back as observational evidence or incorrectly retain stale fitted results.
7. Make historical recording semantics explicit. Existing files may contain the mixed landmark product with no separate mapped-observation channel. Choose and document a detectable version/capability/provenance boundary before changing writers. Do not relabel historical data as rigidified, silently reprocess on read, or rewrite user recordings. If repair is offered, it must be explicit and use recorded definitions and suitable saved inputs.
8. Update ontology and channel documentation to match the final implemented contract. Document any compatibility limits and regenerate only authorized test artifacts.

Exact field/channel names and the historical compatibility mechanism remain design decisions for the implementing agent to resolve and explain. Do not let those choices obscure the required semantic separation.

## Validation requirements

Use focused tests that would fail under the current conflation, followed by existing relevant regression tests.

- Use a deliberately inconsistent/noisy observation configuration so mapped positions differ from rigidified positions. Perfect rest-pose inputs alone cannot demonstrate the fix.
- Assert tracker inputs and mapped trajectories remain unchanged by reconstruction.
- For every present rigidified landmark, verify the owning segment's transform of its scaled local position matches the published position. Verify within-segment distances remain consistent with the recorded fixed scale for posthoc reconstruction. Realtime evolving scale should be checked against that frame's scale, not assumed constant.
- Assert landmark output is independent of the COM enable flag.
- Test missing keypoints, observations without a solvable pose, absent segments, absent scale, shared origin references, and re-entry after missing frames. Rotations and origins must refer to the same solved pose.
- Verify both MediaPipe and RTMPose mappings produce the canonical model identities while retaining distinct tracker inputs. Do not claim numerically identical reconstructions from different measurements.
- Round-trip all three products through Parquet with multiple runs/sources and missing values. Check timestamps, units, descriptor declarations, selection, and checkpoint invalidation.
- Check corresponding streaming and playback handling. Keep optional solver-source output distinct and test observation-reader semantics without requiring a full optimization run.
- Test historical-file handling explicitly; no silent semantic promotion.
- Extend the existing reference-recording workflow on ignored or external copies for real-data acceptance. Do not rerun detection just to validate saved-data consumption. Report unavailable assets and skipped tests honestly.

Follow artifact rules before running tests: verify output paths with the owning repository's `git check-ignore`, or use external temporary storage. Do not install dependencies or alter environments without authorization.

## Blender context to preserve for the originating chat

There are three required paths, not two:

1. **Legacy files to legacy Blender construction:** retain the current loader and Blender-side rigid-body reconstruction.
2. **Parquet trajectories to Blender construction:** load the mapped observation trajectories, project into the legacy construction inputs where needed, and run Blender-side rigid-body reconstruction. This provides the comparable pre-rigidification input path. Support for feeding already rigidified landmarks into this path, if desired, must be labeled explicitly as a different comparison.
3. **Parquet native reconstruction to Blender playback:** load rigidified landmarks and saved segment translations/orientations/geometry; bypass Blender-side rigid-body reconstruction.

Paths 2 and 3 allow comparison from the same run and underlying observations. Similarity is an acceptance question, not a promise that different reconstruction algorithms produce identical outputs. Compare units, alignment, timing, landmark correspondences, segment origins, orientations, and lengths; report remaining differences.

Use **Blender skeleton** for the Blender representation. Keep tracker keypoints, mapped observations, model landmarks, segment poses, and Blender scene objects distinguishable. Naming compatibility is separate from reconstruction-method selection. The legacy projection must not recreate tracker-specific mappings downstream of Forge.

Do not implement Blender changes in this secondary task. Return the finalized trajectory/channel contract, version boundary, relevant file links, tests, and remaining limitations to the human for resuming that design discussion.

## Repository boundaries and delivery

Follow the current workspace Git authorization policy: the owner permits task-related cleanup and integration commits and pushes, with one-sentence-or-shorter messages and no agent attribution. Do not spawn another chat or agent solely on the basis of this historical handoff. Recheck branches, local diffs, core source declarations, and installed dependency state. Preserve user work.

Work across configured editable checkouts as needed, preserving repository ownership boundaries and standalone usability. Do not introduce sibling imports, unauthorized environment changes, or gCloud mutations. Publication is not a prerequisite for consumer integration.

Report validation and inspect untracked files before delivery. Commit and push task-related changes under the owner's standing authorization; verify the resulting repository state and publication outcome.
