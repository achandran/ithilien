"""Native compatibility checks against the pre-removal theme."""
import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / 'tests/fixtures/neovim-highlight-baseline.json').read_text())


@pytest.mark.parametrize('variant', ['dawn', 'dusk'])
@pytest.mark.parametrize('bold,italics', [(False, False), (False, True), (True, False), (True, True)])
def test_standalone_highlights_and_switching(tmp_path, variant, bold, italics):
    nvim = shutil.which('nvim')
    if not nvim:
        pytest.skip('Native highlight checks require Neovim')
    expected = BASELINE['variants'][f'{variant}-{int(bold)}-{int(italics)}']
    inputs = tmp_path / 'inputs.json'
    inputs.write_text(json.dumps(dict(root=str(ROOT), variant=variant, bold=bold,
                                     italics=italics, expected=expected)))
    script = tmp_path / 'standalone.lua'
    script.write_text('''
local input = vim.json.decode(table.concat(vim.fn.readfile(vim.env.ITHILIEN_TEST_INPUT)))
vim.opt.rtp:prepend(input.root)
-- Theme loading may only import Ithilien and Neovim modules.
table.insert(package.loaders, 1, function(name)
  assert(name == 'ithilien' or name:match('^ithilien%.') or name:match('^vim%.'),
    'Unexpected dependency: ' .. name)
end)
-- A loaded statusline keeps its own components and configuration on every load.
package.loaded.lualine = {
  get_config = function() error('Colorscheme must not read lualine configuration') end,
  setup = function() error('Colorscheme must not replace lualine components') end,
}
local theme = require('ithilien')
theme.setup({bold=input.bold, italics=input.italics})
local function check()
  vim.wait(10)
  assert(vim.g.colors_name == 'ithilien-' .. input.variant)
  assert(vim.o.termguicolors)
  for name, expected in pairs(input.expected.highlights) do
    local actual = vim.api.nvim_get_hl(0, {name=name})
    actual.default = nil
    assert(vim.deep_equal(actual, expected), name .. ': ' .. vim.inspect(actual))
  end
  for index, color in pairs(input.expected.terminal) do
    assert(vim.g['terminal_color_' .. index] == color, 'Terminal color ' .. index)
  end
end
vim.cmd.colorscheme('ithilien-' .. input.variant)
check()
local diff_count = #vim.api.nvim_get_autocmds({group='IthilienDiff'})
for _=1,2 do
  vim.cmd.colorscheme(input.variant == 'dawn' and 'ithilien-dusk' or 'ithilien-dawn')
  vim.cmd.colorscheme('ithilien-' .. input.variant)
  check()
  assert(#vim.api.nvim_get_autocmds({group='IthilienDiff'}) == diff_count)
end
-- An unrelated colorscheme keeps ownership after pending callbacks run.
vim.cmd.colorscheme('default')
local normal = vim.api.nvim_get_hl(0, {name='Normal', link=false})
vim.wait(20)
assert(vim.g.colors_name == 'default')
assert(vim.deep_equal(normal, vim.api.nvim_get_hl(0, {name='Normal', link=false})))
''')
    result = subprocess.run(
        [nvim, '--headless', '-u', 'NONE', '-i', 'NONE', '-n', '-l', str(script)],
        cwd=ROOT, env={**os.environ, 'ITHILIEN_TEST_INPUT': str(inputs),
                       'XDG_STATE_HOME': str(tmp_path / 'state'),
                       'XDG_CACHE_HOME': str(tmp_path / 'cache')},
        capture_output=True, text=True, timeout=20,
    )
    assert result.returncode == 0, result.stdout + result.stderr
