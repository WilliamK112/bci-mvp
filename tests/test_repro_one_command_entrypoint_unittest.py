import unittest
from pathlib import Path


class TestReproOneCommandEntrypoint(unittest.TestCase):
    def test_repro_entrypoint_exists_and_references_core_steps(self):
        p = Path('src/repro_one_command.py')
        self.assertTrue(p.exists(), 'src/repro_one_command.py missing')
        t = p.read_text(encoding='utf-8')
        for token in [
            'src/run_full_pipeline.py',
            'src/quick_regression_suite.py',
            'src/final_release_candidate.py',
        ]:
            self.assertIn(token, t)


if __name__ == '__main__':
    unittest.main()
