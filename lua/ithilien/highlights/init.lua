-- Ithilien owns its highlight configuration; loading it never configures another theme.
local M = {}

function M.apply(theme, opts)
  local config = {
    bold = opts.bold,
    italics = opts.italics,
    undercurl = true,
    minimal = false,
    transparent = false,
    dimInactive = false,
    commentStyle = opts.italics and { italic = true } or {},
    functionStyle = {},
    keywordStyle = { bold = opts.bold, italic = false },
    statementStyle = { bold = opts.bold },
    typeStyle = {},
  }
  local highlights = {}
  for _, name in ipairs({ "editor", "syntax", "treesitter", "lsp", "plugins" }) do
    for group, spec in pairs(require("ithilien.highlights." .. name).setup({ theme = theme }, config)) do
      highlights[group] = spec
    end
  end
  vim.o.termguicolors = true
  for group, spec in pairs(highlights) do
    vim.api.nvim_set_hl(0, group, spec)
  end
end

return M
