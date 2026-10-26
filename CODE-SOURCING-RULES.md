# Code Sourcing Rules

**These rules apply to every person and every AI assistant (Claude, ChatGPT, Cursor, Copilot or any other) that changes this repository. Read this file before making any change.**

## The rule in one sentence

No site code is written from scratch: every line of `home.html` and `home.css` is copied from a registered GitHub source, changed only in the ways listed below, logged, and checked by the screening tool before it is committed.

## 1. Where code may come from

- **Only from a public GitHub repository of UI/UX code** (HTML, CSS or JavaScript, or the documentation examples inside such a repo), copied from one specific file at one specific commit.
- **Only with a reuse license:** MIT, Apache-2.0, BSD-2/3-Clause, ISC, CC0-1.0, Unlicense, CC-BY-3.0 or CC-BY-4.0. Never from a site or repo with no license, even if the effect looks perfect.
- **The student's original page** (`original-export/`, registered as `ORIG`) is the one non-GitHub source. Its text and original markup may be reused.
- **Bootstrap 4.3.1 is already loaded on every NHD page.** Its documented components and classes are the preferred building blocks. Copy markup from its docs examples (`BS-*` sources) and restyle it by copying rules from `bootstrap.css` (`BS-CSS`).

## 2. Allowed changes to copied code (and nothing else)

**CSS**
- Change selectors: prefix with `#fm`, rename classes (for example to avoid Bootstrap clashes), or point a rule at an existing element.
- Change any **value**: colors (as hex codes, per `DESIGN.md`), sizes, spacing, durations, radius, shadows, fonts.
- **Remove** properties or whole rules.
- **Not allowed:** adding a property that the upstream rule doesn't have, or using a pseudo-class, combinator, attribute selector or `@media` feature that the upstream file doesn't use. To get a missing property, find another upstream rule that has it and copy that rule too.

**HTML**
- Use only tags that appear in the upstream file of the block they're in.
- Use only attributes that appear in some registered source; use only classes defined in `home.css`, Bootstrap, or a registered source.
- Repeat, reorder, nest and remove copied elements. Fill text slots with the student's text or bracketed placeholders (`[Heading]`, `[Text]`).

**JavaScript**
- **Libraries are pasted completely unchanged** (byte for byte, checked by hash).
- **Setup lines** may only use names that appear in that library's own documentation (README or guide), such as the documented function names and option names. Values (numbers, strings, selectors) may change.

## 3. How the code is marked

Every copied block is wrapped in markers that name its source ID from `sources/registry.json`:

```html
<!-- @source UV-SHRIMP -->
...copied markup...
<!-- @end UV-SHRIMP -->
```

```css
/* @source BS-CSS */
...copied rules...
/* @end BS-CSS */
```

Blocks may be nested (a Uiverse card inside a Bootstrap column). Code outside any block fails the screen.

## 4. Adding something new, step by step

1. Find the component in a licensed GitHub repo. Note the repo, file path and commit.
2. Save an exact copy of the file to `sources/upstream/<NEW-ID>/`.
3. Add an entry to `sources/registry.json`: id, name, repo, commit, version, path, license, author, kind (`html`, `css`, `html-css`, `js-exact` or `js-example`), used_for, local_copy, sha256, and a `changes` list describing every change you made.
4. Paste the code into `home.html` / `home.css` inside `@source NEW-ID` markers. Make only the allowed changes.
5. Run `python3 tools/check_sources.py --write-log`. This screens everything and regenerates `SOURCES.md`.
6. Fix anything it reports. Commit the code, the registry entry, the upstream copy and `SOURCES.md` together.

If no licensed GitHub source exists for something, don't write it. Add it to `unsourced_requests` in the registry so it shows up under "Requests with no source found" in `SOURCES.md`.

## 5. The screening (automatic)

`tools/check_sources.py` runs:
- **on every commit** through the pre-commit hook (turn it on once per clone: `git config core.hooksPath tools/hooks`), and
- **on every push and pull request** on GitHub (`.github/workflows/source-screen.yml`), where it also re-downloads every upstream file from GitHub at its pinned commit and compares hashes.

It fails if:
- any CSS rule or HTML element is outside an `@source` block
- a CSS rule uses properties that no single rule in its upstream file uses together, or a pseudo-class, combinator, attribute selector or `@media` feature not found upstream
- an HTML tag isn't in the upstream file of its block, or an attribute or class isn't traceable
- a library script differs from its upstream file, or a setup script uses names not in the library's docs
- a color property uses `var()` (the NHD editor turns those black)
- a source's license isn't on the allowlist, or its pinned copy doesn't match its hash or GitHub
- `SOURCES.md` is out of date

**What it can't do:** it proves code is traceable to a real upstream file. It can't read minds. Someone could still pick an upstream file in bad faith. The log makes every choice visible so a teacher or reviewer can check it.

## 6. Not site code

`tools/`, `.github/` and the docs are project infrastructure written by Claude (Anthropic). They are disclosed in `SOURCES.md` and are not part of the website.
