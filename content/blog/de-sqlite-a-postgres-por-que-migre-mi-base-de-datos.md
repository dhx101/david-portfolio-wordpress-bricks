---
title: De SQLite a Postgres — por qué migré la base de datos de mi portal antes de lanzarlo
description: Por qué migré de SQLite a PostgreSQL antes de desplegar mi panel de agencia en Vercel, y qué tuve que cambiar en Prisma para hacerlo sin fricciones.
date: 2026-07-09
image: /assets/blog/de-sqlite-a-postgres-por-que-migre-mi-base-de-datos.webp
image_alt: Servidores de base de datos representando una migración de base de datos
---

Empecé a construir el [Web Client Portal](https://dhx101-web-client-portal.vercel.app) con SQLite porque, en desarrollo local, es lo más simple posible: un único archivo, sin servidor que levantar, cero configuración. Pero antes de desplegarlo en producción sobre Vercel, tuve que migrarlo a PostgreSQL. Esto es por qué.

## Por qué SQLite funciona bien en desarrollo

- Cero infraestructura: el archivo de base de datos vive junto al proyecto.
- Arranque instantáneo, ideal para iterar rápido en local.
- Perfecto para prototipar el modelo de datos antes de comprometerse con nada.

## Por qué no sirve en producción sobre Vercel

Vercel ejecuta cada función serverless en un entorno efímero: el sistema de archivos no persiste de forma fiable entre invocaciones, y no hay garantía de que dos peticiones lleguen a la misma instancia. Un archivo SQLite en ese entorno simplemente no sobrevive de forma consistente — es una base de datos pensada para un proceso único y de larga duración, no para funciones que se crean y destruyen constantemente.

PostgreSQL, en cambio, es un servidor de base de datos independiente al que cualquier función serverless se conecta por red, sin depender de dónde se ejecuta cada invocación.

## Qué cambió con Prisma

El ORM (Prisma) hizo esta migración mucho menos dolorosa de lo que habría sido escribiendo SQL a mano:

- Cambiar el `provider` del datasource de `sqlite` a `postgresql` en el schema.
- Revisar tipos que SQLite trata de forma más laxa que Postgres (por ejemplo, `Boolean` y `DateTime` son más estrictos en Postgres).
- Regenerar las migraciones desde cero, ya que el formato de migración de cada motor no es intercambiable.
- Usar `@prisma/adapter-pg` para la conexión, en vez del driver por defecto.

## La lección general

Elegir la base de datos "fácil" para desarrollar rápido en local es una decisión razonable — siempre que se sepa desde el principio que no es la misma decisión que la de producción, y se planifique el cambio antes de que el proyecto dependa de datos reales de clientes, no después.

¿Estás construyendo algo que vas a desplegar en serverless y no sabes qué base de datos elegir? [Contáctame](/#brxe-vzfdra).
