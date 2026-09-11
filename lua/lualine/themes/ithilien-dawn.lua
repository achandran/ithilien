-- Ithilien Dawn
local p = require("ithilien.ithilien-dawn").raw
local bg, fg, a = p.backgrounds, p.foregrounds, p.accents

return {
  normal = {
    a = { fg = p.highlight.foreground, bg = p.highlight.background, gui = "bold" },
    b = { fg = fg.text, bg = bg.surface2 },
    c = { fg = fg.subtext, bg = bg.surface0 },
  },
  insert = { a = { fg = p.highlight.foreground, bg = p.highlight.background, gui = "bold" } },
  visual = { a = { fg = p.highlight.foreground, bg = p.highlight.background, gui = "bold" } },
  replace = { a = { fg = p.highlight.foreground, bg = p.highlight.background, gui = "bold" } },
  command = { a = { fg = p.highlight.foreground, bg = p.highlight.background, gui = "bold" } },
  inactive = {
    a = { fg = fg.muted, bg = bg.mantle },
    b = { fg = fg.muted, bg = bg.mantle },
    c = { fg = fg.muted, bg = bg.mantle },
  },
}
