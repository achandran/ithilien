# C / Soft parchment palette audit

Overall: **FAIL**

WCAG ratios use unrounded values for gates. Normal text requires 4.5:1; 7:1 is an internal enhanced target where specified. APCA floors and ΔEOK floors are project heuristics, not WCAG conformance. A palette PASS does not certify applications or color-only semantics.

## Text contrast

| Role | WCAG | APCA Lc | Result |
|---|---:|---:|---|
| muted UI | 4.94:1 | 65.7 | PASS |
| comments | 5.12:1 | 66.7 | PASS |
| secondary text | 6.82:1 | 74.2 | FAIL |
| normal text | 9.52:1 | 82.2 | PASS |
| bright text | 11.92:1 | 86.6 | PASS |
| highlighted text | 5.32:1 | 37.5 | PASS |
| highlight edge on C / Soft parchment | 3.13:1 | 51.3 | PASS |
| highlight edge on white | 3.95:1 | 66.6 | PASS |
| syntax olive | 5.12:1 | 66.7 | PASS |
| syntax sage | 5.35:1 | 67.8 | PASS |
| syntax gold | 7.11:1 | 75.2 | PASS |
| syntax ochre | 5.0:1 | 65.9 | PASS |
| syntax clay | 5.48:1 | 68.3 | PASS |
| syntax coral | 5.45:1 | 67.5 | PASS |
| syntax aqua | 5.29:1 | 67.4 | PASS |
| syntax blue | 5.51:1 | 68.6 | PASS |
| syntax mauve | 5.28:1 | 67.5 | PASS |
| diff add | 7.63:1 | 65.8 | PASS |
| diff delete | 7.75:1 | 72.1 | PASS |
| diff change | 8.2:1 | 79.7 | PASS |
| diff hunk | 7.92:1 | 75.4 | PASS |
| inline add | 9.81:1 | 61.9 | PASS |
| inline delete | 10.16:1 | 63.7 | PASS |
| inline change | 10.24:1 | 64.0 | PASS |
| inline diff marker | 5.32:1 | 37.5 | PASS |
| conflict marker | 7.65:1 | 72.1 | PASS |
| ANSI black | 11.92:1 | 86.6 | PASS |
| ANSI red | 6.64:1 | 72.9 | PASS |
| ANSI green | 6.11:1 | 71.4 | PASS |
| ANSI yellow | 7.69:1 | 77.0 | PASS |
| ANSI blue | 7.72:1 | 77.2 | PASS |
| ANSI magenta | 6.34:1 | 72.3 | PASS |
| ANSI cyan | 7.33:1 | 75.8 | PASS |
| ANSI white | 6.82:1 | 74.2 | PASS |
| ANSI brightBlack | 4.94:1 | 65.7 | PASS |
| ANSI brightRed | 5.45:1 | 67.5 | PASS |
| ANSI brightGreen | 5.35:1 | 67.8 | PASS |
| ANSI brightYellow | 7.11:1 | 75.2 | PASS |
| ANSI brightBlue | 5.51:1 | 68.6 | PASS |
| ANSI brightMagenta | 5.28:1 | 67.5 | PASS |
| ANSI brightCyan | 5.29:1 | 67.4 | PASS |
| ANSI brightWhite | 9.52:1 | 82.2 | PASS |
| ANSI extendedOchre | 5.0:1 | 65.9 | PASS |
| ANSI extendedClay | 5.48:1 | 68.3 | PASS |
| muted on base | 4.94:1 | 65.7 | PASS |
| comment on base | 5.12:1 | 66.7 | PASS |
| subtext on base | 6.82:1 | 74.2 | PASS |
| text on base | 9.52:1 | 82.2 | PASS |
| bright on base | 11.92:1 | 86.6 | PASS |
| olive on base | 5.12:1 | 66.7 | PASS |
| sage on base | 5.35:1 | 67.8 | PASS |
| gold on base | 7.11:1 | 75.2 | PASS |
| ochre on base | 5.0:1 | 65.9 | PASS |
| clay on base | 5.48:1 | 68.3 | PASS |
| coral on base | 5.45:1 | 67.5 | PASS |
| aqua on base | 5.29:1 | 67.4 | PASS |
| blue on base | 5.51:1 | 68.6 | PASS |
| mauve on base | 5.28:1 | 67.5 | PASS |
| muted on mantle | 4.75:1 | 63.3 | PASS |
| comment on mantle | 4.93:1 | 64.4 | PASS |
| subtext on mantle | 6.56:1 | 71.9 | PASS |
| text on mantle | 9.16:1 | 79.8 | PASS |
| bright on mantle | 11.48:1 | 84.2 | PASS |
| olive on mantle | 4.93:1 | 64.3 | PASS |
| sage on mantle | 5.15:1 | 65.5 | PASS |
| gold on mantle | 6.85:1 | 72.8 | PASS |
| ochre on mantle | 4.81:1 | 63.6 | PASS |
| clay on mantle | 5.28:1 | 65.9 | PASS |
| coral on mantle | 5.25:1 | 65.2 | PASS |
| aqua on mantle | 5.09:1 | 65.0 | PASS |
| blue on mantle | 5.31:1 | 66.3 | PASS |
| mauve on mantle | 5.08:1 | 65.1 | PASS |
| muted on surface0 | 5.27:1 | 69.9 | PASS |
| comment on surface0 | 5.47:1 | 70.9 | PASS |
| subtext on surface0 | 7.28:1 | 78.4 | PASS |
| text on surface0 | 10.17:1 | 86.4 | PASS |
| bright on surface0 | 12.74:1 | 90.8 | PASS |
| olive on surface0 | 5.47:1 | 70.9 | PASS |
| sage on surface0 | 5.71:1 | 72.0 | PASS |
| gold on surface0 | 7.6:1 | 79.3 | PASS |
| ochre on surface0 | 5.34:1 | 70.1 | PASS |
| clay on surface0 | 5.86:1 | 72.4 | PASS |
| coral on surface0 | 5.82:1 | 71.7 | PASS |
| aqua on surface0 | 5.65:1 | 71.6 | PASS |
| blue on surface0 | 5.89:1 | 72.8 | PASS |
| mauve on surface0 | 5.63:1 | 71.6 | PASS |
| muted on surface1 | 4.84:1 | 64.5 | PASS |
| comment on surface1 | 5.02:1 | 65.5 | PASS |
| subtext on surface1 | 6.69:1 | 73.0 | PASS |
| text on surface1 | 9.34:1 | 81.0 | PASS |
| bright on surface1 | 11.69:1 | 85.4 | PASS |
| olive on surface1 | 5.03:1 | 65.5 | PASS |
| sage on surface1 | 5.24:1 | 66.6 | PASS |
| gold on surface1 | 6.98:1 | 73.9 | PASS |
| ochre on surface1 | 4.9:1 | 64.7 | PASS |
| clay on surface1 | 5.38:1 | 67.1 | PASS |
| coral on surface1 | 5.35:1 | 66.3 | PASS |
| aqua on surface1 | 5.18:1 | 66.2 | PASS |
| blue on surface1 | 5.41:1 | 67.4 | PASS |
| mauve on surface1 | 5.17:1 | 66.2 | PASS |
| chrome text on crust | 7.76:1 | 70.1 | PASS |
| chrome subtext on crust | 5.56:1 | 62.2 | PASS |
| chrome bright on crust | 9.72:1 | 74.5 | PASS |
| chrome text on surface2 | 6.36:1 | 59.6 | PASS |
| chrome subtext on surface2 | 4.56:1 | 51.6 | PASS |
| chrome bright on surface2 | 7.97:1 | 64.0 | PASS |
| inactive status label | 4.75:1 | 63.3 | PASS |
| popup border | 5.27:1 | 69.9 | PASS |
| search result | 5.32:1 | 37.5 | PASS |
| selected popup kind | 5.32:1 | 37.5 | PASS |
| selected popup extra | 5.32:1 | 37.5 | PASS |
| substitution | 5.32:1 | 37.5 | PASS |
| error annotation | 5.45:1 | -71.0 | PASS |
| tab label on crust | 5.56:1 | 62.2 | PASS |
| Neovim DiffText | 5.32:1 | 37.5 | PASS |
| selection edge on mantle | 3.02:1 | 48.9 | PASS |
| selection edge on surface0 | 3.35:1 | 55.5 | PASS |
| selection edge on surface1 | 3.07:1 | 50.1 | PASS |
| git add sign | 10.56:1 | 84.3 | PASS |
| git delete sign | 8.84:1 | 80.1 | PASS |
| git change sign | 7.97:1 | 77.9 | PASS |
| status olive | 5.12:1 | -70.3 | PASS |
| status sage | 5.35:1 | -71.4 | PASS |
| status mauve | 5.28:1 | -71.0 | PASS |
| status coral | 5.45:1 | -71.0 | PASS |
| status gold | 7.11:1 | -78.1 | PASS |

