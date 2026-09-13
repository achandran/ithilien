# Ithilien

Two Neovim colorschemes for clear code and precise diffs: **Dawn**, porcelain and black, and **Dusk**, warm gray on graphite. Each uses 18 named colors, with shared selection, cursor, search, and exact-edit colors.

[Install](#install) · [Themes](#themes) · [Usage](#usage) · [Palette](#palette) · [Design](#design) · [Extras](#extras)

## Themes

### Ithilien Dawn

Porcelain whites, black type, steel neutrals, and a deliberate red accent. Shown in **Berkeley Mono Medium, 16 pt**.

![Ithilien Dawn — Python code and character-level diffs in Neovim](docs/assets/ithilien-dawn-neovim.png)

```lua
vim.cmd.colorscheme("ithilien-dawn")
```

### Ithilien Dusk

Warm Graphite: stone-gray reading text, neutral graphite surfaces, and restrained botanical accents. Shown in **Berkeley Mono Retina, 16 pt**.

![Ithilien Dusk — warm graphite Python code and character-level diffs in Neovim](docs/assets/ithilien-dusk-neovim.png)

```lua
vim.cmd.colorscheme("ithilien-dusk")
```

**Read the code. Find the change.** Four diff backgrounds: green for added lines, red for deleted lines, blue for changed lines, and amber for the exact edited characters. Clients with separate added/deleted word highlights use the same amber for both. Diff emphasis keeps ordinary text weight, so even a one-character edit stands out through color.

## Install

Install with [lazy.nvim](https://github.com/folke/lazy.nvim):

```lua
{
  "achandran/ithilien",
  dependencies = { "webhooked/kanso.nvim" },
  lazy = false,
  priority = 1000,
  opts = { bold = true, italics = true },
  config = function(_, opts)
    require("ithilien").setup(opts)
    vim.cmd.colorscheme("ithilien-dawn")
  end,
}
```

Requires Neovim with truecolor enabled (`vim.opt.termguicolors = true`) and
Kansō. Python and the repository's build tools are only needed for development.

### LazyVim

Use this complete configuration instead of the minimal lazy.nvim example above.
Save it as `~/.config/nvim/lua/plugins/ithilien.lua`, then run `:Lazy sync`.
It includes lualine integration.

```lua
return {
  {
    "achandran/ithilien",
    branch = "main",
    dependencies = { "webhooked/kanso.nvim" },
    lazy = false,
    priority = 1000,
    opts = {
      bold = true,
      italics = true,
    },
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
```

Update the plugin with `:Lazy update`.


## Usage

```lua
vim.cmd.colorscheme("ithilien-dawn") -- light
vim.cmd.colorscheme("ithilien-dusk") -- dark
```

`ithilien` is an alias for Dawn. Setup is optional when using the default bold
and italic syntax styles. Exact diff emphasis uses ordinary weight and color.

## Palette

<details>
<summary>Dawn palette — 18 colors</summary>

![Ithilien Dawn palette](docs/assets/ithilien-dawn-palette.svg)

[Named colors and roles](docs/palette-names.md)

</details>

<details>
<summary>Dusk palette — 18 colors</summary>

![Ithilien Dusk palette](docs/assets/ithilien-dusk-palette.svg)

[Named colors and roles](docs/dusk-palette.md)

</details>

Both variants share **Briar** `#B8595C` for selection and cursors, **Heather** `#D6C6DE` for search, and **Celandine** `#D8B46A` for exact edits, all with **Lebethron** black text. The other shades adapt to each appearance.

Palettes and previews are generated from canonical sources. The previews rasterize actual Neovim UI-cell colors with each variant's specified font at 16 pt. They show built-in Python syntax; they are not native Ghostty screenshots or Tree-sitter/LSP captures. Set the font in your terminal; Neovim colorschemes do not change it.

## Design

Dawn takes its visual direction from the **Formex Reef GMT with a white dial, black ceramic bezel, and stainless steel bracelet**: clear markings on a quiet surface, metallic neutrals, and red used deliberately for interaction. Its color names draw from Tolkien’s Ithilien and the wider world of Middle-earth.

Dusk interprets the same watch through its ceramic bezel and metallic neutrals: graphite surfaces and warm stone-gray text. Both variants keep syntax restrained and give changes, search, and selection a clear visual hierarchy.

- **Precise diffs.** Locate added, removed, and changed code, down to individual characters and punctuation.
- **Readable agent sessions.** Support code, explanations, patches, and tool output in Codex and Claude Code. Dawn has saved native Codex replay coverage. Dusk exports are available; native Codex and Claude Code validation for Dusk remains pending. Character-level emphasis depends on the application exposing that role.
- **Long-session comfort.** Readable supporting text and restrained decoration are design goals. Automated contrast checks support them; they do not prove comfort.
- **Consistent interactions.** Briar marks selection and the cursor with black foreground text. Search and inline edits use different hues.

The Neovim implementation builds on [Kansō](https://github.com/webhooked/kanso.nvim), with Ithilien’s palette and highlight mappings. Dawn remains the fixed light palette; Dusk uses Warm Graphite. See [Dusk design and validation](docs/dusk-design.md) for evidence and coverage limits.

## Extras

Matching terminal and application ports live in [extras/](extras/README.md),
following [Kansō's layout](https://github.com/webhooked/kanso.nvim/tree/main/extras).
These include Ghostty, Codex, Claude Code, Firefox, Zsh, Slack, Linear, macOS
selection scripts.

Copy or source the files for the applications you use; see the manual
installation instructions below.

[Extra installation instructions](docs/installation.md) ·
[Development](docs/development.md) · [Tintprobe evaluator](https://github.com/achandran/tintprobe) · [Preview details](docs/development.md#preview-assets)
