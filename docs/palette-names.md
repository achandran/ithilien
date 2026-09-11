# Ithilien Dawn: named colors

<!-- Generated from palette/ithilien-dawn.json; do not edit by hand. -->

All **19 named sRGB colors** define the Formex-inspired Dawn palette. Each color has one single-word name and a documented connection to Tolkien’s work. The exact shades are design interpretations, not colors measured from the books.

Names draw from Ithilien’s plants, waters, materials and people, poetic landscape associations, and its Gondorian neighbours and the wider Anduin landscape. Gondor is its realm; Osgiliath and Pelennor are directly connected across Anduin. Plant names refer to species mentioned in Ithilien, except Mallorn, which draws on Lórien’s golden trees, and Nimloth, the White Tree of Númenor. Material names evoke the regional landscape. The sources establish those connections; botanical shades and the exact hex values are our interpretation.

| Name | Exact hex | Tolkien connection / color association | Roles |
| --- | --- | --- | --- |
| Lebethron | `#000000` | Black wood used for the casket holding the Crown of Gondor. [Source](https://tolkiengateway.net/wiki/Lebethron) | `foregrounds.text`, `foregrounds.bright`, `accents.olive`, `accents.gold`, `accents.ochre`, `accents.clay`, `ansi.black`, `diff.contextForeground`, `diff.inlineForeground`, `diff.addForeground`, `diff.deleteForeground`, `diff.changeForeground`, `diff.hunkForeground`, `diff.conflictForeground`, `highlight.foreground` |
| Ash | `#505456` | Ithilien ash trees; grey bark. [Source](https://tolkiengateway.net/wiki/Ithilien) | `foregrounds.muted`, `foregrounds.comment`, `foregrounds.subtext`, `accents.sage`, `ansi.brightBlack`, `highlight.border` |
| Stonecrop | `#66716D` | Ithilien stonecrops; muted grey-green foliage. [Source](https://tolkiengateway.net/wiki/Ithilien) | `backgrounds.border` |
| Afterglow | `#B8595C` | A poetic name for muted sunset red, inspired by the light at Henneth Annûn; our interpretation, not a canonical Tolkien color name. [Source](https://tolkiengateway.net/wiki/Henneth_Ann%C3%BBn) | `highlight.background`, `highlight.cursor`, `highlight.cursorBlock` |
| Sage | `#315F46` | Sages of Ithilien; green foliage. [Source](https://tolkiengateway.net/wiki/Ithilien) | `ansi.green`, `ansi.brightGreen` |
| Anduin | `#345E77` | The Great River along Ithilien; interpreted as river blue. [Source](https://tolkiengateway.net/wiki/Anduin) | `accents.blue`, `ansi.blue`, `ansi.brightBlue` |
| Mallorn | `#795922` | Dark ochre inspired by the golden leaves of Lórien’s mallorn trees; a shaded interpretation chosen for readable terminal text. A broader Tolkien connection, not an Ithilien tree. [Source](https://tolkiengateway.net/wiki/Mallorn) | `ansi.yellow`, `ansi.brightYellow`, `ansi.extendedOchre` |
| Thyme | `#70516D` | Thyme in Ithilien; muted purple flowers. [Source](https://tolkiengateway.net/wiki/Ithilien) | `accents.mauve`, `ansi.magenta`, `ansi.brightMagenta` |
| Pelennor | `#E2EDDF` | Fields across Anduin from Ithilien; pale field green. [Source](https://tolkiengateway.net/wiki/Pelennor_Fields) | `diff.addBackground` |
| Eglantine | `#F1E2DF` | Wild roses in Ithilien; pale pink petals. [Source](https://tolkiengateway.net/wiki/Ithilien) | `diff.deleteBackground` |
| Spray | `#D7E3EA` | Waterfall spray at Henneth Annûn in Ithilien; pale water. [Source](https://tolkiengateway.net/wiki/Henneth_Ann%C3%BBn) | `diff.changeBackground`, `diff.hunkBackground` |
| Celandine | `#D8B46A` | Celandines in Ithilien; pale golden flowers. [Source](https://tolkiengateway.net/wiki/Ithilien) | `diff.addEmphasis`, `diff.deleteEmphasis`, `diff.changeEmphasis` |
| Clematis | `#D6C6DE` | Trailing clematis in Ithilien; a pale lilac floral interpretation, not a flower color specified by Tolkien. [Source](https://tolkiengateway.net/wiki/Ithilien) | `backgrounds.search`, `diff.conflictBackground` |
| Nimloth | `#FAFAF8` | Soft white inspired by Nimloth, the White Tree of Númenor and ancestor of Gondor’s White Trees; its name means “White Blossom”. The shade is a poetic interpretation. [Source](https://tolkiengateway.net/wiki/Nimloth_(tree)) | `backgrounds.base`, `backgrounds.surface0`, `ansi.white`, `ansi.brightWhite` |
| Gondor | `#DEE0DF` | The realm containing Ithilien; pale gray interpreted from Gondorian stone architecture. [Source](https://tolkiengateway.net/wiki/Ithilien) | `backgrounds.mantle` |
| Anemone | `#F0F1EF` | White anemones in Ithilien; interpreted as a near-white neutral. [Source](https://tolkiengateway.net/wiki/Anemones) | `backgrounds.surface1` |
| Osgiliath | `#C9CECB` | City straddling Anduin at Ithilien’s western edge; weathered stone. [Source](https://tolkiengateway.net/wiki/Osgiliath) | `backgrounds.crust`, `backgrounds.surface2` |
| Briar | `#8B3037` | Briars in Ithilien; dark red fruit and stems. [Source](https://tolkiengateway.net/wiki/Ithilien) | `accents.coral`, `ansi.red`, `ansi.brightRed`, `ansi.extendedClay` |
| Rauros | `#255354` | Deep teal inspired by the shaded waters of Anduin at the Falls of Rauros, north of Ithilien. A poetic color interpretation, not a hue specified by Tolkien. [Source](https://tolkiengateway.net/wiki/Rauros) | `accents.aqua`, `ansi.cyan`, `ansi.brightCyan` |

## Authoring and integration

Edit hex values only in `colors`. Functional roles reference those names: `backgrounds.base` → `Nimloth`, `foregrounds.text` → `Lebethron`, `accents.blue` → `Anduin`. The loader resolves those references to the same role-to-hex mappings used by existing ports and audits.

Neovim also exposes the named palette through `require("ithilien.ithilien-dawn").colors.Anduin`. Dusk and the shared interaction source remain unchanged. Dawn uses Afterglow selection and block cursors with black text.
