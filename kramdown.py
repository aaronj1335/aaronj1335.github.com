"""Python-Markdown set up to produce the same HTML as kramdown did on GitHub Pages.

Jekyll rendered the posts with kramdown's GFM parser, whose output has a distinctive
shape: two-space indentation, curly quotes, GitHub-style header ids and Rouge's
wrappers around code. This reproduces it so the pages didn't change when the build
moved to Python. Rouge's syntax highlighting isn't reproduced; highlight.js does
that in the browser.
"""

import html
import html.entities
import re
import xml.etree.ElementTree as etree

import markdown
from markdown import util
from markdown.blockprocessors import BlockProcessor
from markdown.postprocessors import RawHtmlPostprocessor
from markdown.preprocessors import NormalizeWhitespace, Preprocessor
from markdown.treeprocessors import Treeprocessor

BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "pre", "blockquote", "hr"}
VOID_TAGS = set("area base br col command embed hr img input keygen link meta param source track wbr".split())

NAME = r"[A-Za-z_][\w.:-]*"
HTML_START_TAG = re.compile(rf"<({NAME})((?:\s+{NAME}(?:\s*=\s*(?:\w+|(\"|').*?\3))?)*)\s*(/)?>", re.S)
HTML_ATTRIBUTE = re.compile(rf"({NAME})(?:\s*=\s*(?:(\w+)|(\"|')(.*?)\3))?", re.S)
ESCAPES = {"<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;"}
ESCAPE_TEXT = re.compile(r"[<>&]")
ESCAPE_ATTRIBUTE = re.compile(rf'&(?:{NAME}|#\d+|#x[0-9A-Fa-f]+);|[<>&"]')

LIST_START = re.compile(r" {0,3}([+*-]|\d+\.)[\t| ].*?\n")
LIST_MARKERS = {"ul": r"[+*-]", "ol": r"\d+\."}
BLANK_LINES = re.compile(r"(?:[ \t]*\n)+")
LAZY_LINE = re.compile(r".*\S.*\n")
FENCE_START = re.compile(r" {0,3}[~`]{3,}")
FENCE = re.compile(r" {0,3}(([~`]){3,})\s*?((\S+?)(?:\?\S*)?)?\s*?\n(.*?)^ {0,3}\1\2*\s*?\n", re.M | re.S)
TRAILING_LINK_DEFINITIONS = re.compile(r"(?:^ {0,3}\[[^\n\]]+\]:.*\n?)+\Z", re.M)

ENTITY = re.compile(r"&([\w:][\w.:-]*);|&#(\d+);|&#x([0-9a-fA-F]+);")
SQ_PUNCT = r"""[!"#$%'()*+,\-./:;<=>?@\[\\\]^_`{|}~]"""
SQ_CLOSE = r"[^ \\\t\r\n\[{(-]"
SQ_RULES = [
    (r"""("|')(?=[_*]{1,2}\S)""", [("left", 1)]),
    (rf"""("|')(?={SQ_PUNCT}(?!\.\.)\B)""", [("right", 1)]),
    (r"""(\s?)"'(?=\w)""", [1, "“", "‘"]),
    (r"""(\s?)'"(?=\w)""", [1, "‘", "“"]),
    (r"""(\s?)'(?=\d\ds)""", [1, "’"]),
    (r"""(\s)('|")(?=\w)""", [1, ("left", 2)]),
    (rf"""({SQ_CLOSE})('|")""", [1, ("right", 2)]),
    (r"""("|')(?=\s|s\b|$)""", [("right", 1)]),
    (r"(.?)'", [1, "‘"]),
    (r'(.?)"', [1, "“"]),
]
SQ_RULES = [(re.compile(pattern, re.A | re.M | re.S), substitutions) for pattern, substitutions in SQ_RULES]
CURLY_QUOTES = {("left", '"'): "“", ("left", "'"): "‘", ("right", '"'): "”", ("right", "'"): "’"}
TYPOGRAPHY = {"---": "—", "--": "–", "...": "…", "\\<<": "<<", "\\>>": ">>",
              "<< ": "«\u00a0", " >>": "\u00a0»", "<<": "«", ">>": "»"}
SPAN = re.compile(
    rf"""(?P<quote>[^\\]?["'])|(?P<entity>{ENTITY.pattern})|{"|".join(re.escape(k) for k in TYPOGRAPHY)}"""
)


def escape(text, pattern=ESCAPE_TEXT):
    return pattern.sub(lambda m: ESCAPES.get(m[0], m[0]), text)


def attributes(pairs):
    return "".join(f' {name}="{escape(value, ESCAPE_ATTRIBUTE)}"' for name, value in pairs)


