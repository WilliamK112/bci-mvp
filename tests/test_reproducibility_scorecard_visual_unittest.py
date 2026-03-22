import unittest
from pathlib import Path


class TestReproducibilityScorecardVisual(unittest.TestCase):
    def test_visual_artifacts_exist_and_nonempty(self):
        svg = Path('assets/reproducibility_scorecard.svg')
        md = Path('docs/REPRODUCIBILITY_SCORECARD_VISUAL.md')
        self.assertTrue(svg.exists(), 'assets/reproducibility_scorecard.svg missing')
        self.assertTrue(md.exists(), 'docs/REPRODUCIBILITY_SCORECARD_VISUAL.md missing')
        self.assertGreater(svg.stat().st_size, 100)
        self.assertIn('assets/reproducibility_scorecard.svg', md.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
