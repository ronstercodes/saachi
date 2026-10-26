# Code Sourcing Rules

**These rules apply to every person and every AI assistant (Claude, ChatGPT, Cursor, Copilot or any other) that works on this repository. Read this file before making any change.**

## The rule

1. **The baseline is frozen as written.** The baseline is the code in this repository's first commit:
   - `home.html` and `home.css` as first committed
   - `original-export/nhd_html_css_10-25-2026.md` (the page before the redesign)

2. **Do not generate any new code beyond the baseline.** No newly written HTML, CSS or JavaScript of any size: no new components, effects, layouts, animations or helper scripts, whether invented, "inspired by," or rewritten from memory.

3. **New code may only come directly from a public online GitHub repository of UI/UX code in HTML, CSS or JavaScript,** copied from a specific file in that repo.

4. **Every piece of sourced code must be logged in `SOURCES.md` in the same commit that adds it,** with:
   - repository URL
   - exact file path in the repo
   - author (and component name, if the repo lists one)
   - commit hash or version that was copied
   - license
   - where it went (which file and which section or class names)
   - every change made to it (see rule 6)

5. **License check.** Only copy from repos whose license allows reuse (MIT, Apache 2.0, BSD, ISC, CC0, The Unlicense). Add the license text to `THIRD_PARTY_NOTICES.md` if it isn't there yet. **Don't copy from websites or repos with no license**, even if the effect looks perfect (for example, the tile effect on ayuressence.us was matched with vanilla-tilt.js instead of copying the site's own unlicensed script).

6. **Allowed changes to sourced code, and only these** (each one logged):
   - prefixing selectors with `#fm` so the styles only affect this page
   - renaming classes that clash with Bootstrap (`card`, `container`, `row`, `btn` and so on) or with other components
   - replacing colors with the palette in `DESIGN.md`, written as hex codes
   - setting corner radius to 0 and swapping soft or glowing shadows for the hard print shadow, as `DESIGN.md` requires
   - changing sizes, spacing, durations and delays
   - removing parts (for example a looping animation or a dead link)
   - placeholder text in square brackets, such as `[Heading]` or `[Text]`
   - passing settings to a library (for example `max: 6` for vanilla-tilt) in the existing setup script

7. **The page's own text and images are not code.** The student's words, captions and uploaded pictures are content and are never written by an AI. New text slots use bracketed placeholders only.

## If no GitHub source exists for something

Don't write it. Leave the feature out and note the request at the bottom of `SOURCES.md` under "Requests with no source found."

## Checklist before every commit

- [ ] Every new line of code traces to a row in `SOURCES.md`
- [ ] Each row has repo, file path, author, commit or version, and license
- [ ] License text is in `THIRD_PARTY_NOTICES.md`
- [ ] Every change made to the sourced code is listed in its row
- [ ] Nothing new was written from scratch
- [ ] The page still follows `DESIGN.md` and the NHD rules in `CONTEXT.md`
