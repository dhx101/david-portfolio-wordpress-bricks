# Scripts de generación de páginas

Este sitio es un export estático de WordPress + Bricks Builder (desplegado tal cual, sin WordPress corriendo detrás). `index.html` es la home, editada a mano/exportada desde Bricks. `/proyectos/`, `/estudios/`, `/experiencia/` y `/blog/` son **generadas** por estos scripts a partir de datos, reutilizando el `<head>`/header/footer de `index.html`.

## Setup

```bash
pip install -r scripts/requirements.txt
```

## Añadir contenido

- **Proyecto** → añade una entrada a `assets/data/projects.json` (campos: `name`, `img`, `alt`, `stack`, `miniDescription`, `link`) y una imagen en `assets/projects/`.
- **Estudio** → `assets/data/studies.json`.
- **Trabajo** → `assets/data/workplace.json` (el puesto actual en Ángulo Tres está hardcodeado en `build_pages.py`, no en el JSON, porque no tiene enlace público).
- **Post del blog** → un archivo nuevo en `content/blog/tu-slug.md`, con este frontmatter:
  ```
  ---
  title: Título del post
  description: Descripción para SEO (meta description, og:description)
  date: 2026-07-24
  ---
  Cuerpo en Markdown normal.
  ```
  El slug de la URL (`/blog/tu-slug/`) es el nombre del archivo sin `.md`.

## Regenerar

```bash
python3 scripts/build_pages.py   # /proyectos/, /estudios/, /experiencia/
python3 scripts/build_blog.py    # /blog/ + un directorio por post, y actualiza page-sitemap.xml
```

Corre los dos después de cualquier cambio en los JSON, en `content/blog/`, o en el `<head>`/header/footer de `index.html` — si tocas `index.html`, las páginas generadas quedan desactualizadas hasta que se vuelva a correr esto.

## Cómo está montado

- `_site.py`: extrae `<head>`, header y footer de `index.html` una vez, y expone `build_head()` / `page_shell()` — lo comparten `build_pages.py` y `build_blog.py` para que no haya dos copias de la plantilla de página divergiendo con el tiempo.
- Cada script solo añade el CSS que de verdad es específico de sus páginas — lo que ya vive en el `<head>` de `index.html` (por ejemplo los estilos de `.study-card`/`.job-card`, usados también en el preview de la home) no se repite.
- Los valores de texto que vienen de los JSON/Markdown se escapan con `html.escape()` antes de insertarse — solo los fragmentos ya construidos como HTML (badges, enlaces) no se tocan.
- Un campo obligatorio que falte en un JSON o en el frontmatter de un post da un error explícito (qué archivo, qué campo), no un `KeyError`/`ValueError` críptico.
