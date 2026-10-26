# NHD Site Style Guide: "1901 Apothecary Broadsheet"

Context file for building every page of the NHD website "A Fatal Mix-Up: The 1901 Diphtheria Tragedy and America's First Leap into Drug Regulation." Every new page, section, or component must follow this file. Read it together with `CONTEXT.md` (project and editor context) and `CODE-SOURCING-RULES.md` (where code may come from).

## 1. The idea

The site should feel like a **1901 newspaper front page crossed with a pharmacy medicine label**: printed in ink on aged paper, set in a serif typeface, framed by rules and corners, and calm overall. The one exception is a single dark red "poison label" color, used where the story is about death.

It is **retro and printed**, not cartoony, not modern app UI, not glossy. If a choice would look out of place on a printed page in 1901, don't make it.

Three words to check every decision against: **inked, ruled, restrained.**

## 2. Color

Use only these colors. **Write the hex code directly in the CSS every time.** Do not use CSS variables (`var(--ink)`): the NHD editor turns any `color` or `background-color` that uses a variable into black (#000000) on import. The token names below are only for talking about the colors.

| Token | Hex | Role |
|---|---|---|
| `--ink` | `#243e50` | Main brand color. Masthead, headings, rules, borders, buttons, text on paper. |
| `--ink-deep` | `#1d2b35` | Body text. |
| `--paper` | `#faf6ed` | Main page surface (fresh newsprint). |
| `--paper-aged` | `#efe6d2` | Mats, card backs, alternate bands (older paper). |
| `--mist` | `#c8d5dc` | Outer background and the cool alternate band (the original site background). |
| `--rule` | `#cfc5ae` | Faint printed lines, image mats, ruled-paper lines. |
| `--muted` | `#5d6b75` | Captions, credits, secondary text. |
| `--poison` | `#783b40` | **Accent. Used sparingly.** The "13", hover state of the main Thesis button, the margin line in ruled-paper notes. Nothing else. |

Rules:
- No gradients that act as color (patterns made from gradients are fine, see section 6).
- No pure white `#fff` and no pure black `#000`.
- Text on `--ink` is always `--paper`. Text on paper is `--ink-deep` or `--ink`.
- Never introduce a new color. If something needs emphasis, use weight, size, or a rule, not a new hue.

## 3. Type

- **One typeface family:** `Georgia, "Times New Roman", serif` everywhere. No sans serif, no monospace.
- Title (h1): 64px desktop / 38px phone, bold, `--paper` on `--ink`.
- Subtitle (h2): 26px / 18px, italic, normal weight.
- Section heading (h3): 32px / 24px, normal weight, `--ink`, with a 1px `--ink` rule below.
- Body: 19px / 17px, line height 1.7.
- Captions and credits: 15px italic, `--muted`.
- Labels and small headings may use `font-variant: small-caps` with `letter-spacing: 1px`. Never all caps with wide letter spacing.
- The first paragraph of a page starts with a **drop cap**: about 4x body size, `--ink`, floated left.
- Large numerals (like the 13) are bold Georgia in `--poison`.

## 4. Shape, lines, and depth

- **Corner radius: 0 on everything.** Printed things have square corners. This includes buttons and cards taken from component libraries; set their radius to 0.
- **Borders:** 1px solid `--ink` for frames and boxes. Section dividers are `3px double var(--ink)`. Faint lines use `--rule`.
- **Depth = a hard offset print shadow,** like a slightly misaligned print: `6px 6px 0 var(--ink)` (or `4px 4px 0` for small items). **No blurry, soft shadows.** Only interactive items show the shadow, usually on hover.
- **Dashed outlines** (`1px dashed var(--ink)`) mean "cut along here" and appear behind lifted cards.
- **Ornaments:** a small diamond (a square rotated 45 degrees), double rules, and corner brackets. Nothing else: no icons, no emoji, no clip art.

## 5. Layout

- The page fills the full screen width. Sections are full-width bands that alternate backgrounds: `--ink` (masthead), `--paper`, `--mist` with the dot pattern, `--paper-aged`.
- Content inside a band sits in a column up to 1500px wide, with side padding of `5vw` (16px on phones).
- The first screen (masthead plus slideshow) is at least `100vh` tall.
- Vary the layouts: one centered band, then a two-column band, then a row of cards. Don't repeat the same layout twice in a row.
- Spacing scale: 8, 16, 24, 40, 64, 96px. Bands use 64 to 96px vertical padding.
- Phones (`max-width: 600px`): everything stacks into one column; corners and brackets get smaller.

## 6. Patterns (backgrounds)

All three are from Uiverse (see credits) and recolored to the palette:
- **Diamond lattice** on the masthead (`--ink` with faint lighter diamonds). Source: Javierrocadev "wicked-bullfrog-50".
- **Offset dot grid** on `--mist` bands, dots in `--ink` at low opacity. Source: BadlyWrittenStylesheet "fluffy-bear-71".
- **Ruled notebook paper** behind quotes and notes, ruled in `--rule` with a `--poison` margin line. Source: artvelog "splendid-quail-83".

Patterns always stay faint. Text over a pattern sits on a solid panel when it needs to be read.

## 7. Motion

- Only on hover, click, or once when the page loads. **No animations that loop forever.**
- Duration 0.3 to 0.6s, `ease` or `ease-out`.
- Allowed: fade, a small lift (`translate`), card flip, corner brackets drawing in, button face flipping down.
- Always include the `prefers-reduced-motion` block that turns motion off.
- **JavaScript effects (the `<script>` blocks at the bottom of home.html):**
  - *Tilt and cursor light* (vanilla-tilt.js): framed boxes tilt up to 6 degrees toward the mouse with a soft white light spot (the "lamp light"). This is the only glow allowed on the site. Mouse only; off on phones.
  - *Scroll reveal* (sal.js): content blocks slide up or fade in once, the first time they scroll into view. Add `data-sal="slide-up"` or `data-sal="fade"`, plus `data-sal-duration` (700 to 1000) and `data-sal-delay` (steps of 100 to 150) to stagger a row.
  - *Count up* (countUp.js): the big statistic counts from 0 to whatever number is typed in it, once, when it scrolls into view.
  - All three switch off for visitors who have reduced motion turned on.

## 8. Components (all from https://github.com/uiverse-io/galaxy, MIT license)

Full link to any file below: `https://github.com/uiverse-io/galaxy/blob/main/` + the source file path.

Each is recolored and squared off to match this guide. The structure and effect are kept from the source.

| Component | Used for | Source file |
|---|---|---|
| Corner-bracket frame | Frame around the slideshow; brackets draw in on hover | `Buttons/Dashrath-Sharma_wet-zebra-95.html` |
| Segmented picker | Slide 1 / 2 / 3 / 4 buttons | `Radio-buttons/Pradeepsaranbishnoi_slimy-warthog-37.html` |
| Hover-reveal card | Row of 4 cards: heading slides away, text slides up | `Cards/alexruix_silent-bulldog-61.html` |
| Flip card | Image on front, text on back | `Cards/vamsidevendrakumar_soft-shrimp-94.html` |
| Pop-up tooltip | Hover a term in the text to see its definition | `Tooltips/Quezaquo_bitter-wolverine-27.html` |
| Flip-down button | The main "Click here to see Thesis" button | `Buttons/mi-series_terrible-sheep-85.html` |
| Diamond pattern | Masthead background | `Patterns/Javierrocadev_wicked-bullfrog-50.html` |
| Dot pattern | Mist bands | `Patterns/BadlyWrittenStylesheet_fluffy-bear-71.html` |
| Ruled paper | Quote band | `Patterns/artvelog_splendid-quail-83.html` |

JavaScript libraries (copied unchanged into the bottom of home.html, all MIT):

| Library | Used for | Source |
|---|---|---|
| vanilla-tilt.js 1.8.1 by Sergiu Sandor | Tilt and cursor light | https://github.com/micku7zu/vanilla-tilt.js |
| sal.js 0.8.5 by Miroslaw Ciastek | Scroll reveal | https://github.com/mciastek/sal |
| countUp.js 2.10.1 by Jamie Perkins | Counting number | https://github.com/inorganik/countUp.js |

Changes made to every component: CSS scoped under `#fm`, colors swapped to the palette, radius set to 0, soft or glowing shadows replaced with hard print shadows, looping animations removed, sizes made to fill the layout.

**Credit them.** NHD rules require crediting everything taken from others. List Uiverse.io and each author in the annotated bibliography or wherever your teacher says to credit design sources.

## 9. Placeholder conventions

- The page holds only the student's own words. Empty slots are shown in square brackets: `[Heading]`, `[Text]`, `[Caption]`, `[Caption / credit]`, `[Quote]`, `[Source]`, `[Term]`, `[Definition]`, `[Image description]`.
- New images use the paths `images/photoN.jpg`, which get swapped for the paths from Manage Files.
- Every image gets a caption or credit slot underneath.

## 10. Quick checklist for any new page

- [ ] Only palette colors, `--poison` used in at most one or two places
- [ ] Georgia only; no all-caps headings with wide letter spacing
- [ ] Radius 0; shadows are hard offsets, never blurred
- [ ] Bands are full width and backgrounds alternate; the layout changes from band to band
- [ ] No looping animation; reduced-motion block included
- [ ] All CSS scoped under `#fm`; no `<script>`; no external files
- [ ] Every borrowed component credited
- [ ] Phone layout checked at 390px wide

## 11. NHD WebCentral lessons (learned from the live site)

- **No CSS variables for colors.** The editor rewrites `color:var(--x)` and `background-color:var(--x)` as `#000000`. Write hex codes.
- **Bootstrap 4 is loaded on every page.** Never use its class names for your own elements: `container`, `card`, `row`, `col`, `btn`, `nav`, `navbar`, `badge`, `alert`, `modal`, `carousel-item`, `active`, `collapse`, `jumbotron`. Components copied from a library that use these names get renamed (for example `card` became `rv-card` and `flip-card`).
- **The page sits inside `<div class="container it-is-set">`**, which caps the width at 1140px. To fill the screen, this page's CSS sets `.container.it-is-set{max-width:100%; padding-left:0; padding-right:0;}`.
- Bootstrap adds bottom margins to `p`, `label`, `figure`, `h1` to `h3`. Reset them inside `#fm` where spacing matters.
- **Scripts do run on the published site** (the site allows inline scripts). They do not run inside the editor canvas, so check them with Preview. Content hidden by the scroll reveal still shows normally in the editor.
- The old slideshow script left over from the earlier home page still runs and adds `.carousel-nav` dots; it is hidden with `#fm .carousel-nav{display:none}`. Delete that script block in the editor when possible.
