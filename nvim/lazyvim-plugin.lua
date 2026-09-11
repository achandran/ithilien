-- Copy this spec into your LazyVim plugins directory.
return {
  {
    "achandran/ithilien",
    dependencies = { "webhooked/kanso.nvim", "zenbones-theme/zenbones.nvim", "rktjmp/lush.nvim" },
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
      opts.options = opts.options or {}
      opts.options.theme = vim.g.colors_name == "ithilien-dusk" and "ithilien-dusk" or "ithilien-dawn"
    end,
  },
}
