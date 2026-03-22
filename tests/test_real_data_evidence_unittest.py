import unittest
from pathlib import Path


class TestRealDataEvidence(unittest.TestCase):
    def test_real_data_evidence_doc_exists_and_has_core_fields(self):
        p = Path('docs/REAL_DATA_EVIDENCE.md')
        self.assertTrue(p.exists(), 'docs/REAL_DATA_EVIDENCE.md missing')
        t = p.read_text(encoding='utf-8')
        for token in [
            'Relaxed EDF files',
            'Focused EDF files',
            'Shared subjects',
            'Per-subject file counts',
        ]:
            self.assertIn(token, t)


if __name__ == '__main__':
    unittest.main()