def start_tag(match):
    pairs = {m[1]: m[2] or m[4] or "" for m in HTML_ATTRIBUTE.finditer(match[2])}
    return f"<{match[1]}{attributes(pairs.items())}{' />' if match[4] or match[1] in VOID_TAGS else '>'}"


def entity(match):
    name, decimal, hexadecimal = match.groups()
    if name:
        return chr(html.entities.name2codepoint[name]) if name in html.entities.name2codepoint else match[0]
    return chr(int(decimal or hexadecimal, 10 if decimal else 16))


def smart_quote(text, pos):
    for rule, substitutions in SQ_RULES:
        if match := rule.match(text, pos):
            return "".join(
                match[s] if isinstance(s, int) else CURLY_QUOTES[s[0], match[s[1]]] if isinstance(s, tuple) else s
                for s in substitutions
            ), match.end()


def typography(text):
    out, pos = [], 0
    while match := SPAN.search(text, pos):
        out.append(text[pos:match.start()])
        if match["quote"]:
            quoted, pos = smart_quote(text, match.start())
            out.append(quoted)
            continue
        out.append(entity(ENTITY.match(match[0])) if match["entity"] else TYPOGRAPHY[match[0]])
        pos = match.end()
    return "".join(out) + text[pos:]


class NormalizeWhitespaceExceptBlankLines(NormalizeWhitespace):
    def run(self, lines):
        source = "\n".join(lines).replace(util.STX, "").replace(util.ETX, "")
        return (source.replace("\r\n", "\n").replace("\r", "\n") + "\n\n").expandtabs(self.md.tab_length).split("\n")


class EmptyBlankLines(Preprocessor):
    def run(self, lines):
        return [line if line.strip() else "" for line in lines]


class ListProcessor(BlockProcessor):
    """kramdown's lists, whose items' content starts in the column after the marker."""

    def test(self, parent, block):
        return LIST_START.match(block + "\n")

    def run(self, parent, blocks):
        text = "\n\n".join(blocks) + "\n"
        tag = "ol" if LIST_START.match(text)[1].endswith(".") else "ul"
        item_start = re.compile(rf"( {{0,3}}{LIST_MARKERS[tag]})([\t| ].*?\n)")
        items, pos, nested, last_blank = [], 0, False, False
        while pos < len(text):
            if match := item_start.match(text, pos):
                content = match[2]
                indent = len(match[1]) + len(content) - len(content.lstrip(" "))
                items.append([content.lstrip()])
                item_start = re.compile(rf"( {{0,{min(indent - 1, 3)}}}{LIST_MARKERS[tag]})([\t| ].*?\n)")
                content_line = re.compile(rf" {{{indent}}}.*\S.*\n")
                nested, last_blank = bool(LIST_START.match(items[-1][0])), False
            elif (match := content_line.match(text, pos)) or (not last_blank and (match := LAZY_LINE.match(text, pos))):
                line = match[0].removeprefix(" " * indent)
                if not nested and line != match[0] and LIST_START.match(line):
                    items[-1].append("")
                    nested = True
                items[-1][-1] += line
                last_blank = False
            elif match := BLANK_LINES.match(text, pos):
                items[-1][-1] += match[0]
                nested = last_blank = True
            else:
                break
            pos = match.end()
        rest = text[pos:-1]
        blocks[:] = rest.split("\n\n") if rest else []

        lst = etree.SubElement(parent, tag)
        # kramdown leaves out the <p> around an item's first paragraph unless a blank line follows
        # it, and for the last item, unless every earlier item had its <p> too.
        tight_before = False
        for i, chunks in enumerate(items):
            li = etree.SubElement(lst, "li")
            first_chunk_size = 0
            for chunk in chunks:
                self.parser.parseBlocks(li, chunk.rstrip("\n").split("\n\n"))
                first_chunk_size = first_chunk_size or len(li)
            children = list(li)
            is_last = i == len(items) - 1
            starts_with_p = bool(children) and children[0].tag == "p" and not util.HTML_PLACEHOLDER_RE.fullmatch(
                children[0].text)
            blank_second = first_chunk_size > 1 or (len(children) == 1 and chunks[-1].endswith("\n\n"))
            tight = (
                starts_with_p
                and (not blank_second or (is_last and len(children) == 1))
                and (not is_last or len(items) == 1 or tight_before)
            )
            tight_before = tight_before or tight or not starts_with_p
            if tight:
                li.remove(children[0])
                li.text = children[0].text + ("\n" if len(children) > 1 else "")


