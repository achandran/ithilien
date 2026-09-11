# Installation

## Ghostty

Copy `ghostty/themes/ithilien_dusk.conf` and `ghostty/themes/ithilien_dawn.conf` into `~/.config/ghostty/themes/`. To follow macOS appearance automatically:

```ini
theme = light:ithilien_dawn.conf,dark:ithilien_dusk.conf
```

The generated dark theme uses Berkeley Mono Retina for terminal text and window titles. The light theme uses Berkeley Mono Medium for both. Neither theme sets `font-thicken`. The light theme sets `faint-opacity = 1` to protect agent deletion text, and `minimum-contrast = 1` to disable renderer contrast adjustment, which made vi-mode block cursor text unreadable in the user’s Ghostty setup. The Dawn ANSI white endpoints are light foregrounds for dark backgrounds; default terminal text is dark graphite.

## Neovim and LazyVim

Dawn is on `main`; pull the latest changes or set the plugin `dir` to this local checkout. Neovim 0.12+ is recommended for exact character diffs. Add `vim.opt.diffopt:append("inline:char")` to your configuration; the colorscheme itself does not change your diff algorithm.


Copy `nvim/lazyvim-plugin.lua` into your LazyVim plugin specifications, then run `:Lazy sync`. The spec installs `achandran/ithilien` with Zenbones and Lush for Dawn, and Kanso for Dusk directly from GitHub. Select `ithilien`, `ithilien-dawn`, or `ithilien-dusk` with `:colorscheme`; `ithilien` defaults to Ithilien Dawn.

On macOS, the included LazyVim spec also follows system appearance changes in running Neovim sessions. Install its native watcher first:

```sh
brew install cormacrelf/tap/dark-notify
```

Ithilien Dawn is selected in Light appearance and Ithilien Dusk in Dark appearance. Remove the `cormacrelf/dark-notify` entry from the spec if automatic switching is not wanted.

## AI coding tools

For Codex CLI, copy the generated `.tmTheme` files into `~/.codex/themes/`, then choose one with `/theme`. These themes explicitly define `markup.inserted` and `markup.deleted`, so Codex uses Ithilien's tuned diff backgrounds instead of its built-in mint and pink fallbacks.

For Claude Code 2.1.118 or newer, copy the generated JSON files into `~/.claude/themes/`, then choose one with `/theme`. The generated themes define full-line, dimmed-context, and word-level diff colors. Claude Code does not currently combine two custom files behind its `auto` selection, so select Ithilien Dusk or Ithilien Dawn when appearance changes.

## Slack and Linear

Slack exposes only a subset of its interface colors. In Preferences → Appearance → Custom theme, choose Import theme and paste the appropriate line from `slack/`. Keep window gradients off for the closest Ithilien result.

In Linear Preferences → Interface and theme, create a custom theme and paste the appropriate line from `linear/`. Linear derives its remaining surfaces from these seed colors, so minor generated shades are controlled by Linear rather than Ithilien.


## Dynamic macOS wallpaper

`wallpapers/ithilien.heic` contains two 6016×3760 sRGB frames and Apple's appearance metadata. macOS displays the warm parchment `#F0E9D2` Dawn frame in Light appearance and the olive-black `#171812` Dusk frame in Dark appearance.

To regenerate and inspect it on macOS:

```sh
swiftc -module-cache-path /private/tmp/ithilien-swift-cache scripts/generate_wallpaper.swift -o /private/tmp/generate-ithilien-wallpaper
/private/tmp/generate-ithilien-wallpaper generate wallpapers/ithilien.heic
/private/tmp/generate-ithilien-wallpaper inspect wallpapers/ithilien.heic
```

## Other integrations

- Firefox: load `firefox/manifest.json` as a temporary add-on.
- Zsh selection: source `shell/ithilien.zsh`.
- macOS selection: run `macos/apply-highlight.sh`, then log out and back in.

Paths are relative to the repository root.

### Native cursor regression check

