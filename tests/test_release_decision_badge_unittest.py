import unittest
from pathlib import Path


class TestReleaseDecisionBadge(unittest.TestCase):
    def test_badge_exists_and_nonempty(self):
        p = Path('assets/badge_release_decision.svg')
        self.assertTrue(p.exists(), 'assets/badge_release_decision.svg missing')
        self.assertGreater(p.stat().st_size, 100)
        txt = p.read_text(encoding='utf-8')
        self.assertIn('release-decision', txt)


if __name__ == '__main__':
    unittest.main()
