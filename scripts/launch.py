#!/usr/bin/env python3
"""Generate private project plans and review declared launch evidence. No network calls."""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys
import rules

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = ('web', 'api', 'android', 'ios')
FEATURES = ('accounts', 'payments', 'mailing-list', 'e2ee')
# Each entry is (guide, checkpoints). IDs remain stable across wording changes.
MODULES = {
    'core': ('idea-to-launch.md', {
        'CORE-01': 'Define audience, first useful journey, scope, exclusions and budget.',
        'CORE-02': 'Demonstrate a working journey through real boundaries; label all simulations.',
        'CORE-03': 'Verify ownership/authorization, input limits and safe errors for applicable boundaries.',
        'CORE-04': 'Verify accessible loading, empty, failure and recovery states.',
    }),
    'delivery': ('host-handoff.md', {
        'SHIP-01': 'Build from clean source using documented configuration and commands.',
        'SHIP-02': 'Verify deployed preview/release build, TLS and actual service integrations.',
        'SHIP-03': 'Verify backup restoration, migrations and rollback where state is persistent.',
        'SHIP-04': 'Deliver source/export, runbook, owner, costs, monitoring and maintenance plan.',
    }),
    'platform': ('platform-security.md', {
        'PLAT-01': 'Review selected web/API platform boundaries, or native release configuration, permissions, storage and links.',
        'PLAT-02': 'Test supported browsers/devices, assistive technology, interruption and offline recovery.',
    }),
    'accounts': ('accounts.md', {
        'AUTH-01': 'Verify signup, verification, login and session lifecycle.',
        'AUTH-02': 'Reject expired/replayed recovery proofs; verify recovery and sensitive account changes.',
        'AUTH-03': 'Test cross-user/tenant access and supported MFA/native authentication flows.',
    }),
    'payments': ('commerce.md', {
        'PAY-01': 'Verify hosted/store payment choice, server totals and order ownership.',
        'PAY-02': 'Test authentic, duplicate, reordered and interrupted payment events before fulfillment.',
        'PAY-03': 'Test declines, challenges, refunds and applicable inventory/subscription transitions.',
    }),
    'mailing-list': ('mailing-lists.md', {
        'MAIL-01': 'Verify sender setup, permission records and subscription/confirmation abuse controls.',
        'MAIL-02': 'Verify unsubscribe, complaints and suppression across queued sends and reimports.',
        'MAIL-03': 'Test audience preview, idempotent sends, provider events and import/export access.',
    }),
    'e2ee': ('private-content.md', {
        'CRYPT-01': 'Document threat model, protocol choice, metadata exposure and independent integration review.',
        'CRYPT-02': 'Test device identity, key lifecycle, recovery, revocation and backup limitations.',
        'CRYPT-03': 'Test tampering/replay and absence of plaintext/key leakage at server boundaries.',
    }),
}


def selected_modules(features):
    return ['core', 'delivery', 'platform'] + list(features)


def checkpoints(features, platforms):
    selected = {key: text for module in selected_modules(features)
                for key, text in MODULES[module][1].items()}
    platform_checks = {
        'web': ('WEB-01', 'Verify browser sessions, CSRF, mixed content, cache isolation and supported browser flows.'),
        'api': ('API-01', 'Verify service authentication, object/field authorization, request limits and API compatibility.'),
        'android': ('ANDROID-01', 'Verify Android release manifest, network config, Keystore use, intents and lifecycle on supported devices.'),
        'ios': ('IOS-01', 'Verify iOS release ATS, Keychain use, entitlements, links and lifecycle on supported devices.'),
    }
    selected.update(platform_checks[p] for p in platforms)
    return selected


def validate_selection(platforms, features):
    for values, allowed, label in ((platforms, PLATFORMS, 'platforms'), (features, FEATURES, 'features')):
        if not isinstance(values, list) or any(not isinstance(v, str) or v not in allowed for v in values):
            raise ValueError(f'invalid {label}')
        if len(values) != len(set(values)):
            raise ValueError(f'duplicate {label}')
    if not platforms:
        raise ValueError('select at least one platform')


