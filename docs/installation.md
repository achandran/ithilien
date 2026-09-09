# Installation

## Ghostty

Copy `ghostty/themes/ithilien-dusk` and `ghostty/themes/ithilien-dawn` into `~/.config/ghostty/themes/`. To follow macOS appearance automatically:

```ini
theme = light:ithilien-dawn,dark:ithilien-dusk
```

The generated dark theme uses Berkeley Mono Retina without font thickening. The light theme uses Berkeley Mono with `font-thicken = true`, `faint-opacity = 1` to protect agent deletion text, and `minimum-contrast = 4.5` for unexpected terminal pairs. The Dawn ANSI white endpoints are light foregrounds for dark backgrounds; default terminal text remains black.

## Neovim and LazyVim

Copy `nvim/lazyvim-plugin.lua` into your LazyVim plugin specifications, then run `:Lazy sync`. The spec installs `achandran/ithilien` and its Kanso dependency directly from GitHub. Select `ithilien`, `ithilien-dawn`, or `ithilien-dusk` with `:colorscheme`; `ithilien` defaults to Ithilien Dawn.

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
