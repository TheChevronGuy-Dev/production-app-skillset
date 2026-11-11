import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('rules', ROOT / 'scripts/rules.py')
rules = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rules)

class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = rules.catalog()
        self.items = self.data['rules']

    def test_all_original_numbers_once(self):
        self.assertEqual([], rules.validate(self.data))
        self.assertEqual(list(range(1, 101)), [r['original_number'] for r in self.items])

    def test_duplicate_id_rejected(self):
        self.data['rules'][1]['id'] = 'R001'
        self.assertTrue(rules.validate(self.data))

    def test_missing_guidance_rejected(self):
        self.data['rules'][0]['guidance'] = ' '
        self.assertTrue(rules.validate(self.data))

    def test_profile_selection(self):
        api = rules.select(self.items, 'api')
        self.assertNotIn('payments', {r['pillar'] for r in api})
        self.assertEqual(100, len(rules.select(self.items, 'ecommerce')))
        self.assertIn('R022', [r['id'] for r in rules.select(self.items, query='webhook')])

    def assessment(self):
        return rules.make_assessment(self.items, 'all')

    def test_new_assessment_structure_valid_but_gate_fails(self):
        assessment = self.assessment()
        self.assertEqual([], rules.review(assessment, self.items))
        self.assertTrue(rules.review(assessment, self.items, gate=True))

    def test_pass_needs_evidence(self):
        assessment = self.assessment()
        assessment['rules'][0]['status'] = 'pass'
        self.assertIn('R001: pass requires evidence', rules.review(assessment, self.items))

    def test_fail_requires_nonblank_reason(self):
        assessment = self.assessment()
        for reason in ('', '  ', None, 42):
            assessment['rules'][0].update(status='fail', reason=reason)
            self.assertIn('R001: fail requires reason', rules.review(assessment, self.items))
        assessment['rules'][0]['reason'] = 'Cross-tenant access succeeds; scope query by tenant.'
        self.assertEqual([], rules.review(assessment, self.items))
        self.assertIn('R001: unresolved (fail)', rules.review(assessment, self.items, gate=True))

    def test_deferred_date_format(self):
        assessment = self.assessment()
        entry = assessment['rules'][0]
        entry.update(status='deferred', reason='Pending review', owner='team')
        for value in ('tomorrow', '2027-02-30', '20270101'):
            entry['review_by'] = value
            self.assertIn('R001: review_by must be a valid YYYY-MM-DD date', rules.review(assessment, self.items))
        entry['review_by'] = '2027-01-01'
        self.assertEqual([], rules.review(assessment, self.items))

    def test_review_cli_json_and_windows_bom(self):
        assessment = self.assessment()
        assessment['rules'][0]['status'] = 'fail'
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'assessment.json'
            path.write_text(json.dumps(assessment), encoding='utf-8-sig')
            result = subprocess.run([sys.executable, str(ROOT/'scripts/rules.py'), 'review', str(path), '--format', 'json'], capture_output=True, text=True)
            self.assertEqual(1, result.returncode, result.stderr)
            report = json.loads(result.stdout)
            self.assertFalse(report['valid'])
            self.assertFalse(report['evidence_verified'])
            self.assertIn('R001: fail requires reason', report['errors'])
            assessment['rules'][0]['reason'] = 'Boundary failure; add authorization.'
            path.write_text(json.dumps(assessment), encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT/'scripts/rules.py'), 'review', str(path), '--format', 'json'], capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue(json.loads(result.stdout)['valid'])

    def test_na_and_deferred_require_rationale(self):
        assessment = self.assessment()
        for status in ('not-applicable', 'deferred'):
            assessment['rules'][0]['status'] = status
            self.assertTrue(rules.review(assessment, self.items))
        assessment['rules'][0].update(reason='Awaiting provider setup', owner='team', review_by='2027-01-01')
        self.assertEqual([], rules.review(assessment, self.items))
        self.assertTrue(rules.review(assessment, self.items, gate=True))

    def test_missing_duplicate_and_unknown_ids(self):
        for mutation in ('missing', 'duplicate', 'unknown'):
            assessment = self.assessment()
            if mutation == 'missing':
                assessment['rules'].pop()
            elif mutation == 'duplicate':
                assessment['rules'].append(copy.deepcopy(assessment['rules'][0]))
            else:
                assessment['rules'][0]['id'] = 'R999'
            self.assertTrue(rules.review(assessment, self.items))

    def test_complete_declared_assessment_passes(self):
        assessment = self.assessment()
        assessment['scope'] = 'Synthetic test only; not evidence for an actual application.'
        for entry in assessment['rules']:
            entry.update(status='not-applicable', reason='Synthetic fixture exercising validator only')
        assessment['rules'][0].update(status='pass', evidence='Synthetic evidence field for unit test')
        self.assertEqual([], rules.review(assessment, self.items, gate=True))

    def test_malformed_assessments_are_rejected(self):
        for bad in ([], {}, {'profile': []}, {'profile': 'all', 'rules': [None, {'id': []}]}):
            self.assertTrue(rules.review(bad, self.items))

    def test_cli_from_another_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run([sys.executable, str(ROOT/'scripts/rules.py'), 'list', '--query', 'webhook'], cwd=temp, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn('R022', result.stdout)

    def test_cli_invalid_json_and_empty_filter(self):
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp)/'invalid.json'
            file.write_text('{bad json')
            result = subprocess.run([sys.executable, str(ROOT/'scripts/rules.py'), 'review', str(file)], capture_output=True, text=True)
            self.assertEqual(2, result.returncode)
        result = subprocess.run([sys.executable, str(ROOT/'scripts/rules.py'), 'list', '--pillar', 'typo'], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)

    def test_reference_drift_check(self):
        result = subprocess.run([sys.executable, str(ROOT/'scripts/render_references.py'), '--check'], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_skill_local_links_resolve(self):
        import re
        for target in re.findall(r'\]\(([^)]+)\)', (ROOT/'SKILL.md').read_text()):
            self.assertTrue((ROOT/target).is_file(), target)

if __name__ == '__main__':
    unittest.main()
