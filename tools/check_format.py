"""Check that home.html and home.css match the NHD WebCentral editor's own code format.

Usage:  python3 tools/check_format.py

Rules are explained in EDITOR-FORMAT.md. Prints "Format check passed" or a list of problems.
"""
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = open(os.path.join(ROOT, "home.html"), encoding="utf-8").read()
CSS = open(os.path.join(ROOT, "home.css"), encoding="utf-8").read()
SCRIPT = open(os.path.join(ROOT, "original-export", "carousel-script.js"), encoding="utf-8").read()

# Everything below comes from docs/editor-capabilities-log.md (read from the editor itself).
# Classes the editor's own blocks and the original page put on elements.
ALLOWED_CLASSES = {"auto-nav", "container", "c1363", "carousel", "slide",
                   "rowx", "col-md-3", "col-md-4", "col-md-6", "col-md-8",
                   "bdg-sect", "heading", "paragraph", "row", "cell"}
# Class rules from the original export and the Flexbox block.
ALLOWED_CLASS_SELECTORS = {".c1363", ".slide", ".container.c1363", ".auto-nav", ".row", ".cell"}
# Properties the style panel can set, plus the ones the blocks and original page start with.
PANEL_PROPS = set("""display position top right bottom left text-align
font-family font-size font-weight letter-spacing color line-height text-decoration text-shadow
width flex-basis height max-width min-height margin margin-top margin-right margin-bottom margin-left
padding padding-top padding-right padding-bottom padding-left
opacity background-color border-radius border-top-left-radius border-top-right-radius
border-bottom-right-radius border-bottom-left-radius border border-width border-style border-color
box-shadow background background-image background-repeat background-position background-attachment background-size
transition transition-property transition-duration transition-timing-function perspective transform
flex-direction justify-content align-items order flex flex-grow flex-shrink align-self vertical-align
min-width""".split())
BLOCK_ONLY_PROPS = {"flex-wrap"}  # only allowed in the Flexbox block's own .row / .cell rules
FONTS = {"arial", "arial black", "brush script mt", "comic sans ms", "courier new", "georgia", "helvetica",
         "impact", "lucida sans unicode", "tahoma", "times new roman", "trebuchet ms", "verdana",
         "serif", "sans-serif", "monospace", "cursive"}
ALLOWED_TAG_SELECTORS = {"body"}
# Editor-style ids: "i" followed by 3 to 5 lowercase letters or digits.
ID_RE = re.compile(r"^i[a-z0-9]{3,5}$")
# The editor's device presets.
ALLOWED_MEDIA = {"(max-width: 992px)", "(max-width: 768px)", "(max-width: 480px)"}
# Style panel can set transition and transform (Extra section) but not keyframe animations.
BANNED_CSS = ["@keyframes", "animation", "var(", "!important", "@import", "url(http", "::", "gradient(", "translate"]
ALLOWED_TAGS = {"div", "section", "p", "h1", "h2", "h3", "h4", "h5", "h6", "strong", "b", "i", "em", "u", "br", "hr",
                "a", "img", "span", "ul", "ol", "li", "blockquote", "script"}

errors = []


def norm(s):
    return re.sub(r"\s+", "", s)


# ------------------------------------------------------------------ HTML ---
if "<!--" in HTML:
    errors.append("home.html: HTML comments are not allowed")

scripts = re.findall(r"<script[^>]*>(.*?)</script>", HTML, re.S)
for s in scripts:
    if norm(s) != norm(SCRIPT):
        errors.append("home.html: the only script allowed is the editor's original carousel script "
                      "(original-export/carousel-script.js), unchanged")
if re.search(r"<script[^>]+src=", HTML):
    errors.append("home.html: external scripts are not allowed")

body = re.sub(r"<script[^>]*>.*?</script>", "", HTML, flags=re.S)
for tag in set(re.findall(r"<([a-zA-Z][a-zA-Z0-9]*)", body)):
    if tag.lower() not in ALLOWED_TAGS:
        errors.append(f"home.html: <{tag}> is not a basic editor element")
if re.search(r"\sstyle=", body):
    errors.append("home.html: inline style attributes are not allowed; put styles in home.css under the element's id")
if re.search(r"\son[a-z]+=", body):
    errors.append("home.html: inline event attributes (onclick and so on) are not allowed")
