# Ithilien Dusk palette audit

Overall: **PASS**

WCAG ratios use unrounded values for gates. Normal text requires 4.5:1; 7:1 is an internal enhanced target where specified. APCA floors and ΔEOK floors are project heuristics, not WCAG conformance. A palette PASS does not certify applications or color-only semantics.

## Text contrast

| Role | WCAG | APCA Lc | Result |
|---|---:|---:|---|
| muted UI | 3.72:1 | -27.3 | PASS |
| comments | 6.21:1 | -45.7 | PASS |
| secondary text | 8.04:1 | -57.3 | PASS |
| normal text | 9.33:1 | -64.8 | PASS |
| bright text | 12.09:1 | -79.7 | PASS |
| highlighted text | 5.32:1 | 37.5 | PASS |
| highlight edge on Ithilien Dusk | 4.53:1 | -34.0 | PASS |
| highlight edge on white | 3.95:1 | 66.6 | PASS |
| syntax olive | 7.56:1 | -54.4 | PASS |
| syntax sage | 7.94:1 | -56.7 | PASS |
| syntax gold | 8.97:1 | -62.9 | PASS |
| syntax ochre | 7.1:1 | -51.6 | PASS |
| syntax clay | 6.1:1 | -45.2 | PASS |
| syntax coral | 6.23:1 | -46.2 | PASS |
| syntax aqua | 6.98:1 | -50.8 | PASS |
| syntax blue | 7.81:1 | -55.9 | PASS |
| syntax mauve | 6.9:1 | -50.2 | PASS |
| diff add | 9.94:1 | -77.0 | PASS |
| diff delete | 8.34:1 | -63.3 | PASS |
| diff change | 7.84:1 | -68.6 | PASS |
| diff hunk | 8.63:1 | -67.0 | PASS |
| inline add | 7.09:1 | -71.1 | PASS |
| inline delete | 7.83:1 | -73.0 | PASS |
| inline change | 7.34:1 | -71.8 | PASS |
| inline diff marker | 5.32:1 | 37.5 | PASS |
| conflict marker | 7.79:1 | -63.5 | PASS |
| ANSI red | 6.23:1 | -46.2 | PASS |
| ANSI green | 7.94:1 | -56.7 | PASS |
| ANSI yellow | 8.97:1 | -62.9 | PASS |
| ANSI blue | 7.81:1 | -55.9 | PASS |
| ANSI magenta | 6.9:1 | -50.2 | PASS |
| ANSI cyan | 6.98:1 | -50.8 | PASS |
| ANSI white | 8.04:1 | -57.3 | PASS |
| ANSI brightBlack | 3.72:1 | -27.3 | PASS |
| ANSI brightRed | 9.27:1 | -64.6 | PASS |
| ANSI brightGreen | 12.04:1 | -79.4 | PASS |
| ANSI brightYellow | 10.8:1 | -73.0 | PASS |
| ANSI brightBlue | 10.04:1 | -68.8 | PASS |
| ANSI brightMagenta | 9.55:1 | -66.1 | PASS |
| ANSI brightCyan | 10.05:1 | -68.8 | PASS |
| ANSI brightWhite | 12.09:1 | -79.7 | PASS |
| ANSI extendedOchre | 7.1:1 | -51.6 | PASS |
| ANSI extendedClay | 6.1:1 | -45.2 | PASS |

## Semantic separation under color-vision simulations

Values are ΔEOK distances. They are comparative signals, not universal accessibility thresholds.

| Pair | Normal | Protan | Deutan | Tritan | Gray | Result |
|---|---:|---:|---:|---:|---:|---|
| diff add/delete | 0.135 | 0.112 | 0.061 | 0.141 | 0.079 | PASS |
| diff add/change | 0.066 | 0.062 | 0.049 | 0.082 | 0.037 | PASS |
| diff delete/change | 0.1 | 0.091 | 0.066 | 0.065 | 0.066 | PASS |
| error/warning | 0.138 | 0.135 | 0.093 | 0.123 | 0.1 | PASS |
| ANSI blue/bright blue | 0.074 | 0.069 | 0.074 | 0.075 | 0.072 | PASS |
| ANSI cyan/bright cyan | 0.105 | 0.101 | 0.104 | 0.105 | 0.103 | PASS |

## Close accent pairs for visual review

- `olive/sage`: ΔEOK 0.019
- `clay/coral`: ΔEOK 0.035
- `aqua/blue`: ΔEOK 0.046

## Syntax and diagnostic role review (not gates)

Color alone does not preserve these roles in every simulation. Keywords use bold by default in Day; numbers have literal syntax. Diagnostic signs/messages must retain severity labels; diffs retain + / - / ~ and inline bold.

| Pair | Normal | Protan | Deutan | Tritan | Gray |
|---|---:|---:|---:|---:|---:|
| numbers/keywords | 0.0572 | 0.056 | 0.0389 | 0.0486 | 0.0403 |
| information/hints | 0.0461 | 0.0399 | 0.0396 | 0.0349 | 0.0306 |
| operators/strings | 0.0192 | 0.0177 | 0.0119 | 0.0231 | 0.0134 |
| keywords/errors | 0.0352 | 0.0202 | 0.0152 | 0.0286 | 0.0054 |

## Inline fill versus line background (observations)

These are not text contrast gates. Day uses black inline text with bold and underline in GitSigns; lighter fills trade some boundary contrast for text readability.

- add: fill/line contrast 1.408:1; grayscale ΔEOK 0.0923
- delete: fill/line contrast 1.39:1; grayscale ΔEOK 0.0959
- change: fill/line contrast 1.196:1; grayscale ΔEOK 0.0465

