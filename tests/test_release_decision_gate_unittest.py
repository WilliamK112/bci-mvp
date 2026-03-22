import json
import unittest
from pathlib import Path


class TestReleaseDecisionGate(unittest.TestCase):
    def test_release_decision_gate_schema_and_values(self):
        p = Path('outputs/release_decision_gate.json')
        self.assertTrue(p.exists(), 'outputs/release_decision_gate.json missing')
        obj = json.loads(p.read_text(encoding='utf-8'))

        for k in ['decision', 'suggested_tag', 'checks', 'matrix_avg_score']:
            self.assertIn(k, obj)

        self.assertIn(obj['decision'], ['GO', 'HOLD'])
        self.assertTrue(str(obj['suggested_tag']).startswith('v1.0.0'))
        self.assertGreaterEqual(float(obj['matrix_avg_score']), 0.0)
        self.assertLessEqual(float(obj['matrix_avg_score']), 1.0)

        checks = obj['checks']
        expected = [
            'master_overall_pass',
            'matrix_all_pass',
            'matrix_all_present',
            'overview_overall_pass',
            'overview_sources_present',
            'matrix_avg_score_ge_0_90',
        ]
        for c in expected:
            self.assertIn(c, checks)
            self.assertIsInstance(checks[c], bool)


if __name__ == '__main__':
    unittest.main()
