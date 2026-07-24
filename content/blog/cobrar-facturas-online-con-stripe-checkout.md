---
title: Cómo cobrar facturas online con Stripe Checkout en un panel interno
description: Cómo integré Stripe Checkout en un panel interno para que los clientes paguen facturas online, con verificación de firma de webhook e idempotencia real.
date: 2026-07-03
image: /assets/blog/cobrar-facturas-online-con-stripe-checkout.webp
image_alt: Pago online con tarjeta representando un cobro con Stripe Checkout
---

Añadir "pagar online" a un panel de facturación suena simple hasta que se piensa en todos los casos límite: ¿qué pasa si el navegador se cierra justo después de pagar? ¿Y si el webhook de confirmación llega dos veces? Esto es cómo integré Stripe Checkout en el [Web Client Portal](https://dhx101-web-client-portal.vercel.app) resolviendo esos casos desde el diseño, no como parches después.

## La regla de oro: el navegador nunca es la fuente de verdad

Es tentador marcar una factura como pagada en cuanto Stripe redirige de vuelta al usuario tras el pago. Es también incorrecto: esa redirección puede no llegar a ejecutarse (el usuario cierra la pestaña, pierde conexión) aunque el pago sí se haya completado del lado de Stripe.

La única fuente de verdad es el **webhook** que Stripe envía a un endpoint del servidor cuando el evento `checkout.session.completed` ocurre de verdad — de forma completamente independiente de lo que haga el navegador del cliente.

## Verificación de firma: no confiar en cualquier POST

El endpoint de webhook no puede simplemente aceptar cualquier petición que diga "este pago se completó". Stripe firma cada evento con una clave secreta, y el servidor debe verificar esa firma antes de procesar nada:

```
const event = stripe.webhooks.constructEvent(
  rawBody,
  signatureHeader,
  webhookSecret
)
```

Sin esta verificación, cualquiera que conozca la URL del endpoint podría simular pagos falsos.

## Idempotencia: Stripe puede reenviar el mismo evento

Stripe no garantiza entrega única de cada webhook — puede reenviarlo si no recibe una respuesta rápida. El endpoint necesita ser idempotente: si el mismo `checkout.session.completed` llega dos veces, la segunda vez no debe volver a procesar el pago ni duplicar ningún efecto. En este caso, comprobar si la factura ya está marcada como `PAID` antes de aplicar el cambio es suficiente.

## Integración opcional, sin romper nada sin configurar

Siguiendo un patrón que ya usaba el resto del proyecto (el envío de emails, por ejemplo), la integración de Stripe se activa solo si existe la variable de entorno `STRIPE_SECRET_KEY`. Sin ella, el botón "Pagar ahora" simplemente no aparece — el resto del panel funciona con normalidad. Ninguna integración externa debería ser obligatoria para que el resto de la aplicación arranque.

## Resultado

Un cliente puede pagar su factura desde el propio panel, con la confirmación gestionada de forma fiable por el servidor, sin depender de que su navegador complete correctamente la redirección de vuelta.

¿Necesitas cobros online en tu propia herramienta interna? [Contáctame](/#brxe-vzfdra).
