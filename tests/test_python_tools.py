"""Require real outcomes and plugin pane content, not just source-buffer text."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from evaluate_python_tools import check

class PythonTools(unittest.TestCase):
    def shot(self):
        return {'case':'dap-scopes','width':100,'state':'initial','text':'total 42',
            'defaults':{'fg':0,'bg':0xFAFAF8},'attrs':{},'cells':[{'text':'x','attr':0}],
            'evidence':{'parser':True,'stopped':True,'windows':[{'filetype':'dapui_scopes','text':'total 42'}],'errors':[]}}
    def check(self,s):return check(s,{'Nimloth':'#FAFAF8','Lebethron':'#000000','Ilex':'#000000','Annun':'#000000','Ash':'#000000'})['pass']
    def test_valid(self):self.assertTrue(self.check(self.shot()))
    def test_not_stopped(self):
        s=self.shot();s['evidence']['stopped']=False;self.assertFalse(self.check(s))
    def test_source_cannot_substitute_for_scope(self):
        s=self.shot();s['evidence']['windows'][0]['text']='';self.assertFalse(self.check(s))
    def test_missing_test_outcomes(self):
        s=self.shot();s['case']='neotest-summary';s['text']='test_pass test_fail test_skip'
        s['evidence']['windows']=[{'filetype':'neotest-summary','text':s['text']}]
        s['attr_info']={0:[{'hi_name':g} for g in ('NeotestPassed','NeotestFailed','NeotestSkipped')]}
        s['evidence']['counts']={'passed':1,'failed':1,'skipped':1}
        self.assertTrue(self.check(s))
        s['evidence']['counts']['failed']=0;self.assertFalse(self.check(s))
