#!/usr/bin/env python3
"""Regenerate pillar guides from the canonical catalog, or check for drift."""
import argparse
import sys
from rules import ROOT, catalog, validate

def render(data):
    modules = {}
    for r in data['rules']:
        p = r['pillar']
        if p not in modules:
            modules[p] = f'# {p.title()} rules\n\nRules retain the original numbering. Apply only after checking the condition. Decisions are not mandatory features; controls are required when applicable.\n\n'
        modules[p] += f"## {r['id']} — {r['title']}\n\n**Type:** {r['kind']}. **Applies when:** {r['applies_when']}.\n\n{r['guidance']}\n\n**Verify:** {r['verification']}\n\n"
    for pillar in modules:
        # Plain ID index avoids renderer-specific heading-anchor differences.
        index = '## Contents\n\n' + '\n'.join(f"- {r['id']}: {r['title']}" for r in data['rules'] if r['pillar'] == pillar) + '\n\n'
        marker = modules[pillar].index('## R')
        modules[pillar] = modules[pillar][:marker] + index + modules[pillar][marker:]
    return modules

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = catalog()
    errors = validate(data)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    drift = []
    for pillar, content in render(data).items():
        path = ROOT / 'references' / f'{pillar}.md'
        if args.check:
            if path.read_text(encoding='utf-8') != content:
                drift.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(content, encoding='utf-8')
    if drift:
        print('Regenerate reference files: ' + ', '.join(drift), file=sys.stderr)
        return 1
    print('Pillar references match catalog.' if args.check else 'Pillar references regenerated.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
