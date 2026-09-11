# Ithilien Dawn palette freeze

The approved baseline includes the user-selected consolidated ANSI mapping
(promoted after ad04b15). The prior mapping is preserved in
reports/ansi-consolidation/baseline.json. Do not optimize or change
its colors without an explicit new palette decision. The canonical fingerprint
in tests/test_palette_identity.py enforces this freeze.

- Afterglow #B8595C: cursor and selection backgrounds, black interaction text.
- Regular/bright chromatic slots share Briar #8B3037, Sage #315F46,
  Mallorn #795922, Anduin #345E77, Thyme #70516D, and Rauros #255354.
- The four neutral ANSI slots remain distinct.
- Removed named Lua colors: Fir, Filbert, Eventide and Hyacinth. Callers can
  migrate to Sage, Mallorn, Anduin and Thyme respectively; these have different hex values.
- Poros and Stillwater are consolidated as Rauros #255354 for cyan and aqua text.
  Named Lua callers should migrate both former names to Rauros. Interaction colors are unchanged.
- Approved four-color diff model: Pelennor #E2EDDF added lines, Eglantine #F1E2DF
  deleted lines, Spray #D7E3EA changed lines, Celandine #D8B46A all edited spans.
- Removed named colors Ilex and Rose; addEmphasis/deleteEmphasis now use Celandine.
  All diff text stays black. Search/conflict remains separately mapped to Clematis.
- Ash user/hostname, blue directory, purple Git, black command-entry symbol.
- Interpret palette colors as sRGB. Display P3 reinterpretation is not evaluated.
- Interaction text minimum: WCAG contrast 4.5:1; ordinary text and diff gates remain.

The 4.62:1 interaction candidate passed the supported native evaluation suite.
This is not proof of native Ghostty, fzf, Firefox focused-state behavior, Claude
Code rendering, or long-session comfort. These require separate validation.

The user also approved consolidating Faramir and Juniper onto Ash #505456.
Secondary text and interaction borders retain their roles but share the muted
text color. Named Lua callers should migrate Faramir/Juniper to Ash.
