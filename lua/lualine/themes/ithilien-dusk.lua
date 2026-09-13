-- Ithilien Dusk: mode color stays on the left; right-hand metadata stays neutral.
local p = require("ithilien.ithilien-dusk").raw
local bg, fg, diff = p.backgrounds, p.foregrounds, p.diff

local function active(mode_bg, mode_fg)
  return {
    a = { fg = mode_fg or fg.text, bg = mode_bg, gui = "bold" },
    b = { fg = fg.text, bg = bg.surface2 },
    c = { fg = fg.subtext, bg = bg.surface0 },
    -- Explicit sections prevent Lualine from mirroring a/b/c onto z/y/x.
    x = { fg = fg.subtext, bg = bg.surface0 },
    y = { fg = fg.text, bg = bg.surface2 },
    z = { fg = fg.text, bg = bg.surface2, gui = "bold" },
  }
end

return {
  normal = active(bg.surface2),
  insert = active(diff.addBackground),
  visual = active(p.highlight.background, p.highlight.foreground),
  replace = active(diff.changeEmphasis, diff.inlineForeground),
  command = active(diff.changeBackground),
  inactive = {
    a = { fg = fg.muted, bg = bg.mantle },
    b = { fg = fg.muted, bg = bg.mantle },
    c = { fg = fg.muted, bg = bg.mantle },
  },
}
