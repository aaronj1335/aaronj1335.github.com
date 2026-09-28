"""Builds the site into _site/."""

import datetime
import os
import re
import shutil
from pathlib import Path

import yaml

import kramdown

ROOT = Path(__file__).parent
DESTINATION = ROOT / "_site"
FRONT_MATTER = re.compile(r"\A(---\s*\n.*?\n?)^((---|\.\.\.)\s*$\n?)", re.M | re.S)
POST_FILENAME = re.compile(r"(\d{4})-(\d\d)-(\d\d)-([\w-]+)\.md")
NAME = re.compile(r"\w+")

# Just enough Liquid for the templates in _layouts and _includes, atom.xml, etc.
LIQUID = re.compile(r"({{.*?}}|{%.*?%})", re.S)
VARIABLE = r"\w+(?:\.\w+)*"
OUTPUT = re.compile(rf'\s*({VARIABLE})\s*((?:\|\s*\w+\s*(?::\s*"[^"]*"\s*)?)*)')
FILTER = re.compile(r'\|\s*(\w+)\s*(?::\s*"([^"]*)")?')
CONDITION = re.compile(rf"({VARIABLE})(?: contains '([^']*)')?")
LOOP = re.compile(rf"(\w+) in ({VARIABLE})")
XML_ESCAPES = str.maketrans({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&apos;"})
FILTERS = {
    "date": lambda value, fmt: value.strftime(fmt),
    "date_to_xmlschema": lambda value: value.isoformat(timespec="seconds"),
    "xml_escape": lambda value: value.translate(XML_ESCAPES),
}


def has_front_matter(path):
    with path.open("rb") as file:
        return file.readline().rstrip() == b"---"


def read_text(path):
    if not path.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError(f"{path} links outside {ROOT}")
    return path.read_text(encoding="utf-8")


def read(path):
    text = read_text(path)
    if match := FRONT_MATTER.match(text):
        return yaml.safe_load(match[1]) or {}, text[match.end():]
    return {}, text


def expect(pattern, text):
    if match := pattern.fullmatch(text):
        return match
    raise ValueError(f"unsupported: {text!r}")


def parse(tokens, until=()):
    nodes = []
    for token in tokens:
        if token.startswith("{%"):
            tag, _, argument = token[2:-2].strip().partition(" ")
            if tag in until:
                return nodes, tag
            if tag in ("if", "unless", "for"):
                argument = expect(LOOP if tag == "for" else CONDITION, argument.strip()).groups()
                body, end = parse(tokens, ("else", f"end{tag}"))
                orelse = parse(tokens, (f"end{tag}",))[0] if end == "else" else []
                nodes.append((tag, argument, body, orelse))
            elif tag == "include":
                nodes.append((tag, expect(NAME, argument.strip())[0]))
            else:
                raise ValueError(f"unsupported Liquid: {token!r}")
        elif token.startswith("{{"):
            variable, filters = expect(OUTPUT, token[2:-2]).groups()
            nodes.append(("output", variable, FILTER.findall(filters)))
        elif token:
            nodes.append(token)
    if until:
        raise ValueError(f"missing {{% {until[-1]} %}}")
    return nodes, None


def lookup(variable, context):
    value = context
    for key in variable.split("."):
        value = value.get(key) if isinstance(value, dict) else None
    return value


def render(nodes, context):
    out = []
    for node in nodes:
        if isinstance(node, str):
            out.append(node)
        elif node[0] == "output":
            value = lookup(node[1], context)
            for name, argument in node[2]:
                value = FILTERS[name](value, argument) if argument else FILTERS[name](value)
            out.append("" if value is None else str(value))
        elif node[0] == "include":
            out.append(liquid(read(ROOT / "_includes" / node[1])[1], context))
        elif node[0] == "for":
            name, variable = node[1]
            out += [render(node[2], {**context, name: item}) for item in lookup(variable, context) or ()]
        else:
            tag, (variable, item), body, orelse = node
            value = lookup(variable, context)
            if item is not None:
                value = item in (value or ())
            test = value is not None and value is not False
            out.append(render(body if test == (tag == "if") else orelse, context))
    return "".join(out)


def liquid(template, context):
    return render(parse(iter(LIQUID.split(template)))[0], context)


def layout(content, page, site):
    name = page.get("layout")
    while name:
        data, template = read(ROOT / "_layouts" / f"{expect(NAME, name)[0]}.html")
        content = liquid(template, {"site": site, "page": page, "content": content})
        name = data.get("layout")
    return content


def skip(path, exclude):
    return path.name[0] in "._#~" or path.name.endswith("~") or path.as_posix() in exclude or path.is_symlink()


def source_files(exclude):
    for directory, subdirectories, files in os.walk(ROOT):
        directory = Path(directory)
        subdirectories[:] = sorted(d for d in subdirectories if not skip(directory / d, exclude))
        yield from (directory / f for f in sorted(files) if not skip(directory / f, exclude))


def write(path, text):
    path = DESTINATION / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    site = yaml.safe_load(read_text(ROOT / "_config.yml"))
    site["time"] = datetime.datetime.now(datetime.UTC)
    exclude = {(ROOT / path).as_posix() for path in site.get("exclude", [])}

    posts = []
    for path in sorted((ROOT / "_posts").glob("[!.]*.md")):
        year, month, day, slug = expect(POST_FILENAME, path.name).groups()
        data, body = read(path)
        date = datetime.datetime(int(year), int(month), int(day), tzinfo=datetime.UTC)
        posts.append({**data, "date": date, "url": f"/writings/{slug}/", "id": f"/writings/{slug}", "body": body})
    for previous, post, following in zip([None, *posts[:-1]], posts, [*posts[1:], None], strict=True):
        post["previous"], post["next"] = previous, following
    site["posts"] = posts[::-1]

    pages, static = [], []
    for path in source_files(exclude):
        if not has_front_matter(path):
            static.append(path.relative_to(ROOT))
            continue
        data, body = read(path)
        output = path.relative_to(ROOT).with_suffix(".html" if path.suffix == ".md" else path.suffix)
        url = "/" + output.as_posix()
        if output.name == "index.html":
            url = url.removesuffix("index.html")
        pages.append({**data, "url": url, "name": path.name, "output": output, "body": body})
    site["pages"] = sorted(pages, key=lambda page: page["name"])

    if DESTINATION.exists():
        shutil.rmtree(DESTINATION)
    for post in posts:
        post["content"] = kramdown.convert(liquid(post["body"], {"site": site, "page": post}))
        write(Path(post["url"].strip("/"), "index.html"), layout(post["content"], post, site))
    for page in pages:
        content = liquid(page["body"], {"site": site, "page": page})
        if page["name"].endswith(".md"):
            content = kramdown.convert(content)
        write(page["output"], layout(content, page, site))
    for path in static:
        (DESTINATION / path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, DESTINATION / path)


if __name__ == "__main__":
    main()
