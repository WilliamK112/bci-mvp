import json
import unittest
from pathlib import Path


class TestCrossSubjectSeedSensitivity(unittest.TestCase):
    def test_seed_sensitivity_schema_and_ranges(self):
        p = Path('outputs/cross_subject_seed_sensitivity.json')
        self.assertTrue(p.exists(), 'outputs/cross_subject_seed_sensitivity.json missing')
        obj = json.loads(p.read_text(encoding='utf-8'))

        for k in ['subjects', 'seeds', 'models']:
            self.assertIn(k, obj)

        self.assertGreaterEqual(len(obj['subjects']), 2)
        self.assertGreaterEqual(len(obj['seeds']), 3)

        models = obj['models']
        for m in ['rf', 'mlp']:
            self.assertIn(m, models)
            row = models[m]
            for k in ['seed_scores', 'mean_accuracy', 'std_accuracy', 'min_accuracy', 'max_accuracy']:
                self.assertIn(k, row)
            self.assertEqual(len(row['seed_scores']), len(obj['seeds']))
            self.assertGreaterEqual(float(row['min_accuracy']), 0.0)
            self.assertLessEqual(float(row['max_accuracy']), 1.0)
            self.assertGreaterEqual(float(row['std_accuracy']), 0.0)


if __name__ == '__main__':
    unittest.main()
