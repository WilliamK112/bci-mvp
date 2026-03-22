import unittest
from src.infer import predict_state
from src.model_fallback import mock_predict


class TestInferFallback(unittest.TestCase):
    def test_mock_predict_shape(self):
        out = mock_predict([0.0] * 32)
        self.assertIn(out['label'], ['focused', 'relaxed'])
        self.assertTrue(0.0 <= out['focused_prob'] <= 1.0)
        self.assertTrue(0.0 <= out['relaxed_prob'] <= 1.0)
        self.assertEqual(out['mode'], 'mock_fallback')

    def test_predict_state_without_model_uses_fallback(self):
        out = predict_state([0.1] * 32, model_path='outputs/not_exists.joblib')
        self.assertEqual(out['mode'], 'mock_fallback')


if __name__ == '__main__':
    unittest.main()
