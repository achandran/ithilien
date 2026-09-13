vim.opt.rtp:prepend(assert(vim.env.KANSO_ROOT))
vim.opt.rtp:prepend(vim.fn.getcwd())
local theme = require('ithilien')
local function get(name) return vim.api.nvim_get_hl(0, {name=name,link=false}) end
local function hex(value) return tonumber(value:sub(2),16) end
local function check()
  local p = require('ithilien.ithilien-dusk').raw
  assert(vim.o.background == 'dark')
  assert(get('Normal').bg == hex(p.backgrounds.base))
  assert(get('Normal').fg == hex(p.foregrounds.text))
  for _,name in ipairs({'Identifier','Function','Type','Statement','Number','Boolean','Constant',
    '@type.builtin','@keyword.function'}) do
    assert(get(name).fg == hex(p.foregrounds.text), name .. ' must stay neutral')
  end
  assert(get('String').fg == hex(p.foregrounds.comment))
  for name,color in pairs({DiagnosticError=p.ansi.red, DiagnosticWarn=p.ansi.yellow,
    DiagnosticInfo=p.ansi.blue, DiagnosticHint=p.ansi.cyan, DiagnosticOk=p.ansi.green}) do
    assert(get(name).fg == hex(color), name .. ' must retain its accent')
  end
  for _,name in ipairs({'Visual','VisualNOS','PmenuSel','FzfLuaCursorLine'}) do
    local h = get(name)
    assert(h.fg == 0 and h.bg == hex(p.highlight.background), name)
  end
  for _,name in ipairs({'Search','IncSearch','CurSearch','FzfLuaSearch','LspSignatureActiveParameter'}) do
    local h = get(name)
    assert(h.fg == 0 and h.bg == hex(p.backgrounds.search), name)
  end
  for _,name in ipairs({'DiffText','DiffTextAdd','GitSignsAddInline','GitSignsChangeInline',
    'GitSignsDeleteInline','NeogitDiffAddInline','NeogitDiffDeleteInline'}) do
    local h = get(name)
    assert(h.fg == 0 and h.bg == hex(p.diff.changeEmphasis), name)
    assert(not h.bold and not h.underline and not h.reverse, name .. ' decorated')
  end
  for _,name in ipairs({'visual','replace'}) do
    assert(require('lualine.themes.ithilien-dusk')[name].a.fg == '#000000')
  end
end
theme.load('dusk')
check()
local first = get('Normal')
theme.load('dawn')
assert(get('Normal').fg == 0)
theme.load('dusk')
check()
assert(vim.deep_equal(first,get('Normal')))
theme.setup({bold=false, italics=false})
theme.load('dusk')
check()
for _,name in ipairs({'Type','Statement'}) do assert(not get(name).bold, name) end
assert(not get('Comment').italic)
print('Dusk neutral syntax, diagnostics, interactions, style options, and Dawn/Dusk switching pass')
vim.cmd('qa!')
