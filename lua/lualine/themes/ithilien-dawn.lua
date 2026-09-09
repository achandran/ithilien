-- Ithilien Dawn
local p = require("ithilien.ithilien-dawn").raw
local bg, fg, a = p.backgrounds, p.foregrounds, p.accents

return {
  normal = {
    a = { fg = bg.base, bg = a.olive, gui = "bold" },
    b = { fg = fg.text, bg = bg.surface2 },
    c = { fg = fg.subtext, bg = bg.surface0 },
  },
  insert = { a = { fg = bg.base, bg = a.sage, gui = "bold" } },
  visual = { a = { fg = bg.base, bg = a.mauve, gui = "bold" } },
  replace = { a = { fg = bg.base, bg = a.coral, gui = "bold" } },
  command = { a = { fg = bg.base, bg = a.gold, gui = "bold" } },
  inactive = {
    a = { fg = fg.muted, bg = bg.mantle },
    b = { fg = fg.muted, bg = bg.mantle },
    c = { fg = fg.muted, bg = bg.mantle },
  },
}
