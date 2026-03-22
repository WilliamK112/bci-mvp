import json
import unittest
from pathlib import Path


class TestProjectMasterScorecard(unittest.TestCase):
    def test_master_scorecard_schema_and_bounds(self):
        p = Path('outputs/project_master_scorecard.json')
        self.assertTrue(p.exists(), 'outputs/project_master_scorecard.json missing')
        obj = json.loads(p.read_text(encoding='utf-8'))

        for k in ['overall_pass', 'overall_score', 'pillars', 'pillar_scores']:
            self.assertIn(k, obj)

        self.assertIsInstance(obj['overall_pass'], bool)
        self.assertGreaterEqual(float(obj['overall_score']), 0.0)
        self.assertLessEqual(float(obj['overall_score']), 1.0)

        pillars = obj['pillars']
        scores = obj['pillar_scores']
        for name in ['streaming', 'generalization', 'reproducibility']:
            self.assertIn(name, pillars)
            self.assertIn(name, scores)
            self.assertIsInstance(pillars[name], bool)
            self.assertGreaterEqual(float(scores[name]), 0.0)
            self.assertLessEqual(float(scores[name]), 1.0)

        self.assertTrue(bool(obj['overall_pass']))


if __name__ == '__main__':
    unittest.main()
