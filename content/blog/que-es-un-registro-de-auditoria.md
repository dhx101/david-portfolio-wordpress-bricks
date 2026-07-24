---
title: Qué es un registro de auditoría y por qué toda herramienta interna debería tener uno
description: Qué es un registro de auditoría (audit log), por qué debe ser best-effort y no transaccional, y cómo lo implementé en un panel de administración interno.
date: 2026-07-06
image: /assets/blog/que-es-un-registro-de-auditoria.webp
image_alt: Documentos y registros representando un log de auditoría
---

"¿Quién marcó esta factura como pagada?" es la típica pregunta que, sin un registro de auditoría, no tiene respuesta clara en un panel con varios administradores. Así lo resolví en el [Web Client Portal](https://dhx101-web-client-portal.vercel.app).

## Qué es un registro de auditoría

Un audit log es una tabla que registra, para cada acción administrativa relevante, quién la hizo, qué hizo, sobre qué elemento y cuándo. No es un sistema de logs de errores (eso es otra cosa) — es un historial legible de decisiones humanas dentro de la aplicación: crear una factura, cambiar su estado, dar de baja el acceso de un cliente.

## La decisión de diseño más importante: best-effort, no transaccional

El primer instinto al implementar esto sería escribir la entrada de auditoría dentro de la misma transacción que la acción real, para "garantizar" que nunca se pierde un registro. Es exactamente el error a evitar.

Si escribir la entrada de auditoría formara parte de la transacción de negocio, un problema pasajero en esa escritura (una tabla bloqueada, una conexión lenta) revertiría también la acción real — por ejemplo, dejar sin efecto que una factura se marcó como pagada, solo porque su registro de auditoría no pudo escribirse a tiempo. Eso es mucho peor que simplemente no tener el registro.

Por eso, el registro de auditoría se escribe **después** de que la acción real ya tuvo éxito, envuelto en su propio `try/catch`, sin poder revertir nada:

```
await db.invoice.update({ status: 'PAID' })
// la factura ya está pagada en este punto, pase lo que pase después
await logAudit({ action: 'invoice.status_changed', ... }).catch(logError)
```

Perder una entrada de auditoría pierde "quién lo hizo", no "qué pasó" — la factura sigue correctamente marcada como pagada de todas formas.

## Qué guardar en cada entrada

- **Quién:** el id del actor, más un snapshot de su nombre (por si esa cuenta se elimina después, el registro sigue siendo legible).
- **Qué:** una acción concreta (`invoice.status_changed`, `client_access.deleted`), no un texto libre.
- **Sobre qué:** tipo y id del elemento afectado.
- **Detalle opcional:** por ejemplo, el estado anterior y el nuevo — nunca datos sensibles como una clave de API, aunque la acción sea "actualizar clave de API".

## Conclusión

Un registro de auditoría no necesita ser complejo para ser útil. Lo que sí necesita es una decisión clara sobre su nivel de garantía: en la mayoría de aplicaciones internas, best-effort y desacoplado de la transacción real es la opción correcta.

¿Tu panel interno necesita trazabilidad de quién hace qué? [Contáctame](/#brxe-vzfdra).
