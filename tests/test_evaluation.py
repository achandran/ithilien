import hashlib
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class EvaluationCorpus(unittest.TestCase):
    def test_pinned_sources_are_intact(self):
        sources=json.loads((ROOT/'evaluation/sources.json').read_text())
        for source in sources.values():
            self.assertRegex(source['revision'],r'^[0-9a-f]{40}$')
            for item in source['files']:
                self.assertEqual(hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest(),item['sha256'])
    def test_cases_have_real_edits_and_local_paths(self):
        for case in json.loads((ROOT/'evaluation/cases.json').read_text()):
            paths=[(ROOT/'evaluation'/case[k]).resolve() for k in ('before','after')]
            for path in paths:self.assertTrue(path.is_relative_to(ROOT/'evaluation'))
            self.assertNotEqual(paths[0].read_bytes(),paths[1].read_bytes())

class NativeStateChecks(unittest.TestCase):
    def test_missing_or_recolored_selection_fails(self):
        import sys
        sys.path.insert(0,str(ROOT/'scripts'))
        from evaluation_checks import state_failures
        from ithilienlib import load_palette
        palette=load_palette('ithilien-dawn')
        shot={'case':'mutation','state':'selection','attrs':{},'defaults':{'fg':0,'bg':0xffffff},'cells':[{'text':'x','attr':0}]}
        self.assertTrue(state_failures(shot,palette))
        shot['attrs'][0]={'background':int(palette['highlight']['background'][1:],16)}
        self.assertFalse(state_failures(shot,palette))
        shot['cells'][0]['text']=' '
        self.assertFalse(state_failures(shot,palette))
        shot['attrs'][0]['background']=0xffffff
        self.assertTrue(state_failures(shot,palette))

class CodexColorResolution(unittest.TestCase):
    def test_native_color_depths(self):
        import sys
        sys.path.insert(0,str(ROOT/'scripts'))
        from codex_native import color
        from ithilienlib import load_palette
        p=load_palette('ithilien-dawn')
        self.assertEqual(color('Rgb(0, 95, 255)',p,'#000000'),'#005FFF')
        self.assertEqual(color('Indexed(196)',p,'#000000'),'#FF0000')
        self.assertEqual(color('Indexed(232)',p,'#000000'),'#080808')
        self.assertEqual(color('Red',p,'#000000'),p['ansi']['red'])
        with self.assertRaises(ValueError):color('Unrecognized',p,'#000000')

class PythonCoverage(unittest.TestCase):
    def test_python_syntax_corpus_is_valid_and_varied(self):
        import ast
        cases=json.loads((ROOT/'evaluation/cases.json').read_text())
        python_cases=[c for c in cases if c.get('require_syntax')]
        self.assertGreaterEqual(len(python_cases),3)
        kinds=set()
        for case in python_cases:
            for side in ('before','after'):
                tree=ast.parse((ROOT/'evaluation'/case[side]).read_text())
                kinds.update(type(node).__name__ for node in ast.walk(tree))
        self.assertTrue({'AsyncFunctionDef','AsyncWith','Await','ClassDef','AnnAssign','JoinedStr','ListComp','DictComp','Match','Try','Raise','Lambda'} <= kinds)

    def test_disabled_python_syntax_is_detected(self):
        import sys
        sys.path.insert(0,str(ROOT/'scripts'))
        from evaluation_checks import state_failures
        from ithilienlib import load_palette
        shot={'case':'python','state':'diff','require_syntax':True,'syntax_groups':[]}
        self.assertTrue(state_failures(shot,load_palette('ithilien-dawn')))
        shot['syntax_groups']=['pythonStatement','pythonString','pythonComment']
        self.assertFalse(state_failures(shot,load_palette('ithilien-dawn')))
