# Ithilien Dawn

A light theme for reading code, reviewing changes, and working alongside coding agents.

Porcelain whites. Black type. Steel neutrals. A small, deliberate red accent.

![Ithilien Dawn — Python code and character-level diffs in Neovim](assets/ithilien-dawn-neovim.png)

**Read the code. Find the change.** Four diff backgrounds: green for added lines, red for deleted lines, blue for changed lines, and amber for the exact edited characters. Clients with separate added/deleted word highlights use the same amber for both. Diff emphasis keeps ordinary text weight, so even a one-character edit stands out through color.

[Palette](#palette) · [Design](#design) · [Install](#install) · [Preview details](docs/readme-generation.md)

## Palette

![Ithilien Dawn palette — names, hex values, and semantic roles](assets/ithilien-dawn-palette.svg)

Colors are grouped by surfaces and text, interaction, diffs, and terminal colors. Poros is an aqua text accent; the terminal group contains the six consolidated ANSI colors. Each swatch shows its palette name, a representative role, and exact hex value. Shared colors can serve additional roles; see the full reference below.

The palette and preview images are generated from the theme sources so they stay in sync. The Neovim image above uses actual captured UI-cell colors, rasterized with Berkeley Mono Medium at 16 pt. It shows built-in Python syntax, not a Tree-sitter/LSP configuration or a native Ghostty screenshot.

[Full palette reference](docs/palette-names.md) · [Interactive palette — click swatches to copy hex](palette-preview.html)

Open `palette-preview.html` locally to copy any swatch with a click or Enter. GitHub’s static README images cannot access the clipboard.

## Design

Dawn takes its visual direction from the **Formex Reef GMT with a white dial, black ceramic bezel, and stainless steel bracelet**: clear markings on a quiet surface, metallic neutrals, and red used deliberately for interaction. Its color names draw from Tolkien’s Ithilien and the wider world of Middle-earth.

The aim is a working environment that stays legible without turning every token into an accent. Black carries the text. Muted syntax colors distinguish structure. Stronger backgrounds identify changes, search matches, and selection.

- **Precise diffs.** Locate added, removed, and changed code, down to individual characters and punctuation.
- **Readable agent sessions.** Support code, explanations, patches, and tool output in Codex and Claude Code. Native Codex replay is tested; Claude Code coverage is still developing.
- **Long-session comfort.** Light surfaces, dark text, and restrained decoration are design goals. Automated contrast checks support them; they do not prove comfort.
- **Consistent interactions.** Afterglow marks selection and the cursor with black foreground text. Search and inline edits use different hues.

The Neovim implementation builds on [Kansō](https://github.com/webhooked/kanso.nvim), with Ithilien’s palette and highlight mappings. Dusk is also included as a dark variant; Dawn is the focus of the current design and evaluation work.

## Install

Requires Git and Python 3. Neovim also requires the dependencies described in the [installation guide](docs/installation.md).

```sh
git clone https://github.com/achandran/ithilien.git
cd ithilien
./install.sh
```

The installer configures detected apps, skips missing ones, and backs up replaced files. On macOS it also sets the system text-selection color. Keep the checkout in place: Neovim loads the theme from it.

```sh
./install.sh --dry-run             # inspect the changes first
./install.sh --only ghostty nvim   # install selected integrations
```

To update, run `git pull` followed by `./install.sh`. Follow the installer’s reload and activation instructions; some apps require manual theme selection.

[Installation and supported integrations](docs/installation.md) · [How previews are generated](docs/readme-generation.md)
