# Instructions for AI assistants

**Do not write any new site code.** Read `CODE-SOURCING-RULES.md` first and follow it exactly.

Before changing anything in this repository, read these files in order:

1. `CODE-SOURCING-RULES.md`: code may only be copied from a licensed public GitHub UI/UX source (or the student's original page), changed only in the allowed ways, wrapped in `@source` markers, and registered in `sources/registry.json`.
2. `CONTEXT.md`: project background and how the NHD WebCentral editor behaves (hex colors only, Bootstrap 4.3.1 is on every page, everything scoped under `#fm`).
3. `DESIGN.md`: the "1901 Apothecary Broadsheet" style every change must follow.
4. `HOW-TO-PASTE.md`: how the user gets the code into the editor. Explain changes in plain language; the user doesn't write code.

Before every commit, run:

```
python3 tools/check_sources.py --write-log
```

It must print "Source screen passed". Never weaken, bypass or edit the screening tool to make a change pass. If something can't be sourced, leave it out and add it to `unsourced_requests` in `sources/registry.json`.

Never write the page's text content; use bracketed placeholders such as `[Text]`. Never use em dashes or en dashes in anything you write for this user.
