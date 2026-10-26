# How to put this code into the NHD editor

You don't need to know any code. You copy two files and paste them into two boxes.

## What you need

- `home.html` (everything in it, including the `<script>` parts at the bottom)
- `home.css`

## Steps

1. **Open the editor.** Go to NHD WebCentral, open the site, and pick **home** in the **Page** dropdown at the top.

2. **Open the Import window.** In the toolbar at the top of the editor, click the **Import** button. It looks like a tray with a down arrow:

   ![Import button](docs/images/import-button.png)

   It sits in the right half of the top toolbar, between the trash can and the question mark:

   ![Editor toolbar](docs/images/editor-toolbar.png)

   A window titled **Import** opens with two boxes: **HTML** on the left and **CSS** on the right.

3. **Replace the HTML.** Click inside the **HTML** box, select everything (Ctrl+A on Windows, Cmd+A on Mac), and delete it. Open `home.html`, copy everything, and paste it into the box.

4. **Replace the CSS.** Click inside the **CSS** box, select everything, and delete it. Open `home.css`, copy everything, and paste it into the box.

5. **Save.** Click **Save** at the bottom of the Import window.

6. **Check it with Preview.** Click the **eye icon** in the top toolbar. The slideshow, the click-to-open section, the fade-ins, the counting 13, and the tilt with the cursor light only run in Preview and on the published site, not inside the editor canvas. In the editor, the slideshow shows only its first slide, and clicking selects things instead of clicking them.

## Good to know

- **Replace everything; don't add on.** The yellow warning in the Import window is about this: pasting replaces the whole page.
- **Only one person should edit the page at a time.** If the editor says someone else is "currently editing this page," wait until they're done, or one person's changes can overwrite the other's.
- **Text and pictures:** after importing, click any `[Heading]`, `[Text]`, `[Caption]` and so on in the editor and type over it. For pictures, upload them in **Manage Files**, then swap the `images/photo1.jpg` to `images/photo4.jpg` paths for the paths the editor gives you.
- **If a box turns black after importing,** the CSS probably contains a color written as `var(--something)`. The editor turns those into black. Colors must be plain codes like `#243e50`. See `CONTEXT.md`.
- **If something looks squeezed into the middle of the page,** check that the `.container.it-is-set` rules near the top of `home.css` made it in.
- **The `@source` notes in the code** (like `<!-- @source UV-SHRIMP -->`) record where each piece came from. They don't show on the page. The editor may drop them after import; the copies in this repo keep them.
- **Keep this repo in sync with your text.** Text you type into the editor lives only on the NHD site. If you import `home.html` again later, it brings back the placeholders. Before re-importing, copy your text into `home.html` here first.
- **Don't add new code that wasn't copied from a GitHub UI repo.** Every change has to pass the source screen. See `CODE-SOURCING-RULES.md`.