class FencedCodeProcessor(BlockProcessor):
    def test(self, parent, block):
        return FENCE_START.match(block)

    def run(self, parent, blocks):
        text = "\n\n".join(blocks) + "\n"
        if not (match := FENCE.match(text)):
            return False
        code = etree.SubElement(etree.SubElement(parent, "pre"), "code")
        code.text = util.AtomicString(util.code_escape(match[5]))
        if match[3]:
            code.set("class", f"language-{match[4]}")
        rest = text[match.end():-1]
        blocks[:] = rest.split("\n\n") if rest else []


class TypographyProcessor(Treeprocessor):
    def run(self, root):
        for element in root.iter():
            if element.text and not isinstance(element.text, util.AtomicString):
                element.text = typography(element.text)
            if element.tail:
                element.tail = typography(element.tail)


class HeaderIdProcessor(Treeprocessor):
    def run(self, root):
        used = {}
        for element in root.iter():
            if element.tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
                text = html.unescape("".join(element.itertext())).lower()
                slug = re.sub(r"[^\w\- ]", "", text).replace(" ", "-")
                used[slug] = used.get(slug, -1) + 1
                element.set("id", f"{slug}-{used[slug]}" if used[slug] else slug)


class KramdownRawHtml(RawHtmlPostprocessor):
    def stash_to_string(self, text):
        return HTML_START_TAG.sub(start_tag, text).strip("\n")


def inline(element):
    out = [escape(element.text or "")]
    for child in element:
        if child.tag in BLOCK_TAGS:
            break
        if child.tag == "code":
            out.append(f'<code class="language-plaintext highlighter-rouge">{child.text}</code>')
        elif child.tag in VOID_TAGS:
            out.append(f"<{child.tag}{attributes(child.items())} />")
        else:
            out.append(f"<{child.tag}{attributes(child.items())}>{inline(child)}</{child.tag}>")
        out.append(escape(child.tail or ""))
    return "".join(out)


def blocks(parent, indent):
    return "\n".join(block(child, indent) for child in parent if child.tag in BLOCK_TAGS)


def block(element, indent):
    pad, tag = " " * indent, element.tag
    if tag in ("ul", "ol"):
        return f"{pad}<{tag}>\n" + "".join(list_item(li, indent + 2) for li in element) + f"{pad}</{tag}>\n"
    if tag == "blockquote":
        return f"{pad}<{tag}>\n{blocks(element, indent + 2)}{pad}</{tag}>\n"
    if tag == "pre":
        language = element[0].get("class", "language-plaintext")
        code = element[0].text.rstrip("\n")
        return (f'{pad}<div class="{language} highlighter-rouge"><div class="highlight"><pre class="highlight">'
                f"<code>{code}\n</code></pre></div>{pad}</div>\n")
    if tag == "hr":
        return f"{pad}<hr />\n"
    return f"{pad}<{tag}{attributes(element.items())}>{inline(element)}</{tag}>\n"


def list_item(li, indent):
    pad = " " * indent
    if len(li) and li[0].tag in BLOCK_TAGS and not li.text:
        return f"{pad}<li>\n{blocks(li, indent + 2)}{pad}</li>\n"
    content = inline(li) + blocks(li, indent + 2)
    if content.endswith("\n"):
        content += pad
    return f"{pad}<li>{content}</li>\n"


class KramdownExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.output_formats = {**md.output_formats, "kramdown": lambda root: blocks(root, 0)}
        md.stripTopLevelTags = False
        # kramdown keeps whitespace-only lines inside raw HTML, so only blank them once it's stashed.
        md.preprocessors.register(NormalizeWhitespaceExceptBlankLines(md), "normalize_whitespace", 30)
        md.preprocessors.register(EmptyBlankLines(md), "empty_blank_lines", 15)
        for name in ("indent", "olist", "ulist"):
            md.parser.blockprocessors.deregister(name)
        md.parser.blockprocessors.register(FencedCodeProcessor(md.parser), "fenced_code", 75)
        md.parser.blockprocessors.register(ListProcessor(md.parser), "list", 40)
        md.inlinePatterns.deregister("entity")
        md.treeprocessors.deregister("prettify")
        md.treeprocessors.register(TypographyProcessor(md), "typography", 5)
        md.treeprocessors.register(HeaderIdProcessor(md), "header_id", -5)
        md.postprocessors.register(KramdownRawHtml(md), "raw_html", 30)


def convert(text):
    output = markdown.markdown(text, extensions=[KramdownExtension()], output_format="kramdown")
    # A blank line at the end (ignoring link definitions) comes out as a trailing newline.
    trailing_blank = re.search(r"\n\s*\n\Z", TRAILING_LINK_DEFINITIONS.sub("", text))
    return output + ("\n\n" if trailing_blank else "\n")
