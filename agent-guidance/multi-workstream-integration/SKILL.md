---
name: multi-workstream-integration
description: Coordinate multiple owner agents or chats executing human-approved linear checklists, consolidate their plans and evidence, relay user decisions, and manage dependencies and integration. Use for portfolio-level agent coordination; use linear-checklist-task for each individual execution plan.
---

# Multi-workstream integration

The coordinator maintains an interrogable overview of parallel workstreams. Each
owner uses the standard linear-checklist-task skill for its bounded execution plan.
Read that skill when commissioning owners; preserve its approval, sequential
execution, exact wording/numbering and full-checklist milestone reporting rules.
The coordinator uses the overview reporting rules below instead of repeatedly
printing all nested checklists after each owner's milestone.

## Records and ownership

Maintain a concise board with stable workstream IDs, owner, direct conversation
link, checklist revision, approval state, current step, dependencies and next action.
Link authoritative owner checklists, exact checkouts, checkpoints and evidence.
Distinguish proposed, approved, running, blocked, verified, integrated and published.
Keep an approval record identifying the human instruction and affected revision.

Every owner report to the human must include a clickable link directly to that
owner's conversation. Use the real title and identifier from the environment.
For a confirmed local Codex chat, use `[Chat title](codex://threads/THREAD_ID)`.
Never substitute a report file for a conversation link or invent an agent URL.
If an internal sub-agent has no exposed conversation link, retain its contribution
but designate a suitable accessible owner chat when authorized; otherwise disclose
the limitation and resolve access before promising direct navigation. Creating a
new user-visible chat still requires the environment's authorization.

## Plan and dispatch

1. Recover each stream's purpose, existing implementation, ontology, ownership,
   accepted tradeoffs, baseline and prior approvals before commissioning work.
   Consult existing owners where available; distinguish old proposals from approved
   or completed plans. Scope each assignment and permitted actions explicitly.
2. Ask owners for concise numbered linear checklists, acceptance evidence,
   dependencies and consequential decisions. Keep workspace/environment preparation
   to one outcome-oriented step; keep mechanics internal. Center the actual product
   outcomes. For a bounded phase, state its limit and preserve the larger roadmap.
3. Consolidate owners' exact checklist proposals into one compact approval report,
   including their chat links. Identify conflicting interfaces, dependencies,
   prerequisites and shared-resource scheduling. Mark missing owner responses pending.
4. Relay human approval for the specified revisions without asking the human to
   repeat it in each owner's chat. Distinguish approval of the coordination method
   from approval to execute workstream plans. Do not create a redundant approval
   gate when the human has already authorized the work. Freeze approved wording,
   numbering and order; substantial amendments follow the linear skill's procedure.
   For partial approval, record the exact approved steps and stop before the first
   unapproved step. Revised numbering must not expand the human's approved scope.
5. Dispatch approved ready work and record the baseline and shared-interface owner.
   Independent streams may run concurrently; each owner follows its linear order.
   Serialize measurements or other work that requires exclusive shared resources.
   Coordinate dependencies without forcing unrelated work to wait.

## Relay the human's actual words

When the human gives instructions to an owner, include those instructions verbatim
in the owner message. Label them **User instruction — verbatim**. Preserve words,
punctuation, repetitions and tone; do not silently clean up transcription or replace
the original with a paraphrase. Copy a complete relevant contiguous passage or the
whole message when separating it would lose context. Retain the source message or
exact excerpt in the checkpoint.

Follow the quotation with a separately labeled **Coordinator interpretation and
assignment** containing actionable scope, dependencies, acceptance evidence and any
clarification. Keep the user's text distinguishable from the coordinator's inference.
Resolve consequential ambiguity before dependent action, while continuing safe
independent work. A relayed quotation does not expand authorization or override
applicable higher-priority constraints.

## Monitor, amend and integrate

Owners report the full approved checklist at completed steps in their own chats,
with actual evidence and next action. Collect those milestones and update the board.
Routine human-facing updates show meaningful changes, blockers and decisions with
direct owner links; reproduce the full packet on request or for plan approval.
Use stable references such as W4 v2 step 3 so the human can interrogate any stream.
Do not require acknowledgment of routine progress before continuing authorized work.

Recover ordinary test/tool failures within the approved plan without requesting a
new approval. For a discovery that materially invalidates that plan, pause affected
work, obtain the smallest necessary checklist amendment, relay human judgment and
resume. Preserve completed work and
keep unrelated streams moving. Do not silently rewrite an owner's plan or mark an
unverified step complete to simplify the overview.

Verify both component results and combined behavior against a recorded integration
baseline. Reconcile shared interfaces and stale evidence when that baseline changes.
Publishing and cleanup are separate states: retire worktrees only after preservation,
integration and applicable authorization checks. Preserve existing user work.

At milestones, checkpoint exact plans, approvals, decisions/rationale, chat links,
checkout identities, evidence, active operations and next recovery reads. Use the
context-continuity skill when available. On resume, recover those records and inspect
relevant current sources before dispatching again; do not restart owners or reopen
settled decisions merely because context was compacted. Use bounded waits and report
observed state; promise persistent monitoring only when actually configured.
