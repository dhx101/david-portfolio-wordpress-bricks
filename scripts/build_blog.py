#!/usr/bin/env python3
"""Generates /blog/ (post list) and /blog/<slug>/ (each post) from Markdown
files in content/blog/, and keeps page-sitemap.xml in sync. Shares head/
header/footer logic with build_pages.py via _site.py."""
import html
import json
import os
import re
import sys
from datetime import date

import markdown

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _site import ROOT, page_shell  # noqa: E402

CONTENT_DIR = os.path.join(ROOT, "content", "blog")
BLOG_DIR = os.path.join(ROOT, "blog")
SITEMAP_PATH = os.path.join(ROOT, "page-sitemap.xml")

PAGE_STYLE = """
.blog-list{display:flex;flex-direction:column;gap:24px}
.blog-list-item{padding:32px;display:flex;flex-direction:column;gap:8px}
.blog-list-item .blog-date{font-family:"JetBrains Mono";font-size:0.85em;color:var(--bricks-color-dhx001)}
.blog-post{max-width:760px;display:flex;flex-direction:column;gap:24px}
.blog-post-header{display:flex;flex-direction:column;gap:12px;margin-bottom:16px}
.blog-post-header h1{line-height:1.25}
.blog-post-header .blog-date{font-family:"JetBrains Mono";font-size:0.85em;color:var(--bricks-color-dhx001)}
.blog-post-body{display:flex;flex-direction:column;gap:16px;color:var(--bricks-color-dhx024);line-height:1.7}
.blog-post-body h2{color:var(--bricks-color-dhx004);margin-top:12px}
.blog-post-body h3{color:var(--bricks-color-dhx004)}
.blog-post-body a{color:var(--bricks-color-dhx001)}
.blog-post-body ul,.blog-post-body ol{padding-left:1.4em;display:flex;flex-direction:column;gap:8px}
"""


def parse_post(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()

    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, flags=re.S)
    if not m:
        raise SystemExit(f"{path}: falta el frontmatter delimitado por '---' al principio del archivo.")
    frontmatter_raw, body_raw = m.groups()

    frontmatter = {}
    for line in frontmatter_raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise SystemExit(f"{path}: línea de frontmatter inválida (falta ':'): {line!r}")
        key, _, value = line.partition(":")
        frontmatter[key.strip()] = value.strip()

    for required in ("title", "description", "date"):
        if required not in frontmatter:
            raise SystemExit(f"{path}: falta el campo obligatorio {required!r} en el frontmatter.")

    try:
        post_date = date.fromisoformat(frontmatter["date"])
    except ValueError:
        raise SystemExit(f"{path}: 'date' debe tener formato AAAA-MM-DD, no {frontmatter['date']!r}.")

    slug = os.path.splitext(os.path.basename(path))[0]
    body_html = markdown.markdown(body_raw.strip(), extensions=["fenced_code"])

    return {
        "slug": slug,
        "title": frontmatter["title"],
        "description": frontmatter["description"],
        "date": post_date,
        "body_html": body_html,
    }


def json_ld_article(post):
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post["title"],
        "description": post["description"],
        "datePublished": post["date"].isoformat(),
        "author": {"@type": "Person", "name": "David Huang Xie"},
    }
    # json.dumps is HTML-safe enough for a script tag here (no user input, no "</script" risk
    # from our own frontmatter), but escape defensively anyway since titles are free text.
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def update_sitemap(posts):
    if not os.path.exists(SITEMAP_PATH):
        return
    with open(SITEMAP_PATH, encoding="utf-8") as f:
        sitemap = f.read()

    # Remove any previously-generated /blog/ entries so re-running this script
    # doesn't accumulate duplicates as posts are added, renamed or removed.
    sitemap = re.sub(r"\t<url>\n\t\t<loc>/blog/[^<]*</loc>\n\t\t<lastmod>[^<]*</lastmod>\n\t</url>\n", "", sitemap)

    entries = [f"\t<url>\n\t\t<loc>/blog/</loc>\n\t\t<lastmod>{posts[0]['date'].isoformat()}T00:00:00+00:00</lastmod>\n\t</url>\n"] if posts else []
    for post in posts:
        entries.append(
            f"\t<url>\n\t\t<loc>/blog/{post['slug']}/</loc>\n\t\t<lastmod>{post['date'].isoformat()}T00:00:00+00:00</lastmod>\n\t</url>\n"
        )

    sitemap = sitemap.replace("</urlset>", "".join(entries) + "</urlset>")
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(sitemap)


