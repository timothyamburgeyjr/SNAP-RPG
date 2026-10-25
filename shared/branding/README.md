# SNAP wiki branding assets

Built from the approved SNAP wordmark (the A with the notch-and-tab joint, orange crossbar and sparks).
All text is outlined into paths, so nothing depends on a font being installed.
Palette: slate #39434c, orange #f0502c, cream #f6f2ea.

## How MediaWiki uses them (Vector 2022)

MediaWiki takes three separate logo images and lays them out for you: the **icon** on one side, and the
**wordmark** stacked above the **tagline** beside it. The wordmark and tagline together must stay under
50 px tall. Wikipedia supplies all three; mediawiki.org supplies only an icon and a wordmark.

## Default set (top level)

| File | Role | Size |
|---|---|---|
| icon.svg | `icon` - the A on a slate tile | 50x50 |
| icon-100.png | PNG fallback for `icon` | 100x100 |
| wordmark.svg | `wordmark` - SNAP (with sparks) | 102x34 |
| tagline.svg | `tagline` - "A Free Tabletop RPG" | 102x11 |
| logo-135.png | legacy `1x` logo (non-Vector skins) | 135x135 |
| favicon.ico / favicon.svg | browser tab icon | 16/32/48 + scalable |
| apple-touch-icon.png | iOS home screen | 180x180 |
| icon-192.png / icon-512.png | web app icons | - |
| og-image.png | social share card | 1200x630 |
| icon-transparent.svg | the A on transparent, for light backgrounds | - |
| a-mark-detailed.svg | full-detail A (with the joint), for print and large use | - |
| *-light.svg | cream wordmark/tagline for dark backgrounds | - |

Wordmark and tagline are exactly the same width (edge to edge, measured on ink), and stack to 34 + 2 + 11 = 47 px.

## Alternate lockups (lockups/ folder)

Each folder holds a matched wordmark + tagline pair (plus light versions). Swap in all four files and use the sizes below.

| Folder | Tagline | Width | Wordmark height | Stack |
|---|---|---|---|---|
| free-tabletop-rpg | A Free Tabletop RPG (the default) | 102 | 34 | 47 px |
| tabletop-rpg | A tabletop roleplaying game | 133 | 32 | 45 px |
| tabletop-rpg-sparks | A tabletop roleplaying game (SNAP keeps its sparks) | 110 | 36 | 49 px |
| meaning | Setting-Neutral Adventure Platform (placeholder expansion) | 140 | 34 | 47 px |

The default keeps SNAP's sparks because the tagline is short enough to match at full size. The longer taglines either drop the sparks
(tabletop-rpg) or shrink the type to about 8 px (tabletop-rpg-sparks, meaning).

## LocalSettings.php

Copy the files to a `branding/` folder in the web root (so upgrades never overwrite them), then:

```php
$wgLogos = [
    'icon' => "$wgScriptPath/branding/icon.svg",
    'wordmark' => [
        'src' => "$wgScriptPath/branding/wordmark.svg",
        'width' => 102,
        'height' => 34,
    ],
    'tagline' => [
        'src' => "$wgScriptPath/branding/tagline.svg",
        'width' => 102,
        'height' => 11,
    ],
    // legacy fallback for skins that still use a single logo
    '1x' => "$wgScriptPath/branding/logo-135.png",
];
$wgFavicon = "$wgScriptPath/branding/favicon.ico";
$wgAppleTouchIcon = "$wgScriptPath/branding/apple-touch-icon.png";
```

For another lockup, change the files and the width/height numbers to match the table above.
Keep favicon.ico under 50 KB (it is about 3 KB) so larger sizes are not ignored.

## Notes

- Dark mode: light wordmark/tagline variants are included. Wiring them to night mode needs a small CSS rule in
  MediaWiki:Common.css. The icon already works on both because it sits on its own slate tile.
- The tagline is set in Nunito (SIL Open Font License) and outlined, so no font ships with the wiki.
- The images and SVGs in this folder may carry an embedded content-credentials block added by the platform; it is harmless.

## Cream theme (theme/ folder)

`theme/snap-theme.css` turns Vector 2022's white surface into the SNAP cream by overriding the skin's CSS variables.
Dark mode is untouched: Vector's night palettes are more specific than `:root`, so they still win.
Add `theme/LocalSettings-theme-snippet.php` to LocalSettings.php (the CSS sits in the same `branding/` folder as the logos).
Orange is for accents only: it is 3.2:1 on cream, below the 4.5:1 minimum for text, and orange links would look like red links.

## Paper skin (theme/snap-paper.css and theme/paper/)

Starter CSS for the "old paper, worn border, map fold" look the family asked for, plus the Main Page box classes
(`.snap-banner`, `.snap-box`, `.snap-protocol`). Layer it on top of snap-theme.css.
It is untested on a live wiki: the .mw-body selector in particular must be checked in the browser inspector.
Eye-strain guardrails are in the file's header comment (flat text areas, very low grain, no texture for readers who ask for more contrast).

`theme/paper/` holds two small paper-grain tiles and the two welcome banners drawn through the Oasis (A and B; B is used in the mockups).

SVG schematics: add `$wgFileExtensions[] = 'svg';` to LocalSettings.php. MediaWiki refuses SVGs containing scripts or HTML by default,
so uploaded schematics are static vector files (they still zoom cleanly); an interactive viewer would be linked or embedded separately.
