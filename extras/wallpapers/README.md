# Ithilien wallpapers

Painterly views of Ithilien at Dawn and Dusk.

| Device | Resolution | Dawn | Dusk |
| --- | --- | --- | --- |
| Desktop | 5120 × 2880 | [PNG](ithilien_dawn_desktop_5120x2880.png) | [PNG](ithilien_dusk_desktop_5120x2880.png) |
| iPhone 17 Pro Max | 1320 × 2868 | [PNG](ithilien_dawn_iphone_1320x2868.png) | [PNG](ithilien_dusk_iphone_1320x2868.png) |
| iPad Pro 13-inch | 2064 × 2752 | [PNG](ithilien_dawn_ipad_2064x2752.png) | [PNG](ithilien_dusk_ipad_2064x2752.png) |

## macOS light/dark wallpaper

[Download the dynamic desktop HEIC](ithilien_dynamic_desktop.heic). It contains
both 5K images, with Dawn mapped to Light appearance and Dusk to Dark. Add it in
**System Settings → Wallpaper** and choose **Automatic** if an appearance
selector is offered.

The iPhone and iPad downloads are separate portrait PNGs. Time-of-day switching
must be configured on the device.

## Artwork and regeneration

The PNGs are the approved wallpaper assets. Mobile compositions were generated
separately and resized with Lanczos to the listed dimensions. Wallpaper artwork
is independent of the theme palette generator.

To rebuild the desktop HEIC from its two PNGs on macOS:

```sh
mkdir -p .evaluation-runtime/wallpaper-swift-cache
swift -module-cache-path .evaluation-runtime/wallpaper-swift-cache scripts/generate_wallpaper.swift
```

Requires Apple's Swift toolchain and ImageIO. Encoding uses maximum quality
without resizing; HEIC can still be lossy. The script verifies both frames'
dimensions and the light/dark metadata before replacing the output.
