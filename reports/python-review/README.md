# Python role correction

Day now gives Python one consistent control-flow hierarchy while preserving black ordinary variables, the parchment canvas, and the existing accent palette.

[Before](before.png) · [After](comparison.png) · [Sample](sample.py) · [Before captures](before.json) · [After captures and tool revisions](neovim.json) · [Check summary](summary.json)

## Result

| Role | Revised treatment | Correction |
|---|---|---|
| Declarations, imports, control flow, async/await, exceptions | Clay, bold, upright | Removes inherited blue/mauve keywords and inconsistent Neovim weight/italics |
| Logical and symbolic operators | Olive, regular weight | Clears TextMate's inherited keyword bold; aligns loop `in` |
| Function definitions and custom calls | Dark gold | TextMate now distinguishes calls from ordinary variables |
| Class definitions and function type annotations | Aqua | TextMate now recognizes custom annotations such as `Path` and `Iterable` |
| Numbers, booleans, `None`, uppercase constants | Ochre | Neovim `None` no longer shares the function color; TextMate uppercase constants gain the literal role |
| Decorators | Ochre | TextMate decorator names and `@` now have intentional emphasis |
| Documentation | Olive-gray | Neovim docstrings now share the secondary documentation role |
| String values | Sage | Preserved |
| Ordinary variables and call arguments | Black | Explicit checks protect against overbroad call/annotation selectors |

The updated preview is calmer: exits and exception handling no longer introduce a blue control-flow family, while bold clay provides a redundant structural cue. Gold calls, aqua annotations, and ochre literals remain restrained. This is a role-mapping improvement, not evidence of universal superiority or a new palette.

## Verification

- **71 parsed role assertions per renderer (142 total)**, including all keywords in the sample, literals, function definitions/calls, decorators, custom annotations, docstrings, and negative checks for ordinary variables and call arguments.
- Minimum non-whitespace foreground contrast **5.18:1** on `#F0E9D2` in both specimens; the review fails below 4.5:1.
- Full palette build passes, including Day's 196 contrast checks and six internal semantic-separation gates with color-vision simulations. Palette colors and thresholds are unchanged.
- **845 resolved Neovim highlight checks**, no failures; Night highlights identical to the baseline checkout. Same-session Night → Day → Night also preserves all initial Night groups and clears Python overrides; disabling bold/italics is checked.
- **Six native character-diff cases** still identify exact changed columns with black, underlined foregrounds. Selection and diff tokens are unchanged.
- **11 existing regression tests** pass. All generated Night artifacts and canonical palettes remain byte-identical to the pre-correction commit `546fdf3`.

The 44-line fixture includes decorators, class members, calls, custom and built-in annotations, nullable unions, literals, docstrings, comments, interpolated strings, asynchronous code, exceptions, context managers, comprehensions, and assertions. Both Python compilation and Tree-sitter parsing succeed; this is a syntax fixture, not application code to execute.

## Method and limits

The left panel reconstructs actual installed Python Tree-sitter captures from isolated Neovim. The right reconstructs actual truecolor ANSI output from bat 0.26.1 using the generated TextMate theme, isolated configuration/cache, and no theme fallback. Both use the same 15 px Berkeley Mono. These are captured-style reconstructions, not application screenshots; no personal editor configuration or LSP was loaded. Bat is an independent integration check, not a claim that every Codex renderer uses identical grammar or styling.

Selectors were checked against the [Python grammar pinned by bat 0.26.1](https://github.com/sublimehq/Packages/blob/759d6eed9b4beed87e602a23303a121c3a6c2fb3/Python/Python.sublime-syntax). That grammar nests generic identifiers inside call, decorator, and annotation scopes. Targeting the identifier matters: broad expression scopes can incorrectly color receivers and arguments. The reproduction test catches that regression.

Remaining differences are explicit:

- Neovim distinguishes `self`, members, imported module names, and interpolation delimiters more richly. TextMate keeps many of these black or secondary-colored.
- Custom function parameter/return annotations are covered; the bundled lexical grammar does not expose the same useful context for every variable annotation. This does not substitute for language-server type knowledge.
- A built-in exception constructor such as `ValueError(...)` remains aqua in TextMate and gold in Neovim; one emphasizes the known type, the other the call role.
- Bat's default ANSI output omits comment/docstring italics. Their shared foreground is verified independently of that typography.

No personal application themes were installed. Production changes comprise Day's Python overrides, the canonical TextMate generator and regenerated Day artifact, and a small theme-loading correction. Changing Neovim's background could recursively reload the previous colorscheme, while Kanso's merging retained Day keyword weight. Suppressing that recursive reload and explicitly resetting the owned style fields makes switching reliable without changing fresh-session Night appearance. The accompanying review tools support combined bold/italic styles and retain the original before snapshot.

## Reproduction

```sh
KANSO_ROOT=/path/to/kanso.nvim \
TS_ROOT=/path/to/nvim-treesitter/runtime \
TS_SITE=/path/to/nvim/site \
uv run python scripts/review_python.py

uv run python scripts/build.py
uv run python -m unittest discover -s tests
uv run python scripts/check_neovim.py /path/to/kanso.nvim --baseline /path/to/old/loden
KANSO_ROOT=/path/to/kanso.nvim nvim --headless -u NONE -i NONE -l scripts/check_day_diff.lua
```

Requires Neovim, its installed Python parser/queries, bat, and the macOS/Berkeley Mono review renderer. Tool and parser revisions are recorded in the captures. `before.json` and `before.png` are fixed pre-correction snapshots; reproduction regenerates only the after evidence.
