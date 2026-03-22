import json
import unittest
from pathlib import Path


class TestGeneralizationScorecard(unittest.TestCase):
    def test_generalization_scorecard_schema_and_gates(self):
        p = Path('outputs/generalization_scorecard.json')
        self.assertTrue(p.exists(), 'outputs/generalization_scorecard.json missing')
        obj = json.loads(p.read_text(encoding='utf-8'))

        for k in ['overall_pass', 'score', 'winner_model_loso', 'metrics', 'gates']:
            self.assertIn(k, obj)

        self.assertIsInstance(obj['overall_pass'], bool)
        self.assertGreaterEqual(float(obj['score']), 0.0)
        self.assertLessEqual(float(obj['score']), 1.0)

        gates = obj['gates']
        expected_gates = [
            'cross_subject_best_acc_ge_0_60',
            'cross_dataset_A_to_B_acc_ge_0_50',
            'cross_dataset_B_to_A_acc_ge_0_50',
            'cross_dataset_symmetry_gap_acc_le_0_25',
        ]
        for g in expected_gates:
            self.assertIn(g, gates)
            self.assertIsInstance(gates[g], bool)

        metrics = obj['metrics']
        for m in [
            'cross_subject_best_mean_accuracy',
            'cross_dataset_A_to_B_rf_accuracy',
            'cross_dataset_B_to_A_rf_accuracy',
            'cross_dataset_symmetry_gap_accuracy',
        ]:
            self.assertIn(m, metrics)

        self.assertGreaterEqual(float(metrics['cross_subject_best_mean_accuracy']), 0.60 - 1e-9)
        self.assertGreaterEqual(float(metrics['cross_dataset_A_to_B_rf_accuracy']), 0.50 - 1e-9)
        self.assertGreaterEqual(float(metrics['cross_dataset_B_to_A_rf_accuracy']), 0.50 - 1e-9)
        self.assertLessEqual(float(metrics['cross_dataset_symmetry_gap_accuracy']), 0.25 + 1e-9)
        self.assertTrue(bool(obj['overall_pass']))


if __name__ == '__main__':
    unittest.main()
