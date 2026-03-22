import json
import unittest
from pathlib import Path


class TestReproRunProof(unittest.TestCase):
    def test_repro_run_proof_schema_and_artifacts(self):
        p = Path('outputs/repro_run_proof.json')
        self.assertTrue(p.exists(), 'outputs/repro_run_proof.json missing')
        obj = json.loads(p.read_text(encoding='utf-8'))

        for k in ['repro_command', 'status', 'artifacts']:
            self.assertIn(k, obj)

        self.assertEqual(obj['repro_command'], 'python src/repro_one_command.py')
        self.assertIn(obj['status'], ['PASS', 'FAIL'])
        self.assertIsInstance(obj['artifacts'], list)
        self.assertGreater(len(obj['artifacts']), 0)

        for r in obj['artifacts']:
            self.assertIn('file', r)
            self.assertIn('exists', r)
            self.assertIn('sha256', r)
            self.assertTrue(r['exists'])
            self.assertIsInstance(r['sha256'], str)
            self.assertGreater(len(r['sha256']), 10)

        self.assertEqual(obj['status'], 'PASS')


if __name__ == '__main__':
    unittest.main()
