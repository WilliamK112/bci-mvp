import json
import unittest
from pathlib import Path


class TestV1ReleaseGate(unittest.TestCase):
    def test_v1_release_gate_schema(self):
        p = Path('outputs/v1_release_gate.json')
        self.assertTrue(p.exists(), 'outputs/v1_release_gate.json missing')
        obj = json.loads(p.read_text(encoding='utf-8'))

        for k in ['release', 'go', 'checks', 'next_action']:
            self.assertIn(k, obj)

        self.assertEqual(obj['release'], 'v1.0.0')
        self.assertIsInstance(obj['go'], bool)
        self.assertIsInstance(obj['checks'], dict)
        self.assertIsInstance(obj['next_action'], str)

        expected = [
            'decision_go',
            'suggested_tag_v1',
            'matrix_all_pass',
            'matrix_all_present',
            'master_overall_pass',
            'master_score_ge_0_95',
        ]
        for e in expected:
            self.assertIn(e, obj['checks'])
            self.assertIsInstance(obj['checks'][e], bool)


if __name__ == '__main__':
    unittest.main()
