local M = {}
function M.load(opts)
vim.g.colors_name = nil
vim.o.background = 'light'
vim.cmd('highlight clear')
vim.g.colors_name = 'ithilien-dawn'
local raw = require('ithilien.ithilien-dawn').raw
local bg, fg, a, d = raw.backgrounds, raw.foregrounds, raw.accents, raw.diff
local p = { bg=bg.base, surface=bg.mantle, line=bg.surface1, raised=bg.surface0,
 fg=fg.text, muted=fg.comment, border=bg.border, selection=raw.highlight.background,
 red=a.coral, green=raw.ansi.brightGreen, yellow=raw.ansi.brightYellow, blue=a.blue,
 magenta=a.mauve, cyan=a.aqua, add=d.addBackground, add_emph=d.addEmphasis,
 delete=d.deleteBackground, delete_emph=d.deleteEmphasis, change=d.changeBackground,
 change_emph=d.changeEmphasis, search=bg.search,
 ansi=require('ithilien.ithilien-dawn').terminal }
local palette = require('ithilien.ithilien-dawn')
local accent, diff, highlight, is_light = a, d, raw.highlight, true
  local theme = {
    ui = {
      none = "NONE",
      fg = fg.text,
      fg_dim = fg.subtext,
      fg_reverse = bg.base,
      bg_dim = bg.mantle,
      bg_m3 = bg.crust,
      bg_m2 = bg.mantle,
      bg_m1 = bg.surface0,
      bg = bg.base,
      bg_p1 = bg.surface0,
      bg_p2 = bg.surface1,
      special = is_light and fg.subtext or fg.muted,
      indent_line = bg.surface1,
      active_indent_line = bg.surface2,
      whitespace = bg.surface2,
      nontext = fg.muted,
      bg_visual = highlight.background,
      bg_search = diff.changeEmphasis,
      cursor_line_nr_foreground = fg.muted,
      cursor_line_nr_active_foreground = fg.bright,
      cursor_bg = highlight.background,
      cursor_fg = highlight.foreground,
      pmenu = {
        fg = fg.text,
        fg_sel = highlight.foreground,
        bg = bg.surface0,
        bg_sel = highlight.background,
        bg_thumb = bg.surface2,
        bg_sbar = bg.surface0,
      },
      float = {
        fg = fg.text,
        bg = bg.surface0,
        fg_border = is_light and fg.muted or bg.surface2,
        bg_border = bg.surface0,
      },
    },
    syn = {
      string = accent.sage,
      variable = "NONE",
      number = accent.ochre,
      constant = accent.ochre,
      identifier = accent.mauve,
      parameter = fg.subtext,
      fun = accent.gold,
      statement = accent.clay,
      keyword = accent.clay,
      operator = accent.olive,
      preproc = accent.mauve,
      type = accent.aqua,
      regex = accent.coral,
      deprecated = fg.muted,
      comment = fg.comment,
      punct = fg.subtext,
      special1 = accent.gold,
      special2 = accent.mauve,
      special3 = accent.blue,
    },
    diag = {
      error = accent.coral,
      ok = accent.sage,
      warning = p.yellow,
      info = accent.blue,
      hint = accent.aqua,
    },
    diff = {
      add = diff.addBackground,
      delete = diff.deleteBackground,
      change = diff.changeBackground,
      text = diff.changeEmphasis,
    },
    vcs = {
      added = p.green,
      removed = p.red,
      changed = p.blue,
      untracked = fg.comment,
    },
    term = palette.terminal,
  }


local config = {italic_comments=opts.italics, italic_strings=false}
require('ithilien.highlights').apply(theme, opts)
vim.g.colors_name='ithilien-dawn'
local function hi(name, spec) vim.api.nvim_set_hl(0, name, spec) end
local groups = {
  Cursor={fg=raw.highlight.foreground,bg=raw.highlight.cursorBlock,sp=raw.highlight.cursor,underline=true},
  lCursor={fg=raw.highlight.foreground,bg=raw.highlight.cursorBlock,sp=raw.highlight.cursor,underline=true},
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
  WinSeparator={fg=p.border}, Visual={fg=raw.highlight.foreground,bg=p.selection},
  VisualNOS={link="Visual"},
  Search={fg=p.fg,bg=p.search}, IncSearch={fg=p.fg,bg=p.search,bold=true,underline=true},
  CurSearch={fg=p.fg,bg=p.search,bold=true,underline=true},
  MatchParen={fg=raw.highlight.foreground,bg=p.selection,bold=true,underline=true},
  StatusLine={fg=p.fg,bg=p.surface},StatusLineNC={fg=p.muted,bg=p.surface},
  Pmenu={fg=p.fg,bg=p.raised},PmenuSel={fg=raw.highlight.foreground,bg=p.selection,bold=true},
  PmenuKindSel={fg=raw.highlight.foreground,bg=p.selection},PmenuExtraSel={fg=raw.highlight.foreground,bg=p.selection},
  Folded={fg=p.muted,bg=p.surface},
  DiffAdd={fg=p.fg,bg=p.add},DiffDelete={fg=p.fg,bg=p.delete},IthilienDiffFiller={fg=p.border,bg=p.delete},
  DiffChange={fg=p.fg,bg=p.change},DiffText={fg=p.fg,bg=p.change_emph},
  DiffTextAdd={link='DiffText'},
  GitSignsAdd={fg=p.green},GitSignsChange={fg=p.blue},GitSignsDelete={fg=p.red},
  GitSignsAddLn={fg=p.fg,bg=p.add},GitSignsChangeLn={fg=p.fg,bg=p.change},
  GitSignsDeleteLn={fg=p.fg,bg=p.delete},
  GitSignsAddInline={fg=p.fg,bg=p.add_emph},
  GitSignsChangeInline={fg=p.fg,bg=p.change_emph},
  GitSignsDeleteInline={fg=p.fg,bg=p.delete_emph},
  GitSignsAddPreview={fg=p.fg,bg=p.add},GitSignsDeletePreview={fg=p.fg,bg=p.delete},
  diffAdded={fg=p.fg,bg=p.add},diffRemoved={fg=p.fg,bg=p.delete},
  diffChanged={fg=p.fg,bg=p.change},diffFile={fg=p.fg,bold=true},diffLine={fg=p.blue},
  DiagnosticUnnecessary={fg=p.muted,underline=true},
}
for group, spec in pairs(groups) do hi(group,spec) end
-- Structural/plugin defaults need readable Dawn foregrounds.
for _,name in ipairs({'NvimTreeWinSeparator','NeoTreeIndentMarker','CmpDocumentationBorder',
 'BlinkCmpDocBorder','BlinkCmpSignatureHelpBorder','MiniClueBorder','MiniNotifyBorder',
 'MiniPickBorder','MiniFilesBorder','LspInlayHint','Ignore'}) do
 local h=vim.api.nvim_get_hl(0,{name=name,link=false}); h.fg=tonumber(p.muted:sub(2),16); hi(name,h)
