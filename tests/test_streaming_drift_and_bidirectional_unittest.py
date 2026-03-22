import json
import unittest
from pathlib import Path


class TestStreamingAndBidirectionalArtifacts(unittest.TestCase):
    def test_streaming_drift_schema_and_gate(self):
        p = Path('outputs/streaming_drift.json')
        self.assertTrue(p.exists(), 'outputs/streaming_drift.json missing')
        obj = json.loads(p.read_text(encoding='utf-8'))

        for k in ['n_windows', 'mean_abs_prob_shift', 'p95_abs_prob_shift', 'max_abs_prob_shift', 'pass']:
            self.assertIn(k, obj)

        self.assertGreater(obj['n_windows'], 0)
        self.assertGreaterEqual(obj['mean_abs_prob_shift'], 0.0)
        self.assertGreaterEqual(obj['p95_abs_prob_shift'], 0.0)
        self.assertGreaterEqual(obj['max_abs_prob_shift'], 0.0)
        self.assertIsInstance(obj['pass'], bool)
        self.assertLessEqual(obj['p95_abs_prob_shift'], 0.30 + 1e-9)

    def test_cross_dataset_bidirectional_schema(self):
        p = Path('outputs/cross_dataset_bidirectional.json')
        self.assertTrue(p.exists(), 'outputs/cross_dataset_bidirectional.json missing')
        obj = json.loads(p.read_text(encoding='utf-8'))

        self.assertIn('A_to_B', obj)
        self.assertIn('B_to_A', obj)
        self.assertIn('symmetry_gap_accuracy', obj)
        self.assertIn('symmetry_gap_f1', obj)
        self.assertIn('symmetry_gap_auc', obj)

        for k in ['symmetry_gap_accuracy', 'symmetry_gap_f1', 'symmetry_gap_auc']:
            self.assertGreaterEqual(float(obj[k]), 0.0)

        rf_a = obj['A_to_B']['models']['RF']
        rf_b = obj['B_to_A']['models']['RF']
        for m in (rf_a, rf_b):
            self.assertIn('accuracy', m)
            self.assertIn('f1', m)
            self.assertIn('auc', m)
            self.assertGreaterEqual(float(m['accuracy']), 0.0)
            self.assertLessEqual(float(m['accuracy']), 1.0)


if __name__ == '__main__':
    unittest.main()
