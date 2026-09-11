import json,copy
from pathlib import Path
out=Path(__file__).resolve().parent
p=json.loads(Path('palette/ithilien-dawn.json').read_text())
rows=json.loads((out/'measurements.json').read_text())['candidates']
names=['Briar','Sage','Broom','Anduin','Thyme','Stillwater']
r=next(r for r in rows if r['names']==names)
q=copy.deepcopy(p)
for family,name in zip(['red','green','yellow','blue','magenta','cyan'],names):
 q['ansi'][family]=q['ansi']['bright'+family.capitalize()]=name
(out/'candidate-ansi-only.json').write_text(json.dumps(q,indent=2)+'\n')
report='''# Ithilien Dawn: consolidated ANSI research

Status: candidate recommendation, not adopted or installed. Frozen palette unchanged.

## Scope and method

Examined all 32 combinations of the existing regular/bright chromatic shades. Briar is already shared, so five binary choices remain. No new hex values were optimized. Tested WCAG 2.1 contrast against base, mantle, surface0 and surface1, pairwise OKLab distances, and full-severity Machado protan/deutan/tritan simulations using the repository's ithilienlib functions. Distances are diagnostics, not calibrated usability scores. This is not the full native rendering suite, an unrestricted color search, or proof of comfort.

Reproduce from work/ithilien:

    .venv/bin/python reports/ansi-consolidation/analyze.py
    .venv/bin/python reports/ansi-consolidation/summarize.py

## Recommended first candidate

Regular/bright chromatic slots share these colors; all four neutral slots retain their current values. Afterglow cursor/selection and all diff backgrounds/changed-character emphasis remain unchanged.

| ANSI family | Name | sRGB | Contrast on Asphodel |
|---|---|---|---|
'''
for family,name in zip(['red','green','yellow','blue','magenta','cyan'],names):report+=f'| {family} | {name} | {p["colors"][name]} | {r["contrast_base"][family]:.2f}:1 |\n'
report+='''
The weakest chromatic text pair across the four evaluated surfaces is Broom on Gondor, 4.85:1. This exceeds the project's 4.5:1 floor, with less margin than the all-regular candidate. Colored text on Afterglow is outside this guarantee: interaction text must resolve to black.

## Tradeoffs

| Candidate | Minimum contrast, four surfaces | Minimum OKLab distance, normal | Minimum distance across all four vision conditions |
|---|---:|---:|---:|
'''
for label,x in [('All regular',rows[0]),('All bright',rows[-1]),('Recommended mixed',r)]:report+=f'| {label} | {x["minimum_surface_contrast"]:.2f}:1 | {x["minimum_distance"]["normal"]:.4f} | {min(x["minimum_distance"].values()):.4f} |\n'
report+='''
The mixed candidate ties for the largest worst-pair distance across the four modeled vision conditions within this 32-candidate set. The tied alternative uses Filbert instead of Broom; it has more contrast but looks browner. Broom is the provisional choice for recognizable ANSI yellow/ochre and consistency with the existing extended ochre slot. This is a design judgment, not a measured performance result.

All-regular has the largest contrast reserve. All-bright reuses more existing accent roles. Mixed keeps blue and teal farther apart. No candidate is a universal winner across every pair and condition. Color-blind simulations still contain close pairs; preserve signs, labels and structural cues.

## Semantic names

- Briar: Ithilien briars; deep berry/stem red is an interpretation, not Tolkien's specified color.
- Sage: sages of Ithilien; green foliage interpretation, darker than familiar silvery garden sage.
- Broom: yellow-flowered broom on the approach to Ithilien; this legible dark ochre is not literal bright petals.
- Anduin: river along Ithilien's western edge; restrained river blue is interpretive.
- Thyme: Ithilien thyme; muted mauve inspired by flowers. Keeping the existing name avoids needless API churn.
- Stillwater: poetic shaded-water teal associated with the pool at Henneth Annun, not a canonical Tolkien proper name. Poros is an alternative if geographic names are preferred, but is already bound to a different hex and should not silently change meaning.

Prefer these existing name-to-hex mappings for the first candidate. Dropping a terminal mapping does not automatically permit deleting its named color: Poros remains accents.aqua, for example. Global consolidation would need a separate accent-role decision and rendered tests. Do not rewrite syntax roles just to reduce the count.

## Yellow/ochre naming alternatives

Broom is a provisional identifier, not a final naming recommendation. The user dislikes it.

- Filbert: strongest botanical alternative for this dark nut-brown ochre; filbert thickets occur in Ithilien. Already identifies #624819, so adopting it for #795922 requires an explicit consolidation/migration rather than two colors sharing a name.
- Amber: direct golden-brown color association; a general poetic name, not a specific Ithilien reference.
- Bracken: evocative of browned fern fronds; a landscape association, not asserted here as an explicitly named Ithilien plant.

Recommendation: Filbert if consolidating the two ochres globally; Amber if preserving the current Filbert shade as a separate named color. Candidate identifiers remain unchanged pending the naming decision.

## Sources

- Catppuccin official Ghostty Latte duplicates its six chromatic pairs: https://github.com/catppuccin/ghostty/blob/main/themes/catppuccin-latte.conf
- Gruvbox Material upstream maps regular and bright terminal chromatic slots to the same role: https://github.com/sainnhe/gruvbox-material/blob/master/colors/gruvbox-material.vim
- Ghostty palette/bold configuration: https://ghostty.org/docs/config/reference
- Ithilien geography and flora, with chapter references: https://tolkiengateway.net/wiki/Ithilien
- Broom on the approach: https://lentenlordoftherings.wordpress.com/2017/03/25/on-long-descriptions-of-nature/
- Poros geography: https://www.encyclopedia-of-arda.com/p/poros.html
- Avoid meaning conveyed by color alone: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html

## Next validation

Render the frozen baseline, recommended mixed candidate, and all-regular control using actual ANSI 30-37/90-97 sequences and bold states in Ghostty, with Berkeley Mono Medium 16 and sRGB. Include terminal diffs with single-character changes, Codex indexed-color output, Python tracebacks, pytest output, prompt and selected text. Explicitly distinguish RGB application output, which does not exercise ANSI remapping. Existing truecolor Neovim diff highlights should remain identical for this ANSI-only candidate; verify terminal_color mappings separately. Do not claim success from unchanged truecolor screenshots.

Compare any newly identical semantic roles used by applications. Re-run supported native flows and note unavailable surfaces. Only then decide whether to adopt and prune genuinely unused names. Human review remains necessary to establish comfort and aesthetic preference.
'''
(out/'report.md').write_text(report)
print(out/'report.md')
