import unittest
from fastapi.testclient import TestClient
from api.main import app


class TestAPIContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health(self):
        r = self.client.get('/health')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json().get('ok'), True)

    def test_predict_schema(self):
        payload = {'features': [0.0] * 32}
        r = self.client.post('/predict', json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('label', data)
        self.assertIn('focused_prob', data)
        self.assertIn('relaxed_prob', data)
        self.assertIn('mode', data)

    def test_predict_validation(self):
        payload = {'features': [0.0] * 10}
        r = self.client.post('/predict', json=payload)
        self.assertEqual(r.status_code, 422)


if __name__ == '__main__':
    unittest.main()
