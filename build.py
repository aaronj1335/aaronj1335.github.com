import datetime
import html
import shutil
import string
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).parent
SITE = ROOT / "_site"
SKIP = {"README.md", "build.py", "index.md", "pyproject.toml", "uv.lock"}


def render(name, **values):
    return string.Template((ROOT / "_layouts" / name).read_text()).substitute(values)


def read(path):
    _, front, body = path.read_text().split("---\n", 2)
    return yaml.safe_load(front), markdown.markdown(body, extensions=["fenced_code", "smarty", "toc"])


def write(path, text):
    (SITE / path).parent.mkdir(parents=True, exist_ok=True)
    (SITE / path).write_text(text)


shutil.rmtree(SITE, ignore_errors=True)
shutil.copytree(ROOT, SITE, ignore=lambda _, names: [n for n in names if n[0] in "._" or n in SKIP])

posts = []
for path in sorted((ROOT / "_posts").glob("*.md")):
    post, content = read(path)
    date, slug = datetime.date.fromisoformat(path.name[:10]), path.stem[11:]
    post.update(content=content, date=date, published=f"{date:%d %B, %Y}", slug=slug, url=f"/writings/{slug}/")
    posts.append(post)

for previous, post, following in zip([None, *posts[:-1]], posts, [*posts[1:], None], strict=True):
    page = render(
        "post.html",
        header="" if post.get("custom_header") else render("header.html", **post),
        note=render("cs373.html") if "cs373" in post.get("tags", []) else "",
        content=post["content"],
        previous=f'<a href="{previous["url"]}">&larr; {previous["title"]}</a>' if previous else "",
        next=f'<a class="next" href="{following["url"]}">{following["title"]} &rarr;</a>' if following else "",
        year=post["date"].year,
    )
    write(f"writings/{post['slug']}/index.html", render("default.html", title=post["title"], content=page))

posts.reverse()
index, content = read(ROOT / "index.md")
items = "".join(render("item.html", **p) for p in posts)
page = render("index.html", content=content, posts=items)
write("index.html", render("default.html", title=index["title"], content=page))
entries = "".join(render("entry.xml", **p, escaped=html.escape(p["content"])) for p in posts)
now = datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")
write("atom.xml", render("atom.xml", entries=entries, updated=now))
urls = ["/", "/atom.xml", "/sitemap.txt", *(p["url"] for p in posts)]
write("sitemap.txt", "\n".join(f"http://aaronstacy.com{url}" for url in urls))