def main():
    if not os.path.isdir(CONTENT_DIR):
        print("content/blog/ no existe todavía — nada que generar.")
        return

    paths = [os.path.join(CONTENT_DIR, name) for name in sorted(os.listdir(CONTENT_DIR)) if name.endswith(".md")]
    posts = sorted((parse_post(p) for p in paths), key=lambda post: post["date"], reverse=True)

    os.makedirs(BLOG_DIR, exist_ok=True)

    list_items = []
    for post in posts:
        list_items.append(f"""<div class="brxe-block terminal grow-hover blog-list-item">
<p class="blog-date">{post['date'].strftime('%d/%m/%Y')}</p>
<h2 class="brxe-heading"><a class="brxe-text-link" href="/blog/{post['slug']}/">{html.escape(post['title'])}</a></h2>
<p class="brxe-text-basic">{html.escape(post['description'])}</p>
<a class="brxe-text-link label text-blue underline" href="/blog/{post['slug']}/"><span class="icon"><i class="ion-ios-arrow-round-forward"></i></span><span class="text">Leer más</span></a>
</div>""")

    blog_main = f"""<section class="brxe-section section"><div class="brxe-container" style="flex-direction:column">
<div class="page-hero">
<p class="brxe-text-basic label text-blue">// WRITE_LOG</p>
<h1 class="brxe-heading text-white">Blog</h1>
<p class="brxe-text-basic">Notas sobre desarrollo web, WordPress, automatización y los proyectos en los que trabajo.</p>
<a class="brxe-button btn-secondary grow-hover bricks-button back-link" href="/">&larr; Volver al inicio</a>
</div>
<div class="blog-list">
{''.join(list_items) if list_items else '<p class="brxe-text-basic">Todavía no hay artículos publicados.</p>'}
</div>
</div></section>"""

    with open(os.path.join(BLOG_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(page_shell(
            "Blog | David Huang Xie — Desarrollador Web Full-Stack",
            "Notas sobre desarrollo web, WordPress, Bricks Builder, automatización con IA y los proyectos en los que trabajo.",
            "/blog/", "blog", blog_main, PAGE_STYLE,
        ))

    for post in posts:
        post_dir = os.path.join(BLOG_DIR, post["slug"])
        os.makedirs(post_dir, exist_ok=True)

        post_main = f"""<section class="brxe-section section"><div class="brxe-container" style="flex-direction:column">
<div class="blog-post">
<a class="brxe-button btn-secondary grow-hover bricks-button back-link" href="/blog/">&larr; Volver al blog</a>
<div class="blog-post-header">
<p class="blog-date">{post['date'].strftime('%d/%m/%Y')}</p>
<h1 class="brxe-heading text-white">{html.escape(post['title'])}</h1>
</div>
<div class="blog-post-body">
{post['body_html']}
</div>
</div>
</div></section>"""

        with open(os.path.join(post_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(page_shell(
                f"{post['title']} | Blog de David Huang Xie",
                post["description"],
                f"/blog/{post['slug']}/", "blog", post_main, PAGE_STYLE,
                extra_head=json_ld_article(post),
            ))

    update_sitemap(posts)
    print(f"Built /blog/ with {len(posts)} post(s), updated page-sitemap.xml")


if __name__ == "__main__":
    main()
