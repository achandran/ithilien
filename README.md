# Ithilien

Warm coding themes for long sessions and precise diffs.

| Theme | Canvas | Main text |
| --- | --- | --- |
| **Dawn** · light | `#F0E9D2` | `#000000` |
| **Dusk** · dark | `#171812` | `#C9BA99` |

## Dawn palette

38 colors named for Ithilien’s plants, landscape, people and immediate neighbours.

![Ithilien Dawn: all 38 colors with names, hex values and roles](assets/ithilien-dawn-palette.svg)

[Text palette and name sources](docs/palette-names.md) · [Interactive palette lab](palette-preview.html)

## Reading and diffs

- Warm surfaces and restrained syntax colors; Dawn uses black main text.
- Distinct added, removed and changed lines. Dawn’s exact changed characters are **black and underlined** in Neovim; selected text stays black.

## Install

| Application | Files / setup |
| --- | --- |
| Neovim / LazyVim | [Plugin spec](nvim/lazyvim-plugin.lua); `:colorscheme ithilien-dawn` or `ithilien-dusk` |
| Ghostty | Copy [themes](ghostty/themes/) to `~/.config/ghostty/themes/` |
| Codex | Copy [themes](codex/themes/) to `~/.codex/themes/`; choose with `/theme` |
| Claude Code | Copy [themes](claude-code/themes/) to `~/.claude/themes/`; choose with `/theme` |
| Firefox | [Extension](firefox/manifest.json) |
| Zsh | [Selection config](shell/ithilien.zsh) |
| macOS | [Selection script](macos/apply-highlight.sh) · [Dynamic wallpaper](wallpapers/ithilien.heic) |
| Slack / Linear | [Slack](slack/) · [Linear](linear/) theme strings |

Ghostty automatic appearance:

```ini
theme = light:ithilien-dawn,dark:ithilien-dusk
```

[Installation details](docs/installation.md), including Neovim dependencies and macOS appearance switching. `ithilien` defaults to Dawn.

## Build and check

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run python scripts/build.py
uv run python -m unittest discover -s tests
```

Edit the [canonical palettes](palette/), then rebuild; generated themes, palette chart and reference update together. Dawn stores each hex once under `colors`; roles reference names.

[Dawn audit](reports/ithilien-dawn-audit.md) · [Dusk audit](reports/ithilien-dusk-audit.md) · [Python review](reports/python-review/README.md)
