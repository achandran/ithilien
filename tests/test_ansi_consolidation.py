"""Check the adopted ANSI aliases at their generated application boundaries."""
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from ithilienlib import ROOT, load_palette, resolve_palette


class ANSIConsolidation(unittest.TestCase):
    def test_ghostty_exports_complete_aliases_and_distinct_black(self):
        lines=(ROOT/'ghostty/themes/ithilien_dawn.conf').read_text().splitlines()
        slots={int(k):v for line in lines if line.startswith('palette = ')
               for k,v in [line.removeprefix('palette = ').split('=',1)]}
        self.assertTrue(set(range(16)) <= slots.keys())
        for index in range(1,7):
            self.assertEqual(slots[index],slots[index+8])
        self.assertNotEqual(slots[0],slots[8])
        self.assertEqual(slots[7],slots[15])
        p=load_palette('ithilien-dawn')
        for i,key in enumerate(['black','red','green','yellow','blue','magenta','cyan','white']):
            self.assertEqual(slots[i],p['ansi'][key])
            self.assertEqual(slots[i+8],p['ansi']['bright'+key.capitalize()])

    def test_ansi_and_approved_diff_changes_preserve_other_semantics(self):
        baseline=json.loads((ROOT/'reports/ansi-consolidation/baseline.json').read_text())
        shared=json.loads((ROOT/'palette/ithilien-shared.json').read_text())
        before=resolve_palette(shared,baseline)
        after=load_palette('ithilien-dawn')
        self.assertNotEqual(before['ansi'],after['ansi'])
        # Separately approved four-color diff consolidation.
        # Approved neutral consolidation preserves roles while sharing Ash.
        before['foregrounds']['subtext']=before['foregrounds']['muted']
        before['highlight']['border']=before['foregrounds']['muted']
        # Approved shared teal for application accents and terminal cyan.
        before['accents']['aqua']='#255354'
        # Approved Lily -> Nimloth (formerly Asphodel) surface consolidation, preserving roles.
        before['backgrounds']['surface0']=before['backgrounds']['base']
        # Approved Harlond -> Osgiliath consolidation preserves surface2 role.
        before['backgrounds']['surface2']=before['backgrounds']['crust']
        before['diff']['addEmphasis']=before['diff']['deleteEmphasis']=before['diff']['changeEmphasis']
        self.assertEqual({k:v for k,v in before.items() if k!='ansi'},
                         {k:v for k,v in after.items() if k!='ansi'})