## Changed-line fill versus canvas (observations)

ΔEOK by mode: normal 0.112, protan 0.1042, deutan 0.1138, tritan 0.1129, grayscale 0.1077. These are comparative signals; line markers and inline emphasis remain necessary.

## Expanded surface observations (legacy Night; not gated)

- muted on base: 3.72:1 (target 4.5; below)
- comment on base: 6.21:1 (target 4.5; meets)
- subtext on base: 8.04:1 (target 4.5; meets)
- text on base: 9.33:1 (target 4.5; meets)
- bright on base: 12.09:1 (target 4.5; meets)
- olive on base: 7.56:1 (target 4.5; meets)
- sage on base: 7.94:1 (target 4.5; meets)
- gold on base: 8.97:1 (target 4.5; meets)
- ochre on base: 7.1:1 (target 4.5; meets)
- clay on base: 6.1:1 (target 4.5; meets)
- coral on base: 6.23:1 (target 4.5; meets)
- aqua on base: 6.98:1 (target 4.5; meets)
- blue on base: 7.81:1 (target 4.5; meets)
- mauve on base: 6.9:1 (target 4.5; meets)
- muted on mantle: 3.86:1 (target 4.5; below)
- comment on mantle: 6.43:1 (target 4.5; meets)
- subtext on mantle: 8.33:1 (target 4.5; meets)
- text on mantle: 9.67:1 (target 4.5; meets)
- bright on mantle: 12.53:1 (target 4.5; meets)
- olive on mantle: 7.83:1 (target 4.5; meets)
- sage on mantle: 8.22:1 (target 4.5; meets)
- gold on mantle: 9.3:1 (target 4.5; meets)
- ochre on mantle: 7.36:1 (target 4.5; meets)
- clay on mantle: 6.33:1 (target 4.5; meets)
- coral on mantle: 6.46:1 (target 4.5; meets)
- aqua on mantle: 7.23:1 (target 4.5; meets)
- blue on mantle: 8.09:1 (target 4.5; meets)
- mauve on mantle: 7.15:1 (target 4.5; meets)
- muted on surface0: 3.35:1 (target 4.5; below)
- comment on surface0: 5.6:1 (target 4.5; meets)
- subtext on surface0: 7.24:1 (target 4.5; meets)
- text on surface0: 8.41:1 (target 4.5; meets)
- bright on surface0: 10.9:1 (target 4.5; meets)
- olive on surface0: 6.82:1 (target 4.5; meets)
- sage on surface0: 7.15:1 (target 4.5; meets)
- gold on surface0: 8.09:1 (target 4.5; meets)
- ochre on surface0: 6.4:1 (target 4.5; meets)
- clay on surface0: 5.5:1 (target 4.5; meets)
- coral on surface0: 5.62:1 (target 4.5; meets)
- aqua on surface0: 6.29:1 (target 4.5; meets)
- blue on surface0: 7.04:1 (target 4.5; meets)
- mauve on surface0: 6.22:1 (target 4.5; meets)
- muted on surface1: 2.97:1 (target 4.5; below)
- comment on surface1: 4.95:1 (target 4.5; meets)
- subtext on surface1: 6.4:1 (target 4.5; meets)
- text on surface1: 7.43:1 (target 4.5; meets)
- bright on surface1: 9.64:1 (target 4.5; meets)
- olive on surface1: 6.03:1 (target 4.5; meets)
- sage on surface1: 6.32:1 (target 4.5; meets)
- gold on surface1: 7.15:1 (target 4.5; meets)
- ochre on surface1: 5.66:1 (target 4.5; meets)
- clay on surface1: 4.86:1 (target 4.5; meets)
- coral on surface1: 4.97:1 (target 4.5; meets)
- aqua on surface1: 5.56:1 (target 4.5; meets)
- blue on surface1: 6.22:1 (target 4.5; meets)
- mauve on surface1: 5.5:1 (target 4.5; meets)
- chrome text on crust: 9.9:1 (target 4.5; meets)
- chrome subtext on crust: 8.53:1 (target 4.5; meets)
- chrome bright on crust: 12.83:1 (target 4.5; meets)
- chrome text on surface2: 6.2:1 (target 4.5; meets)
- chrome subtext on surface2: 5.34:1 (target 4.5; meets)
- chrome bright on surface2: 8.03:1 (target 4.5; meets)
- inactive status label: 3.86:1 (target 4.5; below)
- popup border: 1.36:1 (target 3.0; below)
- search result: 5.66:1 (target 4.5; meets)
- selected popup kind: 1.78:1 (target 4.5; below)
- selected popup extra: 1.22:1 (target 4.5; below)
- substitution: 1.01:1 (target 4.5; below)
- error annotation: 1.5:1 (target 4.5; below)
- tab label on crust: 3.95:1 (target 4.5; below)
- Neovim DiffText: 5.32:1 (target 4.5; meets)
- selection edge on mantle: 4.69:1 (target 3.0; meets)
- selection edge on surface0: 4.08:1 (target 3.0; meets)
- selection edge on surface1: 3.61:1 (target 3.0; meets)
- git add sign: 12.04:1 (target 4.5; meets)
- git delete sign: 9.27:1 (target 4.5; meets)
- git change sign: 10.8:1 (target 4.5; meets)
- status olive: 7.56:1 (target 4.5; meets)
- status sage: 7.94:1 (target 4.5; meets)
- status mauve: 6.9:1 (target 4.5; meets)
- status coral: 6.23:1 (target 4.5; meets)
- status gold: 8.97:1 (target 4.5; meets)
