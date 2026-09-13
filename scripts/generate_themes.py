"""Generate Ithilien themes and preview artifacts from the canonical palettes."""

from __future__ import annotations

import json
import plistlib

from ithilienlib import ROOT, load_palette, load_palette_source, ROLE_FAMILIES


def lua_table(value, indent: int = 0) -> str:
    space = " " * indent
    if isinstance(value, dict):
        rows = ["{"]
        for key, item in value.items():
            rows.append(f'{" " * (indent + 2)}["{key}"] = {lua_table(item, indent + 2)},')
        rows.append(f"{space}}}")
        return "\n".join(rows)
    if isinstance(value, list):
        return "{ " + ", ".join(lua_table(item) for item in value) + " }"
    if isinstance(value, bool):
        return "true" if value else "false"
    return f'"{value}"'


def generate_ghostty(palette: dict) -> None:
    bg, fg = palette["backgrounds"], palette["foregrounds"]
    highlight = palette["highlight"]
    ansi_tokens = palette["ansi"]
    ansi = list(ansi_tokens.values())
    is_light = palette["polarity"] == "light"
    lines = [
        f"# {palette['name']} — generated from scripts/palette/{palette['slug']}.json; do not edit by hand.",
        "# Warm, readability-first foundations and diff-aware ANSI colors.",
        "",
        *[f"palette = {index}={color}" for index, color in enumerate(ansi)],
        "",
        f'background = {bg["base"]}',
        f'foreground = {fg["text"]}',
        f'cursor-color = {highlight.get("cursorBlock", highlight["background"])}',
        f'cursor-text = {highlight["foreground"]}',
        *(["cursor-style = block"] if is_light else []),
        f'selection-background = {highlight["background"]}',
        f'selection-foreground = {highlight["foreground"]}',
        "",
        f'font-family = {"Berkeley Mono Medium" if is_light else "Berkeley Mono Retina"}',
        f'window-title-font-family = {"Berkeley Mono Medium" if is_light else "Berkeley Mono Retina"}',
        *(["", "# Preserve the vi-mode cursor contrast fix.",
           "minimum-contrast = 1"] if is_light else []),
    ]
    destination = ROOT / "extras/ghostty" / "themes" / (palette["slug"].replace("-", "_") + ".conf")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines) + "\n")


def generate_neovim_palette(palette: dict) -> None:
    bg, fg, accent, diff = (
        palette["backgrounds"], palette["foregrounds"], palette["accents"], palette["diff"]
    )
    kanso = {
        "inkBg0": bg["base"], "inkBg1": bg["surface0"], "inkBg2": bg["surface1"],
        "inkBg3": bg["surface2"], "inkBg4": palette["highlight"]["background"],
        "zenBg0": bg["crust"], "zenBg1": bg["surface0"], "zenBg2": bg["surface1"],
        "zenBg3": bg["surface2"], "altBlue1": diff["hunkBackground"],
        "altBlue2": palette["highlight"]["background"], "diffGreen": diff["addBackground"],
        "diffRed": diff["deleteBackground"], "diffYellow": diff["changeEmphasis"],
        "diffBlue": diff["changeBackground"], "gitGreen": diff["addForeground"],
        "gitRed": diff["deleteForeground"], "gitYellow": diff["changeForeground"],
        "red": accent["coral"], "red2": diff["deleteForeground"], "red3": accent["coral"],
        "yellow": accent["gold"], "yellow2": diff["changeForeground"], "yellow3": accent["gold"],
        "green": accent["sage"], "green2": diff["addForeground"], "green3": accent["sage"],
        "green4": accent["olive"], "green5": accent["aqua"],
        "blue": accent["blue"], "blue2": accent["aqua"], "blue3": accent["blue"],
        "blue4": accent["aqua"], "violet": accent["mauve"], "violet2": accent["mauve"],
        "violet3": accent["mauve"], "pink": accent["mauve"],
        "orange": accent["ochre"], "orange2": accent["clay"], "aqua": accent["aqua"],
        "fg": fg["text"], "fg2": fg["bright"], "gray": fg["muted"],
        "gray2": fg["subtext"], "gray3": fg["subtext"], "gray4": fg["comment"],
        "gray5": fg["muted"],
    }
    term = list(palette["ansi"].values())
    named_colors = load_palette_source(palette["slug"]).get("colors", {})
    rendered = (
        f"-- Generated from scripts/palette/{palette['slug']}.json; do not edit by hand.\n"
        "return {\n"
        + (f"  colors = {lua_table(named_colors, 2)},\n" if named_colors else "")
        + f"  raw = {lua_table(palette, 2)},\n"
        f"  kanso = {lua_table(kanso, 2)},\n"
        f"  terminal = {lua_table(term, 2)},\n"
        "}\n"
    )
    module_name = f"{palette['slug']}.lua"
    destination = ROOT / "lua" / "ithilien" / module_name
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(rendered)


