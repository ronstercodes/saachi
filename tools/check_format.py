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

# Classes the editor itself puts on the page (from the original export).
ALLOWED_CLASSES = {"auto-nav", "container", "c1363", "carousel", "slide"}
# Class selectors from the original export's CSS.
ALLOWED_CLASS_SELECTORS = {".c1363", ".slide", ".container.c1363", ".auto-nav"}
ALLOWED_TAG_SELECTORS = {"body"}
# Editor-style ids: "i" followed by 3 to 5 lowercase letters or digits.
ID_RE = re.compile(r"^i[a-z0-9]{3,5}$")
# The editor's device presets.
ALLOWED_MEDIA = {"(max-width: 992px)", "(max-width: 768px)", "(max-width: 480px)"}
# Style panel can set transition and transform (Extra section) but not keyframe animations.
BANNED_CSS = ["@keyframes", "animation", "var(", "!important", "@import", "url(http", "::"]
ALLOWED_TAGS = {"div", "p", "h1", "h2", "h3", "h4", "h5", "h6", "strong", "em", "br", "a", "img",
                "span", "ul", "ol", "li", "blockquote", "script", "table", "tr", "td", "th", "tbody", "thead"}

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
    m = re.match(r"^#([a-z0-9]+)(:hover)?$", sel)
    if m:
        if m.group(1) not in ids:
            errors.append(f"home.css: '{sel}' styles an id that isn't in home.html")
    elif sel not in ALLOWED_CLASS_SELECTORS | ALLOWED_TAG_SELECTORS:
        errors.append(f"home.css: selector '{sel}' isn't editor style; use #id or #id:hover")
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
