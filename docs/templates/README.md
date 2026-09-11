# Ithilien

Dawn is a light theme inspired by the Formex Reef GMT with a white dial, black ceramic bezel, and stainless steel bracelet. Color names draw from Tolkien’s Ithilien. Dusk is the dark variant.

## Palette

![Ithilien Dawn palette: named colors, hex values, and roles](assets/ithilien-dawn-palette.svg)

[Palette reference](docs/palette-names.md) · [Interactive preview](palette-preview.html)

![Python diff in Neovim](assets/ithilien-dawn-neovim.png)

Native Neovim UI capture, rendered with Berkeley Mono Medium 16pt. Blue marks changed lines; amber marks exact edits.

## Goals

- Clear diffs, including individual changed characters: dark text on amber, without bold or underline in Neovim.
- Readable coding-agent sessions in Codex and Claude Code.
- Comfort for long working sessions, with dark text on light surfaces in Dawn.
- White-dial clarity, steel neutrals, and restrained red accents.

## Install

Requires Git and Python 3.

```sh
git clone https://github.com/achandran/ithilien.git
cd ithilien
./install.sh
```

To update:

```sh
git pull
./install.sh
```

The installer configures detected apps, skips missing ones, and backs up replaced files. On macOS, it also sets the system text-selection color. Keep the checkout in place: Neovim loads the theme from it.

```sh
./install.sh --dry-run             # preview without changes
./install.sh --only ghostty nvim   # install selected integrations
```

Follow the installer’s reload and activation instructions. Some apps require manual theme selection. See [installation details](docs/installation.md).
