import json
import unittest
from pathlib import Path


class TestStreamingScorecard(unittest.TestCase):
    def test_streaming_scorecard_schema_and_gates(self):
        p = Path('outputs/streaming_scorecard.json')
        self.assertTrue(p.exists(), 'outputs/streaming_scorecard.json missing')
        obj = json.loads(p.read_text(encoding='utf-8'))

        self.assertIn('overall_pass', obj)
        self.assertIn('score', obj)
        self.assertIn('metrics', obj)
        self.assertIn('gates', obj)

        self.assertIsInstance(obj['overall_pass'], bool)
        self.assertGreaterEqual(float(obj['score']), 0.0)
        self.assertLessEqual(float(obj['score']), 1.0)

        gates = obj['gates']
        for k in ['latency_p95_le_120ms', 'throughput_ge_8', 'stability_pass', 'drift_p95_le_0_30']:
            self.assertIn(k, gates)
            self.assertIsInstance(gates[k], bool)

        metrics = obj['metrics']
        self.assertIn('latency_p95_ms', metrics)
        self.assertIn('throughput_windows_per_sec', metrics)
        self.assertIn('drift_p95_abs_prob_shift', metrics)

        self.assertLessEqual(float(metrics['latency_p95_ms']), 120.0 + 1e-9)
        self.assertGreaterEqual(float(metrics['throughput_windows_per_sec']), 8.0 - 1e-9)
        self.assertLessEqual(float(metrics['drift_p95_abs_prob_shift']), 0.30 + 1e-9)
        self.assertTrue(bool(obj['overall_pass']))


if __name__ == '__main__':
    unittest.main()