def generate_neovim_default() -> None:
    destination = ROOT / "colors" / "ithilien.lua"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text('require("ithilien").load("dawn")\n')


def generate_codex_theme(palette: dict) -> None:
    """Generate a TextMate theme understood by Codex CLI's syntax renderer."""
    bg, fg, accent, diff = (
        palette["backgrounds"], palette["foregrounds"], palette["accents"], palette["diff"]
    )

    def rule(name: str, scope: str, foreground: str | None = None,
             background: str | None = None, font_style: str | None = None) -> dict:
        settings = {}
        if foreground:
            settings["foreground"] = foreground
        if background:
            settings["background"] = background
        if font_style is not None:
            settings["fontStyle"] = font_style
        return {"name": name, "scope": scope, "settings": settings}

    day = palette["polarity"] == "light"
    settings = [
        {"settings": {"background": bg["base"], "foreground": fg["text"],
                      "caret": palette["highlight"].get("cursor", palette["highlight"]["background"]),
                      "selection": palette["highlight"]["background"],
                      "invisibles": fg["muted"], "lineHighlight": bg["surface1"] if day else bg["surface0"],
                      **({"selectionForeground": palette["highlight"]["foreground"]} if day else {})}},
        rule("Comments", "comment, punctuation.definition.comment", fg["comment"], font_style="italic"),
        rule("Strings", "string", accent["sage"]),
        rule("Numbers and constants", "constant.numeric, constant.language, constant.character", accent["ochre"]),
        rule("Keywords", "keyword, storage.type, storage.modifier", accent["clay"] if day else accent["mauve"], font_style="bold" if day else None),
        rule("Types", "entity.name.type, entity.name.class, support.type, support.class", accent["aqua"] if day else accent["gold"]),
        rule("Functions", "entity.name.function, support.function, meta.function-call", accent["gold"] if day else accent["blue"]),
        rule("Variables", "variable, support.variable", fg["text"]),
        rule("Properties", "variable.other.property, support.constant", accent["aqua"]),
        rule("Operators", "keyword.operator", accent["olive"] if day else accent["clay"]),
        rule("Punctuation", "punctuation", fg["subtext"]),
        rule("Headings", "markup.heading", accent["gold"], font_style="bold"),
        rule("Links", "markup.underline.link", accent["blue"], font_style="underline"),
        rule("Inserted diff", "markup.inserted, diff.inserted", diff["addForeground"], diff["addBackground"]),
        rule("Deleted diff", "markup.deleted, diff.deleted", diff["deleteForeground"], diff["deleteBackground"]),
        rule("Changed diff", "markup.changed, diff.changed", diff["changeForeground"], diff["changeBackground"]),
    ]
    if day:
        # Use identifier scopes, not whole call/annotation expressions: arguments,
        # literals and punctuation must retain their own roles.
        settings.extend([
            rule("Python variables", "source.python variable.other, meta.generic-name.python", fg["text"]),
            rule("Python calls and definitions", "variable.function.python meta.generic-name.python, variable.function.python, entity.name.function.python meta.generic-name.python", accent["gold"]),
            rule("Python class definitions", "entity.name.class.python meta.generic-name.python", accent["aqua"]),
            rule("Python type annotations", "meta.type.python variable.other, meta.function.parameters.annotation.python meta.generic-name.python, meta.function.annotation.return.python meta.generic-name.python", accent["aqua"]),
            rule("Python constants", "source.python variable.other.constant", accent["ochre"]),
            rule("Python decorators", "variable.annotation.python meta.generic-name.python, variable.annotation.function.python meta.generic-name.python, entity.name.function.decorator.python, punctuation.definition.annotation.python", accent["ochre"]),
            rule("Python operators", "source.python keyword.operator, keyword.control.loop.for.in.python", accent["olive"], font_style=""),
        ])
    theme = {"name": palette["name"], "author": "Ithilien theme generator",
             "semanticClass": f"theme.{palette['slug']}", "settings": settings}
    destination = ROOT / "extras/codex" / "themes" / f"{palette['slug']}.tmTheme"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as output:
        plistlib.dump(theme, output, fmt=plistlib.FMT_XML, sort_keys=False)


