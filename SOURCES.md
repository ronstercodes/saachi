# Code Sources Log

Every piece of outside code in this site is logged here. Rules for adding to it are in `CODE-SOURCING-RULES.md`. License texts are in `THIRD_PARTY_NOTICES.md`.

## Baseline (first commit), and who wrote what

To be transparent about the starting point:

- **Original page** (`original-export/nhd_html_css_10-25-2026.md`): the site as it was before the redesign. This is the student's text and earlier page structure, including an older slideshow script.
- **Written by Claude (Anthropic AI) on 2026-10-25**, before these rules took effect, and frozen as part of the baseline:
  - The overall page layout and section structure in `home.html`
  - The CSS-only slideshow logic (hidden radio buttons that switch slides and captions)
  - The masthead, opening section (drop cap, "13" box), feature section, quote section, click-to-open section and phone layout in `home.css`
  - The NHD fixes (full-width override, Bootstrap margin resets, hiding `.carousel-nav`)
  - The scroll-reveal state classes (`#fm.fx-on ...`), written in place of `sal.css`
  - The short setup script at the bottom of `home.html` ("setup for this page") that starts the three libraries
- **Copied from GitHub:** everything in the tables below.

Under `CODE-SOURCING-RULES.md`, nothing else may be written from scratch from this point on.

## CSS/HTML components: Uiverse.io (uiverse-io/galaxy)

Repository: https://github.com/uiverse-io/galaxy
Commit copied: `adbd2adde0a299a3956ea288fb444ec01891ca41`
License: MIT (Copyright (c) 2023 Uiverse.io)
File link pattern: `https://github.com/uiverse-io/galaxy/blob/main/<file path>`

Changes common to all rows: selectors prefixed with `#fm`; colors replaced with `DESIGN.md` hex codes; corner radius set to 0.

| # | Component | Author | File path | Used in | Other changes |
|---|---|---|---|---|---|
| 1 | Diamond pattern | Javierrocadev | `Patterns/Javierrocadev_wicked-bullfrog-50.html` | Masthead background (`#fm .mast`) | Class `container` renamed to `mast` (Bootstrap clash); gradient colors recolored. |
| 2 | Offset dot pattern | BadlyWrittenStylesheet | `Patterns/BadlyWrittenStylesheet_fluffy-bear-71.html` | Hover-card band background (`#fm .reveal`) | Class `container` renamed to `reveal`; CSS variable `--size` replaced with fixed values (2.4rem, 1.2rem), since the editor breaks variables; dots set to translucent ink. |
| 3 | Ruled notebook paper | artvelog | `Patterns/artvelog_splendid-quail-83.html` | Quote band background (`#fm .notes`) | Class `container` renamed to `notes`; margin line moved to 8vw; line spacing 38px. |
| 4 | Corner-bracket button | Dashrath-Sharma | `Buttons/Dashrath-Sharma_wet-zebra-95.html` | Slideshow frame (`#fm .border-el-btn` and its 4 spans) | Turned from a button into a frame around the slides; `nth-child` indexes shifted by one because the frame div comes first; glow `box-shadow` and `:active` scale removed; bars 4px thick. |
| 5 | Segmented radio picker | Pradeepsaranbishnoi | `Radio-buttons/Pradeepsaranbishnoi_slimy-warthog-37.html` | Slide picker 1 to 4 (`#fm .mydict`) | Radio inputs moved to the top of the slideshow so they can also switch slides; checked state written as `#sa:checked ~ .mydict .da span` and so on; global `:focus` rule removed; labels changed to 1 to 4. |
| 6 | Hover-reveal card | alexruix | `Cards/alexruix_silent-bulldog-61.html` | Row of 4 cards (`#fm .rv`) | Classes renamed `container` to `rv`, `card` to `rv-card`, `card-hidden` to `rv-hidden`, `card-border` to `rv-border` (Bootstrap clash); fixed 190x254 size replaced with a flexible row 340px tall; inner link button removed (no destination); text replaced with `[Heading]` and `[Text]`. |
| 7 | Flip card | vamsidevendrakumar | `Cards/vamsidevendrakumar_soft-shrimp-94.html` | Row of 3 flip cards (`#fm .flips`) | Classes renamed `card` to `flip-card`, `card-inner` to `flip-inner`, `card-front` to `flip-front`, `card-back` to `flip-back`; front holds an image, back holds `[Text]`; hard print shadow added; size 380px tall in a flexible row. |
| 8 | Pop-up tooltip | Quezaquo | `Tooltips/Quezaquo_bitter-wolverine-27.html` | Term definition in the feature text (`#fm .tip`) | Classes `container` to `tip`, `p` to `span.tt` (inline in a paragraph); looping `bounce` animation removed; pop-up keyframes shortened so it opens above the term; size fits a definition; emoji removed. |
| 9 | Flip-down button | mi-series | `Buttons/mi-series_terrible-sheep-85.html` | "Click here to see Thesis" (`#fm #irtjk`) | Applied to the existing link instead of a `<button>`; full width, 96px tall; flipped face turns `#783b40` on hover. |

## JavaScript libraries

Copied unchanged into the `<script>` blocks at the bottom of `home.html`.

| # | Library | Author | Repo | File copied | Version / commit | License | Used for |
|---|---|---|---|---|---|---|---|
| 10 | vanilla-tilt.js | Sergiu Sandor (micku7zu) | https://github.com/micku7zu/vanilla-tilt.js | `dist/vanilla-tilt.min.js` | 1.8.1, `48f4ee931d4d91dcdd2f91803db67a9f3a16587e` | MIT | 3D tilt and cursor light on framed boxes |
| 11 | sal.js | Miroslaw Ciastek (mciastek) | https://github.com/mciastek/sal | `dist/sal.js` | 0.8.5, `789ac41161cffee81365c94142c1a955c5118cc4` | MIT | Scroll reveal (`data-sal` attributes) |
| 12 | countUp.js | Jamie Perkins (inorganik) | https://github.com/inorganik/countUp.js | `dist/countUp.umd.js` | 2.10.1, `a47732056085af3e0e81374db71e088dddf17362` | MIT | The 13 counting up |

Library settings in use (set in the baseline setup script, not changes to the libraries):
- vanilla-tilt: `max: 6, speed: 700, perspective: 1100, scale: 1.02, glare: true, 'max-glare': 0.5, gyroscope: false`, mouse only, on `.border-el-btn, #ipwhb, .rv, .feat-img, .flip-card`
- sal: `threshold: 0.15, once: true`, turned off when reduced motion is on
- countUp: `duration: 2.2, enableScrollSpy: true, scrollSpyOnce: true`
- `sal.css` from the sal repo is **not** included. The editor's CSS importer mangles its variables, so the baseline uses its own state classes instead.

## Log of later additions

Add new rows here, newest at the bottom. One row per sourced piece.

| Date | Repo | File path | Author | Commit / version | License | Where it went | Changes made |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Requests with no source found

List features that were asked for but couldn't be sourced from a GitHub repo, so they were left out.

- (none yet)
