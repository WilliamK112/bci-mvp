import json
import unittest
from pathlib import Path


class TestScorecardsOverview(unittest.TestCase):
    def test_overview_schema_and_consistency(self):
        p = Path('outputs/scorecards_overview.json')
        self.assertTrue(p.exists(), 'outputs/scorecards_overview.json missing')
        obj = json.loads(p.read_text(encoding='utf-8'))

        for k in ['overall_pass', 'all_sources_present', 'average_score', 'rows']:
            self.assertIn(k, obj)

        self.assertIsInstance(obj['overall_pass'], bool)
        self.assertIsInstance(obj['all_sources_present'], bool)
        self.assertGreaterEqual(float(obj['average_score']), 0.0)
        self.assertLessEqual(float(obj['average_score']), 1.0)

        rows = obj['rows']
        self.assertGreaterEqual(len(rows), 4)
        names = {r.get('name') for r in rows}
        for expected in ['streaming', 'generalization', 'reproducibility', 'master']:
            self.assertIn(expected, names)

        for r in rows:
            self.assertIn('pass', r)
            self.assertIn('score', r)
            self.assertIn('source_exists', r)
            self.assertIsInstance(r['pass'], bool)
            self.assertIsInstance(r['source_exists'], bool)
            self.assertGreaterEqual(float(r['score']), 0.0)
            self.assertLessEqual(float(r['score']), 1.0)

        self.assertTrue(bool(obj['all_sources_present']))
        self.assertTrue(bool(obj['overall_pass']))


if __name__ == '__main__':
    unittest.main()
