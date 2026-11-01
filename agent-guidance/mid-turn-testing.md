# Mid-turn compaction investigation

Updated 2026-11-01. Cross-project rollout remains deferred until this question is
resolved. Keep production work and test sessions separate; observe live work
without sending reminders that would contaminate the recovery measurement.

## Ways to obtain an event

The documented `model_auto_compact_token_limit` lowers the automatic compaction
threshold. `model_auto_compact_token_limit_scope` selects total context or growth
after the carried prefix (`body_after_prefix`). A disposable runtime can therefore
exercise automatic compaction without filling the normal context window.
These settings are documented; their effective behavior in our installed runtime
still needs an execution test. [@openaiCodexConfigReference]

`thread/compact/start` is programmatically callable, but explicitly requests
manual compaction. Automating that request does not turn it into a test of the
automatic threshold path. It exposes contextCompaction lifecycle notifications.
The desktop chat-management connector available here has no compact operation.
[@openaiCodexAppServer]

For a controlled automatic test, use a separate app-server process and disposable
fixture, with a process/session-scoped threshold override, ordinary sandboxing and
the user's existing model selection. Do not alter global settings or attach a
second writer to a live desktop chat. The locally generated 0.160.0
ThreadStartParams schema accepts a config object; schema acceptance alone does
not prove that the chosen overrides take effect. Verify effective configuration
before inference. Do not copy credentials into experiment artifacts.

Select a threshold above the initial prompt/instruction load but low enough for
normal implementation tool output to cross it. Avoid thresholds that repeatedly
compact an irreducible prefix. Bound the experiment by elapsed time and compaction
count, and stop after one useful event or repeated non-progress. No fabricated
padding corpus is necessary. Record task start, pre-event edits/tests, compaction,
immediate continuation and task completion. A start-of-turn event alone is not a
mid-turn pass.

## Passive real-work observation

Prefer an existing relevant chat with a genuine event when available. Read only
the selected chat's transcript and task sources; do not modify its code or send
recovery instructions. Capture the last checkpoint/decision before compaction,
the unfinished operation, and the first reads and edits afterward. Separate
evidence of an in-turn boundary from proof of an automatic trigger: the latter
requires trigger telemetry or sufficiently explicit runtime evidence.

On 2026-11-01, the active FreeMoCap chat **hands and stuff**
(`01a13ad4-d911-79c0-98ea-39293ace0d85`) supplied a real event. Turn
`01a19791-959b-7a91-8240-d75e94b2258a` began at 14:44:23 UTC; a compacted record
appeared at 14:58:25.927 UTC, followed by tool calls in the same still-open turn,
without an intervening user continuation. No manual compact request appears in
the inspected interval; this is consistent with automatic mid-turn compaction,
but the compacted record inspected did not explicitly label its trigger.

The agent had maintained a task checkpoint before the event. Its first subsequent
tool read test output and selected source/document sections. Its next tool edited
tests before inspecting a diff in that same command. It did not reread the
checkpoint, owning instructions or actual relevant patch between compaction and
that edit. Thus the pre-edit recovery procedure was not fully followed. This is
not evidence that those edits were wrong or that compaction caused test failures;
no independent review of the full production task was performed. The task was
still active at observation, so there is no final outcome verdict.

### Timing and exposure correction

The event occurred after the revised skill was installed on disk, but that does
not establish that the running agent received the revision. The chat read the
older skill at 13:53:30 UTC (returned at 13:53:31). The actual-patch revision was
written at 14:47:00 and installed through a copy command issued at 14:47:12,
during the turn that had started at 14:44:23. No read or injected copy of the
revised paragraph was found before the 14:58:25 compaction. Therefore this is
evidence about the older guidance and an update-exposure ambiguity, not a fair
failure verdict for the revised skill. The initial assessment overstated that
conclusion. File modification time alone is insufficient; copying also preserved
the source file's timestamp, so transcript installation evidence is preferable.

The other active chat, **Investigate real-time skeleton blinking**
(`01a197a3-2e4b-7360-b01d-74ea21421591`), returned the revised skill text at
15:03:46.890 UTC after requesting it at 15:03:45.801. A subsequent natural
compaction there is an eligible observation of the revision. None had appeared
at the timing audit. Waiting for another event in the older chat alone would
not resolve exposure unless its receipt of the revision is also established.
Detailed local notes are in ignored
`.test-artifacts/compaction-audit/live-midturn-review.md`.

## Next controlled comparison and acceptance criteria

Preserve the instruction-only baseline. A subsequent isolated comparison can
add a `SessionStart` hook matching `compact` that supplies a concise recovery
reminder and points to the checkpoint convention. The documented delivery point
includes the immediate continuation of automatic root-session compaction.
Avoid stopping the turn with `continue: false`. PreCompact/PostCompact can log
manual/auto trigger and turn identity, but their stdout is not the context
injection mechanism. [@openaiCodexHooks]

Record hook firing separately from model-visible delivery and behavioral recovery.
No hook has been installed or tested by this investigation. A hook is a prompt
reminder, not proof of compliance or an editing interlock.

Success requires: an observed boundary after work began; checkpoint and applicable
sources recovered before the next edit; actual relevant patch review; preserved
intent, corrections, ownership and pre-existing work; reconciliation of active
operations; independent correctness checks; and continued work without unnecessary
approval. A single failure should produce a narrow diagnosis, not a full-audit rule.

Do not roll the new hook or additional project-specific instructions out on the
basis of documentation or schema checks alone. First verify event delivery and
recovery behavior, then decide whether the global protocol needs adjustment.
