#!/usr/bin/env python3
"""Generates /proyectos/, /estudios/ and /experiencia/ static pages
from index.html's head/header/footer, reusing the site's design system."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")

with open(INDEX, encoding="utf-8") as f:
    SRC = f.read()

HEAD_START = SRC.index("<head>")
HEAD_END = SRC.index("</head>") + len("</head>")
HEAD = SRC[HEAD_START:HEAD_END]

HEADER_START = SRC.index('<header id="brx-header">')
HEADER_END = SRC.index("</header>") + len("</header>")
HEADER = SRC[HEADER_START:HEADER_END]

FOOTER_START = SRC.index('<footer id="brx-footer">')
FOOTER_END = SRC.index("</footer>") + len("</footer>")
FOOTER = SRC[FOOTER_START:FOOTER_END]


def build_head(title, description, path):
    h = HEAD
    h = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", h, count=1, flags=re.S)
    h = re.sub(
        r'<meta name="description" content=".*?">',
        f'<meta name="description" content="{description}">',
        h, count=1,
    )
    h = re.sub(r'<link rel="canonical" href=".*?">', f'<link rel="canonical" href="{path}">', h, count=1)
    h = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{title}">', h, count=1)
    h = re.sub(
        r'<meta property="og:description" content=".*?">',
        f'<meta property="og:description" content="{description}">',
        h, count=1,
    )
    h = re.sub(r'<meta name="twitter:title" content=".*?">', f'<meta name="twitter:title" content="{title}">', h, count=1)
    h = re.sub(
        r'<meta name="twitter:description" content=".*?">',
        f'<meta name="twitter:description" content="{description}">',
        h, count=1,
    )
    h = h.replace('<meta property="og:url" content="/">', f'<meta property="og:url" content="{path}">', 1)
    return h


NAV_EXTRA = (
    '<a class="brxe-text-link label text-blue underline" href="/proyectos/">Más_Proyectos</a>'
    '<a class="brxe-text-link label text-blue underline" href="/estudios/">Estudios</a>'
    '<a class="brxe-text-link label text-blue underline" href="/experiencia/">Experiencia</a>'
)


def build_header(prefix, active):
    h = HEADER
    # cross-page anchors need "/#..." instead of "#..." so smooth-scroll JS (which
    # only targets same-page "#" links) doesn't try to intercept them
    if prefix:
        h = re.sub(r'href="#(brxe-[a-z]+)"', r'href="/#\1"', h)
    # index.html's header already carries the extra nav links (added directly);
    # only inject them here if they're missing, so re-running this script stays idempotent
    if "Más_Proyectos" in h:
        return h
    h = h.replace(
        '<a id="brxe-hvforz" class="brxe-text-link label text-blue underline" href="%sbrxe-nmkeca" data-brx-anchor="true">Proyectos_Reales</a>'
        % ("/#" if prefix else "#"),
        '<a id="brxe-hvforz" class="brxe-text-link label text-blue underline" href="%sbrxe-nmkeca" data-brx-anchor="true">Proyectos_Reales</a>%s'
        % ("/#" if prefix else "#", NAV_EXTRA),
    )
    return h


FOOTER_SIMPLE = re.sub(
    r'<p id="brxe-dsiurf".*?</p>', "", FOOTER, count=1, flags=re.S
)


def page_shell(title, description, path, active, main_html, extra_style=""):
    head = build_head(title, description, path)
    head = head.replace("</head>", f"<style>{extra_style}</style>\n</head>") if extra_style else head
    header = build_header("/", active)
    body = f"""<!DOCTYPE html>
