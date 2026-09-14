vim.opt.rtp:prepend(vim.fn.getcwd())
local theme=require('ithilien')
local function snapshot()
 local result={}
 for name,_ in pairs(vim.api.nvim_get_hl(0,{})) do result[name]=vim.api.nvim_get_hl(0,{name=name,link=false}) end
 return result
end
theme.load('dawn')
local raw=require('ithilien.ithilien-dawn').raw
assert(not package.loaded["zenbones.specs"], "Dawn must not load Zenbones")
local expected=tonumber(raw.foregrounds.text:sub(2),16)
-- Plain selection fixes the user-confirmed partial V-line rendering regression.
-- Exact diff changes use ordinary weight with color-based emphasis.
for _,name in ipairs({'Visual','VisualNOS'}) do
 local h=vim.api.nvim_get_hl(0,{name=name,link=false})
 assert(h.bg==tonumber(raw.highlight.background:sub(2),16),name..' selection background')
 assert(h.fg==tonumber(raw.highlight.foreground:sub(2),16),name..' selection text')
 for _,key in ipairs({'underline','undercurl','underdouble','underdotted','underdashed','reverse','bold','italic','strikethrough'}) do
  assert(not h[key],name..' must be undecorated: '..key)
  assert(not (h.cterm and h.cterm[key]),name..' cterm must be undecorated: '..key)
 end
 assert(not h.sp,name..' must not set a decoration color')
end
local guides = {SnacksIndent=true, IblIndent=true, IndentBlanklineChar=true, NeoTreeIndentMarker=true}
local checked=0
for name,h in pairs(snapshot()) do
 assert(not h.reverse,'Reversed group: '..name)
 if h.fg and not guides[name] and name~='nvim_set_hl_x_hi_clear_bugfix' then
  local max=math.max(math.floor(h.fg/65536)%256,math.floor(h.fg/256)%256,h.fg%256)
  assert(max<190 or (h.fg==tonumber(raw.highlight.foreground:sub(2),16) and h.bg==tonumber(raw.highlight.background:sub(2),16)),'Unexpected light foreground: '..name)
 end
 checked=checked+1
end
for _,name in ipairs({'Normal','StatusLine','DiffText','DiffTextAdd'}) do
 assert(vim.api.nvim_get_hl(0,{name=name,link=false}).fg==expected,'Dark foreground role: '..name)
end
for _,name in ipairs({'DiffText','DiffTextAdd','GitSignsAddInline','GitSignsDeleteInline','GitSignsChangeInline'}) do
 local h=vim.api.nvim_get_hl(0,{name=name,link=false})
 assert(not h.bold and not h.underline and h.bg,'Missing inline cue: '..name)
end
for mode,sections in pairs(require('lualine.themes.ithilien-dawn')) do
 for section,h in pairs(sections) do assert(h.fg~=raw.backgrounds.base,'Reversed lualine '..mode..section) end
end
local dawn=snapshot()
theme.load('dawn')
for name,h in pairs(dawn) do assert(vim.deep_equal(h,vim.api.nvim_get_hl(0,{name=name,link=false})),'Dawn changed after reloading: '..name) end
local output = vim.env.ITHILIEN_CHECK_OUTPUT or 'tests/results/highlight-checks'
vim.fn.mkdir(output, 'p')
vim.fn.writefile({vim.json.encode({checked=checked,highlights=dawn,dawnReloadUnchanged=true})},output..'/highlights.json')
print(checked..' resolved highlights checked; interaction pair matches palette; Dawn reloading unchanged')
vim.cmd('qa!')