def initialize(output, name, platforms, features):
    validate_selection(platforms, features)
    if not name.strip() or any(ord(c) < 32 for c in name):
        raise ValueError('name must be a nonblank single line')
    entries = checkpoints(features, platforms)
    report = {'schema_version': 1, 'project': name, 'platforms': platforms, 'features': features,
              'scope': 'TODO: repository, revision, environment and exclusions',
              'checks': [{'id': key, 'status': 'todo', 'evidence': '', 'reason': '',
                         'owner': '', 'review_by': ''} for key in entries]}
    catalog = rules.catalog()
    errors = rules.validate(catalog)
    if errors:
        raise ValueError('; '.join(errors))
    # Load all resources before creating the destination. Never overwrite existing work.
    guides = {MODULES[m][0]: (ROOT/'references'/MODULES[m][0]).read_text(encoding='utf-8')
              for m in selected_modules(features)}
    plan = '# Build plan\n\nPlatforms: ' + ', '.join(platforms) + '\nFeatures: ' + (', '.join(features) or 'none')
    plan += '\n\nStart with brief.md, then follow the selected guides. These files plan the work; they are not a runnable app.\n\n'
    plan += '\n'.join(f'- [ ] **{key}** {text}' for key, text in entries.items())
    plan += '\n\n## Guides\n\n' + '\n'.join(f'- [{n}](guides/{n})' for n in guides)
    plan += '\n\nReview launch.json with scripts/launch.py review; --gate also checks the sibling assessment.json. Neither gate verifies evidence truth. Keep filled reviews private.\n'
    output.mkdir(parents=True, exist_ok=False)
    (output/'guides').mkdir()
    for filename, content in guides.items():
        (output/'guides'/filename).write_text(content, encoding='utf-8')
    (output/'brief.md').write_text('# Project brief\n\nProject: ' + name + '\n\n'
        'Describe the audience, problem, first useful journey, platforms, sensitive data, budget, owner and exclusions.\n\n'
        '## Acceptance criteria\n\nDescribe observable success and failure behavior before implementation.\n\n'
        '## Decisions and next steps\n\nRecord choices, reasons, unresolved dependencies and the next small working slice.\n', encoding='utf-8')
    (output/'plan.md').write_text(plan, encoding='utf-8')
    (output/'launch.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    (output/'assessment.json').write_text(json.dumps(rules.make_assessment(catalog['rules'], 'all'), indent=2)+'\n', encoding='utf-8')
    (output/'.gitignore').write_text('launch.json\nassessment.json\n', encoding='utf-8')


def review(report, gate=False):
    if not isinstance(report, dict) or report.get('schema_version') != 1:
        return ['launch report schema_version must equal 1']
    try:
        validate_selection(report.get('platforms'), report.get('features'))
    except ValueError as exc:
        return [str(exc)]
    errors = []
    if not isinstance(report.get('project'), str) or not report['project'].strip():
        errors.append('project must be nonblank')
    expected = checkpoints(report['features'], report['platforms'])
    entries = report.get('checks')
    if not isinstance(entries, list):
        return errors + ['checks must be an array']
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append('check must be an object')
            continue
        key = entry.get('id')
        if not isinstance(key, str) or key not in expected:
            errors.append('unknown or unselected check ID')
            continue
        if key in seen:
            errors.append(f'{key}: duplicate check')
        seen.add(key)
        status = entry.get('status')
        if not isinstance(status, str) or status not in rules.STATUSES:
            errors.append(f'{key}: invalid status')
            continue
        def present(field):
            return isinstance(entry.get(field), str) and bool(entry[field].strip())
        if status == 'pass' and not present('evidence'):
            errors.append(f'{key}: pass requires evidence')
        if status in {'fail', 'not-applicable', 'deferred'} and not present('reason'):
            errors.append(f'{key}: {status} requires reason')
        if status == 'deferred':
            if not present('owner'):
                errors.append(f'{key}: deferred requires owner')
            value = entry.get('review_by')
            try:
                if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
                    raise ValueError()
                date.fromisoformat(value)
            except ValueError:
                errors.append(f'{key}: deferred requires valid YYYY-MM-DD review_by')
        if gate and status in {'todo', 'fail', 'deferred'}:
            errors.append(f'{key}: unresolved ({status})')
    errors.extend(f'{key}: missing check' for key in sorted(set(expected)-seen))
    scope = report.get('scope')
    if gate and (not isinstance(scope, str) or not scope.strip() or scope.lstrip().startswith('TODO:')):
        errors.append('record actual launch scope')
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init', help='create planning files in a NEW directory; does not build an app')
    init.add_argument('--output', required=True, type=Path)
    init.add_argument('--name', required=True)
    init.add_argument('--platform', action='append', choices=PLATFORMS, required=True)
    init.add_argument('--feature', action='append', choices=FEATURES, default=[])
    check = sub.add_parser('review', help='review launch declarations; gate also checks the numbered assessment')
    check.add_argument('file', type=Path)
    check.add_argument('--gate', action='store_true')
    check.add_argument('--assessment', type=Path, help='numbered assessment override (default: sibling assessment.json)')
    check.add_argument('--format', choices=('text', 'json'), default='text')
    args = parser.parse_args(argv)
    try:
        if args.command == 'init':
            initialize(args.output, args.name, args.platform, args.feature)
            print(f'Created planning files in {args.output}. Next: fill brief.md and build the first working journey.')
            return 0
        report = json.loads(args.file.read_text(encoding='utf-8-sig'))
        errors = review(report, args.gate)
        if args.gate:
            assessment_path = args.assessment or args.file.with_name('assessment.json')
            assessment = json.loads(assessment_path.read_text(encoding='utf-8-sig'))
            catalog = rules.catalog()
            catalog_errors = rules.validate(catalog)
            if catalog_errors:
                raise ValueError('; '.join(catalog_errors))
            if not isinstance(assessment, dict) or assessment.get('profile') != 'all':
                errors.append('launch gate requires an all-profile numbered assessment')
            errors.extend('assessment: '+e for e in rules.review(assessment, catalog['rules'], gate=True))
        result = {'valid': not errors, 'gate': args.gate, 'errors': errors, 'evidence_verified': False}
        if args.format == 'json':
            print(json.dumps(result))
        else:
            print('\n'.join(errors) if errors else 'Declaration structure valid; evidence has not been independently verified.')
        return 1 if errors else 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
