# Instructions for AI assistants

Before changing anything in this repository, read these files in order:

1. `EDITOR-FORMAT.md`: the page code must match the NHD WebCentral editor's own format exactly (editor style ids, one rule per id, no custom classes, comments or animations), so the student can edit every part by hand in the editor.
2. `CONTEXT.md`: project background, the teacher's approvals, and how the NHD editor behaves.
3. `HOW-TO-PASTE.md`: how the user gets the code into the editor. Explain changes in plain language; the user doesn't write code.

Before every commit, run `python3 tools/check_format.py`. It must print "Format check passed". Never weaken the checker to make a change pass.

AI help with the code must be credited in the annotated bibliography (see `CONTEXT.md`); don't remove that note.

Never write the page's text content; use bracketed placeholders such as `[Text]`. Never use em dashes or en dashes in anything you write for this user.

The earlier sourced-only version (Bootstrap and Uiverse components, source registry and checker) is kept in `archive/sourced-version/` for reference only.
