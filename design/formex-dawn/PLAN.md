# Ithilien Dawn — Formex direction

## Design brief

Ithilien is the identity; the white-dial Formex Reef GMT on its steel bracelet is the core visual reference. Zenbones supplies the intended typographic foundation. Preserve Ithilien's precise diffs and generated integrations. Dusk is outside this change.

The reference's primary cues are a near-white dial, dark graphite bezel and marker edges, distinct brushed-steel planes, and a very small red GMT accent. Translate these to surfaces, framing and hierarchy; do not simulate metallic textures behind code. Semantic green/amber/blue/purple support reviews and diagnostics even though they are not literal watch colors.

Reference inspected: [white dial and steel bracelet photograph](https://www.watchgecko.com/cdn/shop/products/watches-formex-reef-gmt-white-dial-stainless-steel-bracelet-36223390580899_1445x.jpg?v=1669809405). [Manufacturer page](https://formexwatch.com/watches/reef-gmt-42mm-automatic-cosc-300m-white/). Colors are designed interpretations, not sampled material measurements.

## Baseline

Local branch: `design/formex-dawn`. Baseline: `f864a03992c3dc88eff1817c5c255b0501cdc89a`. Existing palettes and exports stay at that revision while choosing a candidate. Existing tests, reports and actual native diff regression script remain available. No remote branch has been published.

## Milestones

1. **Candidate review (this milestone):** three named draft palettes, identical specimens, grayscale view, specified contrast audit, and a recommendation. Compare surface warmth/brightness independently of syntax and semantic colors.
2. **Selected candidate in Neovim:** integrate Zenbones for Dawn while preserving Dusk's implementation; extend scoped highlights, snapshot resolved values, and run real character diff cases including Unicode and multiline edits. Review native editor screenshots.
3. **Agent and terminal validation:** review actual Ghostty, Codex and Claude Code sessions; test dim output, changed whitespace, wrapping, ANSI and explicit RGB colors. Theme exports cannot control every renderer. Capture baselines and comparisons here; they have not been captured in milestone 1.
4. **Application exports:** generate consistent supported integrations from the selected canonical named palette, document derived shades, validate each in its native interface.
5. **Daily-use evaluation and release:** record several real coding/review sessions under ordinary daylight/evening conditions, address observed issues, and release with reproducible checks and screenshots.

## Candidates

- **A — Neutral white:** closest to a clean white dial; highest canvas luminance of the three. Current design recommendation for fidelity.
- **B — Mineral white:** slightly lower brightness and a subtle warm/green bias. Candidate if A feels too bright in use, but do not assume lower luminance proves comfort.
- **C — Cool steel white:** strongest cool cast; integrates with steel chrome but risks looking icy beside long prose.

Only Asphodel (canvas), Gondor (chrome), Lily (raised surface), and Anemone (active-line surface) change. All syntax, semantic, diff and selection colors are held constant. Palette labels are experimental, not new public theme names.

Named colors reuse existing Ithilien associations and source links. Values are evocative interpretations, not colors specified by Tolkien. The source notes are carried forward, not reverified in this milestone. Functional roles remain separate from color names.

## Acceptance criteria

- Main text and inline diff text: at least 7:1 on supported surfaces.
- Secondary and diagnostic text: at least 4.5:1 on supported surfaces.
- Selection text: at least 7:1. Selection uses dark text on pale steel with a dark outline; the outline against both fill and canvas, and the structural border against canvas, must reach 3:1. All reading surfaces keep dark foreground text, including tabs and selections.
- Exact edits retain explicit foreground, stronger background and underline. Addition/deletion have visible markers; diagnostics have severity labels. Hue is never the sole cue.
- Native integration tests must establish real behavior; HTML spans do not establish actual diff computation.
- Every generated application export must be checked before claiming cross-application consistency.
- Comfort remains a user-observed property, not a contrast score.

## Reproduction and scope

Run `python3 design/formex-dawn/make_candidates.py` to regenerate the three candidates, resolved roles and contrast audit. The comparison fragment currently embeds a snapshot of resolved.json; refresh its `palettes` data when changing candidate values. These draft files are not consumed by the production theme generator.

The comparison is a controlled design specimen. It intentionally includes hypothetical agent prose and manually marked diff spans, not screenshots from those applications. Grayscale is a diagnostic aid, not a full color-vision-deficiency simulation.

## Milestone 1 results

- Existing baseline: 19 unittest cases pass; 200 previously tracked files are byte-identical to the baseline commit.
- Candidate audit: 147 specified contrast pairs pass (49 per candidate).
- Reviewed comparison at 1024 px and narrow 360 px, with working grayscale control. Diff identity survives through +/− markers; exact characters remain emphasized without hue.
- User requirement: all foreground text remains dark. Reversed tab and selection treatments were removed. Selection now uses pale steel with a dark outline and graphite text.
- These are candidate palette checks, not native application acceptance. Selection of a candidate is the next decision; real agent screenshots and Zenbones integration remain future milestones.
