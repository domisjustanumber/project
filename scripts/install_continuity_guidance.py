"""Install reviewed continuity guidance, preserving unrelated personal settings.

Only writes AGENTS.md and the named personal skills; never changes config or Git.
Use --codex-home with a temporary directory to inspect an isolated installation.
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- freemocap-context-continuity:start -->'
END = '<!-- freemocap-context-continuity:end -->'


def merge(existing: str, content: str) -> str:
    """Replace only our managed block; reject damaged or duplicate delimiters."""
    if existing.count(START) != existing.count(END) or existing.count(START) > 1:
        raise ValueError('Ambiguous continuity block; preserve file for manual review')
    block = START + '\n' + content.rstrip() + '\n' + END
    if START in existing:
        start, end = existing.index(START), existing.index(END)
        if end < start:
            raise ValueError('Reversed continuity delimiters')
        return existing[:start] + block + existing[end + len(END):]
    return existing + ('\n\n' if existing else '') + block + '\n'


def install(home: Path) -> list[Path]:
    guidance = ROOT / 'agent-guidance'
    edits = {}
    for path, source in [(home / 'AGENTS.md', guidance / 'global-continuity.md'),
                         (home / 'skills/linear-checklist-task/SKILL.md',
                          guidance / 'checklist-continuity.md')]:
        if path.name == 'SKILL.md' and not path.exists():
            continue
        old = path.read_text(encoding='utf-8') if path.exists() else ''
        edits[path] = merge(old, source.read_text(encoding='utf-8'))
    source = guidance / 'context-continuity/SKILL.md'
    target = home / 'skills/context-continuity/SKILL.md'
    content = source.read_text(encoding='utf-8')
    if target.exists() and target.read_text(encoding='utf-8') != content:
        raise ValueError(f'Existing skill differs; review before replacing: {target}')
    edits[target] = content
    changed = []
    for path, text in edits.items():
        if not path.exists() or path.read_text(encoding='utf-8') != text:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
            changed.append(path)
    return changed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex-home', type=Path, required=True)
    args = parser.parse_args()
    for changed in install(args.codex_home.resolve()):
        print(changed)
