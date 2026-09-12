-- Explicit semantic overrides for colors introduced by plugin defaults.
local M = {}
function M.apply()
  if vim.g.colors_name ~= 'ithilien-dawn' then return end
  local p=require('ithilien.ithilien-dawn').raw
  local b,f,a=p.backgrounds,p.foregrounds,p.ansi
  local groups={
    NeogitSectionHeader={fg=a.blue,bold=true},NeogitChangeModified={fg=a.blue},
    Added={fg=a.green},Removed={fg=a.red},Changed={fg=a.blue},OkMsg={fg=a.green},
    DiagnosticDeprecated={sp=f.muted,strikethrough=true},
    FloatShadow={bg=b.crust,blend=0},FloatShadowThrough={bg=b.crust,blend=0},
    RedrawDebugClear={bg=p.diff.changeEmphasis},RedrawDebugComposed={bg=p.diff.addBackground},
    RedrawDebugRecompose={bg=p.diff.deleteBackground},
    GrugFarResultsChangeIndicator={fg=a.blue},GrugFarResultsRemoveIndicator={fg=a.red},GrugFarResultsAddIndicator={fg=a.green},
    BufferLineFill={bg=b.mantle},BufferLineGroupLabel={fg=f.muted,bg=b.mantle},BufferLineGroupSeparator={bg=b.mantle},
    BufferLineDiagnostic={fg=f.muted,bg=b.base},BufferLineDiagnosticVisible={fg=f.muted,bg=b.base},
    NoiceMini={fg=f.muted,bg=b.base,blend=0},
    FzfLuaHeaderBind={fg=a.blue},FzfLuaHeaderText={fg=f.muted},
    FzfLuaPathColNr={fg=f.muted},FzfLuaPathLineNr={fg=f.muted},
    FzfLuaLiveSym={fg=a.magenta},FzfLuaLivePrompt={fg=a.blue},
    FzfLuaBufNr={fg=f.muted},FzfLuaBufFlagCur={fg=a.blue},FzfLuaBufFlagAlt={fg=f.muted},
    FzfLuaTabMarker={fg=a.blue},FzfLuaTabTitle={fg=f.text},
    FzfLuaNormal={fg=f.text,bg=b.base},FzfLuaBorder={fg=f.muted,bg=b.base},
    FzfLuaPreviewBorder={fg=f.muted,bg=b.base},FzfLuaCursorLine={fg=f.text,bg=p.highlight.background},
    FzfLuaFzfMatch={fg=f.text},
    FzfLuaSearch={fg=f.text,bg=b.search},FzfLuaBackdrop={bg=b.mantle,blend=0},
    fzf1={fg=a.red,bg=b.mantle},fzf2={fg=f.text,bg=b.mantle},fzf3={fg=f.muted,bg=b.mantle},
  }
  -- Neogit's native diff defaults derive additional colors; use Dawn's four roles.
  for _,suffix in ipairs({'','Highlight','Cursor'}) do
    groups['NeogitDiffAdd'..suffix]={fg=f.text,bg=p.diff.addBackground}
    groups['NeogitDiffDelete'..suffix]={fg=f.text,bg=p.diff.deleteBackground}
    groups['NeogitDiffContext'..suffix]={fg=f.text,bg=b.base}
    groups['NeogitHunkHeader'..suffix]={fg=f.text,bg=b.mantle}
  end
  groups.NeogitDiffAddInline={fg=f.text,bg=p.diff.changeEmphasis}
  groups.NeogitDiffDeleteInline={fg=f.text,bg=p.diff.changeEmphasis}
  -- Overlapping TodoBg/TodoFg spans must remain readable at keyword punctuation.
  for keyword,color in pairs({FIX=a.red,TODO=a.blue,HACK=a.yellow,WARN=a.yellow,PERF=a.magenta,NOTE=a.cyan,TEST=a.green}) do
    groups['TodoBg'..keyword]={fg=color,bg=b.mantle,bold=true}
    groups['TodoFg'..keyword]={fg=color}
  end
  for n,h in pairs(groups) do vim.api.nvim_set_hl(0,n,h) end
  -- Neo-tree's truncated names use default highlights; keep the faded tail readable.
  for name,h in pairs(vim.api.nvim_get_hl(0,{})) do
    if name:match('^NeoTree') and not name:match('_%d+$') then
      for _,suffix in ipairs({'68','60','35'}) do
        vim.api.nvim_set_hl(0,name..'_'..suffix,{fg=f.muted,bg=b.base})
      end
    end
  end
  -- Bufferline derives new icon groups from cached parent colors at render time.
  local config=package.loaded['bufferline.config']
  if config and config.get().highlights then
    for name,color in pairs({background=b.base,buffer_visible=b.base,buffer_selected=b.mantle}) do
      local parent=config.get().highlights[name]
      if parent then parent.bg=color end
    end
    local highlights=package.loaded['bufferline.highlights']
    if highlights then highlights.reset_icon_hl_cache() end
    for name,h in pairs(vim.api.nvim_get_hl(0,{})) do
      if name:match('^BufferLineMiniIcons') or name:match('^BufferLineDevIcon') then
        -- Clearing default is required to replace a previously defined icon group.
        h.default=nil
        h.bg=tonumber((name:match('Selected$') and b.mantle or b.base):sub(2),16)
        vim.api.nvim_set_hl(0,name,h)
      end
    end
  end
end
function M.setup()
 local g=vim.api.nvim_create_augroup('IthilienPluginPalette',{clear=true})
 -- Plugins can build highlights after the colorscheme, including on reload.
 vim.api.nvim_create_autocmd('User',{group=g,pattern={'LazyLoad','VeryLazy'},callback=function() vim.schedule(M.apply) end})
 vim.api.nvim_create_autocmd('ColorScheme',{group=g,callback=function() vim.schedule(M.apply) end})
 M.apply()
end
return M
