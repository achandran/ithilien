# Ithilien Dawn: proposed color names

All **38 distinct sRGB colors** below are preserved exactly from Loden Day at `2ec16c0`. These are proposed thematic names, not a palette revision. Multiple roles sharing one hex value share one color name. Functional roles remain explicit: for example, `backgrounds.base` would reference Parchment and `accents.blue` would reference Anduin.

The vocabulary combines warm materials, woodland plants, water, and a few local place names. Anduin is the western boundary of [Ithilien](https://tolkiengateway.net/wiki/Ithilien); Henneth evokes its [hidden waterfall refuge](https://tolkiengateway.net/wiki/Henneth_Ann%C3%BBn); Cormallen evokes the field in [North Ithilien](https://tolkiengateway.net/wiki/North_Ithilien). These color associations are design interpretations, not Tolkien color specifications or invented Elvish translations.

Parchment and Ink keep the foundation easy to understand. Laurel, Fern, and the water colors support the restrained woodland character. Diff names form recognizable families: Glade/Leaf, Petal/Rosehip, and Sunlight/Harvest. Copper keeps the shared black-on-warm-metal selection distinct.

| Suggested name | Exact hex | Existing roles |
| --- | --- | --- |
| Travertine | `#D8D2BE` | `backgrounds.crust` |
| Vellum | `#E8E1CD` | `backgrounds.mantle` |
| Parchment | `#F0E9D2` | `backgrounds.base`, `ansi.white` |
| Ivory | `#F7F0DF` | `backgrounds.surface0`, `ansi.brightWhite` |
| Linen | `#ECE5D2` | `backgrounds.surface1` |
| Lichen | `#C1BEAC` | `backgrounds.surface2` |
| Ash | `#53594E` | `foregrounds.muted`, `foregrounds.comment`, `ansi.brightBlack` |
| Ranger | `#484E43` | `foregrounds.subtext` |
| Ink | `#000000` | `foregrounds.text`, `foregrounds.bright`, `ansi.black`, `diff.contextForeground`, `diff.inlineForeground`, `highlight.foreground` |
| Laurel | `#64602F` | `accents.olive` |
| Fern | `#456344` | `accents.sage`, `ansi.brightGreen` |
| Cormallen | `#5C4619` | `accents.gold`, `ansi.brightYellow` |
| Amber | `#795B28` | `accents.ochre`, `ansi.extendedOchre` |
| Terracotta | `#88483E` | `accents.clay`, `ansi.extendedClay` |
| Rowan | `#A03440` | `accents.coral`, `ansi.brightRed` |
| Henneth | `#28665F` | `accents.aqua`, `ansi.brightCyan` |
| Anduin | `#405B80` | `accents.blue`, `ansi.brightBlue` |
| Heather | `#75516F` | `accents.mauve`, `ansi.brightMagenta` |
| Ember | `#84342F` | `ansi.red` |
| Thicket | `#405A34` | `ansi.green` |
| Bronze | `#5A4006` | `ansi.yellow` |
| Deepwater | `#304564` | `ansi.blue` |
| Bramble | `#67475C` | `ansi.magenta` |
| Stillwater | `#204F49` | `ansi.cyan` |
| Cypress | `#1F3518` | `diff.addForeground` |
| Glade | `#D5E1CA` | `diff.addBackground` |
| Leaf | `#A1BA77` | `diff.addEmphasis` |
| Mahogany | `#6B322E` | `diff.deleteForeground` |
| Petal | `#F0DCD6` | `diff.deleteBackground` |
| Rosehip | `#E2A69B` | `diff.deleteEmphasis` |
| Umber | `#453510` | `diff.changeForeground` |
| Sunlight | `#F4E3AD` | `diff.changeBackground` |
| Harvest | `#D2B16B` | `diff.changeEmphasis` |
| Pool | `#25443F` | `diff.hunkForeground` |
| Mist | `#D5E1DE` | `diff.hunkBackground` |
| Mulberry | `#503348` | `diff.conflictForeground` |
| Mallow | `#E2D3DE` | `diff.conflictBackground` |
| Copper | `#B17232` | `highlight.background` |

Names are suggestions for review. The rename uses the existing role keys and exact color values; it does not silently adopt a new token schema. Dusk has been renamed without recoloring and is outside this Dawn naming proposal.
