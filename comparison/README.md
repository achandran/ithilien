# Ghostty comparison

Run `python3 scripts/compare.py` from the repository. It prepares three isolated config files and prints launch commands for macOS and Linux. Run those commands yourself; no installed config is modified. Close the comparison windows to return to normal. Do not run the installer inside the comparison just to switch themes.

All three use Berkeley Mono Medium, 14 pt, no thickening, default faint opacity, and minimum-contrast 1. Edited spans in the ANSI specimen use ordinary-weight black text on ANSI white. This is a terminal capability specimen, not Dawn’s truecolor diff rendering. This isolates color differences; it is not each theme's untouched default experience. Upstream Kanso and Zenbones have dark block cursors with light text, which intentionally remain visible in the comparison rather than being redesigned to meet Dawn's dark-text rule. Kanso's omitted cursor-text is explicitly set to its light canvas.

In each window run `python3 /absolute/path/to/ithilien/scripts/compare.py --scenario` (the preparation step prints your exact path). Compare ANSI endpoints, both prompt variants, code, character emphasis, diff signs, diagnostic messages, dimmed text, and mouse selection. The explicit black prompt is a deliberate compatibility test: Zenbones maps ANSI black to its pale canvas; terminal default text is the portable alternative.

For zsh vi mode, use your ordinary shell, type the provided command without executing it, press Escape, and move over letters/digits/punctuation. Use `v` to inspect ZLE selection. Your personal zsh selection hook can override the theme, so record whether it is active; a clean baseline is `zsh -f` followed by `bindkey -v` (this omits automatic Ghostty hooks too). Judge the ordinary-shell run separately from the clean baseline.

For actual Neovim comparison, install all three plugins, then switch with `:colorscheme kanso-pearl`, `:colorscheme zenbones`, and `:colorscheme ithilien-dawn` after `:set background=light termguicolors`. Use the identical files and `:set diffopt+=inline:char` on supported Neovim versions. Neovim theme changes are separate from the terminal theme. The terminal specimen deliberately uses ANSI, not hardcoded Dawn truecolor, to avoid biasing the comparison.

For Codex/Claude, compare identical saved diff content in their actual interfaces and record the selected application theme. Switching Ghostty alone does not recolor explicit application truecolor. No native-agent superiority is inferred from the ANSI specimen.

Score each run 1–5: exact-edit recognition, code scanning, comments, selections, cursor readability, visual distraction, watch resemblance. Record errors and time to find the changes before preference. Repeat in a different order, then use each for a full session at the same display brightness. Do not pick a winner solely from swatches.

## Upstream snapshots

- Kanso: https://github.com/webhooked/kanso.nvim at `1afbbb449aa0254823dbe1932e3cbb51886ff9fe`, `extras/ghostty/kanso-pearl`.
- Zenbones: https://github.com/zenbones-theme/zenbones.nvim at `8304d8df9b823ff11e103afa62f38c39f534abe6`, `extras/ghostty/zenbones_light`.

Original configs are retained in `upstream/` alongside their MIT licenses. Dawn is read from this checkout whenever configurations are prepared. Launch commands require Ghostty config-default-files/config-file support; this kit has not been visually validated through native Ghostty automation.

Use the included fixture for native diffs:

```sh
nvim -d comparison/scenarios/before.py comparison/scenarios/after.py
```

Set each editor colorscheme in turn as described above. Locate the changed digits (including the Unicode-prefixed string), inserted equals, removed space, and unchanged context. The expected edits are visible in these small fixtures; use them to verify changed-character boundaries, not to measure blind search speed. For an unbiased speed comparison, use an unfamiliar real diff and vary the theme order.