## Semantic separation under color-vision simulations

Values are ΔEOK distances. They are comparative signals, not universal accessibility thresholds.

| Pair | Normal | Protan | Deutan | Tritan | Gray | Result |
|---|---:|---:|---:|---:|---:|---|
| diff add/delete | 0.127 | 0.061 | 0.072 | 0.142 | 0.059 | PASS |
| diff add/change | 0.123 | 0.101 | 0.117 | 0.127 | 0.11 | PASS |
| diff delete/change | 0.074 | 0.061 | 0.056 | 0.059 | 0.051 | PASS |
| error/warning | 0.151 | 0.054 | 0.085 | 0.15 | 0.062 | PASS |
| ANSI blue/bright blue | 0.079 | 0.082 | 0.078 | 0.079 | 0.079 | PASS |
| ANSI cyan/bright cyan | 0.076 | 0.079 | 0.074 | 0.076 | 0.076 | PASS |

## Close accent pairs for visual review

- `olive/ochre`: ΔEOK 0.036
- `sage/aqua`: ΔEOK 0.044
- `olive/sage`: ΔEOK 0.047

## Syntax and diagnostic role review (not gates)

Color alone does not preserve these roles in every simulation. Keywords use bold by default in Day; numbers have literal syntax. Diagnostic signs/messages must retain severity labels; diffs retain + / - / ~ and inline bold.

| Pair | Normal | Protan | Deutan | Tritan | Gray |
|---|---:|---:|---:|---:|---:|
| numbers/keywords | 0.0708 | 0.0566 | 0.0302 | 0.0526 | 0.0216 |
| information/hints | 0.0778 | 0.0663 | 0.0597 | 0.0258 | 0.0098 |
| operators/strings | 0.0466 | 0.029 | 0.0378 | 0.0598 | 0.0098 |
| keywords/errors | 0.059 | 0.0246 | 0.0131 | 0.064 | 0.0013 |

## Inline fill versus line background (observations)

These are not text contrast gates. Day uses black inline text with bold and underline in GitSigns; lighter fills trade some boundary contrast for text readability.

- add: fill/line contrast 1.231:1; grayscale ΔEOK 0.0602
- delete: fill/line contrast 1.44:1; grayscale ΔEOK 0.1092
- change: fill/line contrast 1.676:1; grayscale ΔEOK 0.1583
