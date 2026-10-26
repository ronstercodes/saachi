#!/usr/bin/env python3
"""Source screening for the NHD site code.

Checks that every piece of code in home.html and home.css traces back to a
registered upstream source (sources/registry.json) and was not written from
scratch. See CODE-SOURCING-RULES.md for the rules this enforces.

Usage:
  python3 tools/check_sources.py                 run the screen
  python3 tools/check_sources.py --write-log     regenerate SOURCES.md
  python3 tools/check_sources.py --check-log     fail if SOURCES.md is out of date
  python3 tools/check_sources.py --verify-online also re-download every upstream
                                                 file from GitHub at its pinned
                                                 commit and compare hashes

Requires: pip install tinycss2

Note: this tool is project infrastructure, not site code. It was written by
Claude (Anthropic) and is disclosed in SOURCES.md.
"""
import hashlib
import json
import os
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from html.parser import HTMLParser

import tinycss2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(ROOT, "sources", "registry.json")
HTML_FILE = os.path.join(ROOT, "home.html")
CSS_FILE = os.path.join(ROOT, "home.css")
LOG_FILE = os.path.join(ROOT, "SOURCES.md")

MARK_RE = re.compile(r"^\s*@(source|end)\s+([A-Z0-9-]+)\s*$")
GLOBAL_ATTRS = {"id", "class"}
JS_WORDS = set(
    "var let const new function return if else for while true false null undefined "
    "this typeof document window".split()
)
COLOR_PROPS = {"color", "background-color", "border-color", "outline-color", "fill", "stroke"}

# Small AI-written additions, allowed by the teacher on 2026-10-25 if credited.
# They must stay small enough to type by hand: no scripts, few declarations per rule.
AI_ID = "AI"
AI_LIMITS = {"css rules": 25, "html elements": 15, "scripts": 0}
AI_MAX_DECLS = 6


# ---------------------------------------------------------------- upstream ---

def unescape_md(text):
    return re.sub(r"\\([^\w\s])", r"\1", text)


def split_upstream(entry):
    """Return (html_text, css_text, raw_text) for a registered source."""
    path = os.path.join(ROOT, entry["local_copy"])
    raw = open(path, encoding="utf-8", errors="replace").read()
    ext = os.path.splitext(path)[1].lower()
    if ext == ".css":
        return "", raw, raw
    if ext == ".js":
        return "", "", raw
    text = unescape_md(raw) if ext == ".md" else raw
    if entry["id"] == "ORIG" and "**CSS**" in text:
        html_part, css_part = text.split("**CSS**", 1)
        return html_part, css_part, raw
    styles = re.findall(r"<style[^>]*>(.*?)</style>", text, re.S)
    fences = re.findall(r"```(?:css|scss)\s*\n(.*?)```", text, re.S)
    html_part = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.S)
    return html_part, "\n".join(styles + fences), raw


def html_vocab(html_text):
    tags = {t.lower() for t in re.findall(r"<([a-zA-Z][\w-]*)", html_text)}
    attrs, classes = set(), set()
    for tag in re.findall(r"<[a-zA-Z][^<>]*>", html_text):
        for name in re.findall(r"\s([a-zA-Z_:][\w:.-]*)(?=\s*=|\s|/?>)", tag):
            attrs.add(name.lower())
        for val in re.findall(r'class\s*=\s*"([^"]*)"', tag):
            classes.update(val.split())
    return tags, attrs, classes


def selector_features(sel):
    s = re.sub(r'"[^"]*"|\'[^\']*\'', "", sel)
    pseudos = set(re.findall(r"::?[a-zA-Z-]+", s))
    combs = set(c for c in re.findall(r"[>+~]", re.sub(r"\[[^\]]*\]", "", s)))
    attr_sel = set(a.lower() for a in re.findall(r"\[\s*([a-zA-Z_:][\w:.-]*)", s))
    return pseudos, combs, attr_sel


def media_features(prelude):
    return set(re.findall(r"\(\s*([a-z-]+)", prelude))


def decl_names(content):
    names = []
    for d in tinycss2.parse_declaration_list(content, skip_whitespace=True, skip_comments=True):
        if d.type == "declaration":
            names.append(d.lower_name)
    return names


def decls(content):
    return [d for d in tinycss2.parse_declaration_list(content, skip_whitespace=True, skip_comments=True)
            if d.type == "declaration"]


