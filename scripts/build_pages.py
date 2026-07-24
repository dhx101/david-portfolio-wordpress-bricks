#!/usr/bin/env python3
"""Generates /proyectos/, /estudios/ and /experiencia/ static pages
from index.html's head/header/footer, reusing the site's design system.
Shared extraction/shell logic lives in _site.py."""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _site import ROOT, page_shell  # noqa: E402

# Rules already present in index.html's own <head> (added there for its
# hardcoded homepage preview cards) are NOT repeated here — only what's
# actually specific to these generated pages.
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
"""

os.makedirs(os.path.join(ROOT, "proyectos"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "estudios"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "experiencia"), exist_ok=True)

DATA = os.path.join(ROOT, "assets", "data")


def load_json(name):
    path = os.path.join(DATA, name)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def require(entry, field, index, source):
    if field not in entry:
        raise SystemExit(f"{source} entrada {index} sin campo obligatorio {field!r}: {entry}")
    return entry[field]


def esc(value):
    return html.escape(str(value)) if value is not None else ""


# ---------------------------------------------------------------- PROYECTOS
projects = load_json("projects.json")

cards = []
for i, p in enumerate(projects):
    img = require(p, "img", i, "projects.json")
    alt = require(p, "alt", i, "projects.json")
    name = require(p, "name", i, "projects.json")
    mini_description = require(p, "miniDescription", i, "projects.json")

    stack_badges = "".join(f'<p class="brxe-text-basic badge-infraestructure">{esc(s)}</p>' for s in p.get("stack", []))
    if p.get("link"):
        link_html = (f'<a class="brxe-text-link label text-blue underline" href="{esc(p["link"])}" target="_blank" '
                     f'rel="noopener noreferrer"><span class="icon"><i class="ion-ios-arrow-round-forward"></i></span>'
                     f'<span class="text">Visita la web</span></a>')
    else:
        link_html = '<p class="brxe-text-basic label" style="color:var(--bricks-color-dhx025)">Proyecto interno / sin enlace público</p>'
    cards.append(f"""<div class="brxe-block terminal grow-hover project-card">
<div class="project-card-image background-glow"><img src="/assets/projects/{esc(img)}" alt="{esc(alt)}" loading="lazy"></div>
<div class="project-card-body">
<h2 class="brxe-heading">{esc(name)}</h2>
<div class="project-card-stack">{stack_badges}</div>
<p class="brxe-text-basic">{esc(mini_description)}</p>
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
studies = load_json("studies.json")

study_cards = []
for i, s in enumerate(studies):
    degree = require(s, "degree", i, "studies.json")
    institution = require(s, "institution", i, "studies.json")
    img = require(s, "img", i, "studies.json")
    description = require(s, "description", i, "studies.json")

    desc = "".join(f'<p class="brxe-text-basic">{esc(d)}</p>' for d in description)
    study_cards.append(f"""<div class="brxe-block terminal grow-hover study-card">
<div class="study-card-image background-glow"><img src="/assets/{esc(img)}" alt="{esc(degree)}" loading="lazy"></div>
<div class="study-card-body">
<div class="study-card-header">
<h2 class="brxe-heading">{esc(degree)}</h2>
<p class="brxe-text-basic badge-primary">{esc(s.get('time', ''))}</p>
</div>
<p class="brxe-text-basic label text-blue">{esc(institution)}</p>
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
workplace = load_json("workplace.json")

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
for i, j in enumerate(jobs):
    position = require(j, "position", i, "workplace.json (o entrada fija)")
    company = require(j, "company", i, "workplace.json (o entrada fija)")
    mini_description = require(j, "miniDescription", i, "workplace.json (o entrada fija)")

    funciones = "".join(f'<p class="brxe-text-basic badge-infraestructure">{esc(fn)}</p>' for fn in j.get("funciones", []))
    if j.get("img"):
        img_html = f'<div class="job-card-image"><img src="/assets/{esc(j["img"])}" alt="{esc(company)}" loading="lazy"></div>'
    else:
        img_html = '<div class="job-card-image placeholder"><p class="brxe-text-basic label" style="text-align:center">Trabajo actual<br>bajo NDA</p></div>'
    if j.get("link"):
        link_html = (f'<a class="brxe-text-link label text-blue underline" href="{esc(j["link"])}" target="_blank" '
                     f'rel="noopener noreferrer"><span class="icon"><i class="ion-ios-arrow-round-forward"></i></span>'
                     f'<span class="text">Visita la web</span></a>')
    else:
        link_html = ""
    time_html = f'<p class="brxe-text-basic badge-primary">{esc(j["time"])}</p>' if j.get("time") else ""
    job_cards.append(f"""<div class="brxe-block terminal grow-hover job-card">
{img_html}
<div class="job-card-body">
<div class="job-card-header">
<h2 class="brxe-heading">{esc(position)}</h2>
{time_html}
</div>
<p class="brxe-text-basic label text-blue">{esc(company)}</p>
<p class="brxe-text-basic">{esc(mini_description)}</p>
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
