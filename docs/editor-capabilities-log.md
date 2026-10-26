# NHD WebCentral Editor: What It Can Make (log, 2026-10-25)

Read straight from the editor's own settings in the logged in editor (site.nhdwebcentral.org/Edit). Nothing on the site was changed. This is the reference for `EDITOR-FORMAT.md` and `tools/check_format.py`: if something isn't listed here, the editor can't make it.

## Blocks and the code each one adds

When a block is dropped on the page, the editor gives each element an id like `#imyi` and turns any starting styles into a `#id{...}` rule.

| Block (panel name) | Code it adds | Starting styles |
|---|---|---|
| Section | `div` | `min-height:40px; padding-top:8px; padding-bottom:8px` |
| Title | `h1` | none |
| Subtitle | `h2` | none |
| Header | `h3` | none |
| Horizontal Rule | `hr` | none |
| Primary Source Quote | text, `br`, then `i` "Add Source Credit" | `i`: `font-size:smaller` |
| Secondary Source Quote | same as Primary | `i`: `font-size:smaller` |
| Spacer | empty box `div` | none |
| Image and Source Credit | `div` > `img` + `div` "Add Source Credit" | outer: `display:flex; align-items:center; flex-direction:column; text-align:center`; credit: `font-size:smaller` |
| Navigation Button | `div` "Nav Button" (a link button) | none |
| Section Header & Text | `section.bdg-sect` > `h1.heading` + `p.paragraph` | none |
| Embed MP3, MP4 or PDF | embed `div` | none |
| 2 Columns | `div.rowx` > 2 x `div.col-md-6` | each: `margin-bottom:5px` |
| 3 Columns | `div.rowx` > 3 x `div.col-md-4` | each: `margin-bottom:5px` |
| 4 Columns | `div.rowx` > 4 x `div.col-md-3` | each: `margin-bottom:5px` |
| Columns 3/7 | `div.rowx` > `div.col-md-4` + `div.col-md-8` | each: `margin-bottom:5px` |
| Columns 7/3 | `div.rowx` > `div.col-md-8` + `div.col-md-4` | each: `margin-bottom:5px` |
| Columns 3/4/3 | `div.rowx` > `col-md-3` + `col-md-6` + `col-md-3` | each: `margin-bottom:5px` |
| Flexbox | `div.row` > 2 x `div.cell` | class rules: `.row{display:flex; justify-content:flex-start; align-items:stretch; flex-wrap:nowrap; padding:10px}`, `@media (max-width: 768px){.row{flex-wrap:wrap}}`, `.cell{min-height:75px; flex-grow:1; flex-basis:100%}` |
| auto-Nav | `[***smart-nav***]` nav bar | none |
| Image Carousel | `div.carousel` with `img.slide` + its script | none |
| Text, Hyperlink Text | `div` / `a` | none |
| Custom Code | raw HTML box (scripts don't show in the canvas) | none |

`col-md-*` are Bootstrap grid classes (Bootstrap 4.3.1 is on every page), so column blocks stack on phones by themselves.

## Style panel: every property it can set

| Section | Properties |
|---|---|
| General | display, position, top, right, bottom, left, text-align |
| Font | font-family, font-size, font-weight, letter-spacing, color, line-height, text-align, text-decoration, text-shadow |
| Dimension | width, flex-basis, height, max-width, min-height, margin (each side), padding (each side) |
| Decorations | opacity, background-color, border-radius (each corner), border (width, style, color; all four sides together), box-shadow, background (image from a file, repeat, position, attachment, size) |
| Extra | transition (property, duration, timing), perspective, transform (rotate x/y/z, scale x/y/z only, no move/translate) |
| Flex | display, flex-direction, justify-content, align-items, order, flex (grow, shrink, basis), align-self, vertical-align |

**Fonts in the list:** Arial, Arial Black, Brush Script MT, Comic Sans MS, Courier New, Georgia, Helvetica, Impact, Lucida Sans Unicode, Tahoma, Times New Roman, Trebuchet MS, Verdana.

**States (hover and so on):** hover, active, nth-of-type(2n).

**Device sizes:** Desktop; Tablet (`@media (max-width: 992px)`); Mobile landscape (`@media (max-width: 768px)`); Mobile portrait (`@media (max-width: 480px)`).

## What the panel can't do

- No italic or uppercase settings (no `font-style`, `text-transform`). Italic comes from the text editor's italic button (`<i>`), as in the quote blocks.
- No single-side borders (`border-top`, `border-bottom` only); borders apply to all four sides. A divider line is the Horizontal Rule block.
- No gradients: background image is a file picker.
- No `object-fit`, no `flex-wrap` (except inside the Flexbox block's own rules), no `translate` moves, no keyframe animations, no `::before` / `::after`.

## Other findings

- The editor does not autosave (`autosave: false`); changes only stick when Save is clicked.
- At the time of reading, the editor's copy of Home held the archived sourced version (`#fm` wrapper) with **no CSS rules loaded**. Someone was also "currently editing this page." Check the page in Preview before saving anything over it.
