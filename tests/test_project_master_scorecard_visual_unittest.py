import unittest
from pathlib import Path


class TestProjectMasterScorecardVisual(unittest.TestCase):
    def test_visual_artifacts_exist_and_nonempty(self):
        svg = Path('assets/project_master_scorecard.svg')
        md = Path('docs/PROJECT_MASTER_SCORECARD_VISUAL.md')
        self.assertTrue(svg.exists(), 'assets/project_master_scorecard.svg missing')
        self.assertTrue(md.exists(), 'docs/PROJECT_MASTER_SCORECARD_VISUAL.md missing')
        self.assertGreater(svg.stat().st_size, 100)
        self.assertIn('assets/project_master_scorecard.svg', md.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
