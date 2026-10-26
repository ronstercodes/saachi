# Editor Format Rules

The page code must look exactly like code the NHD WebCentral editor writes itself, so every part of it can be selected, dragged and restyled in the editor like any block added by hand. The teacher approved this approach on 2026-10-25 (see `CONTEXT.md`). Everything allowed here comes from `docs/editor-capabilities-log.md`, which was read from the editor itself. AI help with the code still has to be credited in the annotated bibliography.

Before every commit, run:

```
python3 tools/check_format.py
```

It must print "Format check passed".

## HTML

- Only elements the editor's blocks and text tools make: `div`, `section`, `p`, headings, `hr`, `strong`, `b`, `i`, `em`, `u`, `br`, `a`, `img`, `span`, lists, `blockquote`.
- Every element that gets styled has an **editor style id**: `i` plus 3 to 5 lowercase letters or digits (like `#itsa`, `#i2k2s`, `#iw3ta`). Ids are unique.
- **No custom class names.** Only the classes the editor's own blocks add: `auto-nav`, `container`, `c1363`, `carousel`, `slide` (original page); `rowx` and `col-md-3`, `col-md-4`, `col-md-6`, `col-md-8` (column blocks); `bdg-sect`, `heading`, `paragraph` (Section Header & Text); `row`, `cell` (Flexbox).
- Columns are built like the editor's column blocks: a `div.rowx` holding `div.col-md-*` cells. Give the `rowx` its own id with `display:flex`, and `display:block` at 768px so columns stack on phones.
- **No comments, no inline `style=`, no `onclick` or other event attributes, no `data-` or `aria-` attributes.**
- **The only script** is the editor's original carousel script, unchanged (kept in `original-export/carousel-script.js`).
- Keep the original ids and text from the student's page: `#itsa`, `#i2k2s`, `#isl1`, `#ihq6k`, `#ipwhb`, `#irtjk`, and the `[***smart-nav***]` tag.

## CSS

- **One rule per element**, written as `#id{...}`. Hover styles are `#id:hover{...}` (the style panel's State menu).
- The original page's own rules (`body`, `.c1363`, `.slide`, `.container.c1363`, `.auto-nav`) may stay.
- **Allowed:** only properties the style panel can set (full list in the log): fonts, colors, spacing, size, borders on all four sides, radius, box and text shadows (several layers allowed), background color, opacity, flex layout, `transition`, and `transform` with rotate and scale only. Hover, active and nth-of-type(2n) states.
- **Not allowed:** comments, `@keyframes` and `animation`, gradients, `translate`, `font-style`, `text-transform`, `object-fit`, `flex-wrap`, single-side borders, `var()`, `!important`, `@import`, pseudo-elements (`::before`), grouped selectors (`#a, #b`), class or tag selectors beyond the original ones. Use `<i>` for italics and the `hr` element for divider lines.
- **Colors as hex codes** (`#243e50`). The editor turns `var(--x)` colors black.
- **Phone and tablet layouts** only through the editor's device sizes: `@media (max-width: 992px)`, `(max-width: 768px)`, `(max-width: 480px)`.
- **Fonts** only from the editor's Font list: Arial, Arial Black, Brush Script MT, Comic Sans MS, Courier New, Georgia, Helvetica, Impact, Lucida Sans Unicode, Tahoma, Times New Roman, Trebuchet MS, Verdana.

## Content

- The page text is the student's own. New text slots use bracketed placeholders: `[Heading]`, `[Text]`, `[Caption]`, `[Quote]`, `[Source]`, `[Year]`, `[Section label]`.
- New images point at `../90886777/uploaded/[your-image].png` until the student uploads real ones through Manage Files.
