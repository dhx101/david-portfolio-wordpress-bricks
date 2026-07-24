---
title: Por qué construí un portal de clientes para una agencia WordPress
description: Cómo y por qué desarrollé un portal en Next.js para que los clientes de una agencia WordPress vean el estado de su sitio, sus facturas y las paguen online, sin depender de emails sueltos ni hojas de cálculo.
date: 2026-07-24
---

Cualquiera que gestione varios sitios WordPress para clientes conoce el problema: la información sobre cada sitio —si está caído, si tiene actualizaciones pendientes, si la factura del mes está pagada— acaba repartida entre el correo, una hoja de cálculo y la memoria de quien lleva la cuenta. Funciona mientras hay dos o tres clientes. Deja de funcionar en cuanto hay diez.

Por eso construí [Web Client Portal](/proyectos/): un panel donde cada cliente de una agencia WordPress inicia sesión y ve el estado real de su sitio, y donde la agencia gestiona todo desde una única vista en vez de entrar sitio por sitio.

## El problema concreto

Una agencia que lleva WordPress para varios clientes necesita responder, a diario, preguntas como:

- ¿Qué sitios tienen actualizaciones de WordPress, plugins o temas pendientes?
- ¿Algún sitio ha dejado de responder?
- ¿Qué facturas siguen sin pagar?
- ¿Hay tickets de soporte abiertos que llevan días sin respuesta?

Sin una herramienta centralizada, cada una de esas preguntas exige entrar sitio por sitio, o confiar en que alguien se acuerde de mirar. Ninguna de las dos opciones escala.

## Lo que construí

El portal conecta con cada WordPress a través de un plugin propio ([WP Admin Desk](/proyectos/)) que expone un pequeño API REST: versión de núcleo, plugins y temas pendientes, y si el sitio usa WooCommerce, pedidos pendientes y stock bajo. Un cron sincroniza esos datos periódicamente, así que el panel siempre refleja el estado real, no lo que alguien recuerde.

Con esos datos, la agencia tiene un panel de **"sitios que necesitan atención"**: no una lista de todos los sitios, sino solo los que tienen un problema real — y solo avisa por email cuando un sitio empeora de verdad, no en cada sincronización rutinaria mientras el mismo problema sigue ahí. Eso evita la fatiga de alertas que hace que la gente deje de leer los avisos.

Cada cliente, por su lado, entra a su propio panel y ve el estado de su sitio, su historial de facturas, y puede **pagarlas online con Stripe** sin tener que escribir un email pidiendo el número de cuenta.

## Decisiones técnicas que marcaron la diferencia

Dos decisiones concretas terminaron siendo las más importantes del proyecto:

**El navegador nunca es la fuente de verdad para un pago.** Una factura se marca como pagada solo cuando Stripe confirma el cobro mediante un webhook firmado — nunca en el momento en que el cliente vuelve del checkout, porque esa redirección solo demuestra que el navegador volvió, no que el pago se completó. El webhook además es idempotente: si Stripe reenvía el mismo evento, no pasa nada raro.

**Un email fallido no puede ser un email perdido.** Si el proveedor de email está caído, la notificación se queda en cola con reintento y backoff en vez de desaparecer en un log que nadie mira. Es la diferencia entre "el cliente nunca se enteró de que le llegó una factura" y "se enteró con un poco de retraso".

## El resultado

El portal está desplegado y en uso — puedes [probarlo tú mismo](https://dhx101-web-client-portal.vercel.app) con las credenciales de demostración que aparecen en la propia web. Stack: Next.js 16, TypeScript, Prisma y PostgreSQL, con Stripe para pagos, tests automatizados (Vitest + Playwright) y despliegue continuo en Vercel.

Si gestionas WordPress para varios clientes y te suena el problema que describo arriba, [hablemos](/#brxe-vzfdra).
