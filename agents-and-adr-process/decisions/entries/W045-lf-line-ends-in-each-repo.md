# W045 — LF line ends in each repo, set by .gitattributes and checked by check_line_ends.py

**Status:** accepted, 2026-11-23 (user; the rule given in the skellycam session, the form confirmed here).

## Decision

1. **The rule.** Each text file of each repo uses LF line ends, on each system.
2. **git sets it.** The kit block `line-ends` of `.gitattributes` holds `* text=auto eol=lf`. git
   then writes LF into the index and into each working tree, also when `core.autocrlf` is set. A
   line of a repo, for example `golden/** -text`, comes after the block.
3. **A check enforces it.** `tools/check_line_ends.py` fails a commit and CI when the index holds a
   CRLF or a mixed text file. It skips binary files and `-text` paths. A pre-commit hook and the doc
   test run it.
4. **The sync writes LF.** `kit_sync.py` writes LF into each file that it writes.
5. **The change.** A repo runs `git add --renormalize .` one time, in a commit by itself. Each old
   working tree runs `tools/check_line_ends.py --refresh`. It refuses when a tracked file has a
   change, so it cannot delete work. Agents do not use `git reset --hard` for this.
6. **This repo.** The root `.gitattributes` of freemocap/project has the same rule.

## Reason

- The user, in words: "we must use linux line endings everywhere for all repos" and "this must be
  enforced by git rules".
- On a Windows system with `core.autocrlf=true`, the working tree had CRLF while the index had LF.
  A tool that kept the line ends of a file then wrote CRLF.

## Evidence

- skellycam: the index held 961 LF files and 0 CRLF files, and `git add --renormalize .` changed
  nothing (reported by the skellycam session, 2026-11-23).
- This repo: 80 LF files and 0 CRLF files in the index, 2026-11-23.
- `git checkout-index --force --all` did not write the CRLF working files again on this system.
  `--refresh` deletes and checks out each such file. Its test covers a `-text` golden file and a
  refusal on a local change.

## Alternatives rejected

- **Keep the line ends that a file has.** It keeps a CRLF working file CRLF, against the rule.
- **`core.autocrlf=false` on each machine.** It is not in git, so a new clone or system does not get it.

## Not repeated

- `git status` marks a file that differs only by CRLF as modified. The refresh guard uses
  `git diff HEAD`, which compares the text after the rule.
- `git diff HEAD` does not show a change of a file marked `--assume-unchanged` or
  `--skip-worktree`. With only that guard, `--refresh` lost an edit behind `--assume-unchanged`, and
  deleted a `--skip-worktree` file that `git checkout` then did not write (found by the skellycam
  review, 2026-11-23). `--refresh` now refuses such a file, and it compares the content of each file
  with the index blob (`git hash-object`) before it deletes the first one.
