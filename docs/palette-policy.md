# Palette policy and history

## Approval constraints

The approved baseline includes the user-selected consolidated ANSI mapping
(promoted after ad04b15). The prior mapping is preserved in
tests/fixtures/ansi-baseline.json. Do not optimize or change
its colors without an explicit new palette decision. The canonical fingerprint
in tests/test_palette_identity.py enforces this freeze.

- Briar #B8595C: cursor and selection backgrounds, black interaction text.
- Regular/bright chromatic slots share Annûn #8B3037, Sage #315F46,
  Mallorn #795922, Anduin #345E77, Thyme #70516D, and Rauros #255354.
- The four neutral ANSI slots remain distinct.
- Removed named Lua colors: Fir, Filbert, Eventide and Hyacinth. Callers can
  migrate to Sage, Mallorn, Anduin and Thyme respectively; these have different hex values.
- Poros and Stillwater are consolidated as Rauros #255354 for cyan and aqua text.
  Named Lua callers should migrate both former names to Rauros. Interaction colors are unchanged.
- Approved four-color diff model: Pelennor #E2EDDF added lines, Eglantine #F1E2DF
  deleted lines, Spray #D7E3EA changed lines, Celandine #D8B46A all edited spans.
- Removed named colors Ilex and Rose; addEmphasis/deleteEmphasis now use Celandine.
  All diff text stays black. Search/conflict remains separately mapped to Heather.
- Ash user/hostname, blue directory, purple Git, black command-entry symbol.
- Interpret palette colors as sRGB. Display P3 reinterpretation is not evaluated.
- Interaction text minimum: WCAG contrast 4.5:1; ordinary text and diff gates remain.

The 4.62:1 interaction candidate passed the supported native evaluation suite.
This is not proof of native Ghostty, fzf, Firefox focused-state behavior, Claude
Code rendering, or long-session comfort. These require separate validation.

The user also approved consolidating Faramir and Juniper onto Ash #505456.
Secondary text and interaction borders retain their roles but share the muted
text color. Named Lua callers should migrate Faramir/Juniper to Ash.

These records use the names at the time of approval. For subsequent naming
changes and current role mappings, use the generated [palette reference](palette-names.md).

## Design history

Dawn evolved through parchment, black-text, neutral-white, and consolidated ANSI
experiments. Those studies helped establish the current black reading text,
restrained syntax, Briar selection, and ordinary-weight diff emphasis. They are
historical design evidence, not validation of the current theme.

The pre-cleanup snapshot is commit
[`b6b766b`](https://github.com/achandran/ithilien/tree/b6b766b66fcd2d5d8d58a0aedf3b7e06ae7a3223).
It preserves the removed `reports/day-*`, `reports/python-review`,
`design/formex-dawn`, Formex implementation reports, identity-rename record,
and their one-off review and palette-experiment scripts. Use that revision to
inspect historical artifacts; do not regenerate old reports with today's palette
and treat them as the original experiment.

Current approval constraints are above; current names and roles are in
[palette names](palette-names.md).

### ANSI consolidation

The adopted mapping shares each regular/bright chromatic pair while preserving
separate neutral roles. It chooses existing colors for a restrained terminal
palette without recoloring syntax roles merely to reduce the color count.
At adoption, the names were Annûn, Sage, Mallorn, Anduin, Thyme, and Rauros.
Approval of this mapping did not establish native rendering quality or comfort;
those require separate evaluation. Later approved naming and role consolidations
are recorded in the approval constraints above.

The pre-consolidation palette is retained in
[the regression fixture](../tests/fixtures/ansi-baseline.json). The full historical
study, candidate measurements, manual comparison kit, and experiment viewer remain
available at [commit cd88baf](https://github.com/achandran/ithilien/tree/cd88baf8468f8046a0b0f254d6f5c43525bb8579).

### Current evidence

`make build` generates Dawn and Dusk palette audits into ignored
`tests/evaluation/results/palette/` before generating the README palette chart. Native
evidence also belongs in ignored `tests/evaluation/results/`; see
[development](development.md) for execution and coverage limits. Saved native
captures and dependency builds were preserved so offline analysis remains available.


The reusable evaluation engine was subsequently extracted into
[Tintprobe](https://github.com/achandran/tintprobe). Its repository preserves the
shared source history. Ithilien retains its approved palette policy and native
plugin assertions, and pins the evaluator used to generate measurements.

### Warm Graphite Dusk

Dawn's palette is fixed. The approved Dusk direction uses graphite `#202120`,
warm stone-gray reading text `#BDB7AB`, raised graphite `#282A28`, and supporting
text `#AAA497`. Dusk has exactly 18 named colors, sharing Briar, Celandine,
Heather, and Lebethron with Dawn. Both variants use black interaction text and
ordinary-weight exact edits. Dusk typography is Berkeley Mono Retina 16 pt;
Dawn remains Berkeley Mono Medium 16 pt.

See [Dusk design and validation](dusk-design.md) for scope and evidence.