class CssVocab:
    def __init__(self):
        self.rules = []          # list of frozenset(prop names)
        self.keyframes = []      # list of frozenset(prop names)
        self.pseudos, self.combs, self.attr_sel = set(), set(), set()
        self.media = set()
        self.classes = set()

    def feed(self, css_text):
        self._walk(tinycss2.parse_stylesheet(css_text, skip_comments=True, skip_whitespace=True))

    def _walk(self, nodes, in_keyframes=False):
        for n in nodes:
            if n.type == "qualified-rule":
                props = frozenset(decl_names(n.content))
                sel = tinycss2.serialize(n.prelude)
                if in_keyframes:
                    self.keyframes.append(props)
                    continue
                self.rules.append(props)
                p, c, a = selector_features(sel)
                self.pseudos |= p
                self.combs |= c
                self.attr_sel |= a
                self.classes |= set(re.findall(r"\.([a-zA-Z_][\w-]*)", sel))
            elif n.type == "at-rule" and n.content is not None:
                kw = n.lower_at_keyword
                if kw == "media":
                    self.media |= media_features(tinycss2.serialize(n.prelude))
                    self._walk(tinycss2.parse_rule_list(n.content, skip_comments=True, skip_whitespace=True))
                elif kw.endswith("keyframes"):
                    self._walk(tinycss2.parse_rule_list(n.content, skip_comments=True, skip_whitespace=True), True)
                elif kw == "supports":
                    self._walk(tinycss2.parse_rule_list(n.content, skip_comments=True, skip_whitespace=True))


class Upstream:
    def __init__(self, entry):
        self.entry = entry
        html_text, css_text, raw = split_upstream(entry)
        self.raw = raw
        self.tags, self.attrs, self.classes = html_vocab(html_text)
        if entry["kind"].startswith("js"):
            # a library or usage example is embedded with a <script> tag
            self.tags.add("script")
            # class names used in selector strings, e.g. querySelectorAll(".js-tilt")
            self.classes |= set(re.findall(r"[\"']\.([A-Za-z_][\w-]*)[\"']", raw))
        self.css = CssVocab()
        if css_text.strip():
            self.css.feed(css_text)
        # attributes styled by the source's CSS, e.g. [data-scroll]
        self.attrs |= self.css.attr_sel
        self.words = set(re.findall(r"[A-Za-z_$][\w$]*", raw))


# ------------------------------------------------------------------ checks ---

class Report:
    def __init__(self):
        self.errors = []
        self.usage = defaultdict(Counter)   # id -> Counter(kind)

    def err(self, where, msg):
        self.errors.append(f"{where}: {msg}")


def check_registry(reg, rep, online=False):
    allow = set(reg["license_allowlist"])
    ups = {}
    for e in reg["sources"]:
        for k in ("id", "repo", "commit", "path", "license", "author", "kind", "local_copy", "sha256"):
            if not e.get(k):
                rep.err("registry", f"{e.get('id')} is missing '{k}'")
        if e["license"] not in allow:
            rep.err("registry", f"{e['id']} license '{e['license']}' is not on the allowlist")
        path = os.path.join(ROOT, e["local_copy"])
        if not os.path.exists(path):
            rep.err("registry", f"{e['id']} local copy missing: {e['local_copy']}")
            continue
        digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if digest != e["sha256"]:
            rep.err("registry", f"{e['id']} local copy was modified (hash mismatch)")
        if online:
            url = f"https://raw.githubusercontent.com/{e['repo']}/{e['commit']}/{e['path']}"
            try:
                data = urllib.request.urlopen(url, timeout=30).read()
                if hashlib.sha256(data).hexdigest() != e["sha256"]:
                    rep.err("registry", f"{e['id']} does not match GitHub at {e['commit'][:10]} ({url})")
            except Exception as ex:  # noqa: BLE001
                rep.err("registry", f"{e['id']} could not be verified online: {ex}")
        ups[e["id"]] = Upstream(e)
    return ups


