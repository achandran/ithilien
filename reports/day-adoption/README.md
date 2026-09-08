# Accepted Day palette

Warm parchment **`#F0E9D2`**, black neutral text **`#000000`**, and the existing restrained syntax accents are now in the canonical Day palette. All neutral text roles, neutral ANSI entries, and diff-context text use black. Semantic syntax, diagnostic colors, and colored diff-line foregrounds remain intact.

[Code before/after](code-normal.png) · [Agent prose and precise diffs](agent.png) · [Full design rationale](../day-review/README.md) · [Audit](../loden-day-audit.md)

The richer golden changed-line fill **`#F4E3AD`** addresses the parchment experiment's weak line/canvas separation. It increases normal ΔEOK from 0.0111 to 0.0440 against the accepted canvas, while preserving 7.85:1 changed-line text contrast and 3.09:1 against the ochre inline highlight. Changed characters remain black; GitSigns adds underline and bold for precise spans.

Neutral text contrast is **17.29:1**; syntax is **5.18–7.37:1**. Contrast gates have not been weakened. The nine tests and 830 resolved Neovim checks pass. Night is unchanged. The wallpaper and generated Day ports have been refreshed. This is a repository change, not an installation into user applications; it remains uncommitted.

[Protan](code-protan.png) · [Deutan](code-deutan.png) · [Tritan](code-tritan.png) · [Grayscale](code-grayscale.png)

These matched specimens use identical 15 px Berkeley Mono and manually assigned roles. They show individual changed digits, an inserted equals sign, and marked whitespace. They do not prove that a native coding-agent renderer computes those spans correctly. The normal and simulated code samples plus the agent specimen were visually reviewed. Long-session comfort still needs actual use.

The left pane is the [frozen pre-adoption snapshot](before.json), after the black-inline-diff correction but before the parchment/black-neutral adoption. Earlier experiments now reference that snapshot, so their comparisons remain reproducible.

```sh
uv run python scripts/review_adoption.py --png
```