<html lang="es-ES" prefix="og: https://ogp.me/ns#">
{head}
<body class="page-template-default page wp-theme-bricks brx-body">
{header}
<main id="brx-content">
{main_html}
</main>
{FOOTER_SIMPLE}
<script id="bricksforge-gsap-js" src="/wp-content/plugins/bricksforge/assets/vendor/gsap.min.js"></script>
<script id="bricksforge-scrolltrigger-js" src="/wp-content/plugins/bricksforge/assets/vendor/ScrollTrigger.min.js"></script>
<script id="bricksforge-splittext-js" src="/wp-content/plugins/bricksforge/assets/vendor/SplitText.min.js"></script>
<script id="dhx-animations-js" src="/assets/js/animations.js"></script>
</body></html>"""
    return body


PAGE_STYLE = """
.page-hero{display:flex;flex-direction:column;gap:16px;max-width:760px;margin-bottom:40px}
.page-hero .back-link{display:inline-flex;align-items:center;gap:6px;width:max-content}
.proyectos-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
@media (max-width:1024px){.proyectos-grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:767px){.proyectos-grid{grid-template-columns:1fr}}
.project-card{display:flex;flex-direction:column}
.project-card-image{aspect-ratio:4/3;overflow:hidden;position:relative}
.project-card-image img{width:100%;height:100%;object-fit:cover;display:block}
.project-card-body{padding:24px;display:flex;flex-direction:column;gap:12px;flex-grow:1}
.project-card-stack{display:flex;flex-wrap:wrap;gap:8px}
.project-card-body>a,.project-card-body>p:last-child{margin-top:auto}
.estudios-list,.experiencia-list{display:flex;flex-direction:column;gap:24px}
.study-card,.job-card{display:grid;grid-template-columns:260px 1fr;gap:32px;padding:32px}
@media (max-width:767px){.study-card,.job-card{grid-template-columns:1fr}}
.study-card-image,.job-card-image{aspect-ratio:4/3;overflow:hidden;border-radius:16px;background:var(--bricks-color-dhx017);display:flex;align-items:center;justify-content:center;padding:16px}
.study-card-image img,.job-card-image img{width:100%;height:100%;object-fit:contain;display:block}
.job-card-image{background:#f4f4f2;padding:24px}
.job-card-image.placeholder{background:transparent;background-image:linear-gradient(-45deg,#010101,#131313);border:2px solid var(--bricks-border-color);padding:0}
.study-card-header,.job-card-header{display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;align-items:baseline}
.study-card-body,.job-card-body{display:flex;flex-direction:column;gap:12px}
.study-card-desc,.job-card-desc{display:flex;flex-direction:column;gap:12px}
.job-card-funciones{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
"""

os.makedirs(os.path.join(ROOT, "proyectos"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "estudios"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "experiencia"), exist_ok=True)

# ---------------------------------------------------------------- PROYECTOS
with open(os.path.join(ROOT, "..", "nextjs-portfolio", "public", "jsons", "projects.json")
          if False else "/workspace/nextjs-portfolio/public/jsons/projects.json", encoding="utf-8") as f:
    projects = json.load(f)

cards = []
for p in projects:
    stack_badges = "".join(f'<p class="brxe-text-basic badge-infraestructure">{s}</p>' for s in p.get("stack", []))
    if p.get("link"):
        link_html = (f'<a class="brxe-text-link label text-blue underline" href="{p["link"]}" target="_blank" '
                     f'rel="noopener noreferrer"><span class="icon"><i class="ion-ios-arrow-round-forward"></i></span>'
                     f'<span class="text">Visita la web</span></a>')
    else:
        link_html = '<p class="brxe-text-basic label" style="color:var(--bricks-color-dhx025)">Proyecto interno / sin enlace público</p>'
    cards.append(f"""<div class="brxe-block terminal grow-hover project-card">
<div class="project-card-image background-glow"><img src="/assets/projects/{p['img']}" alt="{p['alt']}" loading="lazy"></div>
<div class="project-card-body">
<h3 class="brxe-heading">{p['name']}</h3>
<div class="project-card-stack">{stack_badges}</div>
<p class="brxe-text-basic">{p['miniDescription']}</p>
{link_html}
</div>
</div>""")

proyectos_main = f"""<section class="brxe-section section"><div class="brxe-container" style="flex-direction:column">
<div class="page-hero">
<p class="brxe-text-basic label text-blue">// ALL_DEPLOYMENTS</p>
<h1 class="brxe-heading text-white">Proyectos</h1>
<p class="brxe-text-basic">Estos son los proyectos web reales en los que he trabajado a lo largo de mi carrera, tanto para clientes como personales: WordPress, Elementor, Woocommerce, React y más. Cada uno incluye el stack utilizado y, cuando está disponible, un enlace para visitarlo.</p>
<a class="brxe-button btn-secondary grow-hover bricks-button back-link" href="/">&larr; Volver al inicio</a>
</div>
<div class="proyectos-grid">
{''.join(cards)}
</div>
</div></section>"""

with open(os.path.join(ROOT, "proyectos", "index.html"), "w", encoding="utf-8") as f:
    f.write(page_shell(
        "Proyectos | David Huang Xie — Desarrollador Web Full-Stack",
        "Proyectos web reales en los que he trabajado: WordPress, Elementor, Woocommerce, React y más. Explora los sitios y aplicaciones que he desarrollado para clientes y proyectos propios.",
        "/proyectos/", "proyectos", proyectos_main, PAGE_STYLE,
    ))

# ----------------------------------------------------------------- ESTUDIOS
with open("/workspace/nextjs-portfolio/public/jsons/studies.json", encoding="utf-8") as f:
    studies = json.load(f)

study_cards = []
for s in studies:
    desc = "".join(f'<p class="brxe-text-basic">{d}</p>' for d in s["description"])
    study_cards.append(f"""<div class="brxe-block terminal grow-hover study-card">
<div class="study-card-image background-glow"><img src="/assets/{s['img']}" alt="{s['degree']}" loading="lazy"></div>
<div class="study-card-body">
<div class="study-card-header">
<h3 class="brxe-heading">{s['degree']}</h3>
<p class="brxe-text-basic badge-primary">{s['time']}</p>
</div>
<p class="brxe-text-basic label text-blue">{s['institution']}</p>
<div class="study-card-desc">{desc}</div>
</div>
</div>""")

estudios_main = f"""<section class="brxe-section section"><div class="brxe-container" style="flex-direction:column">
<div class="page-hero">
<p class="brxe-text-basic label text-blue">// ACADEMIC_LOG</p>
<h1 class="brxe-heading text-white">Estudios</h1>
<p class="brxe-text-basic">Mi trayectoria académica: estudios universitarios, un Erasmus+ en Portugal y los cursos y bootcamps que he realizado a lo largo de mi carrera para especializarme en desarrollo web.</p>
<a class="brxe-button btn-secondary grow-hover bricks-button back-link" href="/">&larr; Volver al inicio</a>
</div>
<div class="estudios-list">
{''.join(study_cards)}
</div>
</div></section>"""

with open(os.path.join(ROOT, "estudios", "index.html"), "w", encoding="utf-8") as f:
    f.write(page_shell(
        "Estudios | David Huang Xie — Desarrollador Web Full-Stack",
        "Trayectoria académica de David Huang Xie: Bootcamp de Desarrollo Web Full-Stack, Diseño UX, Marketing e Investigación de Mercados y Erasmus+ en Portugal.",
        "/estudios/", "estudios", estudios_main, PAGE_STYLE,
    ))

# -------------------------------------------------------------- EXPERIENCIA
with open("/workspace/nextjs-portfolio/public/jsons/workplace.json", encoding="utf-8") as f:
    workplace = json.load(f)

angulotres = {
    "position": "Diseñador y Desarrollador Web",
    "company": "Ángulo Tres",
    "time": "2024 - Actualidad",
    "img": "experiencia/AnguloTres.webp",
    "miniDescription": (
        "Agencia en la que trabajo actualmente. Mi puesto de contrato es Diseñador Web, pero en la práctica cubro "
        "todo el ciclo de vida de los proyectos digitales de la agencia: diseño, desarrollo con WordPress y Bricks "
        "Builder, automatización de procesos internos y de clientes con n8n y agentes de IA, SEO técnico e "
        "infraestructura on-premise. Por confidencialidad con los clientes de la agencia no puedo enlazar los "
        "proyectos concretos en los que trabajo aquí."
    ),
    "funciones": [
        "Desarrollo y maquetación web con WordPress y Bricks Builder",
        "Automatización de procesos con n8n, agentes de IA y MCP",
        "SEO técnico on-page y off-page, Core Web Vitals",
        "Infraestructura on-premise: Docker, servidores locales, LLMs locales",
    ],
    "link": None,
}

jobs = [angulotres] + workplace

job_cards = []
for j in jobs:
    funciones = "".join(f'<p class="brxe-text-basic badge-infraestructure">{fn}</p>' for fn in j.get("funciones", []))
    if j.get("img"):
        img_html = f'<div class="job-card-image"><img src="/assets/{j["img"]}" alt="{j["company"]}" loading="lazy"></div>'
    else:
        img_html = '<div class="job-card-image placeholder"><p class="brxe-text-basic label" style="text-align:center">Trabajo actual<br>bajo NDA</p></div>'
    if j.get("link"):
        link_html = (f'<a class="brxe-text-link label text-blue underline" href="{j["link"]}" target="_blank" '
                     f'rel="noopener noreferrer"><span class="icon"><i class="ion-ios-arrow-round-forward"></i></span>'
                     f'<span class="text">Visita la web</span></a>')
    else:
        link_html = ""
    time_html = f'<p class="brxe-text-basic badge-primary">{j["time"]}</p>' if j.get("time") else ""
    job_cards.append(f"""<div class="brxe-block terminal grow-hover job-card">
{img_html}
<div class="job-card-body">
<div class="job-card-header">
<h3 class="brxe-heading">{j['position']}</h3>
{time_html}
</div>
<p class="brxe-text-basic label text-blue">{j['company']}</p>
<p class="brxe-text-basic">{j['miniDescription']}</p>
<div class="job-card-funciones">{funciones}</div>
{link_html}
</div>
</div>""")

experiencia_main = f"""<section class="brxe-section section"><div class="brxe-container" style="flex-direction:column">
<div class="page-hero">
<p class="brxe-text-basic label text-blue">// WORK_LOG</p>
<h1 class="brxe-heading text-white">Experiencia</h1>
<p class="brxe-text-basic">Mi trayectoria profesional, desde mis prácticas universitarias hasta mi puesto actual en Ángulo Tres, donde cubro desarrollo web, automatización con IA, SEO técnico e infraestructura.</p>
<a class="brxe-button btn-secondary grow-hover bricks-button back-link" href="/">&larr; Volver al inicio</a>
</div>
<div class="experiencia-list">
{''.join(job_cards)}
</div>
</div></section>"""

with open(os.path.join(ROOT, "experiencia", "index.html"), "w", encoding="utf-8") as f:
    f.write(page_shell(
        "Experiencia | David Huang Xie — Desarrollador Web Full-Stack",
        "Trayectoria profesional de David Huang Xie: Ángulo Tres, Almoraima Soluciones y La Buhardilla del Marketing. Desarrollo web, automatización con IA y SEO técnico.",
        "/experiencia/", "experiencia", experiencia_main, PAGE_STYLE,
    ))

print("Built /proyectos/, /estudios/, /experiencia/")
