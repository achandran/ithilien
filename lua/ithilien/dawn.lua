local M = {}
function M.load(opts)
vim.g.colors_name = nil
vim.o.background = 'light'
vim.cmd('highlight clear')
vim.g.colors_name = 'ithilien-dawn'
local lush = require('lush')
local util = require('zenbones.util')
local generator = require('zenbones.specs')
local mode = 'light'
local raw = require('ithilien.ithilien-dawn').raw
local bg, fg, a, d = raw.backgrounds, raw.foregrounds, raw.accents, raw.diff
local p = { bg=bg.base, surface=bg.mantle, line=bg.surface1, raised=bg.surface0,
 fg=fg.text, muted=fg.comment, border=bg.border, selection=raw.highlight.background,
 red=a.coral, green=raw.ansi.brightGreen, yellow=raw.ansi.brightYellow, blue=a.blue,
 magenta=a.mauve, cyan=a.aqua, add=d.addBackground, add_emph=d.addEmphasis,
 delete=d.deleteBackground, delete_emph=d.deleteEmphasis, change=d.changeBackground,
 change_emph=d.changeEmphasis, search=bg.search,
 ansi=require('ithilien.ithilien-dawn').terminal }
local palette = util.palette_extend({
  bg = lush.hsluv(p.bg), fg = lush.hsluv(p.fg),
  rose = lush.hsluv(p.red), leaf = lush.hsluv(p.green),
  wood = lush.hsluv(p.yellow), water = lush.hsluv(p.blue),
  blossom = lush.hsluv(p.magenta), sky = lush.hsluv(p.cyan),
}, mode)
local config = {italic_comments=opts.italics, italic_strings=false}
lush(generator.generate(palette, mode, config))
local function hi(name, spec) vim.api.nvim_set_hl(0, name, spec) end
local groups = {
  Cursor={fg=p.fg,bg=raw.highlight.cursorBlock,sp=raw.highlight.cursor,underline=true},
  lCursor={fg=p.fg,bg=raw.highlight.cursorBlock,sp=raw.highlight.cursor,underline=true},
  Normal = {fg=p.fg,bg=p.bg}, NormalNC={fg=p.fg,bg=p.bg},
  NormalFloat={fg=p.fg,bg=p.raised}, FloatBorder={fg=p.border,bg=p.raised},
  Comment={fg=p.muted,italic=config.italic_comments == true},
  String={fg=p.muted,italic=config.italic_strings == true},
  Delimiter={fg=p.fg}, SpecialComment={fg=p.muted},
  FlashBackdrop={fg=p.muted},HopUnmatched={fg=p.muted},ComplHint={fg=p.muted},
  CmpItemAbbrDeprecated={fg=p.muted,strikethrough=true},
  Identifier={fg=p.fg}, Function={fg=p.fg}, Type={fg=p.fg,bold=true},
  Statement={fg=p.fg,bold=true}, Special={fg=p.blue}, Constant={fg=p.fg},
  LineNr={fg=p.muted}, CursorLineNr={fg=p.fg,bold=true}, CursorLine={bg=p.line},
  SignColumn={bg=p.bg}, NonText={fg=p.border}, Whitespace={fg=p.border},
  WinSeparator={fg=p.border}, Visual={fg=p.fg,bg=p.selection,sp=raw.highlight.border,underline=true},
  Search={fg=p.fg,bg=p.search}, IncSearch={fg=p.fg,bg=p.search,bold=true,underline=true},
  CurSearch={fg=p.fg,bg=p.search,bold=true,underline=true},
  MatchParen={fg=p.fg,bg=p.selection,bold=true,underline=true},
  StatusLine={fg=p.fg,bg=p.surface},StatusLineNC={fg=p.muted,bg=p.surface},
  Pmenu={fg=p.fg,bg=p.raised},PmenuSel={fg=p.fg,bg=p.selection,bold=true},
  Folded={fg=p.muted,bg=p.surface},
  DiffAdd={fg=p.fg,bg=p.add},DiffDelete={fg=p.fg,bg=p.delete},
  DiffChange={fg=p.fg,bg=p.change},DiffText={fg=p.fg,bg=p.change_emph,bold=true,underline=true},
  DiffTextAdd={link='DiffText'},
  GitSignsAdd={fg=p.green},GitSignsChange={fg=p.blue},GitSignsDelete={fg=p.red},
  GitSignsAddLn={fg=p.fg,bg=p.add},GitSignsChangeLn={fg=p.fg,bg=p.change},
  GitSignsDeleteLn={fg=p.fg,bg=p.delete},
  GitSignsAddInline={fg=p.fg,bg=p.add_emph,bold=true,underline=true},
  GitSignsChangeInline={fg=p.fg,bg=p.change_emph,bold=true,underline=true},
  GitSignsDeleteInline={fg=p.fg,bg=p.delete_emph,bold=true,underline=true},
  GitSignsAddPreview={fg=p.fg,bg=p.add},GitSignsDeletePreview={fg=p.fg,bg=p.delete},
  diffAdded={fg=p.fg,bg=p.add},diffRemoved={fg=p.fg,bg=p.delete},
  diffChanged={fg=p.fg,bg=p.change},diffFile={fg=p.fg,bold=true},diffLine={fg=p.blue},
  DiagnosticUnnecessary={fg=p.muted,underline=true},
}
for group, spec in pairs(groups) do hi(group,spec) end
for _,kind in ipairs({'Add','Change','Delete'}) do
  hi('GitSigns'..kind..'LnInline',{link='GitSigns'..kind..'Inline'})
