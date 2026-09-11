-- ZENBONES_ROOT, LUSH_ROOT and KANSO_ROOT point to dependency checkouts.
for _,key in ipairs({'ZENBONES_ROOT','LUSH_ROOT','KANSO_ROOT'}) do vim.opt.rtp:prepend(assert(vim.env[key])) end
vim.opt.rtp:prepend(vim.fn.getcwd())
local theme=require('ithilien')
local function snapshot()
 local result={}
 for name,_ in pairs(vim.api.nvim_get_hl(0,{})) do result[name]=vim.api.nvim_get_hl(0,{name=name,link=false}) end
 return result
end
theme.load('dusk')
local dusk=snapshot()
theme.load('dawn')
local raw=require('ithilien.ithilien-dawn').raw
local expected=tonumber(raw.foregrounds.text:sub(2),16)
local checked=0
for name,h in pairs(snapshot()) do
 assert(not h.reverse,'Reversed group: '..name)
 if h.fg and name~='nvim_set_hl_x_hi_clear_bugfix' then
  local max=math.max(math.floor(h.fg/65536)%256,math.floor(h.fg/256)%256,h.fg%256)
  assert(max<190,'Light foreground: '..name)
 end
 checked=checked+1
end
for _,name in ipairs({'Normal','Visual','PmenuSel','StatusLine','DiffText','DiffTextAdd'}) do
 assert(vim.api.nvim_get_hl(0,{name=name,link=false}).fg==expected,'Dark foreground role: '..name)
end
for _,name in ipairs({'DiffText','DiffTextAdd','GitSignsAddInline','GitSignsDeleteInline','GitSignsChangeInline'}) do
 local h=vim.api.nvim_get_hl(0,{name=name,link=false})
 assert(h.bold and h.underline and h.bg,'Missing inline cue: '..name)
end
for mode,sections in pairs(require('lualine.themes.ithilien-dawn')) do
 for section,h in pairs(sections) do assert(h.fg~=raw.backgrounds.base,'Reversed lualine '..mode..section) end
end
local dawn=snapshot()
theme.load('dusk')
for name,h in pairs(dusk) do assert(vim.deep_equal(h,vim.api.nvim_get_hl(0,{name=name,link=false})),'Dusk changed after switching: '..name) end
vim.fn.writefile({vim.json.encode({checked=checked,highlights=dawn,duskSwitchUnchanged=true})},'reports/formex-dawn-highlights.json')
print(checked..' resolved highlights checked; no reversed/light foregrounds; Dusk switching unchanged')
vim.cmd('qa!')
