#!/usr/bin/env python3
"""Offline catalog/checklist utility. Never scans, modifies, or certifies an app."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = {
    'all': None,
    'web': {'security', 'performance', 'ux', 'search', 'operations', 'engineering'},
    'saas': {'security', 'performance', 'ux', 'operations', 'analytics', 'communications', 'localization', 'engineering'},
    'ecommerce': None,
    'api': {'security', 'performance', 'operations', 'engineering'},
    'mobile': {'security', 'performance', 'ux', 'operations', 'communications', 'localization', 'engineering'},
}
STATUSES = {'todo', 'pass', 'fail', 'not-applicable', 'deferred'}

def catalog():
    return json.loads((ROOT / 'data/rules.json').read_text(encoding='utf-8'))

def validate(data):
    errors = []
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        return ['catalog schema_version must equal 1']
    rules = data.get('rules')
    if not isinstance(rules, list) or len(rules) != 100:
        return ['catalog must contain 100 rules']
    for index, rule in enumerate(rules, 1):
        if not isinstance(rule, dict):
            errors.append(f'row {index} must be an object')
            continue
        if rule.get('id') != f'R{index:03}' or rule.get('original_number') != index:
            errors.append(f'row {index} has an invalid or out-of-order ID')
        for key in ('pillar', 'title', 'applies_when', 'guidance', 'verification'):
            if not isinstance(rule.get(key), str) or not rule[key].strip():
                errors.append(f'row {index} missing {key}')
        if rule.get('kind') not in {'control', 'decision'}:
            errors.append(f'row {index} invalid kind')
        pillar = rule.get('pillar')
        if isinstance(pillar, str) and not (ROOT / 'references' / f'{pillar}.md').is_file():
            errors.append(f'row {index} missing reference')
    return errors

def select(rules, profile='all', pillar=None, query=None):
    allowed = PROFILES[profile]
    return [r for r in rules if (allowed is None or r['pillar'] in allowed)
            and (not pillar or r['pillar'] == pillar)
            and (not query or query.casefold() in json.dumps(r).casefold())]

def make_assessment(rules, profile):
    return {'schema_version': 1, 'catalog_version': catalog()['version'], 'profile': profile,
            'scope': 'Describe repository, revision, deployment, features and exclusions.',
            'rules': [{'id': r['id'], 'status': 'todo', 'evidence': '', 'reason': '',
                       'owner': '', 'review_by': ''} for r in rules]}

def review(assessment, rules, gate=False):
    """Validate human assertions; a pass is not independent evidence verification."""
    if not isinstance(assessment, dict):
        return ['assessment must be an object']
    errors = []
    if assessment.get('schema_version') != 1:
        errors.append('unsupported assessment schema')
    if assessment.get('catalog_version') != catalog()['version']:
        errors.append('catalog version mismatch; regenerate or migrate assessment')
    profile = assessment.get('profile')
    if not isinstance(profile, str) or profile not in PROFILES:
        return errors + ['unknown profile']
    entries = assessment.get('rules')
    if not isinstance(entries, list):
        return errors + ['rules must be an array']
    expected = {r['id'] for r in select(rules, profile)}
    known = {r['id'] for r in rules}
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append('rule entry must be an object')
            continue
        rid = entry.get('id')
        if not isinstance(rid, str) or rid not in known:
            errors.append('unknown rule ID')
            continue
        if rid in seen:
            errors.append(f'{rid}: duplicate entry')
        seen.add(rid)
        status = entry.get('status')
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(f'{rid}: invalid status')
            continue
        def present(key):
            return isinstance(entry.get(key), str) and bool(entry[key].strip())
        if status == 'pass' and not present('evidence'):
            errors.append(f'{rid}: pass requires evidence')
        if status in {'not-applicable', 'deferred'} and not present('reason'):
            errors.append(f'{rid}: {status} requires reason')
        if status == 'deferred' and not all(present(k) for k in ('owner', 'review_by')):
            errors.append(f'{rid}: deferred requires owner and review_by')
        if gate and status in {'todo', 'fail', 'deferred'}:
            errors.append(f'{rid}: unresolved ({status})')
    for rid in sorted(expected - seen):
        errors.append(f'{rid}: missing profile rule')
    if gate and (not isinstance(assessment.get('scope'), str)
                 or not assessment['scope'].strip()
                 or assessment['scope'].startswith('Describe repository')):
        errors.append('replace the scope placeholder with actual review scope')
    return errors

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('validate', help='validate the bundled 100-rule catalog')
    for name in ('list', 'checklist', 'init'):
        p = sub.add_parser(name)
        p.add_argument('--profile', choices=PROFILES, default='all')
        if name != 'init':
            p.add_argument('--pillar')
            p.add_argument('--query')
    p = sub.add_parser('review', help='validate assessment structure and declared evidence')
    p.add_argument('file', type=Path)
    p.add_argument('--gate', action='store_true', help='also reject unresolved selected rules')
    args = parser.parse_args(argv)
    try:
        data = catalog()
        errors = validate(data)
        if errors:
            raise ValueError('; '.join(errors))
        rules = data['rules']
        if args.command == 'validate':
            print('Catalog valid: 100 rules. This does not inspect any application.')
        elif args.command == 'review':
            errors = review(json.loads(args.file.read_text(encoding='utf-8')), rules, args.gate)
            if errors:
                print('\n'.join(errors), file=sys.stderr)
                return 1
            print('Assessment structure valid. Declared evidence has not been independently verified.')
        else:
            chosen = select(rules, args.profile, getattr(args, 'pillar', None), getattr(args, 'query', None))
            if not chosen:
                raise ValueError('no matching rules; check filter spelling')
            if args.command == 'init':
                print(json.dumps(make_assessment(chosen, args.profile), indent=2))
            elif args.command == 'list':
                for r in chosen:
                    print(f"{r['id']} [{r['pillar']}] {r['title']}")
            else:
                print('# Project review checklist\n\nCandidate rules only; assess applicability. This is not an app scan.\n')
                for r in chosen:
                    print(f"- [ ] **{r['id']} {r['title']}** ({r['kind']})\n  - Applies: {r['applies_when']}\n  - Implement: {r['guidance']}\n  - Verify: {r['verification']}\n")
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
