# KAX0 — The decisions of the kit are in agents-and-adr-process/decisions/

**Status:** accepted, 2026-11-23 (user, "for now, a decisions folder under agents-and-adr-process. That may change.").

## Decision

1. The decisions about the kit itself are entries of the log in `agents-and-adr-process/decisions/`.
2. The log uses the rules, the skill and the template of the kit in `bootstrap/`.
3. `bootstrap/decisions/` stays the template log that a new repo copies. It holds only entry 0001.
4. The place can change. A move needs a new entry that supersedes this one.

## Reason

- The kit design decisions of 2026-11-23 were in no log. The kit log in `bootstrap/` is copied into
  each new repo, so a kit decision there would go into each repo.
- The user chose this place for now.

## Consequences

- A test of this repo runs the kit `check_decision_log.py` on this log.
