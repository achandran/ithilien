# Extras

Companion ports for the Ithilien Neovim colorscheme. Dawn and Dusk exports are
generated from the same canonical palettes as the Neovim theme where supported.
Application rendering and coverage differ; see the [installation guide](../docs/installation.md).

| Application | Files |
| --- | --- |
| Ghostty | [Theme configs](ghostty/themes/) |
| Codex CLI | [TextMate themes](codex/themes/) and [UI config](codex/config.toml) |
| Claude Code | [Themes](claude-code/themes/) |
| Firefox | [Manifests and selection styles](firefox/) |
| Zsh / fzf | [Shell styles and prompt](shell/) |
| Slack | [Import strings](slack/) |
| Linear | [Import strings](linear/) |
| macOS | [System selection scripts](macos/) |
| Wallpaper | [Dynamic HEIC](wallpapers/ithilien.heic) |

From the repository root, `./install.sh --only ghostty` installs one integration;
`./install.sh --dry-run` previews the full installer. The installer requires
Python 3 and retains the existing destination paths and backup behavior.

The source folders previously at the repository root now live under `extras/`.
Update any custom scripts or symlinks that refer directly to checkout paths.
Installed copies do not need to move. Neovim's `colors/`, `lua/`, and `plugin/`
runtime directories remain at the root.

Contributors: edit `palette/` and the generators rather than generated exports.
See [development](../docs/development.md) for regeneration and evaluation.
