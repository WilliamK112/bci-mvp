import unittest
from pathlib import Path


class TestReleaseDecisionGateVisual(unittest.TestCase):
    def test_visual_artifacts_exist_and_nonempty(self):
        svg = Path('assets/release_decision_gate.svg')
        md = Path('docs/RELEASE_DECISION_GATE_VISUAL.md')
        self.assertTrue(svg.exists(), 'assets/release_decision_gate.svg missing')
        self.assertTrue(md.exists(), 'docs/RELEASE_DECISION_GATE_VISUAL.md missing')
        self.assertGreater(svg.stat().st_size, 100)
        self.assertIn('assets/release_decision_gate.svg', md.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
