---
name: context-continuity
description: Preserve task decisions at milestones and recover targeted context after compaction, a handoff, or a resumed session; use when continuing substantial work whose reasoning spans context windows.
---

# Context continuity

Compaction can preserve the next action while losing the reasons that make it
correct. Treat recovery as part of continuing the task, not a new task or an
approval gate. Restore the context needed for the next change before editing.

## Preserve at milestones

For substantial ongoing work, maintain one concise checkpoint per task. Update
it after a material decision, user correction, completed checklist item, or a
change to the next action. If warned of impending compaction, refresh it then;
do not rely on advance notice or a hook giving the model another turn.

Use the project's established handoff location. Otherwise use a task-specific
file in an ignored `.test-artifacts/continuity/` directory, after checking the
owning repository's ignore rules, or an external temporary directory. State the
absolute checkpoint path in the conversation so the continuation can find it.
Use a stable task identifier; do not overwrite another chat's checkpoint.
Put durable architectural decisions in maintained project documentation, and
reference those decisions from the checkpoint. Keep secrets out of both.

Preserve the following information, omitting inapplicable fields:

- Objective, success criteria, current user corrections, scope and authorization.
- Exact checkout paths and branch identities; changed files and pre-existing work
  to preserve. A revision alone does not identify uncommitted working code.
- Decisions and rationale: the owning component, relevant ontology terms and
  boundaries, existing interfaces to reuse, and rejected alternatives with reasons.
- Evidence: verified facts separately from hypotheses; tests actually run and
  their results, limitations and the code state tested. Planned tests are not passes.
- Progress: the exact approved checklist, completion state and approval evidence
  when one exists; active processes or partial operations needing reconciliation.
- Next action and a short recovery reading list: file paths plus headings or
  symbols, with the question each source answers. Include the relevant work-plan
  stage, not every work plan. Flag stale or conflicting sources explicitly.

When producing a compaction summary or handoff, preserve this checkpoint's path,
recent decisions and corrections, unresolved questions, and the next recovery
step. Link existing artifacts rather than retelling the entire conversation.

## Recover before the next change

After compaction, handoff, or resume, expect incomplete recall. Read the checkpoint
and relevant sections of applicable `AGENTS.md` files. Follow its targeted reading
list into maintained ontology, ownership, strategy and interface documentation.
Verify that paths refer to the intended checkout rather than an older worktree.
Before resuming an edit, read the actual changed lines for the affected files and
interfaces, alongside their current implementation. Status, filenames and diff
statistics locate changes; they do not establish what changed. Inspect relevant
unstaged and staged patches separately, and read relevant untracked files directly.
Outside Git, compare against the task's saved baseline when available; otherwise
record that change provenance is unknown. Distinguish pre-existing user work from
the task's partial implementation and preserve both. Resolve truncated patch output
with narrower reads. Limit review to the next edit and its dependencies; do not
audit unrelated changes. Reconcile active processes before repeating operations.

Recovery is sufficient when you can identify the next action's purpose, owning
component, applicable definitions and constraints, existing implementation to
extend, and evidence that will establish completion. Briefly report the recovered
direction if useful, then continue the already authorized work automatically.
Reopen only decisions affected by new evidence or explicit user changes.

When a summary lacks a definition or interface, search the owning repository
before creating one. Absence from the summary is not evidence of absence from the
project. Narrow inspection to the next action and expand only to resolve a
specific gap; routine recovery does not require auditing every repository,
rereading every plan, or rerunning previously valid tests.

## Resolve gaps proportionately

Use current explicit user decisions and applicable policy to determine intended
behavior; use code, configuration and tests to establish implemented behavior.
A dated plan is evidence of a proposal, not proof it was approved or implemented.
Neither code nor prose alone resolves a disagreement about intended design.

Correct a stale breadcrumb or factual note within the authorized scope when its
replacement is supported by evidence. Record the correction and its reason in
the checkpoint. If consequential intent remains ambiguous after targeted
inspection, present the conflicting sources, affected decision and smallest
question the user must resolve. Pause only dependent work and continue independent
authorized work. Ordinary missing context, a corrected link, or compaction itself
does not require a user check-in. Preserve uncertainties rather than filling them
with a plausible new architecture.