end
-- Explicit sign families avoid inherited black combined signs and Gitsigns'
-- faded staged colors. Underline marks staging without reducing contrast.
for kind, color in pairs({Add=p.green,Change=p.blue,Delete=p.red,
 Changedelete=p.blue,Topdelete=p.red,Untracked=p.green}) do
  for _,suffix in ipairs({'','Nr','Cul'}) do
    hi('GitSigns'..kind..suffix,{fg=color})
    hi('GitSignsStaged'..kind..suffix,{fg=color,underline=true})
  end
  local line = ({Add=p.add,Change=p.change,Changedelete=p.change,Untracked=p.add})[kind]
  if line then
    hi('GitSigns'..kind..'Ln',{fg=p.fg,bg=line})
    hi('GitSignsStaged'..kind..'Ln',{fg=p.fg,bg=line})
  end
end
for _,kind in ipairs({'Add','Change','Delete'}) do
  hi('GitSigns'..kind..'LnInline',{link='GitSigns'..kind..'Inline'})
  hi('GitSigns'..kind..'VirtLnInline',{link='GitSigns'..kind..'Inline'})
end
-- Older Gitsigns releases used this capitalization for deleted virtual spans.
hi('GitSignsDeleteVirtLnInLine',{link='GitSignsDeleteInline'})
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

-- The plugin inventory includes reversed labels. Dawn never uses
-- light foregrounds except explicit palette interaction pairs: normalize reverse groups and
-- pale foregrounds, while retaining explicit dark semantic colors.
local function luminance(hex)
 local function ch(n) n=n/255; return n<=0.04045 and n/12.92 or ((n+0.055)/1.055)^2.4 end
 return .2126*ch(math.floor(hex/65536)%256)+.7152*ch(math.floor(hex/256)%256)+.0722*ch(hex%256)
end
for name,h in pairs(vim.api.nvim_get_hl(0,{})) do
 if not h.link then
  local interaction = h.fg==tonumber(raw.highlight.foreground:sub(2),16) and h.bg==tonumber(raw.highlight.background:sub(2),16)
  if not interaction and (h.reverse or (h.fg and luminance(h.fg)>.3) or (h.bg and luminance(h.bg)<.3)) then
   h.reverse=nil; h.fg=tonumber(p.fg:sub(2),16)
   if h.bg then h.bg=tonumber(p.surface:sub(2),16) end
   hi(name,h)
  end
 end
end
for _,name in ipairs({'Type','Statement','Title','CursorLineNr'}) do
 local h=vim.api.nvim_get_hl(0,{name=name,link=false}); h.bold=opts.bold;hi(name,h)
end
-- Deliberate plugin semantics, applied after the generic foreground safeguard.
for _,name in ipairs({'SnacksIndent','IblIndent','IndentBlanklineChar'}) do
 hi(name,{fg=bg.surface2,nocombine=true})
end
for _,name in ipairs({'SnacksIndentScope','SnacksIndentChunk','IblScope','MiniIndentscopeSymbol'}) do
 hi(name,{fg=fg.muted,nocombine=true})
end
hi('NeoTreeIndentMarker',{fg=bg.surface2})
hi('NeoTreeGitStaged',{fg=p.green,underline=true})
hi('SnacksDashboardDesc',{fg=p.fg})
hi('SnacksDashboardIcon',{fg=p.blue})
hi('SnacksDashboardFooter',{fg=p.muted})
hi('SnacksDashboardSpecial',{fg=p.muted})
hi('BlinkCmpLabelMatch',{fg=p.fg,bold=true})
hi('LspSignatureActiveParameter',{fg=p.fg,bg=p.search,bold=true})
hi('BlinkCmpSignatureHelpActiveParameter',{link='LspSignatureActiveParameter'})
for _,name in ipairs({'BufferLineBufferSelected','BufferLineNumbersSelected',
 'BufferLineCloseButtonSelected','BufferLineDuplicateSelected'}) do
 local h=vim.api.nvim_get_hl(0,{name=name,link=false});h.bg=tonumber(bg.mantle:sub(2),16);hi(name,h)
end
require('ithilien.plugin_palette').setup()
local lualine=package.loaded['lualine']
if lualine then local c=lualine.get_config();require('ithilien.statusline').configure(c);lualine.setup(c) end

end
return M
