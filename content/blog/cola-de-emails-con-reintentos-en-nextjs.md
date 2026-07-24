---
title: Cola de emails con reintentos en Next.js — cómo evitar perder notificaciones
description: Cómo implementé un outbox de emails con reintentos y backoff exponencial en Next.js y Postgres para no perder notificaciones cuando falla el proveedor de correo.
date: 2026-06-29
image: /assets/blog/cola-de-emails-con-reintentos-en-nextjs.webp
image_alt: Bandeja de entrada de correo representando el envío de notificaciones
---

Cuando un email de notificación falla en producción — el proveedor está caído, hay un rate limit temporal, un timeout de red — la reacción más común es simplemente perder ese email. En un panel donde el email es la forma en la que un cliente se entera de que su web tiene un problema, eso no es aceptable. Así resolví este problema en el [Web Client Portal](https://dhx101-web-client-portal.vercel.app).

## El problema concreto

`sendMail()` llamaba directamente a la API del proveedor de correo (Resend) en el momento de crear una factura o cambiar el estado de un ticket. Si esa llamada fallaba, el email se perdía para siempre — la factura ya se había creado, pero nadie se enteraba.

## La solución: patrón outbox

En vez de enviar el email de forma síncrona, la acción de negocio escribe una fila en una tabla `EmailJob` (destinatario, asunto, cuerpo, estado) y termina ahí. Un proceso separado, disparado por un cron, es responsable de recorrer los emails pendientes e intentar entregarlos.

```
createInvoice() → INSERT EmailJob(status=PENDING) → responde al usuario
                                    ↓
                    cron cada X tiempo → intenta enviar → ¿éxito?
                                                          → sí: DELIVERED
                                                          → no: reintenta con backoff
```

La parte clave: la acción de negocio (crear la factura) **nunca depende de que el email se envíe con éxito**. Un fallo de email nunca debe revertir ni bloquear una acción de negocio ya completada.

## Backoff exponencial, con límite

Cada intento fallido incrementa el tiempo de espera antes del siguiente reintento, hasta un máximo (en mi caso, capado a 12 horas entre intentos) y un número máximo de intentos (8). Pasado ese límite, el job se marca como `DEAD` y queda registrado para revisión manual, en vez de reintentar indefinidamente un email que nunca va a entregarse.

## Por qué no usar una cola externa (SQS, RabbitMQ)

Para el volumen de este proyecto, montar infraestructura de colas externa era sobredimensionado. Una tabla en la misma base de datos Postgres que ya usa la aplicación, más un cron, resuelve el mismo problema —durabilidad ante fallos temporales— sin añadir una pieza de infraestructura nueva que mantener.

## Resultado

Si el proveedor de email cae durante una hora, ningún aviso se pierde: simplemente se entrega en cuanto el proveedor vuelve a responder, de forma transparente para el usuario.

¿Te interesa cómo aplicar este mismo patrón a tu propio sistema? [Contáctame](/#brxe-vzfdra).
