"""Mutation checks for rendered Git review evidence."""
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from evaluate_git_review import check

COLORS={'Celandine':'#D8B46A','Nimloth':'#FAFAF8','Lebethron':'#000000'}

def fixture():
    lines=['LIMIT = 10','LIMIT = 11']
    return {'width':100,'state':'initial','case':'diffview','text':'\n'.join(lines),'defaults':{'fg':0,'bg':0xFAFAF8},
      'attrs':{0:{},1:{'background':0xD8B46A}},
      'cells':[{'row':r,'col':i,'text':c,'attr':1 if i==9 else 0} for r,line in enumerate(lines) for i,c in enumerate(line)],
      'evidence':{'windows':[{'diff':True},{'diff':True}],'messages':''}}

class GitReviewGates(unittest.TestCase):
    def test_visible_patch_passes(self):
        assert check(fixture(),COLORS)['pass_']

    def test_wrong_character_emphasis_fails(self):
        shot=fixture()
        # An emphasized '1' elsewhere cannot stand in for the changed final digit.
        shot['cells'][19]['attr']=0
        shot['cells'][18]['attr']=1
        assert not check(shot,COLORS)['pass_']

    def test_missing_native_window_fails(self):
        shot=fixture();shot['evidence']['windows']=[]
        assert not check(shot,COLORS)['pass_']

    def test_off_palette_and_low_contrast_fail(self):
        shot=fixture();shot['attrs'][0]={'foreground':0xeeeeee}
        result=check(shot,COLORS)
        assert result['off_palette'] and result['contrast']['failures'] and not result['pass_']
