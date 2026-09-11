# Ithilien Dawn palette freeze

The approved baseline includes the user-selected consolidated ANSI mapping
(promoted after ad04b15). The prior mapping is preserved in
reports/ansi-consolidation/baseline.json. Do not optimize or change
its colors without an explicit new palette decision. The canonical fingerprint
in tests/test_palette_identity.py enforces this freeze.

- Afterglow #B8595C: cursor and selection backgrounds, black interaction text.
- Regular/bright chromatic slots share Briar #8B3037, Sage #315F46,
  Mallorn #795922, Anduin #345E77, Thyme #70516D, and Stillwater #255354.
- The four neutral ANSI slots remain distinct.
- Removed named Lua colors: Fir, Filbert, Eventide and Hyacinth. Callers can
  migrate to Sage, Mallorn, Anduin and Thyme respectively; these have different hex values.
- Poros remains a separate application accent. Diff and interaction colors are unchanged.
- Ash user/hostname, blue directory, purple Git, black command-entry symbol.
- Interpret palette colors as sRGB. Display P3 reinterpretation is not evaluated.
- Interaction text minimum: WCAG contrast 4.5:1; ordinary text and diff gates remain.

The 4.62:1 interaction candidate passed the supported native evaluation suite.
This is not proof of native Ghostty, fzf, Firefox focused-state behavior, Claude
Code rendering, or long-session comfort. These require separate validation.