def generate_claude_theme(palette: dict) -> None:
    """Generate a Claude Code 2.1.118+ custom theme."""
    bg, fg, accent, diff = (
        palette["backgrounds"], palette["foregrounds"], palette["accents"], palette["diff"]
    )
    overrides = {
        "claude": accent["coral"] if palette["polarity"] == "light" else accent["ochre"], "claudeShimmer": accent["gold"],
        "text": fg["text"], "inverseText": palette["highlight"]["foreground"],
        "inactive": fg["muted"], "inactiveShimmer": fg["comment"], "subtle": fg["comment"],
        "suggestion": accent["olive"], "permission": accent["gold"],
        "permissionShimmer": accent["ochre"], "remember": accent["mauve"],
        "success": palette["ansi"]["brightGreen"] if palette["polarity"] == "light" else accent["sage"], "error": accent["coral"], "warning": palette["ansi"]["brightYellow"] if palette["polarity"] == "light" else accent["gold"],
        "warningShimmer": accent["ochre"], "merged": accent["mauve"],
        "promptBorder": accent["olive"], "promptBorderShimmer": accent["sage"],
        "planMode": accent["blue"], "autoAccept": accent["sage"],
        "bashBorder": accent["clay"], "ide": accent["aqua"],
        "fastMode": accent["ochre"], "fastModeShimmer": accent["gold"],
        "diffAdded": diff["addBackground"], "diffRemoved": diff["deleteBackground"],
        "diffAddedDimmed": bg["surface0"], "diffRemovedDimmed": bg["surface0"],
        "diffAddedWord": diff["addEmphasis"], "diffRemovedWord": diff["deleteEmphasis"],
        "userMessageBackground": bg["surface0"], "userMessageBackgroundHover": bg["surface1"],
        "bashMessageBackgroundColor": bg["mantle"], "memoryBackgroundColor": bg["surface0"],
        "selectionBg": palette["highlight"]["background"],
        "rate_limit_fill": accent["olive"], "rate_limit_empty": bg["surface2"],
        "briefLabelYou": accent["blue"], "briefLabelClaude": accent["ochre"],
    }
    theme = {"name": palette["name"], "base": palette["polarity"], "overrides": overrides}
    destination = ROOT / "extras/claude-code" / "themes" / f"{palette['slug']}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(theme, indent=2) + "\n")


def generate_app_palettes(palette: dict) -> None:
    """Generate importable palettes for apps with constrained theme APIs."""
    bg, fg, accent = palette["backgrounds"], palette["foregrounds"], palette["accents"]
    slack_colors = [bg["mantle"], bg["surface0"], palette["highlight"]["background"],
                    palette["highlight"]["foreground"], bg["surface1"], fg["text"],
                    accent["sage"], accent["coral"]]
    slack = ROOT / "extras/slack" / f"{palette['slug']}.txt"
    slack.parent.mkdir(parents=True, exist_ok=True)
    slack.write_text(",".join(slack_colors) + "\n")

    linear_colors = [bg["base"], fg["text"], bg["mantle"], fg["text"],
                     palette["highlight"]["background"], palette["highlight"]["foreground"]]
    linear = ROOT / "extras/linear" / f"{palette['slug']}.txt"
    linear.parent.mkdir(parents=True, exist_ok=True)
    linear.write_text(",".join(linear_colors) + "\n")


