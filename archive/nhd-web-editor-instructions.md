# Context: Writing HTML/CSS for the NHD WebCentral Editor

> **Updated 2026-10-25.** For this repo, `CLAUDE.md`, `CODE-SOURCING-RULES.md`, `CONTEXT.md` and `DESIGN.md` take priority over this file. This file is the general reference for how the editor behaves.

You are helping a user build pages for a National History Day (NHD) website using **NHD WebCentral** (site.nhd.org/Edit). The user does not write code themselves. They copy and paste whatever you give them, so your output must work on the first paste with no editing.

## How the editor works

- NHD WebCentral is built on **GrapesJS**, a drag and drop page builder.
- Code gets into a page two ways:
  1. **Import box** ("Paste your HTML/CSS and click Import"). Accepts HTML and CSS only.
  2. **Custom Code block** ("Insert your code"). Accepts raw HTML, but any code containing `<script>` shows the warning *"Custom code with <script> can't be rendered on the canvas"* and only appears in Preview or on the published site.
- **JavaScript does work on the published site.** There is no separate JS box, but `<script>` tags pasted into the Import window's HTML box are kept and run in **Preview** and on the **published site**. They do **not** run inside the editor canvas. The site's security settings allow inline scripts (`script-src 'unsafe-inline'`).
- The editor loads **Bootstrap 4.3.1**, jQuery and Font Awesome on every page, and wraps each page in `<div class="container it-is-set">` (capped at 1140px wide).
- Clicks inside the editing canvas select elements instead of triggering them. Interactions should be tested with the **Preview** (eye icon) button.

## Hard rules

1. **Keep scripts inline and at the bottom of the HTML.** Put any `<script>` at the end of the HTML box. No external script files except from the site's approved hosts. The page must still look right with scripts off, since the editor canvas never runs them. Prefer the CSS-only tricks below when they do the job.
2. **No full page tags.** Do not output `<!DOCTYPE>`, `<html>`, `<head>`, `<body>`, `<meta>`, or `<title>`. Output a fragment only.
3. **No external resources.** NHD sites must be self contained. No Google Fonts, no CDNs, no `@import`, no external images, iframes, or embeds. Use system font stacks, for example:
   - Body: `"Avenir Next", "Segoe UI", Helvetica, Arial, sans-serif`
   - Headings: `"Futura", "Trebuchet MS", "Avenir Next", sans-serif`
   - Serif: `Georgia, "Times New Roman", serif`
4. **Images** must be uploaded by the user through **Manage Files** and referenced by the path the editor gives them. Use clear placeholder paths like `src="images/photo1.jpg"` and tell the user to swap in their uploaded file path.
5. **Scope all CSS.** Wrap everything in one container with a unique id (for example `<div id="nj">`) and prefix every selector with it (`#nj .card { ... }`). Never style `html`, `body`, `*`, or bare tag selectors globally, because that would restyle the rest of the site and the editor.
6. **Set colors explicitly** on the wrapper (background and text) so the site's default styles do not leak in.

## Delivering the code

- **Give HTML and CSS as two separate code blocks** (or two separate files when files are available): one with the markup only, one with the CSS rules only (no `<style>` tags inside the CSS block).
- Tell the user: paste each into its matching field in the Import box. If the Import box has a single field, paste the HTML, then the CSS below it wrapped in `<style>` and `</style>`.
- Keep paste instructions short and in plain language. Assume no coding knowledge.

## Making things interactive without JavaScript (preferred when possible)

Use CSS state tricks. These worked in testing:

- **Toggles and switches:** a hidden `<input type="checkbox">` inside a `<label>`, followed by a styled span. `#nj .sw:checked + .switch { ... }`
- **Theme toggle, tabs, pickers, modals:** hidden checkboxes or radio buttons placed at the **top of the wrapper, before the content div**, with `<label for="id">` elements acting as buttons. Style with sibling selectors: `#themeToggle:checked ~ .wrap { ... }`
- **Modal:** radio group with states closed / open / saved. Overlay shows on `#open:checked ~ .wrap .overlay`. Cancel and backdrop are labels pointing at "closed".
- **Toast or confirmation message:** hidden by default, shown with a slide in and out keyframe animation when a radio becomes checked.
- **Accordions:** native `<details>` and `<summary>`.
- **Sliders** need a script to update anything. Without one, use a row of radio "pill" labels.
- Hide inputs accessibly, not with `display: none`: `position: absolute; opacity: 0; width: 1px; height: 1px; pointer-events: none;`

## Animation guidance

- CSS `@keyframes`, `transition`, `:hover`, `:active`, and `animation-delay` all work.
- Good load animations: fade or slide in with staggered `animation-delay` set in inline `style` attributes.
- Decorative effects (starfields, glows, shimmer) can be done with layered `radial-gradient` backgrounds and keyframes.
- Always include a reduced motion block:
  `@media (prefers-reduced-motion: reduce) { #nj * { animation: none !important; transition: none !important; } }`

## Cautions

- The GrapesJS CSS parser can drop newer selectors. Avoid relying on `:has()` for anything essential; use it only for optional polish.
- **Write colors as hex codes, never `var(--x)`.** On import the editor rewrote every `color:var(--x)` and `background-color:var(--x)` as `#000000`. Also avoid custom properties in inline `style` attributes; use real values (`style="width:40%"`).
- **Don't reuse Bootstrap class names** for your own elements: `container`, `card`, `row`, `col`, `btn`, `nav`, `navbar`, `badge`, `alert`, `modal`, `carousel-item`, `active`, `collapse`, `jumbotron`.
- **Full width** needs `.container.it-is-set{max-width:100%; padding-left:0; padding-right:0;}`.
- Bootstrap adds margins to `p`, `label`, `figure` and headings; reset them inside your wrapper where spacing matters.
- Pasting into the Import window **replaces the whole page**, which also clears out old scripts.
- Keep ids simple and unique (letters only, no spaces). The editor may add its own ids to elements but keeps existing ones.
- `position: fixed` works but should be checked in Preview.
- Include a `@media (max-width: 600px)` block so layouts work on phones.

## Response style for this user

- Never use em dashes or en dashes in responses.
- Be brief: deliver the code, then a few lines of plain paste instructions.