class PageParser(HTMLParser):
    def __init__(self, ups, rep, global_attrs, class_pool):
        super().__init__(convert_charrefs=True)
        self.ups, self.rep = ups, rep
        self.global_attrs, self.class_pool = global_attrs, class_pool
        self.stack = []
        self.script = None

    def where(self):
        return f"home.html line {self.getpos()[0]}"

    def handle_comment(self, data):
        m = MARK_RE.match(data)
        if not m:
            return
        kind, sid = m.groups()
        if kind == "source":
            if sid not in self.ups and sid != AI_ID:
                self.rep.err(self.where(), f"unknown source id {sid}")
            self.stack.append(sid)
        else:
            if not self.stack or self.stack[-1] != sid:
                self.rep.err(self.where(), f"@end {sid} does not match open block {self.stack[-1] if self.stack else 'none'}")
            else:
                self.stack.pop()

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.script = {"line": self.getpos()[0], "text": "", "src": self.stack[-1] if self.stack else None}
        if not self.stack:
            self.rep.err(self.where(), f"<{tag}> is not inside any @source block")
            return
        if self.stack[-1] == AI_ID:
            self.rep.usage[AI_ID]["html elements"] += 1
            for name, val in attrs:
                if name == "class" and val:
                    for c in val.split():
                        if c not in self.class_pool:
                            self.rep.err(self.where(), f"class '{c}' is not defined in home.css, Bootstrap, or any source")
            return
        open_ids = [s for s in self.stack if s in self.ups]
        if not open_ids:
            return
        sid = open_ids[-1]
        self.rep.usage[sid]["html elements"] += 1
        if not any(tag in self.ups[s].tags for s in open_ids):
            self.rep.err(self.where(), f"<{tag}> does not appear in the upstream of {', '.join(open_ids)}")
        for name, val in attrs:
            if name not in self.global_attrs:
                self.rep.err(self.where(), f"attribute '{name}' on <{tag}> is not used by any registered source")
            if name == "class" and val:
                for c in val.split():
                    if c not in self.class_pool:
                        self.rep.err(self.where(), f"class '{c}' is not defined in home.css, Bootstrap, or any source")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        if self.script is not None:
            self.script["text"] += data

    def handle_endtag(self, tag):
        if tag == "script" and self.script is not None:
            check_script(self.script, self.ups, self.rep)
            self.script = None


def strip_js_strings(js):
    js = re.sub(r"/\*.*?\*/", " ", js, flags=re.S)
    js = re.sub(r"//[^\n]*", " ", js)
    return re.sub(r"\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`", " ", js)


def check_script(script, ups, rep):
    where = f"home.html line {script['line']}"
    sid = script["src"]
    if sid == AI_ID:
        rep.usage[AI_ID]["scripts"] += 1
        return
    if sid not in ups:
        rep.err(where, "<script> is not inside a registered @source block")
        return
    up, kind = ups[sid], ups[sid].entry["kind"]
    rep.usage[sid]["scripts"] += 1
    if kind == "js-exact":
        if script["text"].strip() != up.raw.strip():
            rep.err(where, f"script differs from the upstream file of {sid}; libraries must be pasted unchanged")
    elif kind == "js-example":
        idents = set(re.findall(r"[A-Za-z_$][\w$]*", strip_js_strings(script["text"])))
        extra = sorted(i for i in idents if i not in up.words and i not in JS_WORDS)
        if extra:
            rep.err(where, f"script uses names not found in {sid}'s documentation: {', '.join(extra)}")
    else:
        rep.err(where, f"source {sid} is not a JavaScript source (kind {kind})")


