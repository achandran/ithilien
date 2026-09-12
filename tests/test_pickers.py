import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from evaluate_pickers import check
class PickerGates(unittest.TestCase):
    def shot(self):
        return {'case':'cmp','width':100,'state':'initial','text':'reading','attrs':{},'defaults':{'fg':0,'bg':0xFAFAF8},'cells':[{'text':'x','attr':0}], 'evidence':{'windows':[{'filetype':'cmp_menu','text':'reading'}],'visible':True,'errors':[]}}
    def test_valid(self):self.assertTrue(check(self.shot(),{'white':'#FAFAF8','black':'#000000'})['pass'])
    def test_missing_popup(self):
        s=self.shot();s['evidence']['windows']=[];self.assertFalse(check(s,{'white':'#FAFAF8','black':'#000000'})['pass'])
    def test_hidden_completion(self):
        s=self.shot();s['evidence']['visible']=False;self.assertFalse(check(s,{'white':'#FAFAF8','black':'#000000'})['pass'])
