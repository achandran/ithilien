# README generation

Edit `docs/templates/README.md`, then run `uv run python scripts/build.py`.
The build regenerates the palette chart, native Python syntax and diff images, provenance,
and README together. Do not edit the generated README or images directly.

The images require macOS, Swift/AppKit, Neovim, the `../kanso` checkout,
and Berkeley Mono Medium (regular and oblique OTF files in `~/Library/Fonts`).
Missing dependencies fail the build rather than silently keeping a stale image.
The synthetic Python fixture lives in `evaluation/fixtures/readme`.

This is a rasterization of Neovim's external UI cells with built-in Python
syntax, not a terminal screenshot or a Tree-sitter/LSP capture. Its provenance
records the palette hash, Neovim version and Kanso revision.

Both previews preserve captured foreground/background colors and bold/italic text styles. They are not native Ghostty screenshots.
