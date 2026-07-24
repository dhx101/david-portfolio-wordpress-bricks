---
title: Core Web Vitals — qué son y cómo afectan a tu posicionamiento
description: Qué son los Core Web Vitals de Google (LCP, INP, CLS), por qué son parte del SEO técnico y cómo mejorarlos en una web WordPress paso a paso.
date: 2026-06-10
image: /assets/blog/core-web-vitals-que-son.webp
image_alt: Métricas de velocidad y rendimiento web en pantalla
---

Dentro del [SEO On-Page](/blog/seo-on-page/), hay un grupo de métricas que Google usa directamente como señal de posicionamiento: los Core Web Vitals. No son opinión ni buenas prácticas genéricas — son números concretos que Google mide en tu web real.

## Las tres métricas

### LCP (Largest Contentful Paint)

Mide cuánto tarda en cargarse el elemento más grande visible al entrar en la página (normalmente una imagen o un bloque de texto grande). Google considera bueno un LCP por debajo de 2,5 segundos.

**Causas típicas de un LCP lento:** imágenes sin comprimir, un hosting lento, o demasiados plugins de WordPress cargando recursos antes de mostrar contenido.

### INP (Interaction to Next Paint)

Mide cuánto tarda la web en responder cuando el usuario hace clic, toca o escribe algo. Sustituyó a la antigua métrica FID en 2024. Un INP alto se nota como una web que "se queda pillada" al interactuar.

**Causas típicas:** JavaScript pesado ejecutándose en el hilo principal, animaciones mal optimizadas.

### CLS (Cumulative Layout Shift)

Mide cuánto "salta" el contenido de la página mientras carga — por ejemplo, cuando haces clic en un botón y en ese momento carga una imagen encima que te hace pulsar otra cosa por accidente.

**Causas típicas:** imágenes o anuncios sin dimensiones reservadas, fuentes que cargan tarde y desplazan el texto.

## Cómo comprobar los tuyos

La herramienta más directa es **PageSpeed Insights** (pagespeed.web.dev): introduces tu URL y te da los tres valores medidos con datos reales de usuarios, no solo una simulación.

## Cómo mejorarlos en WordPress

- Usa formatos de imagen modernos (WebP) y compresión antes de subirlas.
- Reduce el número de plugins a los estrictamente necesarios — cada uno añade peso.
- Activa caché a nivel de servidor o de plugin.
- Reserva siempre el espacio de imágenes y banners con `width`/`height` definidos, para evitar saltos de layout.
- Elige un hosting con buen tiempo de respuesta del servidor (TTFB), no solo "mucho espacio en disco".

## Conclusión

Los Core Web Vitals no son un checkbox técnico aislado: miden literalmente si tu web se siente rápida y estable para quien la usa, y Google lo usa como uno más de sus factores de posicionamiento.

### ¿Quieres saber cómo están tus Core Web Vitals?

Los reviso y priorizo qué corregir primero según el impacto real en tu posicionamiento. [Contáctame](/#brxe-vzfdra).
