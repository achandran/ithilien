-- A quiet watch dial: red GMT-hand tip, dark digits, no seconds or animation.
local M = {}
local function palette()
  return require('ithilien.ithilien-dawn').raw
end
function M.clock()
  return {
    { function() return '▸' end,
      color = function() local p = palette(); return { fg=p.accents.coral, bg=p.backgrounds.base } end,
      padding = { left=1, right=0 }, separator = '' },
    { function() return os.date('%I:%M %p') end,
      color = function() local p = palette(); return { fg=p.foregrounds.text, bg=p.backgrounds.base, gui='bold' } end,
      padding = { left=1, right=1 }, separator = '' },
  }
end
function M.configure(opts)
  opts.options = opts.options or {}
  opts.options.theme = 'ithilien-dawn'
  opts.sections = opts.sections or {}
  opts.sections.lualine_z = M.clock()
  return opts
end
return M
