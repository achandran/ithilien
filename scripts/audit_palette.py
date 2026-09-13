"""Audit Ithilien's palette and write human- and machine-readable reports."""

from __future__ import annotations

import json
import math
import sys
from itertools import combinations

from ithilienlib import ROOT, apca, delta_e, load_palette, oklch, simulated_hex, wcag


SIMULATIONS = ("normal", "protan", "deutan", "tritan", "grayscale")


def main(variant: str = "ithilien-dusk") -> None:
    palette = load_palette(variant)
    backgrounds = palette["backgrounds"]
    foregrounds = palette["foregrounds"]
    accents = palette["accents"]
    ansi = palette["ansi"]
    diff = palette["diff"]
    highlight = palette["highlight"]

    day = palette["polarity"] == "light"
    contrast_specs = [
        ("muted UI", foregrounds["muted"], backgrounds["base"], 4.5 if day else 3.0, 25),
        ("comments", foregrounds["comment"], backgrounds["base"], 4.5, 45),
        ("secondary text", foregrounds["subtext"], backgrounds["base"], 7.0, 55),
        ("normal text", foregrounds["text"], backgrounds["base"], 7.0, 60),
        ("bright text", foregrounds["bright"], backgrounds["base"], 7.0, 75),
        ("highlighted text", highlight["foreground"], highlight["background"], 4.5, 0 if day else 35),
        # Selection/cursor boundaries are non-text UI components: WCAG 3:1
        # applies, while APCA is reported for reference but is not a gate.
        (f"highlight edge on {palette['name']}", highlight.get("border", highlight["background"]), backgrounds["base"], 3.0, 0),
        ("highlight edge on white", highlight.get("border", highlight["background"]), "#FFFFFF", 3.0, 0),
        *[(f"syntax {name}", color, backgrounds["base"], 4.5, 44) for name, color in accents.items()],
        ("diff add", diff["addForeground"], diff["addBackground"], 7.0, 60),
        ("diff delete", diff["deleteForeground"], diff["deleteBackground"], 7.0, 60),
        ("diff change", diff["changeForeground"], diff["changeBackground"], 7.0, 60),
        ("diff hunk", diff["hunkForeground"], diff["hunkBackground"], 7.0, 60),
        ("inline add", diff["inlineForeground"], diff["addEmphasis"], 7.0, 60),
        ("inline delete", diff["inlineForeground"], diff["deleteEmphasis"], 7.0, 60),
        ("inline change", diff["inlineForeground"], diff["changeEmphasis"], 7.0, 60),
        (
            "inline diff marker",
            highlight["foreground"],
            highlight["background"],
            4.5,
            0 if day else 35,
        ),
        ("conflict marker", diff["conflictForeground"], diff["conflictBackground"], 7.0, 60),
        *[
            (f"ANSI {name}", color, backgrounds["base"], 3.0 if name == "brightBlack" and not day else 4.5, 20 if name == "brightBlack" else 44)
            for name, color in ansi.items()
            if (day and name not in {"white", "brightWhite"}) or (not day and name != "black")
        ],
    ]

    # Day's supported text-bearing surfaces; crust/surface2 are chrome, not code.
    # Night keeps its existing gates; expanded observations are reported separately.
    surface_specs = []
    for surface in ("base", "mantle", "surface0", "surface1"):
        for name, color in {**foregrounds, **accents}.items():
            surface_specs.append((f"{name} on {surface}", color, backgrounds[surface], 4.5, 0))
    for surface in ("crust", "surface2"):
        for name in (foregrounds if day and surface == "crust" else ("text", "subtext", "bright")):
            surface_specs.append((f"chrome {name} on {surface}", foregrounds[name], backgrounds[surface], 4.5, 0))
    surface_specs += [
        ("inactive status label", foregrounds["muted"], backgrounds["mantle"], 4.5, 0),
        ("popup border", foregrounds["muted"] if day else backgrounds["surface2"], backgrounds["surface0"], 3.0, 0),
        ("search result", highlight["foreground"] if day else foregrounds["text"], highlight["background"] if day else diff["changeEmphasis"], 4.5, 0),
        ("selected popup kind", highlight["foreground"] if day else foregrounds["subtext"], highlight["background"], 4.5, 0),
        ("selected popup extra", highlight["foreground"] if day else foregrounds["muted"], highlight["background"], 4.5, 0),
        ("substitution", highlight["foreground"] if day else foregrounds["text"], highlight["background"] if day else diff["deleteForeground"], 4.5, 0),
        ("error annotation", foregrounds["text"] if day else foregrounds["text"], diff["deleteBackground"] if day else accents["coral"], 4.5, 0),
        ("tab label on crust", foregrounds["subtext"] if day else foregrounds["muted"], backgrounds["crust"], 4.5, 0),
        ("Neovim DiffText", highlight["foreground"], highlight["background"], 4.5, 0),
        *[(f"selection edge on {surface}", highlight.get("border", highlight["background"]), backgrounds[surface], 3.0, 0)
          for surface in ("mantle", "surface0", "surface1")],
        *[(f"git {state} sign", diff[f"{state}Foreground"], backgrounds["base"], 4.5, 0)
          for state in ("add", "delete", "change")],
        *[(f"status {name}", highlight["foreground"] if day else backgrounds["base"], highlight["background"] if day else accents[name], 4.5, 0)
          for name in ("olive", "sage", "mauve", "coral", "gold")],
    ]
    observations = [dict(name=n, foreground=f, background=b, wcag=round(wcag(f,b),2),
                         target=t, passed=wcag(f,b)>=t) for n,f,b,t,_ in surface_specs]
    if day:
        contrast_specs.extend(surface_specs)
        # Light ANSI endpoints are intended for dark indexed backgrounds, not
        # for the parchment canvas. Test their actual foreground/background use.
        contrast_specs.extend([
            (f"ANSI {light} on {dark}", ansi[light], ansi[dark], 4.5, 0)
            for light in ("white", "brightWhite")
            for dark in ("black", "red", "green", "yellow", "blue", "magenta", "cyan",
                         "brightRed", "brightGreen", "brightYellow", "brightBlue", "brightMagenta", "brightCyan")
        ])
        contrast_specs.extend([
            (f"ANSI black on {light}", ansi["black"], ansi[light], 7.0, 0)
            for light in ("white", "brightWhite")
        ])
        # Agent diff renderers can preserve syntax foregrounds over line fills.
        contrast_specs.extend([
            (f"diff {state} syntax {role}", color, diff[state+"Background"], 4.5, 0)
            for state in ("add", "delete", "change")
            for role, color in {**foregrounds, **accents}.items()
        ])

    contrasts = []
    failures = []
    for name, foreground, background, wcag_target, apca_target in contrast_specs:
        wcag_value = wcag(foreground, background)
        apca_value = apca(foreground, background)
        # Compare unrounded values: WCAG does not round a failing ratio up.
        passed = wcag_value >= wcag_target and abs(apca_value) >= apca_target
        contrasts.append(
            {
                "name": name,
                "foreground": foreground,
                "background": background,
                "wcag": round(wcag_value, 2),
                "wcagTarget": wcag_target,
                "apcaLc": round(apca_value, 1),
                "apcaTarget": apca_target,
                "passed": passed,
            }
        )
        if not passed:
            failures.append(name)

    all_colors = {}
    for family in ("backgrounds", "highlight", "foregrounds", "accents", "ansi", "diff"):
        for name, value in palette[family].items():
            all_colors[f"{family}.{name}"] = value

    color_data = {}
    for name, value in all_colors.items():
        lightness, chroma, hue = oklch(value)
        color_data[name] = {
            "hex": value,
            "oklch": [round(lightness, 4), round(chroma, 4), round(hue, 1) if math.isfinite(hue) else None],
            "inSrgb": True,
            "simulations": {mode: simulated_hex(value, mode) for mode in SIMULATIONS[1:]},
        }

    semantic_pairs = {
        # Diff state separation considers both foreground and line background.
        # Glyphs (+, -, ~) provide the final redundant, non-color cue.
        "diff add/delete": (
            diff["addForeground"], diff["deleteForeground"],
            diff["addBackground"], diff["deleteBackground"], 0.03,
        ),
        "diff add/change": (
            diff["addForeground"], diff["changeForeground"],
            diff["addBackground"], diff["changeBackground"], 0.03,
        ),
        "diff delete/change": (
            diff["deleteForeground"], diff["changeForeground"],
            diff["deleteBackground"], diff["changeBackground"], 0.03,
        ),
        "error/warning": (
            accents["coral"], accents["gold"],
            backgrounds["base"], backgrounds["base"], 0.05,
        ),
        "ANSI blue/bright blue": (
            ansi["blue"], ansi["brightBlue"], backgrounds["base"], backgrounds["base"], 0.03,
        ),
        "ANSI cyan/bright cyan": (
            ansi["cyan"], ansi["brightCyan"], backgrounds["base"], backgrounds["base"], 0.03,
        ),
    }
    separations = []
    for name, (first, second, first_bg, second_bg, floor) in semantic_pairs.items():
        values = {
            mode: round(max(delta_e(first, second, mode), delta_e(first_bg, second_bg, mode)), 3)
            for mode in SIMULATIONS
        }
        passed = min(max(delta_e(first, second, mode), delta_e(first_bg, second_bg, mode))
                     for mode in SIMULATIONS) >= floor
        informational = day and (name.startswith("diff ") or name.startswith("ANSI "))
        # Dawn intentionally aliases chromatic regular/bright slots. Their
        # separation is reported, not required; export tests enforce the aliases.
        entry = {"name": name, "deltaEOK": values, "floor": floor, "passed": passed}
        if informational: entry["informational"] = True
        separations.append(entry)
        if not passed and not informational:
            failures.append(name)

    # Track all accent proximity for discovery without turning every close hue
    # into a failure; semantic intent determines whether proximity is harmful.
    proximity = []
    for (left_name, left), (right_name, right) in combinations(accents.items(), 2):
        value = delta_e(left, right)
        if value < 0.05:
            proximity.append({"pair": f"{left_name}/{right_name}", "deltaEOK": round(value, 3)})
    proximity.sort(key=lambda item: item["deltaEOK"])

    role_pairs = {"numbers/keywords": ("ochre", "clay"), "information/hints": ("blue", "aqua"),
                  "operators/strings": ("olive", "sage"), "keywords/errors": ("clay", "coral")}
    role_review = [{"name": name, "deltaEOK": {mode: round(delta_e(accents[a], accents[b], mode), 4)
                    for mode in SIMULATIONS}} for name, (a,b) in role_pairs.items()]
    inline_review = [dict(state=state,
                          lineContrast=round(wcag(diff[state+'Emphasis'], diff[state+'Background']),3),
                          lineDeltaEOK={mode:round(delta_e(diff[state+'Emphasis'], diff[state+'Background'], mode),4)
                                        for mode in SIMULATIONS}) for state in ('add','delete','change')]
    changed_line_canvas = {mode:round(delta_e(diff['changeBackground'], backgrounds['base'], mode),4)
                           for mode in SIMULATIONS}
    report = {
        "palette": palette["name"],
        "colorSpace": palette["colorSpace"],
        "passed": not failures,
        "failures": failures,
        "contrast": contrasts,
        "inlineEmphasisReview": inline_review,
        "changedLineCanvasReview": changed_line_canvas,
        "surfaceObservations": observations,
        "semanticRoleReview": role_review,
        "colors": color_data,
        "semanticSeparation": separations,
        "accentProximityReview": proximity,
    }

    reports = ROOT / "tests/evaluation/results/palette"
    reports.mkdir(parents=True, exist_ok=True)
    report_stem = f"{variant}-audit"
    json_report = reports / f"{report_stem}.json"
    markdown_report = reports / f"{report_stem}.md"
    json_report.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")

    lines = [
        f"# {palette['name']} palette audit",
        "",
        f"Overall: **{'PASS' if report['passed'] else 'FAIL'}**",
        "",
        "WCAG ratios use unrounded values for gates. Normal text requires 4.5:1; 7:1 is an internal enhanced target where specified. APCA floors and ΔEOK floors are project heuristics, not WCAG conformance. A palette PASS does not certify applications or color-only semantics.",
        "",
        "## Text contrast",
        "",
        "| Role | WCAG | APCA Lc | Result |",
        "|---|---:|---:|---|",
    ]
    for check in contrasts:
        lines.append(
            f"| {check['name']} | {check['wcag']}:1 | {check['apcaLc']} | "
            f"{'PASS' if check['passed'] else 'FAIL'} |"
        )
    lines.extend(
        [
            "",
            "## Semantic separation under color-vision simulations",
            "",
            "Values are ΔEOK distances. They are comparative signals, not universal accessibility thresholds.",
            "",
            "| Pair | Normal | Protan | Deutan | Tritan | Gray | Result |",
            "|---|---:|---:|---:|---:|---:|---|",
        ]
    )
    for check in separations:
        values = check["deltaEOK"]
        lines.append(
            f"| {check['name']} | {values['normal']} | {values['protan']} | {values['deutan']} | "
            f"{values['tritan']} | {values['grayscale']} | {'INFO' if check.get('informational') else 'PASS' if check['passed'] else 'FAIL'} |"
        )
    lines.extend(["", "## Close accent pairs for visual review", ""])
    lines.extend(f"- `{item['pair']}`: ΔEOK {item['deltaEOK']}" for item in proximity)
    lines.extend(["", "## Syntax and diagnostic role review (not gates)", "",
                  "Color alone does not preserve these roles in every simulation. Keywords use bold by default in Day; numbers have literal syntax. Diagnostic signs/messages retain severity labels. Diff line signs retain + / - / ~; edited spans intentionally use ordinary weight and color-based emphasis. Color-vision simulations do not certify exact-span discoverability.", "",
                  "| Pair | Normal | Protan | Deutan | Tritan | Gray |", "|---|---:|---:|---:|---:|---:|"])
    for check in role_review:
        lines.append("| " + check["name"] + " | " + " | ".join(str(check["deltaEOK"][m]) for m in SIMULATIONS) + " |")
    lines.extend(["", "## Inline fill versus line background (observations)", "",
                  "These are not text contrast gates. Day intentionally uses ordinary-weight black inline text with color-based emphasis, without added bold or underline. Fill visibility and exact-span discoverability require separate native and human evaluation.", ""])
    for check in inline_review:
        lines.append(f"- {check['state']}: fill/line contrast {check['lineContrast']}:1; grayscale ΔEOK {check['lineDeltaEOK']['grayscale']}")
    lines.extend(["", "## Changed-line fill versus canvas (observations)", "",
                  "ΔEOK by mode: " + ", ".join(f"{mode} {value}" for mode,value in changed_line_canvas.items()) + ". These are comparative signals; line markers and inline emphasis remain necessary."])
    if not day:
        lines.extend(["", "## Expanded surface observations (legacy Night; not gated)", ""])
        lines.extend(f"- {c['name']}: {c['wcag']}:1 (target {c['target']}; {'meets' if c['passed'] else 'below'})" for c in observations)
    markdown_report.write_text("\n".join(lines) + "\n")

    for check in contrasts:
        print(
            f"{'PASS' if check['passed'] else 'FAIL'}  WCAG {check['wcag']:>5}:1  "
            f"APCA {check['apcaLc']:>6}  {check['name']}"
        )
    for check in separations:
        minimum = min(check["deltaEOK"].values())
        print(f"{'INFO' if check.get('informational') else 'PASS' if check['passed'] else 'FAIL'}  ΔEOK min {minimum:>5}  {check['name']}")
    print(f"\nWrote {markdown_report}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ithilien-dusk")