for attr in set(re.findall(r"\s(data-[\w-]+|aria-[\w-]+|role)=", body)):
    errors.append(f"home.html: attribute '{attr}' is not something the editor adds")

classes = set()
for val in re.findall(r'class="([^"]*)"', body):
    classes |= set(val.split())
for c in sorted(classes - ALLOWED_CLASSES):
    errors.append(f"home.html: class '{c}' is not one of the editor's own classes; style by id instead")

ids = re.findall(r'id="([^"]+)"', body)
for i, n in Counter(ids).items():
    if n > 1:
        errors.append(f"home.html: id '{i}' is used {n} times")
    if not ID_RE.match(i):
        errors.append(f"home.html: id '{i}' doesn't look like an editor id (i + 3 to 5 lowercase letters/digits)")

# ------------------------------------------------------------------- CSS ---
if "/*" in CSS:
    errors.append("home.css: CSS comments are not allowed")
for b in BANNED_CSS:
    if b in CSS:
        errors.append(f"home.css: '{b}' is not allowed")


def rules(text, ctx):
    out = []
    pos = 0
    while True:
        m = re.compile(r"\s*([^{}]+?)\s*\{").match(text, pos)
        if not m:
            break
        sel = m.group(1).strip()
        depth, j = 1, m.end()
        while depth and j < len(text):
            depth += {"{": 1, "}": -1}.get(text[j], 0)
            j += 1
        inner = text[m.end():j - 1]
        if sel.startswith("@media"):
            q = sel[len("@media"):].strip()
            if ctx:
                errors.append("home.css: nested @media is not allowed")
            if q not in ALLOWED_MEDIA:
                errors.append(f"home.css: @media {q} is not one of the editor's device sizes {sorted(ALLOWED_MEDIA)}")
            out += rules(inner, q)
        elif sel.startswith("@"):
            errors.append(f"home.css: {sel} is not allowed")
        else:
            out.append((ctx, sel, inner))
        pos = j
    if text[pos:].strip():
        errors.append(f"home.css: could not read the CSS near: {text[pos:pos + 40].strip()!r}")
    return out


seen = Counter()
for ctx, sel, inner in rules(CSS, None):
    seen[(ctx, sel)] += 1
    if "," in sel:
        errors.append(f"home.css: '{sel}' groups selectors; the editor writes one rule per element")
        continue
    m = re.match(r"^#([a-z0-9]+)(:hover|:active|:nth-of-type\(2n\))?$", sel)
    if m:
        if m.group(1) not in ids:
            errors.append(f"home.css: '{sel}' styles an id that isn't in home.html")
    elif sel not in ALLOWED_CLASS_SELECTORS | ALLOWED_TAG_SELECTORS:
        errors.append(f"home.css: selector '{sel}' isn't editor style; use #id or #id:hover")
    for prop, val in re.findall(r"([a-z-]+)\s*:\s*([^;]+)", inner):
        if prop in BLOCK_ONLY_PROPS and sel in {".row", ".cell"}:
            continue
        if prop not in PANEL_PROPS:
            errors.append(f"home.css: '{sel}' sets '{prop}', which the editor's style panel can't set")
            continue
        if prop == "font-family":
            for f in val.split(","):
                if f.strip().strip("'\"").lower() not in FONTS:
                    errors.append(f"home.css: font '{f.strip()}' isn't in the editor's font list")
        if prop == "transform" and re.sub(r"(rotate[XYZ]?|scale[XYZ]?)\([^)]*\)|\s|none", "", val):
            errors.append(f"home.css: '{sel}' transform '{val}' uses more than rotate and scale")
        elif prop.startswith("border") and prop not in {"border", "border-width", "border-style", "border-color"} and "radius" not in prop:
            errors.append(f"home.css: '{sel}' sets a single-side border; the panel only sets all four sides")
    for name in re.findall(r"rgba?\(|hsla?\(", inner):
        errors.append(f"home.css: '{sel}' uses {name}; write colors as hex codes")
for (ctx, sel), n in seen.items():
    if n > 1:
        errors.append(f"home.css: '{sel}' has {n} rules{' in @media ' + ctx if ctx else ''}; merge them into one")

if errors:
    print(f"FORMAT CHECK FAILED: {len(errors)} problem(s)\n")
    for e in errors:
        print(" - " + e)
    sys.exit(1)
print(f"Format check passed: {len(ids)} elements, {sum(seen.values())} rules, editor format only.")
