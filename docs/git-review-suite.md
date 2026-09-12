# Git review regression suite

The first compatibility profile loads pinned Diffview, Neogit, Gitsigns, Plenary,
and Kanso checkouts, without loading or changing your personal Neovim setup.
The Ithilien palette remains frozen.

```sh
# One-time dependency fetch, then the full 12-case matrix:
.venv/bin/python scripts/evaluate_git_review.py --fetch-dependencies
# Subsequent unattended runs require no network:
.venv/bin/python scripts/evaluate_git_review.py
# Include this required gate in the combined evaluation:
.venv/bin/python scripts/evaluate_suite.py --git-review
```

Revisions and source URLs are in `evaluation/git-review-dependencies.json`.
Missing dependencies, modified checkouts, revision mismatches, missing windows,
and renderer errors fail the run. Fetching never updates an existing checkout.
To deliberately upgrade a dependency, update its pin and check it out explicitly.

| Plugin | Rendered coverage | Not yet covered |
|---|---|---|
| Diffview | Two-way Python working-tree diff; exact edited digit on both sides | Three-way conflicts, history, search/selection overlays |
| Neogit | Staged file and untracked file in status | Expanded hunks, commit popup, conflict resolution |
| Gitsigns | Actual floating hunk preview and inline digit emphasis | Staged preview, inline preview, search overlays |

Every scene runs at 100 and 160 columns, initially and after a colorscheme reload.
The fixture includes a digit replacement and operator deletion. The automated
character-emphasis assertion currently targets the digit, not the operator.
Rendered foreground/background membership and a 4.5:1 text-contrast floor are
checked throughout. Mutation tests reject absent panes, misplaced emphasis,
off-palette colors, and low-contrast text. Git commands only touch a temporary
repository; hooks are not installed and commits are not signed.

Outputs include a gallery, native RGB cell evidence, dependency pins, Neovim
version, fixture digest, palette digest, and the configured rendering profile.
The gallery uses Berkeley Mono Medium at 16 pt. It reconstructs Neovim cells;
it does not verify Ghostty pixels, font availability, or long-session comfort.

Initial result: 12/12 passed after mapping Neogit's section headers and modified
file labels to Anduin. Their upstream defaults previously produced 48
out-of-palette, low-contrast cells per Neogit capture.

Next coverage milestones: expanded Git hunks and conflicts, then isolated pytest
and debugpy workflows with Neotest and DAP UI. Picker alternatives and contextual
navigation follow. These remain untested until their actual renderers are added;
this profile does not imply complete plugin support.
