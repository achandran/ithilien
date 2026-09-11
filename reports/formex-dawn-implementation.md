# Ithilien Dawn — Neutral white implementation

Neutral white is implemented as Dawn's canonical palette. The canvas is Asphodel `#F6F6F3`, the reading foreground is Lebethron `#25292B`, and secondary text is Ash `#596166`. Dawn uses Zenbones/Lush; Dusk retains Kanso.

## Behavior

- Dark foregrounds on light surfaces, including selection, cursor cells, completion, tabs and lualine segments.
- Quiet syntax with readable punctuation. Bold keywords and restrained secondary text supply hierarchy.
- Added/deleted/changed lines have pale semantic fills. Exact characters use explicit graphite foregrounds, stronger fills, bold and underline.
- `DiffTextAdd` links to the neutral change treatment because Neovim can use it for unmatched characters in either buffer; it does not universally mean a newly added character.
- Selection is pale steel with a dark underline in Neovim. Interfaces supporting an outline can use `highlight.border`. The fill alone does not meet a 3:1 boundary target; applications lacking border/underline support need native evaluation.
- The palette generator updates Dawn's Ghostty, Codex, Claude, Slack and Linear exports. These exports do not certify native renderer behavior.
- No personal settings were installed, and the development branch has not been pushed.

## Validation

- **19 unit tests pass.** Dawn's old parchment fingerprint was intentionally updated to the selected neutral palette. Dusk's frozen fingerprint is unchanged.
- **196 canonical contrast checks pass.** Text requirements remain 4.5:1, with 7:1 for the designated enhanced pairs. Main text on the canvas is 13.56:1; selected text is 8.70:1.
- **583 resolved Neovim text/structure pairs pass.** Text uses 4.5:1 and structural groups use 3:1, against the explicit background or Normal fallback. Dynamic overlays may produce additional combinations outside this audit.
- **851 resolved highlight groups inspected.** No reversed groups. No light foregrounds except an excluded, synthetic Kanso workaround group that does not render user text. Dawn-specific surfaces and lualine labels use dark text.
- **Eight real diff cases pass** on Neovim 0.12.5: digit replacement, inserted equals, separated digits, removed space, trailing space, replaced operator, a digit edit after a Unicode prefix, and multiline changes with unchanged context. Tests assert actual changed columns from Neovim's diff engine.
- **Dusk → Dawn → Dusk restores Dusk's prior resolved highlights.** Tracked Dusk palette and generated theme artifacts remain unchanged.

## Honest limitations

Diff hue distances do not meet the old separation threshold under every color-vision simulation. These failures are now reported as informational instead of being counted as passed gates: Dawn's diff contract relies on explicit markers and underlined spans. There is no claim that colors alone distinguish changes in grayscale.

Computer Use rejected access to Ghostty for safety reasons. Native window inspection was therefore not performed. Codex CLI 0.154.0 is available, but its themed interactive diff was not visually verified. Claude Code is absent from PATH. Native agent validation and long-session comfort remain open work, not successful checks.

The dark-foreground rule covers the styles controlled by Dawn. An application can still emit explicit truecolor or inverse video, and conventional terminal ANSI white endpoints remain light for compatibility. The terminal palette cannot globally prevent such output. Ghostty's existing faint-opacity and minimum-contrast safeguards remain in the Dawn export.

The bundled dynamic wallpaper and shared Firefox/system-selection artifacts still represent the prior design. They were intentionally not regenerated from Dawn in this milestone because they also serve Dusk. Old review reports describe their historical revisions.

## Run locally

From this checkout, with dependencies available:

```sh
uv run python scripts/build.py
uv run python -m unittest discover -s tests
ZENBONES_ROOT=/path/to/zenbones.nvim LUSH_ROOT=/path/to/lush.nvim \
  nvim --headless -u NONE -i NONE -l scripts/check_day_diff.lua
ZENBONES_ROOT=/path/to/zenbones.nvim LUSH_ROOT=/path/to/lush.nvim \
  KANSO_ROOT=/path/to/kanso.nvim \
  nvim --headless -u NONE -i NONE -l scripts/check_formex_dawn.lua
uv run python scripts/check_dawn_contrast.py
```

For interactive Neovim, add the checkout and dependencies to runtimepath, enable `termguicolors`, and select `ithilien-dawn`. Set `diffopt` to include `internal,inline:char` for exact changes. Applying a colorscheme alone does not choose the diff algorithm.

Next milestone: native agent/window verification, application-specific treatment of selection boundaries, and several ordinary coding/review sessions before release.
