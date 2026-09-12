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
and [palette names](palette-names.md). The retained
[ANSI study](../reports/ansi-consolidation/report.md) documents the adopted mapping;
its baseline is also a regression-test fixture. Names in that historical study
predate the current naming scheme.

Current palette audits are `reports/ithilien-dawn-audit.*` and
`reports/ithilien-dusk-audit.*`. Current native evidence belongs in ignored
`evaluation/results/`; see [development](development.md) for execution and
coverage limits. Existing saved native captures and dependency builds were
preserved during cleanup so offline analysis remains available.
