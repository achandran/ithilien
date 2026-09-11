-- Copy this spec into your LazyVim plugins directory.
return {
  {
    "achandran/ithilien",
    dependencies = { "webhooked/kanso.nvim" },
    lazy = false,
    priority = 1000,
    opts = {
      bold = true,
      italics = true,
    },
  },
  {
    "cormacrelf/dark-notify",
    config = function()
      require("dark_notify").run({
        schemes = {
          light = { colorscheme = "ithilien" },
          dark = { colorscheme = "ithilien-dusk" },
        },
      })
    end,
  },
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "ithilien",
    },
  },
  {
    "nvim-lualine/lualine.nvim",
    opts = function(_, opts)
      require("ithilien.statusline").configure(opts)
    end,
  },
}
