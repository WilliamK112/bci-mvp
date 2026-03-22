import unittest
from src.streaming import StreamingStateFilter, StreamingConfig


class TestStreamingFilter(unittest.TestCase):
    def test_hysteresis_transitions(self):
        f = StreamingStateFilter(StreamingConfig(alpha=1.0, high_threshold=0.6, low_threshold=0.4))
        self.assertEqual(f.update(0.2)["state"], "relaxed")
        self.assertEqual(f.update(0.65)["state"], "focused")
        self.assertEqual(f.update(0.45)["state"], "focused")
        self.assertEqual(f.update(0.35)["state"], "relaxed")


if __name__ == "__main__":
    unittest.main()
