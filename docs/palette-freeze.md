# Ithilien Dawn palette freeze

The palette at commit 2360cab is the approved baseline. Do not optimize or change
its colors without an explicit new palette decision. The canonical fingerprint
in tests/test_palette_identity.py enforces this freeze.

- Rosehip #B8595C: cursor and selection backgrounds, black interaction text.
- Briar #8B3037: terminal red.
- Ash user/hostname, blue directory, purple Git, black command-entry symbol.
- Interpret palette colors as sRGB. Display P3 reinterpretation is not evaluated.
- Interaction text minimum: WCAG contrast 4.5:1; ordinary text and diff gates remain.

The 4.62:1 interaction candidate passed the supported native evaluation suite.
This is not proof of native Ghostty, fzf, Firefox focused-state behavior, Claude
Code rendering, or long-session comfort. These require separate validation.
