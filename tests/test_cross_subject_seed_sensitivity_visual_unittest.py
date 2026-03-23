import unittest
from pathlib import Path


class TestCrossSubjectSeedSensitivityVisual(unittest.TestCase):
    def test_visual_artifacts_exist_and_nonempty(self):
        svg = Path('assets/cross_subject_seed_sensitivity.svg')
        md = Path('docs/CROSS_SUBJECT_SEED_SENSITIVITY_VISUAL.md')
        self.assertTrue(svg.exists(), 'assets/cross_subject_seed_sensitivity.svg missing')
        self.assertTrue(md.exists(), 'docs/CROSS_SUBJECT_SEED_SENSITIVITY_VISUAL.md missing')
        self.assertGreater(svg.stat().st_size, 100)
        self.assertIn('assets/cross_subject_seed_sensitivity.svg', md.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
