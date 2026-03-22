import unittest
from pathlib import Path


class TestScorecardsOverviewVisual(unittest.TestCase):
    def test_visual_artifacts_exist_and_nonempty(self):
        svg = Path('assets/scorecards_overview.svg')
        md = Path('docs/SCORECARDS_OVERVIEW_VISUAL.md')
        self.assertTrue(svg.exists(), 'assets/scorecards_overview.svg missing')
        self.assertTrue(md.exists(), 'docs/SCORECARDS_OVERVIEW_VISUAL.md missing')
        self.assertGreater(svg.stat().st_size, 100)
        self.assertIn('assets/scorecards_overview.svg', md.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
