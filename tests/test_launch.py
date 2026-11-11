import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import launch
import rules


class LaunchTests(unittest.TestCase):
    def invoke(self, *args):
        return subprocess.run([sys.executable, str(ROOT/'scripts/launch.py'), *map(str, args)], capture_output=True, text=True)

    def create(self, directory, features=None, platforms=None):
        path = Path(directory)/'plan'
        launch.initialize(path, 'A useful idea', platforms or ['web'], features or [])
        return path, json.loads((path/'launch.json').read_text(encoding='utf-8'))

    def test_features_select_only_requested_work_and_preserve_all_rules(self):
        with tempfile.TemporaryDirectory() as temp:
            path, report = self.create(temp, ['payments', 'mailing-list'], ['android', 'ios'])
            ids = {entry['id'] for entry in report['checks']}
            self.assertIn('PAY-02', ids)
            self.assertIn('ANDROID-01', ids)
            self.assertIn('IOS-01', ids)
            self.assertNotIn('WEB-01', ids)
            self.assertIn('MAIL-02', ids)
            self.assertNotIn('AUTH-01', ids)
            self.assertNotIn('CRYPT-01', ids)
            self.assertEqual(['android', 'ios'], report['platforms'])
            self.assertEqual(100, len(json.loads((path/'assessment.json').read_text())['rules']))
            self.assertTrue((path/'guides/commerce.md').is_file())
            self.assertFalse((path/'guides/private-content.md').exists())

    def test_dual_mobile_target_requires_both_platform_checks(self):
        with tempfile.TemporaryDirectory() as temp:
            _, report = self.create(temp, platforms=['android', 'ios'])
            report['checks'] = [e for e in report['checks'] if e['id'] != 'IOS-01']
            self.assertIn('IOS-01: missing check', launch.review(report))

    def test_refuses_to_overwrite_existing_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            path, _ = self.create(temp)
            before = (path/'brief.md').read_bytes()
            result = self.invoke('init', '--output', path, '--name', 'Changed', '--platform', 'web')
            self.assertEqual(2, result.returncode)
            self.assertEqual(before, (path/'brief.md').read_bytes())

    def test_invalid_selection_creates_nothing(self):
        for platforms, features in [([], []), (['web', 'web'], []), (['unknown'], []), (['web'], ['accounts', 'accounts']), (['web'], ['bad'])]:
            with self.subTest(platforms=platforms, features=features), tempfile.TemporaryDirectory() as temp:
                path = Path(temp)/'plan'
                with self.assertRaises(ValueError):
                    launch.initialize(path, 'Idea', platforms, features)
                self.assertFalse(path.exists())

    def test_new_plan_is_structurally_valid_but_cannot_pass_gate(self):
        with tempfile.TemporaryDirectory() as temp:
            path, report = self.create(temp)
            self.assertEqual([], launch.review(report))
            result = self.invoke('review', path/'launch.json', '--gate', '--format', 'json')
            self.assertEqual(1, result.returncode, result.stderr)
            data = json.loads(result.stdout)
            self.assertFalse(data['evidence_verified'])
            self.assertTrue(any('assessment:' in e for e in data['errors']))

    def test_missing_duplicate_unknown_checks(self):
        for change in ('missing', 'duplicate', 'unknown'):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temp:
                _, report = self.create(temp)
                if change == 'missing': report['checks'].pop()
                elif change == 'duplicate': report['checks'].append(dict(report['checks'][0]))
                else: report['checks'][0]['id'] = 'AUTH-01'
                self.assertTrue(launch.review(report))

    def test_evidence_rationale_and_deferral(self):
        with tempfile.TemporaryDirectory() as temp:
            _, report = self.create(temp)
            entry = report['checks'][0]
            for status in ('pass', 'fail', 'not-applicable', 'deferred'):
                entry['status'] = status
                self.assertTrue(launch.review(report))
            entry.update(status='deferred', reason='Waiting for a test device', owner='maintainer', review_by='2027-02-30')
            self.assertTrue(launch.review(report))
            entry['review_by'] = '2027-02-28'
            self.assertEqual([], launch.review(report))
            self.assertTrue(launch.review(report, gate=True))

    def test_completed_declarations_require_complete_all_profile_assessment(self):
        with tempfile.TemporaryDirectory() as temp:
            path, report = self.create(temp, list(launch.FEATURES))
            report['scope'] = 'Synthetic test fixture, not a real release'
            for entry in report['checks']:
                entry.update(status='pass', evidence='Synthetic fixture only')
            (path/'launch.json').write_text(json.dumps(report), encoding='utf-8-sig')
            assessment = json.loads((path/'assessment.json').read_text())
            assessment['scope'] = report['scope']
            for entry in assessment['rules']:
                entry.update(status='not-applicable', reason='Synthetic fixture only')
            (path/'assessment.json').write_text(json.dumps(assessment), encoding='utf-8')
            result = self.invoke('review', path/'launch.json', '--gate', '--format', 'json')
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertFalse(json.loads(result.stdout)['evidence_verified'])
            assessment['rules'][0].update(status='fail', reason='Authorization failure')
            (path/'assessment.json').write_text(json.dumps(assessment), encoding='utf-8')
            self.assertEqual(1, self.invoke('review', path/'launch.json', '--gate').returncode)
            assessment['rules'][0]['status'] = 'not-applicable'
            assessment['profile'] = 'api'
            (path/'assessment.json').write_text(json.dumps(assessment), encoding='utf-8')
            self.assertEqual(1, self.invoke('review', path/'launch.json', '--gate').returncode)

    def test_malformed_reports_and_input_errors(self):
        for report in (None, [], {}, {'schema_version': 1, 'platforms': [], 'features': []}, {'schema_version': 1, 'platforms': ['web'], 'features': [], 'checks': [None, {'id': []}]}):
            self.assertTrue(launch.review(report))
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'bad.json'
            path.write_text('{broken')
            self.assertEqual(2, self.invoke('review', path).returncode)
            path.unlink()
            self.assertEqual(2, self.invoke('review', path).returncode)

    def test_cli_runs_from_other_directory_with_spaces(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'my idea'
            result = subprocess.run([sys.executable, str(ROOT/'scripts/launch.py'), 'init', '--name', 'My idea', '--platform', 'web', '--feature', 'accounts', '--output', str(path)], cwd=temp, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((path/'guides/accounts.md').exists())

    def test_every_platform_and_feature_has_usable_resources(self):
        for platform in launch.PLATFORMS:
            with tempfile.TemporaryDirectory() as temp:
                path, report = self.create(temp, list(launch.FEATURES), [platform])
                self.assertEqual([], launch.review(report))
                self.assertEqual(len(launch.MODULES), len(list((path/'guides').glob('*.md'))))


if __name__ == '__main__':
    unittest.main()
