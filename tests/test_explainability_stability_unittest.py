import json
import unittest
from pathlib import Path


class TestExplainabilityStability(unittest.TestCase):
    def test_explainability_stability_artifact(self):
        p = Path('outputs/explainability_stability.json')
        self.assertTrue(p.exists(), 'outputs/explainability_stability.json missing')
        obj = json.loads(p.read_text(encoding='utf-8'))

        for k in ['run1', 'run2', 'top5_jaccard', 'top_band_consistent', 'pass']:
            self.assertIn(k, obj)

        self.assertGreaterEqual(float(obj['top5_jaccard']), 0.0)
        self.assertLessEqual(float(obj['top5_jaccard']), 1.0)
        self.assertIsInstance(obj['top_band_consistent'], bool)
        self.assertIsInstance(obj['pass'], bool)

        # project gate expectation from explainability_stability.py
        self.assertGreaterEqual(float(obj['top5_jaccard']), 0.5)
        self.assertTrue(bool(obj['top_band_consistent']))
        self.assertTrue(bool(obj['pass']))


if __name__ == '__main__':
    unittest.main()
