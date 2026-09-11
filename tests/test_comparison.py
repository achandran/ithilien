import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import compare

class ComparisonTests(unittest.TestCase):
    def test_isolated_configs_match_typography_and_renderer(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(compare,'ROOT',Path(temp)), contextlib.redirect_stdout(io.StringIO()):
            compare.prepare()
            for name in compare.SOURCES:
                text=(Path(temp)/f'comparison/generated/{name}.conf').read_text()
                self.assertIn('minimum-contrast = 1',text)
                self.assertIn('font-family = Berkeley Mono Medium',text)
                self.assertIn('font-thicken = false',text)
                self.assertEqual(text.count('cursor-style ='),1)
