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
- No drop cap: no licensed GitHub source was found for one (see `SOURCES.md`, "Requests with no source found").
- Large numerals (like the 13) are bold Georgia in `--poison`.

## 4. Shape, lines, and depth

- **Corner radius: 0 on everything.** Printed things have square corners. This includes buttons and cards taken from component libraries; set their radius to 0.
- **Borders:** 1px solid `--ink` for frames and boxes. Section dividers are `3px double #243e50`. Faint lines use `--rule`.
- **Depth = a hard offset print shadow,** like a slightly misaligned print: `6px 6px 0 #243e50` (or `4px 4px 0` for small items). **No blurry, soft shadows.** Only interactive items show the shadow, usually on hover.
- **Dashed outlines** (`1px dashed #243e50`) mean "cut along here" and appear behind lifted cards.
- **Ornaments:** double rules, the diamond pattern, and corner brackets. Nothing else: no icons, no emoji, no clip art.

## 5. Layout

- The page fills the full screen width. Sections are full-width bands that alternate backgrounds: `--ink` (masthead), `--paper`, `--mist` with the dot pattern, `--paper-aged`.
- Bands are Bootstrap `container-fluid` blocks with `px-lg-5` side padding; content sits in Bootstrap rows and columns.
- The first screen (masthead plus slideshow) uses Bootstrap's `min-vh-100` so it fills the screen.
- Vary the layouts: one centered band, then a two-column band, then a row of cards. Don't repeat the same layout twice in a row.
- Spacing uses Bootstrap's spacing classes; bands use `py-6` (5rem, copied from Bootstrap's `py-5`).
- Phones: Bootstrap's grid stacks every row into one column.

## 6. Patterns (backgrounds)

All three are from Uiverse (see credits) and recolored to the palette:
- **Diamond lattice** on the masthead (`--ink` with faint lighter diamonds). Source: Javierrocadev "wicked-bullfrog-50".
- **Offset dot grid** on `--mist` bands, dots in `--ink` at low opacity. Source: BadlyWrittenStylesheet "fluffy-bear-71".
- **Ruled notebook paper** behind quotes and notes, ruled in `--rule` with a `--poison` margin line. Source: artvelog "splendid-quail-83".

Patterns always stay faint. Text over a pattern sits on a solid panel when it needs to be read.

## 7. Motion

- Only on hover, click, or once when content scrolls into view. **No animations that loop forever.**
- Allowed: fade, a small lift, card flip, corner brackets drawing in, button face flipping down, the slideshow sliding.
- Reduced motion: Bootstrap's reduced-motion rule, applied to all of `#fm`, turns off CSS transitions.
- **JavaScript effects (the `<script>` blocks at the bottom of home.html):**
  - *Tilt and cursor light* (vanilla-tilt.js): framed boxes (`js-tilt` class) tilt up to 6 degrees toward the mouse with a soft white light spot (the "lamp light"). This is the only glow allowed on the site.
  - *Scroll reveal* (ScrollOut): columns with a `data-scroll` attribute fade in once, the first time they scroll into view. Nothing is hidden until the script runs, so everything stays visible in the editor.
  - *Count up* (countUp.js): the 13 counts up from 0 once, when it scrolls into view. If the number changes, change `13` in the last script too.
  - *Slideshow and click-to-open* run on Bootstrap's own script, which NHD already loads.

## 8. Components

Every component and its exact source file is listed in `SOURCES.md`, which the screening tool generates. In short:

| Part of the page | Built from |
|---|---|
| Layout, bands, rows, columns, spacing | Bootstrap 4.3.1 grid docs and utility classes |
| Masthead | Bootstrap jumbotron + Uiverse diamond pattern (Javierrocadev) |
| Slideshow | Bootstrap carousel + Uiverse corner-bracket frame (Dashrath-Sharma) + Uiverse object-fit rule (Admin12121) |
| "13 Children died" box | Bootstrap card, with countUp.js |
| Hover cards | Uiverse hover-reveal card (alexruix) on the Uiverse dot pattern (BadlyWrittenStylesheet) |
| Feature image and text | Bootstrap figure, images and typography + Uiverse tooltip (Quezaquo) |
| Flip cards | Uiverse flip card (vamsidevendrakumar) + Uiverse object-fit rule (ProgramaConPid) |
| Quote | Bootstrap blockquote on the Uiverse ruled paper (artvelog) |
| Click-to-open section | Bootstrap collapse accordion |
| Thesis button | Original link + Uiverse flip-down button (mi-series) |
| Effects | vanilla-tilt.js, ScrollOut, countUp.js |

All restyling follows the allowed changes in `CODE-SOURCING-RULES.md`: values changed to this guide's colors, sizes, radius 0 and hard shadows; selectors renamed or prefixed with `#fm`.

**Credit them.** NHD rules require crediting everything taken from others. List Bootstrap, Uiverse.io and each author, vanilla-tilt.js, ScrollOut and countUp.js in the annotated bibliography or wherever your teacher says to credit design sources.

## 9. Placeholder conventions

- The page holds only the student's own words. Empty slots are shown in square brackets: `[Heading]`, `[Text]`, `[Caption]`, `[Caption / credit]`, `[Quote]`, `[Source]`, `[Term]`, `[Definition]`, `[Image description]`.
- New images use the paths `images/photoN.jpg`, which get swapped for the paths from Manage Files.
- Every image gets a caption or credit slot.

## 10. Quick checklist for any change

- [ ] `python3 tools/check_sources.py --write-log` passes (see `CODE-SOURCING-RULES.md`)
- [ ] Only palette colors, written as hex codes; `#783b40` used in at most one or two places
- [ ] Georgia only; no all-caps headings with wide letter spacing
- [ ] Radius 0; shadows are hard offsets, never blurred
- [ ] Bands are full width and backgrounds alternate; the layout changes from band to band
- [ ] No looping animation
- [ ] All CSS scoped under `#fm` (except the NHD full-width override)
- [ ] Phone layout checked at 390px wide

## 11. NHD WebCentral lessons

See `CONTEXT.md`, "Lessons learned on the live site."
