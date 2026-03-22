import json
import unittest
from pathlib import Path


class TestReleaseReadinessMatrix(unittest.TestCase):
    def test_matrix_schema_and_consistency(self):
        p = Path('outputs/release_readiness_matrix.json')
        self.assertTrue(p.exists(), 'outputs/release_readiness_matrix.json missing')
        obj = json.loads(p.read_text(encoding='utf-8'))

        for k in ['all_present', 'all_pass', 'avg_score', 'rows']:
            self.assertIn(k, obj)

        self.assertIsInstance(obj['all_present'], bool)
        self.assertIsInstance(obj['all_pass'], bool)
        self.assertGreaterEqual(float(obj['avg_score']), 0.0)
        self.assertLessEqual(float(obj['avg_score']), 1.0)

        rows = obj['rows']
        self.assertGreaterEqual(len(rows), 5)
        names = {r.get('name') for r in rows}
        for expected in ['streaming', 'generalization', 'reproducibility', 'master', 'overview']:
            self.assertIn(expected, names)

        for r in rows:
            self.assertIn('present', r)
            self.assertIn('pass', r)
            self.assertIn('score', r)
            self.assertIsInstance(r['present'], bool)
            self.assertIsInstance(r['pass'], bool)
            self.assertGreaterEqual(float(r['score']), 0.0)
            self.assertLessEqual(float(r['score']), 1.0)

        self.assertTrue(bool(obj['all_present']))
        self.assertTrue(bool(obj['all_pass']))


if __name__ == '__main__':
    unittest.main()
