local M = {}

M.config = {
  bold = true,
  italics = true,
}

function M.setup(opts)
  M.config = vim.tbl_deep_extend("force", M.config, opts or {})
end

function M.load(variant)
  local is_light = variant == "dawn" or variant == "day" or variant == "light"
  if is_light then return require("ithilien.dawn").load(M.config) end
  local palette = require(is_light and "ithilien.ithilien-dawn" or "ithilien.ithilien-dusk")
  local raw = palette.raw
  local bg, fg, accent, diff = raw.backgrounds, raw.foregrounds, raw.accents, raw.diff
  local highlight = raw.highlight

  local theme = {
    ui = {
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
      warning = accent.gold,
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
      added = diff.addForeground,
      removed = diff.deleteForeground,
      changed = diff.changeForeground,
      untracked = fg.comment,
    },
    term = palette.terminal,
  }

  require("kanso").setup({
    bold = M.config.bold,
    italics = M.config.italics,
    undercurl = true,
    transparent = false,
    dimInactive = false,
    terminalColors = true,
    commentStyle = M.config.italics and { italic = true } or {},
    keywordStyle = { bold = is_light and M.config.bold or false, italic = true },
    functionStyle = {},
    statementStyle = { bold = is_light and M.config.bold or false },
    typeStyle = {},
    background = { dark = "ink", light = "pearl" },
    theme = is_light and "pearl" or "ink",
    colors = {
      palette = palette.kanso,
      theme = { all = theme, ink = {}, zen = {}, pearl = {} },
    },
    overrides = function()
      local overrides = {
        Visual = { fg = highlight.foreground, bg = highlight.background },
        DiffAdd = { fg = diff.addForeground, bg = diff.addBackground },
        DiffDelete = { fg = diff.deleteForeground, bg = diff.deleteBackground },
        DiffChange = { fg = diff.changeForeground, bg = diff.changeBackground },
        DiffText = { fg = highlight.foreground, bg = highlight.background, bold = true },
        Added = { fg = diff.addForeground },
        Removed = { fg = diff.deleteForeground },
        Changed = { fg = diff.changeForeground },
        GitSignsAdd = { fg = diff.addForeground },
        GitSignsDelete = { fg = diff.deleteForeground },
        GitSignsChange = { fg = diff.changeForeground },
        GitSignsAddInline = { fg = diff.inlineForeground, bg = diff.addEmphasis, bold = true, underline = is_light or nil },
        GitSignsDeleteInline = { fg = diff.inlineForeground, bg = diff.deleteEmphasis, bold = true, underline = is_light or nil },
        GitSignsChangeInline = { fg = diff.inlineForeground, bg = diff.changeEmphasis, bold = true, underline = is_light or nil },
        GitSignsAddLnInline = { fg = diff.inlineForeground, bg = diff.addEmphasis, bold = true, underline = is_light or nil },
        GitSignsDeleteLnInline = { fg = diff.inlineForeground, bg = diff.deleteEmphasis, bold = true, underline = is_light or nil },
        GitSignsChangeLnInline = { fg = diff.inlineForeground, bg = diff.changeEmphasis, bold = true, underline = is_light or nil },
        GitConflictCurrent = { fg = diff.conflictForeground, bg = diff.conflictBackground },
        GitConflictIncoming = { fg = diff.conflictForeground, bg = diff.conflictBackground },
        GitConflictAncestor = { fg = diff.hunkForeground, bg = diff.hunkBackground },
        DiagnosticVirtualTextError = { fg = accent.coral, bg = bg.surface0 },
        DiagnosticVirtualTextWarn = { fg = accent.gold, bg = bg.surface0 },
        DiagnosticVirtualTextInfo = { fg = accent.blue, bg = bg.surface0 },
        DiagnosticVirtualTextHint = { fg = accent.aqua, bg = bg.surface0 },
      }
      if is_light then
        -- Python's explicit Kanso subclasses otherwise bypass the keyword role.
        for _, capture in ipairs({
          "keyword", "keyword.function", "keyword.coroutine", "keyword.conditional",
          "keyword.repeat", "keyword.return", "keyword.exception", "keyword.import",
          "keyword.type", "keyword.modifier", "keyword.directive", "keyword.debug",
        }) do
          overrides["@" .. capture .. ".python"] = { fg = accent.clay, bold = M.config.bold, italic = false }
        end
        overrides["@keyword.operator.python"] = { fg = accent.olive, bold = false, italic = false }
        overrides["@constant.builtin.python"] = { fg = accent.ochre, bold = false, italic = false }
        overrides["@string.documentation.python"] = { fg = fg.comment, italic = M.config.italics }
        -- Explicit pairs avoid inherited reverse/search foregrounds and pale borders.
        overrides.PmenuKindSel = { fg = highlight.foreground, bg = highlight.background }
        overrides.PmenuExtraSel = { fg = highlight.foreground, bg = highlight.background }
        overrides.SnacksPickerSelected = { fg = accent.olive, bold = true }
        overrides.Substitute = { fg = highlight.foreground, bg = highlight.background }
        overrides["@comment.error"] = { fg = bg.base, bg = accent.coral, bold = M.config.bold }
        overrides.MiniTablineTabpagesection = { fg = highlight.foreground, bg = highlight.background, bold = true }
        overrides.SnacksPickerPickWin = { fg = highlight.foreground, bg = highlight.background, bold = true }
        overrides.Search = { fg = highlight.foreground, bg = highlight.background }
        overrides.IncSearch = { fg = highlight.foreground, bg = highlight.background }
        overrides.CurSearch = overrides.IncSearch
        overrides.FloatBorder = { fg = fg.muted, bg = bg.surface0 }
        overrides.CmpCompletionBorder = { link = "FloatBorder" }
        overrides.BlinkCmpMenuBorder = { link = "FloatBorder" }
        overrides.WinSeparator = { fg = fg.muted }
        overrides.CursorLine = { bg = bg.surface1 }
        overrides.CursorLineNr = { fg = fg.text, bold = true }
        overrides.StatusLine = { fg = fg.text, bg = bg.mantle, bold = true }
        overrides.StatusLineNC = { fg = fg.subtext, bg = bg.mantle }
        overrides.CurSearch = { fg = highlight.foreground, bg = highlight.background, bold = true, underline = true }
        overrides.DiffText = { fg = highlight.foreground, bg = highlight.background, bold = true, underline = true }
        -- Neovim uses this in either buffer for unmatched characters; it does
        -- not encode old/new direction, so keep the neutral change treatment.
        overrides.DiffTextAdd = { link = "DiffText" }
        -- Severity remains available when info/hint hues converge.
        overrides.DiagnosticUnderlineInfo = { sp = accent.blue, undercurl = false, underline = true }
        overrides.DiagnosticUnderlineHint = { sp = accent.aqua, undercurl = false, underdotted = true }
        overrides.PmenuMatch = { fg = accent.clay, bg = bg.surface0, bold = true }
        overrides.PmenuMatchSel = { fg = highlight.foreground, bg = highlight.background, bold = true }
      end
      return overrides
    end,
  })

  -- Changing 'background' can reload the previous colorscheme recursively.
  -- Keep its name for Kanso's highlight clear, but suppress that reload here.
  local previous_colors_name = vim.g.colors_name
  vim.g.colors_name = nil
  vim.o.background = is_light and "light" or "dark"
  vim.g.colors_name = previous_colors_name
  require("kanso").load(is_light and "pearl" or "ink")
  vim.g.colors_name = is_light and "ithilien-dawn" or "ithilien-dusk"

  local function sync_lualine()
    local lualine = package.loaded["lualine"]
    if not lualine then
      return
    end
    local config = lualine.get_config()
    config.options.theme = vim.g.colors_name
    lualine.setup(config)
  end
  if package.loaded["lualine"] then
    sync_lualine()
  else
    vim.schedule(sync_lualine)
  end
end

return M
