# Ithilien Dawn: named colors

<!-- Generated from palette/ithilien-dawn.json; do not edit by hand. -->

All **18 named sRGB colors** define the Formex-inspired Dawn palette. Each color has one single-word name and a documented connection to Tolkien’s work. The exact shades are design interpretations, not colors measured from the books.

Names draw from Ithilien’s plants, waters, materials and people, poetic landscape associations, and its Gondorian neighbors and the wider Anduin landscape. Gondor is its realm; Osgiliath and Pelennor are directly connected across Anduin. Plant names refer to species mentioned in Ithilien, except Mallorn, which draws on Lórien’s golden trees, and Nimloth, the White Tree of Númenor. Material names evoke the regional landscape. The sources establish those connections; botanical shades and the exact hex values are our interpretation.

| Name | Exact hex | Tolkien connection / color association | Roles |
| --- | --- | --- | --- |
| Lebethron | `#000000` | Black wood used for the casket holding the Crown of Gondor. [Source](https://tolkiengateway.net/wiki/Lebethron) | `foregrounds.text`, `foregrounds.bright`, `accents.olive`, `accents.gold`, `accents.ochre`, `accents.clay`, `ansi.black`, `diff.contextForeground`, `diff.inlineForeground`, `diff.addForeground`, `diff.deleteForeground`, `diff.changeForeground`, `diff.hunkForeground`, `diff.conflictForeground`, `highlight.foreground` |
| Ash | `#505456` | Ithilien ash trees; gray bark. [Source](https://tolkiengateway.net/wiki/Ithilien) | `backgrounds.border`, `foregrounds.muted`, `foregrounds.comment`, `foregrounds.subtext`, `accents.sage`, `ansi.brightBlack`, `highlight.border` |
| Briar | `#B8595C` | Muted rose red inspired by the hips of Ithilien briars; a botanical interpretation, not a shade specified by Tolkien. [Source](https://tolkiengateway.net/wiki/Eglantine) | `highlight.background`, `highlight.cursor`, `highlight.cursorBlock` |
| Ilex | `#315F46` | Deep green inspired by the evergreen foliage of the great ilexes of Ithilien; the exact shade is a design interpretation. [Source](https://tolkiengateway.net/wiki/Ithilien) | `ansi.green`, `ansi.brightGreen` |
| Anduin | `#345E77` | The Great River along Ithilien; interpreted as river blue. [Source](https://tolkiengateway.net/wiki/Anduin) | `accents.blue`, `ansi.blue`, `ansi.brightBlue` |
| Mallorn | `#795922` | Dark ochre inspired by the golden leaves of Lórien’s mallorn trees; a shaded interpretation chosen for readable terminal text. A broader Tolkien connection, not an Ithilien tree. [Source](https://tolkiengateway.net/wiki/Mallorn) | `ansi.yellow`, `ansi.brightYellow`, `ansi.extendedOchre` |
| Iris | `#70516D` | Muted purple inspired by iris flowers. Frodo and Sam encountered irises in Ithilien; this shade is a floral interpretation, not a color specified by Tolkien. [Source](https://tolkiengateway.net/wiki/Iris) | `accents.mauve`, `ansi.magenta`, `ansi.brightMagenta` |
| Pelennor | `#E2EDDF` | Pale field green inspired by the cultivated lands of Gondor across Anduin from Ithilien. [Source](https://tolkiengateway.net/wiki/Pelennor_Fields) | `diff.addBackground` |
| Eglantine | `#F1E2DF` | Pale blush inspired by the petals of Ithilien’s sweet-briar. [Source](https://tolkiengateway.net/wiki/Ithilien) | `diff.deleteBackground` |
| Henneth | `#D7E3EA` | Pale blue-gray inspired by the waterfall curtain at Henneth Annûn, the Window on the West in Ithilien. A shortened place-name element, not a Tolkien word for mist or blue. [Source](https://tolkiengateway.net/wiki/Henneth_Ann%C3%BBn) | `diff.changeBackground`, `diff.hunkBackground` |
| Celandine | `#D8B46A` | Muted golden yellow inspired by the bright celandine flowers of Ithilien; a softened interpretation. [Source](https://tolkiengateway.net/wiki/Ithilien) | `diff.addEmphasis`, `diff.deleteEmphasis`, `diff.changeEmphasis` |
| Heather | `#D6C6DE` | Pale lilac inspired by the pink-purple flowers of heather growing in Ithilien; the exact shade is a botanical interpretation, not a color specified by Tolkien. [Source](https://encyclopedia-of-arda.com/h/heather.php) | `backgrounds.search`, `diff.conflictBackground` |
| Nimloth | `#FAFAF8` | Soft white inspired by Nimloth, the White Tree of Númenor and ancestor of Gondor’s White Trees; its name means “White Blossom”. The shade is a poetic interpretation. [Source](https://tolkiengateway.net/wiki/Nimloth_(tree)) | `backgrounds.base`, `backgrounds.surface0`, `ansi.white`, `ansi.brightWhite` |
| Gondor | `#DEE0DF` | The realm containing Ithilien; pale gray interpreted from Gondorian stone architecture. [Source](https://tolkiengateway.net/wiki/Ithilien) | `backgrounds.mantle` |
| Anemone | `#F0F1EF` | White anemones in Ithilien; interpreted as a near-white neutral. [Source](https://tolkiengateway.net/wiki/Anemones) | `backgrounds.surface1` |
| Osgiliath | `#C9CECB` | City straddling Anduin at Ithilien’s western edge; weathered stone. [Source](https://tolkiengateway.net/wiki/Osgiliath) | `backgrounds.crust`, `backgrounds.surface2` |
| Annûn | `#8B3037` | Deep sunset red inspired by the light through the waterfall at Henneth Annûn in Ithilien. Paired with Henneth’s pale waterfall blue; the shade is an interpretation, not the literal meaning of Annûn. Uses Annun in code. [Source](https://encyclopedia-of-arda.com/w/windowofthesunset.php) | `accents.coral`, `ansi.red`, `ansi.brightRed`, `ansi.extendedClay` |
| Rauros | `#255354` | Deep teal inspired by the shaded waters of Anduin at the Falls of Rauros, north of Ithilien. A poetic color interpretation, not a hue specified by Tolkien. [Source](https://tolkiengateway.net/wiki/Rauros) | `accents.aqua`, `ansi.cyan`, `ansi.brightCyan` |

## Authoring and integration

Edit hex values only in `colors`. Functional roles reference those names: `backgrounds.base` → `Nimloth`, `foregrounds.text` → `Lebethron`, `accents.blue` → `Anduin`. The loader resolves those references to the same role-to-hex mappings used by existing ports and audits.

Neovim also exposes the named palette through `require("ithilien.ithilien-dawn").colors.Anduin`. Dusk and the shared interaction source remain unchanged. Dawn uses Briar selection and block cursors with black text.
