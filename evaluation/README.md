# Ithilien evaluation profile

The shared evaluator now lives in [Tintprobe](https://github.com/achandran/tintprobe).
Ithilien pins its revision and declares its inputs in `../tintprobe.json`.

This directory keeps project-specific policy: theme adapters, a rubric, the Formex
aesthetic reference, plugin workflow Lua, and their dependency pins. They are
Ithilien expectations, not universal color-scheme requirements. Python adapters
live in `tests/workflows/`; palette and plugin regressions remain with the theme.

Shared source fixtures, capture code, color mathematics, and reporting ship with
Tintprobe. `deps/`, `results/`, and `local.mk` remain ignored local state.
See [development](../docs/development.md) for supported commands.

The rubric explicitly retains Ithilien’s experimental weighted totals with
`legacy_weighted_score: true`. Standalone Tintprobe comparisons leave totals off
by default; these totals remain project heuristics, not a universal theme ranking.
