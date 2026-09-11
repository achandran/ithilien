-- KANSO_ROOT=../kanso GITSIGNS_ROOT=/path/to/gitsigns.nvim nvim --headless -u NONE -i NONE -l scripts/check_gitsigns.lua
vim.opt.rtp:prepend(assert(vim.env.KANSO_ROOT, 'Set KANSO_ROOT'))
vim.opt.rtp:prepend(assert(vim.env.GITSIGNS_ROOT, 'Set GITSIGNS_ROOT'))
vim.opt.rtp:prepend(vim.fn.getcwd())
local p = require('ithilien.ithilien-dawn').raw
local function rgb(s) return tonumber(s:sub(2),16) end
local function check()
  for kind,color in pairs({Add=p.ansi.green,Change=p.ansi.blue,Delete=p.ansi.red,
      Changedelete=p.ansi.blue,Topdelete=p.ansi.red,Untracked=p.ansi.green}) do
    for _,suffix in ipairs({'','Nr','Cul'}) do
      for _,staged in ipairs({false,true}) do
        local name='GitSigns'..(staged and 'Staged' or '')..kind..suffix
        local h=vim.api.nvim_get_hl(0,{name=name,link=false})
        assert(h.fg==rgb(color),name..': lost semantic foreground')
        assert((h.underline==true)==staged,name..': lost stage distinction')
      end
    end
  end
  for _,kind in ipairs({'Add','Change','Delete'}) do
    local h=vim.api.nvim_get_hl(0,{name='GitSigns'..kind..'Inline',link=false})
    assert(h.bg==rgb(p.diff.changeEmphasis) and h.fg==0 and not h.underline and not h.bold)
  end
  local h=vim.api.nvim_get_hl(0,{name='GitSignsStagedChangedeleteLn',link=false})
  assert(h.bg==rgb(p.diff.changeBackground) and h.fg==0 and not h.underline)
end
require('ithilien').load('dawn')
local gs=require('gitsigns.highlight')
check()
-- Plugin already loaded when switching back to Dawn; fallback creation runs again.
require('ithilien').load('dawn')
gs.setup_highlights()
check()
print('PASS: sign colors, staged cues, combined signs, plain inline spans, both load orders')
vim.cmd('qa!')
