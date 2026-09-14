# Installation

## Neovim and LazyVim

Ithilien has no external colorscheme dependency. Existing installations can remove
the old colorscheme dependency from Ithilien's plugin specification.

Dawn and Dusk are on `main`; pull the latest changes or set the plugin `dir` to this local checkout. Neovim 0.12+ is recommended for exact character diffs. Loading Ithilien requests `inline:char` on supported Neovim versions. Switching to another colorscheme restores the previous `diffopt` unless you changed it in the meantime.


For a minimal lazy.nvim setup, see the [README](../README.md#install). Select `ithilien-dawn` or `ithilien-dusk` with `:colorscheme`; `ithilien` is an alias for Dawn.

### LazyVim

Save it as `~/.config/nvim/lua/plugins/ithilien.lua`, then run `:Lazy sync`.
It includes lualine integration.

```lua
return {
  {
    "achandran/ithilien",
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
      colorscheme = "ithilien-dawn", -- or "ithilien-dusk"
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

## Ghostty

Copy `extras/ghostty/themes/ithilien_dawn.conf` and `extras/ghostty/themes/ithilien_dusk.conf` into `~/.config/ghostty/themes/`:

```ini
theme = light:ithilien_dawn.conf,dark:ithilien_dusk.conf
font-size = 16
```

Dawn uses Berkeley Mono Medium and Dusk uses Berkeley Mono Retina, both at 16 pt. Neither sets `font-thicken`. Select a single theme filename instead of the light/dark pair to keep a fixed appearance. The light theme leaves `faint-opacity` unset so Ghostty uses its default dim-text rendering, and sets `minimum-contrast = 1` to disable renderer contrast adjustment, which made vi-mode block cursor text unreadable in the user’s Ghostty setup. Faint opacity applies to all terminal text carrying the dim attribute, including dimmed diff text. The Dawn ANSI white endpoints are light foregrounds for dark backgrounds; default terminal text is black.


## AI coding tools

For Codex CLI, copy the `.tmTheme` files from `extras/codex/themes/` into `~/.codex/themes/`, then choose one with `/theme`. Optionally merge `tui.animations = false` from `extras/codex/config.toml` into your config to disable motion, without replacing other settings. These themes explicitly define `markup.inserted` and `markup.deleted`, so Codex uses Ithilien's tuned diff backgrounds instead of its built-in mint and pink fallbacks.

For Claude Code 2.1.118 or newer, copy the JSON files from `extras/claude-code/themes/` into `~/.claude/themes/`, then choose one with `/theme`. The generated themes define full-line, dimmed-context, and word-level diff colors.

## Slack and Linear

Slack exposes only a subset of its interface colors. In Preferences → Appearance → Custom theme, choose Import theme and paste the appropriate line from `extras/slack/`. Keep window gradients off for the closest Ithilien result.

In Linear Preferences → Interface and theme, create a custom theme and paste the appropriate line from `extras/linear/`. Linear derives its remaining surfaces from these seed colors, so minor generated shades are controlled by Linear rather than Ithilien.


## Other integrations

- Firefox: load `extras/firefox/manifest.json` as a temporary add-on.
- Zsh selection: source `extras/shell/ithilien.zsh`.
- macOS selection: run `extras/macos/apply-highlight.sh`, then log out and back in.

Paths are relative to the repository root.

### Native cursor regression check

With Dawn loaded, use zsh `bindkey -v`, type a command without executing it, press Escape, and move the block over letters and punctuation. Check dark text remains readable in the pale block, then return to insert mode. The user confirmed that changing `minimum-contrast` from 4.5 to 1 fixes the unreadable block in this workflow (version reported as “1.31”; exact version string unverified). Automated tests pin this setting and audit the exported pair, but do not emulate Ghostty rendering. Applications emitting their own colors no longer receive automatic contrast correction.

## Firefox and shell selection

`extras/firefox/manifest.json` now defaults to Dawn. The `extras/firefox/ithilien-dawn/` and `extras/firefox/ithilien-dusk/` exports set the matching appearance, browser surfaces, and address-field selection. Load the desired manifest through `about:debugging` > This Firefox > Load Temporary Add-on. This expires on restart; permanent extension distribution requires signing.

Each Firefox export also includes optional `userContent.css` for website `::selection`: Dawn uses Briar `#B8595C` with black text `#000000`. To use it, merge the rule into the active profile's `chrome/userContent.css`, enable `toolkit.legacyUserProfileCustomizations.stylesheets` in about:config, and restart Firefox. Browser theme colors alone do not control website selection.

For Zsh, add `source /absolute/path/to/ithilien/extras/shell/ithilien-dawn.zsh`
to `.zshrc` and start a new session. Use `ithilien-dusk.zsh` for Dusk.
ZLE visual selection and Ghostty mouse selection are separate systems.
Non-region ZLE settings are preserved; later shell/plugin hooks can override them.

System selection is available through `extras/macos/apply-highlight-ithilien-dawn.sh`; the legacy apply-highlight.sh also uses Dawn. These remain opt-in global changes.

Optionally source `/absolute/path/to/ithilien/extras/shell/prompt.zsh` after the selection script to use the Dawn prompt: Ash username and hostname, blue path, purple Git information, and a black command-entry symbol. It enables PROMPT_SUBST and uses a literal newline, preserving your existing vcs_info hooks. This replaces the effective prompt on shell startup; later prompt-framework hooks can override it.

### Neovim linewise selection rendering

Dawn Visual and VisualNOS use Briar backgrounds and black foregrounds with no underline or other decoration. The user confirmed that removing selection styling fixes partial-line rendering in Ghostty. Exact diff-character highlights use ordinary-weight black text on Celandine backgrounds, without added bold or underline; the native highlight regression check asserts both contracts. Earlier reports describing an underlined Visual selection are historical.

### fzf history search

The sourced Zsh theme also sets generated fzf colors in `FZF_DEFAULT_OPTS` and `FZF_CTRL_R_OPTS`, preserving existing bindings and preview options. Dawn uses black text, Briar for the current row, underlined matching characters, and a Briar prompt. Start a new shell after installation. Later fzf options or plugin configuration can override these colors. Sourcing the generated shell file repeatedly replaces its previous color option.

### macOS system selection

Run the appropriate script from `extras/macos/` to change the global system
selection color. These scripts are opt-in and do not create automatic backups.
Log out and back in if applications retain their previous color.

### Dawn diff presentation

Dawn diff windows use subdued dotted filler, pane labels, and matching syntax when a revision buffer lacks a filetype. Neovim 0.12 uses character-level inline diffs. Window presentation is restored on leaving diff mode. Labels identify FILE/REVISION/BUFFER when provenance is known; integrations may set `b:ithilien_diff_label` to a more specific label such as INDEX or WORKING COPY.

### Existing LazyVim theme configuration

Use the [README configuration](../README.md#lazyvim). If you previously used the
retired installer, its installed copies remain in place. Keep one Ithilien plugin
specification; remove an obsolete `ithilien-installed.lua` only after transferring
any custom settings. Existing backups remain under `~/.local/share/ithilien/backups/`.
