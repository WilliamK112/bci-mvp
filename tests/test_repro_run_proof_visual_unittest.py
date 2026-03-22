import unittest
from pathlib import Path


class TestReproRunProofVisual(unittest.TestCase):
    def test_visual_artifacts_exist_and_nonempty(self):
        svg = Path('assets/repro_run_proof.svg')
        md = Path('docs/REPRO_RUN_PROOF_VISUAL.md')
        self.assertTrue(svg.exists(), 'assets/repro_run_proof.svg missing')
        self.assertTrue(md.exists(), 'docs/REPRO_RUN_PROOF_VISUAL.md missing')
        self.assertGreater(svg.stat().st_size, 100)
        self.assertIn('assets/repro_run_proof.svg', md.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
