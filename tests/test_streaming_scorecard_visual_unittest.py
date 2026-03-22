import unittest
from pathlib import Path


class TestStreamingScorecardVisual(unittest.TestCase):
    def test_visual_artifacts_exist_and_nonempty(self):
        svg = Path('assets/streaming_scorecard.svg')
        md = Path('docs/STREAMING_SCORECARD_VISUAL.md')
        self.assertTrue(svg.exists(), 'assets/streaming_scorecard.svg missing')
        self.assertTrue(md.exists(), 'docs/STREAMING_SCORECARD_VISUAL.md missing')
        self.assertGreater(svg.stat().st_size, 100)
        text = md.read_text(encoding='utf-8')
        self.assertIn('assets/streaming_scorecard.svg', text)


if __name__ == '__main__':
    unittest.main()
