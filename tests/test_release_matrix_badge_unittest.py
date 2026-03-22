import unittest
from pathlib import Path


class TestReleaseMatrixBadge(unittest.TestCase):
    def test_badge_exists_and_nonempty(self):
        p = Path('assets/badge_release_matrix.svg')
        self.assertTrue(p.exists(), 'assets/badge_release_matrix.svg missing')
        self.assertGreater(p.stat().st_size, 100)
        txt = p.read_text(encoding='utf-8')
        self.assertIn('release-matrix', txt)


if __name__ == '__main__':
    unittest.main()
