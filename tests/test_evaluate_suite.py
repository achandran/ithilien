import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from evaluate_suite import execution_failed
class SuiteStatus(unittest.TestCase):
    def test_quality_failure_is_not_execution_failure(self):
        r={'stages':{'neovim':{'status':'pass'}},'themes':[{'codex_diff':{'captures':60,'status':'fail'}}]}
        self.assertFalse(execution_failed(r))
    def test_missing_native_capture_is_execution_failure(self):
        r={'stages':{'neovim':{'status':'pass'}},'themes':[{'codex_diff':{'status':'fail'}}]}
        self.assertTrue(execution_failed(r))
    def test_failed_neovim_stage_cannot_be_masked(self):
        self.assertTrue(execution_failed({'stages':{'neovim':{'status':'fail'}},'themes':[]}))

    def test_blocked_workflow_is_not_pass(self):
        from evaluate_suite import workflow_status
        self.assertEqual(workflow_status({'pass':False,'results':[{'pass':False,'status':'blocked'}]}),'blocked')
        self.assertEqual(workflow_status({'pass':False,'results':[{'pass':False,'status':'blocked'},{'pass':False,'status':'fail'}]}),'fail')

    def test_missing_dependency_is_recorded(self):
        from evaluate_suite import run_workflow
        r={'stages':{},'themes':[]}
        def missing():raise FileNotFoundError('dependency absent')
        run_workflow(r,'native',missing)
        self.assertEqual(r['stages']['native']['status'],'blocked')
        self.assertTrue(execution_failed(r))

    def test_empty_workflow_cannot_pass(self):
        from evaluate_suite import workflow_status
        self.assertEqual(workflow_status({'pass':True,'results':[]}),'fail')

    def test_gallery_lists_native_profiles(self):
        import tempfile
        from evaluate_suite import write_index
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);(out/'pickers').mkdir();(out/'pickers/gallery.html').write_text('fixture')
            write_index(out,{'themes':[],'stages':{'pickers':{'status':'pass','gallery':'pickers/gallery.html'},'codex':{'status':'blocked','reason':'cargo absent'}}})
            page=(out/'index.html').read_text()
            self.assertIn('pickers/gallery.html',page)
            self.assertIn('cargo absent',page)

    def test_quality_gate_failure_rejects_successful_capture(self):
        import json,tempfile
        from evaluate_suite import finalize
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            for name in ('neovim','python'):
                (out/name).mkdir();(out/name/'scorecard.json').write_text(json.dumps({'results':[{'gates':{'failures':['contrast'] if name=='neovim' else []}}]}))
            r={'stages':{'neovim':{'status':'pass'},'python':{'status':'pass'},'interactions':{'status':'pass'}},'interactions':{'quality_pass':True},'themes':[{'codex_diff':{'captures':1,'status':'pass'},'agent_gates':{'status':'pass'}}]}
            self.assertTrue(finalize(r,out,True))
            self.assertEqual(r['required_execution_status'],'complete')
            self.assertEqual(r['acceptance_status'],'fail')
            self.assertEqual(r['stages']['neovim']['quality_status'],'fail')

    def test_permission_failure_is_blocked_not_silently_passed(self):
        from evaluate_suite import interaction_status
        error='fzf did not render a live result list: operation not permitted'
        r={'results':[{'errors':[error]}]}
        self.assertEqual(interaction_status(r),'blocked')
        r['results'].append({'errors':['Unexpected rendering error']})
        self.assertEqual(interaction_status(r),'fail')