def generate_shared_highlights(palette: dict, variant: bool = False) -> None:
    highlight = palette["highlight"]

    shell = ROOT / "extras/shell" / (f"{palette['slug']}.zsh" if variant else "ithilien.zsh")
    shell.parent.mkdir(parents=True, exist_ok=True)
    shell.write_text(
        "# Ithilien ZLE visual selection — generated; do not edit by hand.\n"
        f'zle_highlight=("${{(@)zle_highlight:#region:*}}" '
        f'"region:bg={highlight["background"]},fg={highlight["foreground"]}")\n'
    )

    # Append explicit colors after user options; preserve bindings and previews.
    bg, fg = palette["backgrounds"], palette["foregrounds"]
    prompt_color = palette['ansi']['red'] if palette['polarity'] == 'light' else highlight.get('cursor', palette['accents']['coral'])
    colors = (f"--color={palette['polarity']},bg:{bg['base']},fg:{fg['text']},"
              f"bg+:{highlight['background']},fg+:{highlight['foreground']},"
              f"hl:{fg['text']}:underline,hl+:{highlight['foreground']}:underline,"
              f"info:{fg['text']},header:{fg['text']},border:{fg['comment']},"
              f"prompt:{prompt_color},pointer:{fg['text'] if palette['polarity'] == 'light' else highlight['foreground']},"
              f"marker:{fg['text'] if palette['polarity'] == 'light' else highlight['foreground']},spinner:{prompt_color},"
              f"gutter:{bg['base']},query:{fg['text']}")
    with shell.open("a") as output:
        output.write(
            "\n# fzf, including Ctrl-R history; safe to source repeatedly.\n"
            'if [[ -n ${_ITHILIEN_FZF_COLORS-} ]]; then\n'
            '  FZF_DEFAULT_OPTS=${FZF_DEFAULT_OPTS//"$_ITHILIEN_FZF_COLORS"/}\n'
            '  FZF_CTRL_R_OPTS=${FZF_CTRL_R_OPTS//"$_ITHILIEN_FZF_COLORS"/}\n'
            'fi\n'
            f"_ITHILIEN_FZF_COLORS='{colors}'\n"
            'export FZF_DEFAULT_OPTS="${FZF_DEFAULT_OPTS% } $_ITHILIEN_FZF_COLORS"\n'
            'export FZF_CTRL_R_OPTS="${FZF_CTRL_R_OPTS% } $_ITHILIEN_FZF_COLORS"\n'
        )

    r, g, b = (int(highlight["background"][index : index + 2], 16) / 255 for index in (1, 3, 5))
    macos = ROOT / "extras/macos" / (f"apply-highlight-{palette['slug']}.sh" if variant else "apply-highlight.sh")
    macos.parent.mkdir(parents=True, exist_ok=True)
    macos.write_text(
        "#!/bin/sh\n"
        "# Ithilien system text highlight — generated; log out and back in after applying.\n"
        f'defaults write -g AppleHighlightColor -string "{r:.6f} {g:.6f} {b:.6f} Other"\n'
    )
    macos.chmod(0o755)

    bg, fg, accent = palette["backgrounds"], palette["foregrounds"], palette["accents"]
    firefox_manifest = {
        "manifest_version": 2,
        "name": palette["name"],
        "version": "0.2.0",
        "theme": {
            "colors": {
                "frame": bg["mantle"],
                "frame_inactive": bg["crust"],
                "tab_background_text": fg["subtext"],
                "tab_text": fg["text"],
                "toolbar": bg["surface0"],
                "bookmark_text": fg["text"],
                "icons": fg["subtext"],
                "toolbar_field": bg["base"],
                "toolbar_field_focus": bg["base"],
                "toolbar_field_text": fg["text"],
                "toolbar_field_border": bg["surface2"],
                "toolbar_field_highlight": highlight["background"],
                "toolbar_field_highlight_text": highlight["foreground"],
                "popup": bg["surface0"],
                "popup_text": fg["text"],
                "popup_border": bg["surface2"],
                "button_background_hover": bg["surface1"],
                "button_background_active": highlight["background"],
                "icons_attention": accent["gold"],
            },
            "properties": {"color_scheme": palette["polarity"], "content_color_scheme": palette["polarity"]},
        },
    }
    firefox = ROOT / "extras/firefox" / palette["slug"] / "manifest.json" if variant else ROOT / "extras/firefox" / "manifest.json"
    firefox.parent.mkdir(parents=True, exist_ok=True)
    firefox.write_text(json.dumps(firefox_manifest, indent=2) + "\n")
    (firefox.parent / "userContent.css").write_text(
        "/* Generated Ithilien website selection; optional Firefox profile customization. */\n"
        f'::selection {{ background: {highlight["background"]} !important; color: {highlight["foreground"]} !important; }}\n'
    )


