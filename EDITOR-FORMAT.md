# Editor Format Rules

The page code must look exactly like code the NHD WebCentral editor writes itself, so every part of it can be selected, dragged and restyled in the editor like any block added by hand. The teacher approved this approach on 2026-10-25 (see `CONTEXT.md`). AI help with the code still has to be credited in the annotated bibliography.

Before every commit, run:

```
python3 tools/check_format.py
```

It must print "Format check passed".

## HTML

- Only basic editor elements: `div`, `p`, headings, `strong`, `em`, `br`, `a`, `img`, `span`, lists, `blockquote`, tables.
- Every element that gets styled has an **editor style id**: `i` plus 3 to 5 lowercase letters or digits (like `#itsa`, `#i2k2s`, `#iw3ta`). Ids are unique.
- **No custom class names.** The only classes are the editor's own from the original page: `auto-nav`, `container`, `c1363`, `carousel`, `slide`.
- **No comments, no inline `style=`, no `onclick` or other event attributes, no `data-` or `aria-` attributes.**
- **The only script** is the editor's original carousel script, unchanged (kept in `original-export/carousel-script.js`).
- Keep the original ids and text from the student's page: `#itsa`, `#i2k2s`, `#isl1`, `#ihq6k`, `#ipwhb`, `#irtjk`, and the `[***smart-nav***]` tag.

## CSS

- **One rule per element**, written as `#id{...}`. Hover styles are `#id:hover{...}` (the style panel's State menu).
- The original page's own rules (`body`, `.c1363`, `.slide`, `.container.c1363`, `.auto-nav`) may stay.
- **Allowed:** anything the style panel can set: fonts, colors, spacing, borders, radius, shadows, backgrounds and gradients, flex layout, opacity, `transform` and `transition` (Extra section).
- **Not allowed:** comments, `@keyframes` and `animation`, `var()`, `!important`, `@import`, pseudo-elements (`::before`), grouped selectors (`#a, #b`), class or tag selectors beyond the original ones.
- **Colors as hex codes** (`#243e50`). The editor turns `var(--x)` colors black.
- **Phone and tablet layouts** only through the editor's device sizes: `@media (max-width: 992px)`, `(max-width: 768px)`, `(max-width: 480px)`.
- **Fonts** from the editor's Font list (Georgia, Times New Roman, Arial, Helvetica, Verdana, Trebuchet MS and so on). No web fonts.

## Content

- The page text is the student's own. New text slots use bracketed placeholders: `[Heading]`, `[Text]`, `[Caption]`, `[Quote]`, `[Source]`, `[Year]`, `[Section label]`.
- New images point at `../90886777/uploaded/[your-image].png` until the student uploads real ones through Manage Files.