def check_css(ups, rep):
    text = open(CSS_FILE, encoding="utf-8").read()
    nodes = tinycss2.parse_stylesheet(text, skip_comments=False, skip_whitespace=True)
    stack = []

    def line(n):
        return f"home.css line {n.source_line}"

    def check_rule(n, sid, in_media=None):
        up = ups[sid].css
        sel = tinycss2.serialize(n.prelude).strip()
        props = decl_names(n.content)
        rep.usage[sid]["css rules"] += 1
        if not up.rules and not up.keyframes:
            rep.err(line(n), f"{sid} has no CSS upstream, so it cannot be the source of '{sel}'")
            return
        pset = set(props)
        if not any(pset <= r for r in up.rules):
            best = max(up.rules, key=lambda r: len(pset & r), default=frozenset())
            rep.err(line(n), f"'{sel}' uses properties not found together in any {sid} rule: "
                             f"{', '.join(sorted(pset - best))}")
        p, c, a = selector_features(sel)
        for label, ours, theirs in (("pseudo-classes", p, up.pseudos), ("combinators", c, up.combs),
                                    ("attribute selectors", a, up.attr_sel)):
            if ours - theirs:
                rep.err(line(n), f"'{sel}' uses {label} not found in {sid}: {', '.join(sorted(ours - theirs))}")
        for d in decls(n.content):
            if d.lower_name in COLOR_PROPS and "var(" in tinycss2.serialize(d.value):
                rep.err(line(n), f"'{sel}' uses var() in {d.lower_name}; the NHD editor turns this black")

    def check_ai_rule(n):
        sel = tinycss2.serialize(n.prelude).strip()
        rep.usage[AI_ID]["css rules"] += 1
        ds = decls(n.content)
        if len(ds) > AI_MAX_DECLS:
            rep.err(line(n), f"AI rule '{sel}' has {len(ds)} declarations; keep AI rules to {AI_MAX_DECLS} or fewer")
        for d in ds:
            if d.lower_name in COLOR_PROPS and "var(" in tinycss2.serialize(d.value):
                rep.err(line(n), f"'{sel}' uses var() in {d.lower_name}; the NHD editor turns this black")

    for n in nodes:
        if n.type == "comment":
            m = MARK_RE.match(n.value)
            if not m:
                continue
            kind, sid = m.groups()
            if kind == "source":
                if sid not in ups and sid != AI_ID:
                    rep.err(line(n), f"unknown source id {sid}")
                stack.append(sid)
            elif not stack or stack[-1] != sid:
                rep.err(line(n), f"@end {sid} does not match open block")
            else:
                stack.pop()
            continue
        if n.type == "error":
            rep.err(line(n), f"CSS parse error: {n.message}")
            continue
        if stack and stack[-1] == AI_ID:
            if n.type == "qualified-rule":
                check_ai_rule(n)
            elif n.type == "at-rule" and n.lower_at_keyword == "media":
                for r in tinycss2.parse_rule_list(n.content, skip_comments=True, skip_whitespace=True):
                    if r.type == "qualified-rule":
                        check_ai_rule(r)
            else:
                rep.err(line(n), "only plain rules and @media are allowed in AI blocks")
            continue
        if not stack or stack[-1] not in ups:
            rep.err(line(n), "CSS is not inside a registered @source block")
            continue
        sid = stack[-1]
        if n.type == "qualified-rule":
            check_rule(n, sid)
        elif n.type == "at-rule":
            kw = n.lower_at_keyword
            if kw == "media":
                feats = media_features(tinycss2.serialize(n.prelude))
                if feats - ups[sid].css.media:
                    rep.err(line(n), f"@media features not found in {sid}: {', '.join(sorted(feats - ups[sid].css.media))}")
                for r in tinycss2.parse_rule_list(n.content, skip_comments=True, skip_whitespace=True):
                    if r.type == "qualified-rule":
                        check_rule(r, sid)
            elif kw.endswith("keyframes"):
                for r in tinycss2.parse_rule_list(n.content, skip_comments=True, skip_whitespace=True):
                    if r.type == "qualified-rule":
                        pset = set(decl_names(r.content))
                        if not any(pset <= k for k in ups[sid].css.keyframes):
                            rep.err(line(r), f"keyframe step uses properties not found in {sid}'s keyframes")
                rep.usage[sid]["keyframes"] += 1
            else:
                rep.err(line(n), f"@{kw} is not allowed")
    if stack:
        rep.err("home.css", f"unclosed @source block(s): {', '.join(stack)}")


def css_classes_defined():
    text = open(CSS_FILE, encoding="utf-8").read()
    v = CssVocab()
    v.feed(text)
    return v.classes


# -------------------------------------------------------------------- log ---

