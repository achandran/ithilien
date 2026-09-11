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
