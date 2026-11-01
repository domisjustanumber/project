# Context continuity audit

Audited 2026-11-01. Scope: personal Codex guidance and the eight canonical
repositories in `repos.toml`. Other projects and alternate worktrees are excluded.

## Runtime evidence and deployment choice

The installed CLI and app-server package report `0.160.0`; `features list`
reports `hooks` stable/enabled. The user config had no compaction override and
there was no personal `AGENTS.md` or `hooks.json` before this change.

An isolated app-server process with a separate Codex home successfully completed
`initialize` and `config/read` under `--strict-config` and returned the supplied
`compact_prompt` marker. The process was terminated after the read. No model turn
or actual compaction was run. This verifies parsing/readback, not compaction
behavior, prompt effectiveness, or applicability to this desktop chat's runtime.
Evidence is in ignored `.test-artifacts/compaction-audit/runtime-result.json`.

The official sample documents `compact_prompt`,
`experimental_compact_prompt_file`, and an automatic-compaction token threshold.
These options remain unset globally: accepting a setting does not establish
that it controls the active compaction path. [@openaiCodexConfig]

`PreCompact` and `PostCompact` support manual/auto triggers and common JSON
output; plain stdout is ignored, and `continue: false` stops processing.
Their documented output does not establish additional-context injection. This
limitation does not apply to all hooks: `SessionStart` with matcher `compact`
can add developer context through stdout or `hookSpecificOutput.additionalContext`.
It runs before the next model request, including the immediate continuation of
automatic root-session compaction during a turn. `continue: false` would stop
that continuation. [@openaiCodexHooks]

The original audit omitted this SessionStart path. No hook is installed because
its delivery has not been verified in the installed runtime, not because the
documented capability is absent. Current guidance remains the tested baseline;
a hook-assisted comparison is a possible follow-up rather than a prerequisite
or a reason to replace the checkpoint protocol.

The API also supports opaque compaction state. This audit does not equate an
API capability with a verified desktop implementation. [@openaiCompaction]

The deployed baseline is personal `AGENTS.md` guidance plus a continuity skill
and a continuation section in the personal checklist skill. `AGENTS.md` is a
documented instruction mechanism; in this session the desktop visibly reloaded
the new global instructions after installation. That confirms loading, not
perfect model compliance after compaction. [@openaiAgentsMd]

## Maintained sources and installation

- [Protocol](context-continuity/SKILL.md): source for the installed personal skill.
- [Global guidance](global-continuity.md): managed section of personal AGENTS.md.
- [Checklist continuation](checklist-continuity.md): managed personal and workspace
  checklist-skill section. Existing checklist approval and ordering rules remain.
- [Installer](../scripts/install_continuity_guidance.py): preserves unrelated
  content, rejects ambiguous blocks or conflicting existing skills, and supports
  an isolated `--codex-home`. It never edits Codex configuration or Git state.

Install explicitly with `python -B scripts/install_continuity_guidance.py
--codex-home <personal-codex-directory>`. Review source and destination together
when updating the protocol; a differing installed skill requires reconciliation.
Packaged plugin files are not edited, so plugin upgrades cannot erase this policy.

## Repository findings

All four branch-pinned dependencies match Core's `sfn26` source declarations;
Core is also on `sfn26`. The utilities are on `main`, with no named branch policy
for logs or pings. Core uses editable local dependencies. Alternate `cleanup-*`,
Forge worktrees and theme checkouts are not substitutes for manifest checkouts.

Existing user changes were present in workspace AGENTS.md, Core and Tracker.
The audit recorded their paths and hashes before editing existing files.

| Repository | Gap addressed by recovery guidance |
| --- | --- |
| Workspace | Moved ontology links, obsolete Forge entry paths, copied geometry conventions, and no targeted recovery index |
| Core | Ownership guidance lacked conditional links to ontology, recording, transport and active work plans |
| Cam | No AGENTS entry point; camera-group tasks and dual-backend guidance needed discoverable pointers |
| Tracker | Composition guidance needed checkpoint and recovery routing; legacy CLAUDE overview needed current entry-point precedence |
| Forge | No AGENTS entry point; CLAUDE had broken workspace/ontology paths and obsolete pytest installation advice |
| Blender addon | No AGENTS entry point for data ingestion, world/rest-space conversions and packaging/testing boundaries |
| Logs | No AGENTS entry point for independent logging lifecycle and the relay handoff |
| Pings | No AGENTS entry point distinguishing lightweight client, server and cloud mutation policy |
| Docs | No AGENTS entry point for browser theme versus Node CLI and site content ownership |

Historical status statements are not fresh test evidence. The Core ontology's
obsolete posthoc-deferred paragraph is replaced by a maintained status pointer.
The current ontology, conventions, source definitions and task-specific plans
must be read together where intent and implementation differ. This is a routing
and continuity change, not an architectural migration or a claim that all old
plans have been reconciled.

## Verification boundary

Validation covers installation preservation/idempotence, skill format, local
breadcrumb existence, bibliography consistency and representative recovery
scenarios. It cannot prove that every model will obey the instructions, that
automatic compaction preserves every rationale, or that remote compaction uses
the custom prompt setting. Two manual UI trials now demonstrate bounded recovery
for analysis and disposable implementation work; see [validation](VALIDATION.md).
Passing configuration readback alone is not behavioral evidence. The subsequent
[mid-turn investigation](mid-turn-testing.md) separates controlled triggering,
passive observation, and verified hook delivery.