def generate_color_reference() -> None:
    source = load_palette_source('ithilien-dawn')
    roles = {name: [] for name in source['colors']}
    for family in ROLE_FAMILIES:
        for role, name in source[family].items():
            roles[name].append(f'`{family}.{role}`')
    lines = [
        '# Ithilien Dawn: named colors', '',
        '<!-- Generated from scripts/palette/ithilien-dawn.json; do not edit by hand. -->', '',
        f'All **{len(source["colors"])} named sRGB colors** define the Formex-inspired Dawn palette. '
        'Each color has one single-word name and a documented connection to Tolkien’s work. '
        'The exact shades are design interpretations, not colors measured from the books.', '',
        'Names draw from Ithilien’s plants, waters, materials and people, poetic landscape associations, and its '
        'Gondorian neighbors and the wider Anduin landscape. Gondor is its realm; Osgiliath and Pelennor '
        'are directly connected across Anduin. Plant names refer to species mentioned in '
        'Ithilien, except Mallorn, which draws on Lórien’s golden trees, and Nimloth, the White Tree of Númenor. Material names evoke the regional landscape. The sources establish those '
        'connections; botanical shades and the exact hex values are our interpretation.', '',
        '| Name | Exact hex | Tolkien connection / color association | Roles |',
        '| --- | --- | --- | --- |',
    ]
    for name, color in source['colors'].items():
        note = source['colorNotes'][name]
        lines.append(f"| {note.get('displayName', name)} | `{color}` | {note['meaning']} [Source]({note['source']}) | {', '.join(roles[name])} |")
    lines.extend(['', '## Authoring and integration', '',
        'Edit hex values only in `colors`. Functional roles reference those names: '
        '`backgrounds.base` → `Nimloth`, `foregrounds.text` → `Lebethron`, '
        '`accents.blue` → `Anduin`. The loader resolves those references to the same '
        'role-to-hex mappings used by existing ports and audits.', '',
        'Neovim also exposes the named palette through '
        '`require("ithilien.ithilien-dawn").colors.Anduin`. '
        'Dawn uses Briar selection and block cursors with black text.', ''])
    (ROOT/'docs/palette-names.md').write_text('\n'.join(lines))


def main() -> None:
    palettes = {"day": load_palette("ithilien-dawn")}
    for palette in palettes.values():
        generate_ghostty(palette)
        generate_neovim_palette(palette)
        generate_codex_theme(palette)
        generate_claude_theme(palette)
        generate_app_palettes(palette)
    generate_neovim_default()
    generate_shared_highlights(palettes["day"])
    for palette in palettes.values():
        generate_shared_highlights(palette, variant=True)
    generate_color_reference()
    from palette_chart import generate_chart
    generate_chart()
    print("Generated Ithilien Dawn themes for all supported applications")


if __name__ == "__main__":
    main()
