"""Mutation checks for the rendered workflow gates."""
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from evaluate_installed_workflows import check, ROOT


class WorkflowGates(unittest.TestCase):
    def setUp(self):
        self.palette={int(v[1:],16) for v in json.loads((ROOT/'palette/ithilien-dawn.json').read_text())['colors'].values()}
        self.shot={'case':'blink','width':100,'state':'initial','text':'summarize',
                   'defaults':{'fg':0,'bg':0xFAFAF8},'attrs':{},
                   'cells':[{'row':0,'col':0,'text':'s','attr':0}],
                   'evidence':{'parser':True,'plugins':['blink.cmp'],'blink_visible':True,'windows':[]}}

    def test_valid(self):
        self.assertTrue(check(self.shot,self.palette)['pass'])

    def test_missing_popup_is_failure(self):
        self.shot['evidence']['blink_visible']=False
        self.assertFalse(check(self.shot,self.palette)['pass'])

    def test_missing_python_parser_is_failure(self):
        self.shot['evidence']['parser']=False
        self.assertFalse(check(self.shot,self.palette)['pass'])

    def test_missing_expected_content_is_failure(self):
        self.shot['text']=''
        self.assertFalse(check(self.shot,self.palette)['pass'])

    def test_color_leak_is_failure(self):
        self.shot['attrs']={0:{'foreground':0x123456}}
        self.assertTrue(check(self.shot,self.palette)['off_palette'])

    def test_low_contrast_palette_pair_is_failure(self):
        self.shot['attrs']={0:{'foreground':0xF0F1EF}}
        result=check(self.shot,self.palette)
        self.assertFalse(result['off_palette'])
        self.assertFalse(result['pass'])

    def test_diff_without_emphasis_is_failure(self):
        self.shot.update(case='python-diff',text='str(total) total=')
        self.assertIn('Missing rendered Celandine overlay',check(self.shot,self.palette)['failures'])

    def test_runtime_notification_is_failure(self):
        self.shot['text']+=' Lua callback:'
        self.assertFalse(check(self.shot,self.palette)['pass'])

    def test_plugin_loaded_without_window_is_failure(self):
        self.shot.update(case='neo-tree',text='palette_workflow.py')
        self.shot['evidence']['plugins']=['neo-tree.nvim']
        self.assertIn('Plugin window absent: neo-tree',check(self.shot,self.palette)['failures'])

    def test_terminal_permission_failure_is_blocked_not_pass(self):
        self.shot.update(case='fzf-lua',text='palette_workflow.py')
        self.shot['evidence'].update(plugins=['fzf-lua'],history=['[Fzf-lua] fzf error 2: operation not permitted'])
        result=check(self.shot,self.palette)
        self.assertEqual(result['status'],'blocked')
        self.assertFalse(result['pass'])


    def test_filename_in_background_cannot_satisfy_picker(self):
        self.shot.update(case='fzf-lua',text='palette_workflow.py')
        self.shot['evidence'].update(plugins=['fzf-lua'],windows=[{'filetype':'fzf','text':'nvim/cache.lua'}])
        self.assertIn('Expected Python file absent from visible fzf result pane',check(self.shot,self.palette)['failures'])
        self.shot['evidence']['windows'][0]['text']='palette_workflow.py'
        self.assertTrue(check(self.shot,self.palette)['pass'])


    def test_permission_blocker_cannot_pass_even_with_visible_result(self):
        self.shot.update(case='fzf-lua',text='palette_workflow.py')
        self.shot['evidence'].update(plugins=['fzf-lua'],
            windows=[{'filetype':'fzf','text':'palette_workflow.py'}],
            history=['[Fzf-lua] fzf error 2: operation not permitted'])
        result=check(self.shot,self.palette)
        self.assertEqual(result['status'],'blocked')
        self.assertFalse(result['pass'])
