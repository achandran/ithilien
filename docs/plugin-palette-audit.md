# Neovim palette membership

Dawn explicitly maps core defaults, Fzf-lua, Bufferline, and Grug-far colors that
otherwise fall outside its palette. Overrides also run after LazyLoad, VeryLazy,
and colorscheme reloads. They do not run when another theme is active. Fzf's
backdrop uses an opaque palette surface instead of a blended gray.

Run the portable semantic regression check from the repository:

```sh
KANSO_ROOT=../kanso nvim --headless -u NONE -i NONE -n -l scripts/check_plugin_semantics.lua
```

Audit your installed Lazy configuration:

```sh
python3 scripts/audit_installed_palette.py --output evaluation/results/plugin-palette
```

Use `--init` and `--lazy-root` for nonstandard installations. This loads your
configuration and installed plugins, substitutes this checkout for Ithilien,
disables Lazy's automatic installation/update checks, and redirects state and
cache to a temporary directory. Your configuration still executes its own code.
The report records startup, plugin loading, and colorscheme reload snapshots.
Any off-palette RGB foreground, background, or special color fails the command,
as does a missing or unloaded configured plugin. Alternate themes and the
OS appearance watcher are explicitly excluded and recorded.

This is a highlight-definition gate, not a claim of exhaustive pixel coverage.
Plugin-local namespaces, terminal ANSI output, image/emoji rendering, and states
created only by interaction need separate rendered checks. Anti-aliasing naturally
produces intermediate pixel colors and should not fail palette membership.
