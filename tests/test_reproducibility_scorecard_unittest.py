import json
import unittest
from pathlib import Path


class TestReproducibilityScorecard(unittest.TestCase):
    def test_reproducibility_scorecard_schema_and_gates(self):
        p = Path('outputs/reproducibility_scorecard.json')
        self.assertTrue(p.exists(), 'outputs/reproducibility_scorecard.json missing')
        obj = json.loads(p.read_text(encoding='utf-8'))

        for k in ['overall_pass', 'score', 'checks']:
            self.assertIn(k, obj)

        self.assertIsInstance(obj['overall_pass'], bool)
        self.assertGreaterEqual(float(obj['score']), 0.0)
        self.assertLessEqual(float(obj['score']), 1.0)

        checks = obj['checks']
        expected = [
            'repro_cross_subject_pass',
            'repro_release_signature_pass',
            'determinism_audit_pass',
            'explainability_stability_pass',
        ]
        for c in expected:
            self.assertIn(c, checks)
            self.assertIsInstance(checks[c], bool)
            self.assertTrue(checks[c])

        self.assertTrue(bool(obj['overall_pass']))


if __name__ == '__main__':
    unittest.main()
