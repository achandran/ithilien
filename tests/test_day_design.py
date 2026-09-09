"""Regression tests for contrast gating and Day's integration contracts."""
import contextlib
import copy
import io
import json
import plistlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import audit_palette
from lodenlib import ROOT, load_palette, wcag, oklch, delta_e

class DayDesign(unittest.TestCase):
    def audit(self, palette):
        with tempfile.TemporaryDirectory() as temp, patch.object(audit_palette,'ROOT',Path(temp)), patch.object(audit_palette,'load_palette',return_value=palette), contextlib.redirect_stdout(io.StringIO()):
            try: audit_palette.main('loden-day')
            except SystemExit: pass
            return json.loads((Path(temp)/'reports/loden-day-audit.json').read_text())

    def test_day_passes(self):
        self.assertTrue(self.audit(load_palette('loden-day'))['passed'])

    def test_mantle_comment_regression_is_rejected(self):
        p=copy.deepcopy(load_palette('loden-day'))
        p['foregrounds']['comment']='#62695F'  # passes base, fails mantle
        self.assertGreaterEqual(wcag(p['foregrounds']['comment'],p['backgrounds']['base']),4.5)
        self.assertIn('comment on mantle',self.audit(p)['failures'])

    def test_informational_muted_and_ansi_are_not_exempt(self):
        p=copy.deepcopy(load_palette('loden-day'))
        p['foregrounds']['muted']=p['ansi']['brightBlack']='#7B7A6B'
        failures=self.audit(p)['failures']
        self.assertIn('muted UI',failures)
        self.assertIn('ANSI brightBlack',failures)

    def test_wcag_gate_does_not_round_up(self):
        real=audit_palette.wcag
        p=load_palette('loden-day')
        def contrast(f,b):
            if f==p['foregrounds']['comment'] and b==p['backgrounds']['base']: return 4.499
            return real(f,b)
        with patch.object(audit_palette,'wcag',side_effect=contrast):
            self.assertIn('comments',self.audit(p)['failures'])

    def test_inline_diff_foreground_is_black(self):
        p=load_palette('loden-day')
        self.assertEqual(p['diff']['inlineForeground'], '#000000')
        for state in ('add', 'delete', 'change'):
            self.assertGreaterEqual(wcag('#000000',p['diff'][state+'Emphasis']),7.0)

    def test_black_main_text_on_parchment(self):
        p=load_palette('loden-day')
        self.assertEqual(p['backgrounds']['base'], '#F0E9D2')
        self.assertEqual(p['foregrounds']['text'], '#000000')
        self.assertEqual(p['foregrounds']['bright'], '#000000')
        self.assertNotEqual(p['foregrounds']['comment'],p['foregrounds']['text'])
        self.assertEqual(p['diff']['contextForeground'], '#000000')

    def test_terminal_endpoint_collapse_is_rejected(self):
        p=copy.deepcopy(load_palette('loden-day'))
        p['ansi']['white']=p['ansi']['brightWhite']='#000000'
        self.assertIn('ANSI white on black',self.audit(p)['failures'])

    def test_syntax_on_added_lines_is_gated(self):
        p=copy.deepcopy(load_palette('loden-day'))
        p['diff']['addBackground']='#B2CCA4'
        self.assertIn('diff add syntax ochre',self.audit(p)['failures'])

    def test_changed_line_does_not_merge_with_canvas(self):
        p=load_palette('loden-day')
        # A design regression floor in normal vision, not a WCAG requirement.
        self.assertGreaterEqual(delta_e(p['diff']['changeBackground'],p['backgrounds']['base']),0.03)
        self.assertGreaterEqual(wcag(p['highlight']['background'],p['diff']['changeBackground']),3.0)

    def test_surface_order(self):
        p=load_palette('loden-day')['backgrounds']
        values=[oklch(p[k])[0] for k in ['surface0','base','surface1','mantle','crust','surface2']]
        self.assertTrue(all(a>b for a,b in zip(values,values[1:])))

    def test_codex_day_roles_and_selection(self):
        p=load_palette('loden-day')
        with (ROOT/'codex/themes/loden-day.tmTheme').open('rb') as f: theme=plistlib.load(f)
        rules={r['name']:r['settings'] for r in theme['settings'] if 'name' in r}
        for role,token in [('Keywords','clay'),('Functions','gold'),('Types','aqua'),('Operators','olive')]:
            self.assertEqual(rules[role]['foreground'],p['accents'][token])
        self.assertEqual(theme['settings'][0]['settings']['selectionForeground'],p['highlight']['foreground'])

if __name__=='__main__': unittest.main()
