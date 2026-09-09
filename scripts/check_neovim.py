"""Audit resolved highlights with a real Kanso checkout; optionally compare Night.

Usage: python scripts/check_neovim.py /path/to/kanso.nvim [--baseline /path/to/old/loden]
"""
import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path
from lodenlib import ROOT, wcag

LUA = '''
vim.opt.rtp:prepend(vim.env.KANSO_ROOT)
vim.opt.rtp:prepend(vim.env.LODEN_ROOT)
require('loden').load(vim.env.LODEN_VARIANT)
if vim.env.LODEN_SWITCH_CHECK == '1' then
  local before = {}
  for name,_ in pairs(vim.api.nvim_get_hl(0, {})) do
    before[name] = vim.api.nvim_get_hl(0, {name=name,link=false})
  end
  local loden = require('loden')
  loden.setup({bold=false,italics=false})
  loden.load('day')
  for _,group in ipairs({'@keyword.return.python','@keyword.exception.python','@string.documentation.python'}) do
    local h = vim.api.nvim_get_hl(0, {name=group,link=false})
    assert(not h.bold and not h.italic, 'Python typography options: '..group)
  end
  loden.setup({bold=true,italics=true})
  loden.load('night')
  for name,h in pairs(before) do
    assert(vim.deep_equal(h, vim.api.nvim_get_hl(0, {name=name,link=false})), 'Night after switching: '..name)
  end
  for _,group in ipairs({'@keyword.return','@keyword.exception','@constant.builtin','@string.documentation'}) do
    assert(vim.deep_equal(vim.api.nvim_get_hl(0, {name=group..'.python',link=false}),
                         vim.api.nvim_get_hl(0, {name=group,link=false})), 'Day override leaked into Night: '..group)
  end
end
local resolved = {}
for name,_ in pairs(vim.api.nvim_get_hl(0, {})) do
  resolved[name] = vim.api.nvim_get_hl(0, {name=name,link=false})
end
vim.fn.writefile({vim.json.encode(resolved)}, vim.env.LODEN_OUTPUT)
vim.cmd('qa!')
'''
# These are deliberately invisible helper glyphs / Neovim error sentinels, not text.
EXCLUDED = {'@markup.heading.1.delimiter.vimdoc', '@markup.heading.2.delimiter.vimdoc',
            'SnacksPickerCursor', 'NvimFigureBrace', 'NvimInternalError',
            'NvimInvalidSingleQuotedUnknownEscape', 'NvimSingleQuotedUnknownEscape'}
DECORATIVE = {'@ibl.indent.char.1', '@ibl.scope.char.1', '@ibl.whitespace.char.1',
              'Indent', 'IndentBlanklineContextChar', 'IndentGuide', 'IndentGuidesEven',
              'IndentGuidesOdd', 'IndentLine', 'SnacksIndent', 'SnacksIndentChunk',
              'SnacksIndentScope', 'TroubleIndent', 'Whitespace', 'IndentBlanklineChar',
              'IndentBlanklineSpaceChar', 'IndentBlanklineSpaceCharBlankline',
              'IblIndent', 'IblWhitespace', 'IblScope', 'EndOfBuffer'}

def capture(root, kanso, variant, temp, switch_check=False):
    script = temp / 'capture.lua'
    script.write_text(LUA)
    output = temp / 'highlights.json'
    env = dict(os.environ, KANSO_ROOT=str(kanso), LODEN_ROOT=str(root),
               LODEN_VARIANT=variant, LODEN_OUTPUT=str(output), LODEN_SWITCH_CHECK='1' if switch_check else '0')
    subprocess.run(['nvim','--headless','-u','NONE','-i','NONE','-l',str(script)], env=env, check=True)
    return json.loads(output.read_text())

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kanso', type=Path)
    parser.add_argument('--baseline', type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        h = capture(ROOT,args.kanso.resolve(),'day',temp)
        for name in ('GitSignsAddInline', 'GitSignsDeleteInline', 'GitSignsChangeInline',
                     'GitSignsAddLnInline', 'GitSignsDeleteLnInline', 'GitSignsChangeLnInline'):
            assert h[name]['fg'] == 0 and h[name].get('underline'), name
        assert h['DiffText']['fg'] == 0
        assert h['DiffText'].get('underline')
        assert h['DiffTextAdd']['fg'] == 0 and h['DiffTextAdd'].get('underline')
        assert h['CursorLineNr']['fg'] == 0 and h['CursorLineNr'].get('bold')
        assert h['LineNr'] != h['CursorLineNr']
        assert h['StatusLine'] != h['StatusLineNC']
        assert h['DiagnosticUnderlineInfo'].get('underline')
        assert h['DiagnosticUnderlineHint'].get('underdotted')
        checks = []
        base = h['Normal']['bg']
        for name, c in sorted(h.items()):
            if 'fg' not in c or name in EXCLUDED:
                continue
            # Resolved explicit pairs, otherwise editor canvas. Float and cursor-line
            # overlays are covered by the canonical palette surface matrix.
            fg, bg = c['fg'], c.get('bg',base)
            floor = 3 if any(word in name for word in ('Border','Separator')) else 4.5
            # Decorative whitespace/indent marks are not informational text.
            if name in DECORATIVE:
                continue
            ratio = wcag(f'#{fg:06X}', f'#{bg:06X}')
            checks.append(dict(group=name, foreground=f'#{fg:06X}',background=f'#{bg:06X}',
                               ratio=round(ratio,3),target=floor,passed=ratio>=floor))
        failures = [c for c in checks if not c['passed']]
        night_equal = None
        if args.baseline:
            night_equal = capture(ROOT,args.kanso.resolve(),'night',temp) == capture(args.baseline.resolve(),args.kanso.resolve(),'night',temp)
            assert night_equal, 'Night resolved highlights changed'
        capture(ROOT, args.kanso.resolve(), 'night', temp, switch_check=True)
        report = dict(kansoCommit=subprocess.check_output(['git','-C',str(args.kanso),'rev-parse','HEAD'],text=True).strip(),
                      passed=not failures,nightIdentical=night_equal,nightSwitchIdentical=True,checks=checks,excluded=sorted(EXCLUDED),decorative=sorted(DECORATIVE))
        (ROOT/'reports/day-review/neovim.json').write_text(json.dumps(report,indent=2)+'\n')
        print(f'{len(checks)} resolved highlight checks; {len(failures)} failures; Night identical: {night_equal}; Night switching: PASS')
        for c in failures: print(c)
        assert not failures

if __name__ == '__main__': main()
