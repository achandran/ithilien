-- Explicit semantic overrides for colors introduced by plugin defaults.
local M = {}
function M.apply()
  if vim.g.colors_name ~= 'ithilien-dawn' then return end
  local p=require('ithilien.ithilien-dawn').raw
  local b,f,a=p.backgrounds,p.foregrounds,p.ansi
  local groups={
    Added={fg=a.green},Removed={fg=a.red},Changed={fg=a.blue},OkMsg={fg=a.green},
    DiagnosticDeprecated={sp=f.muted,strikethrough=true},
    FloatShadow={bg=b.crust,blend=0},FloatShadowThrough={bg=b.crust,blend=0},
    RedrawDebugClear={bg=p.diff.changeEmphasis},RedrawDebugComposed={bg=p.diff.addBackground},
    RedrawDebugRecompose={bg=p.diff.deleteBackground},
    GrugFarResultsChangeIndicator={fg=a.blue},GrugFarResultsRemoveIndicator={fg=a.red},GrugFarResultsAddIndicator={fg=a.green},
    BufferLineFill={bg=b.mantle},BufferLineGroupLabel={fg=f.muted,bg=b.mantle},BufferLineGroupSeparator={bg=b.mantle},
    BufferLineDiagnostic={fg=f.muted,bg=b.base},BufferLineDiagnosticVisible={fg=f.muted,bg=b.base},
    FzfLuaHeaderBind={fg=a.blue},FzfLuaHeaderText={fg=f.muted},
    FzfLuaPathColNr={fg=f.muted},FzfLuaPathLineNr={fg=f.muted},
    FzfLuaLiveSym={fg=a.magenta},FzfLuaLivePrompt={fg=a.blue},
    FzfLuaBufNr={fg=f.muted},FzfLuaBufFlagCur={fg=a.blue},FzfLuaBufFlagAlt={fg=f.muted},
    FzfLuaTabMarker={fg=a.blue},FzfLuaTabTitle={fg=f.text},
    FzfLuaNormal={fg=f.text,bg=b.base},FzfLuaBorder={fg=f.muted,bg=b.base},
    FzfLuaPreviewBorder={fg=f.muted,bg=b.base},FzfLuaCursorLine={fg=f.text,bg=p.highlight.background},
    FzfLuaSearch={fg=f.text,bg=b.search},FzfLuaBackdrop={bg=b.mantle,blend=0},
    fzf1={fg=a.red,bg=b.mantle},fzf2={fg=f.text,bg=b.mantle},fzf3={fg=f.muted,bg=b.mantle},
  }
  for n,h in pairs(groups) do vim.api.nvim_set_hl(0,n,h) end
end
function M.setup()
 local g=vim.api.nvim_create_augroup('IthilienPluginPalette',{clear=true})
 -- Plugins can build highlights after the colorscheme, including on reload.
 vim.api.nvim_create_autocmd('User',{group=g,pattern={'LazyLoad','VeryLazy'},callback=function() vim.schedule(M.apply) end})
 vim.api.nvim_create_autocmd('ColorScheme',{group=g,callback=function() vim.schedule(M.apply) end})
 M.apply()
end
return M