end
for suffix, color in pairs({Error=p.red,Warn=p.yellow,Info=p.blue,Hint=p.cyan,Ok=p.green}) do
  hi('Diagnostic'..suffix,{fg=color})
  hi('DiagnosticSign'..suffix,{fg=color})
  hi('DiagnosticVirtualText'..suffix,{fg=color})
  hi('DiagnosticUnderline'..suffix,{sp=color,undercurl=true})
end
for group, target in pairs({['@diff.plus']='diffAdded',['@diff.minus']='diffRemoved',['@diff.delta']='diffChanged',
  ['@markup.heading']='Title',['@markup.link.url']='Underlined'}) do hi(group,{link=target}) end
hi('Title',{fg=p.fg,bold=true})
hi('Underlined',{fg=p.blue,underline=true})
for i,color in ipairs(p.ansi) do vim.g['terminal_color_'..(i-1)]=color end

-- Zenbones' broad plugin inventory includes reversed labels. Dawn never uses
-- light foregrounds on dark surfaces: normalize inherited reverse groups and
-- pale foregrounds, while retaining explicit dark semantic colors.
local function luminance(hex)
 local function ch(n) n=n/255; return n<=0.04045 and n/12.92 or ((n+0.055)/1.055)^2.4 end
 return .2126*ch(math.floor(hex/65536)%256)+.7152*ch(math.floor(hex/256)%256)+.0722*ch(hex%256)
end
for name,h in pairs(vim.api.nvim_get_hl(0,{})) do
 if not h.link then
  if h.reverse or (h.fg and luminance(h.fg)>.3) or (h.bg and luminance(h.bg)<.3) then
   h.reverse=nil; h.fg=tonumber(p.fg:sub(2),16)
   if h.bg then h.bg=tonumber(p.surface:sub(2),16) end
   hi(name,h)
  end
 end
end
for _,name in ipairs({'Type','Statement','Title','CursorLineNr'}) do
 local h=vim.api.nvim_get_hl(0,{name=name,link=false}); h.bold=opts.bold;hi(name,h)
end
local lualine=package.loaded['lualine']
if lualine then local c=lualine.get_config();c.options.theme='ithilien-dawn';lualine.setup(c) end

end
return M
