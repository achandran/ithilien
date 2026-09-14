vim.opt.rtp:prepend(vim.fn.getcwd())
require('ithilien').load('dawn')
local function hl(n) return vim.api.nvim_get_hl(0,{name=n,link=false}) end
assert(hl('NeoTreeGitAdded').fg==0x315F46)
assert(hl('NeoTreeGitModified').fg==0x345E77)
assert(hl('NeoTreeGitDeleted').fg==0x8B3037)
assert(hl('NeoTreeGitStaged').fg==0x315F46 and hl('NeoTreeGitStaged').underline)
assert(hl('BufferLineWarningSelected').fg==0x795922)
assert(hl('BlinkCmpLabelMatch').bold and hl('BlinkCmpLabelMatch').fg==0)
assert(hl('BlinkCmpSignatureHelpActiveParameter').bg==0xD6C6DE)
assert(hl('SnacksIndent').fg==0xC9CECB)
assert(hl('SnacksIndentScope').fg==0x505456)
assert(hl('BufferLineBufferSelected').bg==0xDEE0DF)
assert(hl('DiffText').bg==0xD8B46A and not hl('DiffText').bold)
assert(hl('SnacksDashboardDesc').fg==0)
assert(hl('SnacksDashboardIcon').fg==0x345E77)
for _,name in ipairs({'SnacksDashboardFooter','SnacksDashboardSpecial'}) do
 assert(hl(name).fg==0x505456 and not hl(name).bold)
end
-- Reproduce Bufferline's cached default icon after a colorscheme reload.
local old_config=package.loaded['bufferline.config']
local parents={buffer_visible={bg='#E6E6E4'}}
package.loaded['bufferline.config']={get=function() return {highlights=parents} end}
vim.api.nvim_set_hl(0,'BufferLineMiniIconsRegressionInactive',{fg=0x70516D,bg=0xE6E6E4,default=true})
require('ithilien.plugin_palette').apply()
assert(hl('BufferLineMiniIconsRegressionInactive').bg==0xFAFAF8)
assert(parents.buffer_visible.bg=='#FAFAF8')
package.loaded['bufferline.config']=old_config
assert(hl('TodoFgTODO').fg~=hl('TodoBgTODO').bg)
assert(hl('TodoBgTODO').bg==0xDEE0DF)
assert(hl('FzfLuaFzfMatch').fg==0)
assert(hl('NeoTreeRootName_35').fg==0x505456)
local palette=vim.json.decode(table.concat(vim.fn.readfile('scripts/palette/ithilien.json'),'\n')).variants['ithilien-dawn'].colors
local allowed={}
for _,value in pairs(palette) do allowed[tonumber(value:sub(2),16)]=true end
local function audit()
 for name,h in pairs(vim.api.nvim_get_hl(0,{})) do
  for _,attr in ipairs({'fg','bg','sp'}) do
   assert(not h[attr] or allowed[h[attr]], name..'.'..attr..' is outside the palette')
  end
 end
end
audit()
-- Emulate plugins creating defaults after the theme has loaded.
for _,event in ipairs({'LazyLoad','VeryLazy'}) do
 vim.api.nvim_set_hl(0,'FzfLuaHeaderBind',{fg=0x00FA9A})
 vim.api.nvim_set_hl(0,'BufferLineFill',{bg=0xC8C8C6})
 vim.api.nvim_exec_autocmds('User',{pattern=event})
 assert(vim.wait(500,function() return hl('FzfLuaHeaderBind').fg==0x345E77 end))
 audit()
end
vim.cmd('colorscheme ithilien-dawn')
vim.wait(50)
audit()
assert(hl('FzfLuaBackdrop').blend==0)
-- Scheduled Dawn corrections must not recolor another active theme.
vim.g.colors_name='other-theme'
vim.api.nvim_set_hl(0,'FzfLuaHeaderBind',{fg=0x123456})
require('ithilien.plugin_palette').apply()
assert(hl('FzfLuaHeaderBind').fg==0x123456)
print('PASS: plugin semantics, palette membership, late loading, reload, and theme isolation')
vim.cmd('qa!')