With Dawn loaded, use zsh `bindkey -v`, type a command without executing it, press Escape, and move the block over letters and punctuation. Check dark text remains readable in the pale block, then return to insert mode. The user confirmed that changing `minimum-contrast` from 4.5 to 1 fixes the unreadable block in this workflow (version reported as “1.31”; exact version string unverified). Automated tests pin this setting and audit the exported pair, but do not emulate Ghostty rendering. Applications emitting their own colors no longer receive automatic contrast correction.

## One-command installer

Run `./install.sh --apply` after `git pull` (Python 3 required). Without `--apply`, it prints a dry run. `--only ghostty nvim codex claude slack linear firefox` selects a subset. Detection uses executables on PATH and macOS application bundles; browser-only installations and apps in custom locations may be skipped.

Changed existing files are backed up under `~/.local/share/ithilien/backups/<timestamp>/`, preserving their full path beneath that directory. Restore a file by copying its backup over the installed file. To undo a newly created LazyVim integration, remove `lua/plugins/ithilien-installed.lua`; other newly created theme files can likewise be removed. Repeated identical installs do not rewrite files or create backups.

Ghostty always installs to `~/.config/ghostty/config` and `~/.config/ghostty/themes/`, even if a native macOS config exists; that native file is left untouched. For other integrations the installer respects XDG_CONFIG_HOME, CODEX_HOME, CLAUDE_CONFIG_DIR and NVIM_APPNAME. It refuses symlink destinations. Other Ghostty settings are preserved; explicit font, cursor, or contrast settings can override the installed theme. Existing custom LazyVim theme specifications may also require reconciliation. Non-LazyVim configurations get manual instructions rather than automatic init-file edits. No dependencies are downloaded by this script.

Slack and Linear require their in-app import controls. Codex and Claude custom themes require their CLI theme selectors; desktop app detection alone does not establish CLI custom-theme support. Firefox receives Dawn/Dusk theme files under `~/.local/share/ithilien/firefox`; activation remains manual. Zsh receives both selection files and a backed-up managed Dawn highlight block in `.zshrc` (honoring ZDOTDIR). Wallpaper, macOS selection and mobile devices are outside automatic installation.

## Firefox and shell selection

`firefox/manifest.json` now defaults to Dawn. Separate `firefox/ithilien-dawn/` and `firefox/ithilien-dusk/` exports set the correct light/dark scheme, browser surfaces, and address-field selection. Load the desired manifest through `about:debugging` > This Firefox > Load Temporary Add-on. This expires on restart; permanent extension distribution requires signing.

Each Firefox export also includes optional `userContent.css` for website `::selection`: Dawn uses Ranger brushed steel `#C4CAC8` with Lebethron `#25292B`. To use it, merge the rule into the active profile's `chrome/userContent.css`, enable `toolkit.legacyUserProfileCustomizations.stylesheets` in about:config, and restart Firefox. The installer stages this file but does not overwrite profile CSS or toggle preferences. Browser theme colors alone do not control website selection.

`./install.sh --apply --only zsh firefox` installs these integrations when detected. Start a new zsh session after installation. The managed shell block defaults to Dawn; source `ithilien-dusk.zsh` instead for Dusk. ZLE visual selection and Ghostty mouse selection are separate systems. Non-region ZLE settings are preserved. The source can still be overridden by later shell/plugin hooks.

System selection exports now include `macos/apply-highlight-ithilien-dawn.sh` and `macos/apply-highlight-ithilien-dusk.sh`; the legacy apply-highlight.sh defaults to Dawn. They remain opt-in global changes. The dynamic wallpaper is unchanged.

The zsh installer also writes the Dawn prompt from `shell/prompt.zsh` into the managed block: graphite username, ANSI 9 (Rosehip) hostname, blue path and purple Git information. It enables PROMPT_SUBST and uses a literal newline, preserving your existing vcs_info hooks. This replaces the effective prompt on shell startup; later prompt-framework hooks can override it.