def render_log(reg, rep):
    out = ["# Code Sources Log", "",
           "**Generated by `tools/check_sources.py --write-log` from `sources/registry.json`. Don't edit by hand.**", "",
           "Every line of site code in `home.html` and `home.css` sits inside an `@source` block that names one of the "
           "sources below. The screening tool checks that each block really matches its upstream file "
           "(see `CODE-SOURCING-RULES.md`). Exact copies of every upstream file are kept in `sources/upstream/`.", "",
           "## Summary", "",
           "| ID | Source | Repo | Version / commit | License | Used for | Blocks used |",
           "|---|---|---|---|---|---|---|"]
    for e in reg["sources"]:
        use = rep.usage.get(e["id"], Counter())
        used = ", ".join(f"{v} {k}" for k, v in sorted(use.items())) or "not used"
        ver = (e.get("version") + ", " if e.get("version") else "") + f"`{e['commit'][:10]}`"
        out.append(f"| {e['id']} | {e['name']} | [{e['repo']}](https://github.com/{e['repo']}) | {ver} | "
                   f"{e['license']} | {e['used_for']} | {used} |")
    ai = rep.usage.get(AI_ID, Counter())
    out.append(f"| {AI_ID} | Small additions written with AI help (Claude, Anthropic), approved by the teacher 2026-10-25 | "
               f"n/a | n/a | credit required | Glue code too small or specific to source from GitHub | "
               f"{', '.join(f'{v} {k}' for k, v in sorted(ai.items())) or 'not used'} |")
    out += ["", "## Details", ""]
    for e in reg["sources"]:
        url = f"https://github.com/{e['repo']}/blob/{e['commit']}/{e['path']}"
        out += [f"### {e['id']}: {e['name']}", "",
                f"- File: [{e['path']}]({url})",
                f"- Author: {e['author']}",
                f"- License: {e['license']}",
                f"- Commit: `{e['commit']}`" + (f" (version {e['version']})" if e.get("version") else ""),
                f"- SHA-256 of copied file: `{e['sha256']}`",
                f"- Local copy: `{e['local_copy']}`",
                f"- Kind: {e['kind']}",
                f"- Used for: {e['used_for']}"]
        if e.get("changes"):
            out.append("- Changes made:")
            out += [f"  - {c}" for c in e["changes"]]
        out.append("")
    out += [f"### {AI_ID}: AI-assisted additions", "",
            "- Written with Claude (Anthropic). Credit it in the annotated bibliography (see `CONTEXT.md`).",
            f"- Limits enforced by the checker: at most {AI_LIMITS['css rules']} CSS rules, "
            f"{AI_LIMITS['html elements']} HTML elements, {AI_LIMITS['scripts']} scripts, "
            f"and {AI_MAX_DECLS} declarations per rule, so every AI line could be typed by hand.",
            "- Marked in the code with `@source AI` ... `@end AI`.", ""]
    out += ["## Not site code", ""]
    out += [f"- {x}" for x in reg.get("infrastructure", [])]
    out += ["", "## Requests with no source found", ""]
    out += [f"- {x}" for x in reg.get("unsourced_requests", [])] or ["- (none)"]
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------- main ---

def main(argv):
    reg = json.load(open(REGISTRY, encoding="utf-8"))
    rep = Report()
    ups = check_registry(reg, rep, online="--verify-online" in argv)

    global_attrs = set(GLOBAL_ATTRS)
    class_pool = css_classes_defined()
    for u in ups.values():
        global_attrs |= u.attrs
        class_pool |= u.classes | u.css.classes

    check_css(ups, rep)
    p = PageParser(ups, rep, global_attrs, class_pool)
    p.feed(open(HTML_FILE, encoding="utf-8").read())
    p.close()
    if p.stack:
        rep.err("home.html", f"unclosed @source block(s): {', '.join(p.stack)}")

    for k, limit in AI_LIMITS.items():
        used = rep.usage.get(AI_ID, Counter())[k]
        if used > limit:
            rep.err("AI blocks", f"{used} {k} written with AI; the limit is {limit}")

    log = render_log(reg, rep)
    if "--write-log" in argv:
        open(LOG_FILE, "w", encoding="utf-8").write(log)
        print("SOURCES.md written.")
    if "--check-log" in argv:
        current = open(LOG_FILE, encoding="utf-8").read() if os.path.exists(LOG_FILE) else ""
        if current != log:
            rep.err("SOURCES.md", "out of date; run: python3 tools/check_sources.py --write-log")

    if rep.errors:
        print(f"SOURCE SCREEN FAILED: {len(rep.errors)} problem(s)\n")
        for e in rep.errors:
            print(" - " + e)
        return 1
    total = sum(sum(c.values()) for c in rep.usage.values())
    print(f"Source screen passed: {total} code blocks checked against {len(ups)} registered sources.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
