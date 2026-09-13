# Design history

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

Current decisions and approval constraints live in [palette freeze](palette-freeze.md)
and [palette names](palette-names.md).

## ANSI consolidation

The adopted mapping shares each regular/bright chromatic pair while preserving
separate neutral roles. It chooses existing colors for a restrained terminal
palette without recoloring syntax roles merely to reduce the color count.
The current names are Annûn, Sage, Mallorn, Anduin, Thyme, and Rauros.
Approval of this mapping did not establish native rendering quality or comfort;
those require separate evaluation. Later approved naming and role consolidations
are recorded in the palette freeze.

The pre-consolidation palette is retained in
[the regression fixture](../tests/fixtures/ansi-baseline.json). The full historical
study, candidate measurements, manual comparison kit, and experiment viewer remain
available at [commit cd88baf](https://github.com/achandran/ithilien/tree/cd88baf8468f8046a0b0f254d6f5c43525bb8579).

## Current evidence

`make build` generates Dawn and Dusk palette audits into ignored
`evaluation/results/palette/` before generating the palette preview. Native
evidence also belongs in ignored `evaluation/results/`; see
[development](development.md) for execution and coverage limits. Saved native
captures and dependency builds were preserved so offline analysis remains available.
