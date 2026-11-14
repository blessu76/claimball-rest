---
title: Móviles pequeños, texto grande y una red de seguridad
description: Antes de seguir adelante, revisamos las pantallas de Claimball en un móvil estrecho con texto grande, y añadimos una red de seguridad para que un archivo dañado no detenga la app.
summary: Antes de seguir adelante, revisamos el menú, Mi récord y la clasificación de Claimball en un móvil estrecho con el texto ampliado un 50 por ciento, en inglés, árabe y coreano. También añadimos un guardián global de errores y un valor seguro de reserva para que la app siga abriendo si no se puede leer un elemento guardado. Sigue en pruebas y llegará pronto a iOS y Android.
slug: small-screens-and-safety-nets
lang: es
category: devlog
translation_of: en
keywords: Claimball, accesibilidad, pantallas pequeñas, fiabilidad, diario
copy_review: iris 2026-11-14
---
Un juego que abre mal o corta su texto no es divertido, por buenas que sean las reglas. Esta es una ronda de revisiones en las versiones de prueba interna de TestFlight, que todavía no se han publicado.

## Pantallas estrechas, texto grande

Probamos el menú, la pantalla Mi récord y la de clasificación con el ancho de un móvil estrecho y el texto ampliado un 50 por ciento, en inglés, árabe y coreano, y comprobamos que nada se desborda ni se superpone.

## Una red de seguridad para los errores

Si algo inesperado sale mal, un guardián global de errores lo captura en lugar de dejar que la app se caiga.

## Abre aunque un guardado no se pueda leer

Si un elemento guardado no se puede leer al arrancar, el juego recurre a un valor seguro por defecto para ese elemento y abre igualmente, en lugar de quedarse en una pantalla en blanco.

## Traducciones

En cada compilación se ejecuta una comprobación de traducciones que señala los textos que faltan o están rotos. Las traducciones en sí se hicieron con IA y todavía no las han revisado hablantes nativos.

## Lo que viene

Claimball sigue en pruebas y llegará pronto a iOS y Android. Todavía no hay fecha de lanzamiento.

## Preguntas frecuentes

### ¿Cómo comprueban las pantallas pequeñas y el texto grande?
Probamos el menú, la pantalla Mi récord y la de clasificación con el ancho de un móvil estrecho y el texto ampliado un 50 por ciento, en inglés, árabe y coreano, y comprobamos que nada se desborda ni se superpone.

### ¿Qué pasa si algo falla en la app?
Si algo inesperado sale mal, un guardián global de errores lo captura en lugar de dejar que la app se caiga. Si un elemento guardado no se puede leer al arrancar, el juego recurre a un valor seguro por defecto para ese elemento y abre igualmente.

### ¿Se han revisado las traducciones?
En cada compilación se ejecuta una comprobación de traducciones que señala los textos que faltan o están rotos. Las traducciones en sí se hicieron con IA y todavía no las han revisado hablantes nativos.

### ¿Ya se ha lanzado Claimball?
Todavía no. Sigue en pruebas y llegará pronto a iOS y Android, y aún no hay fecha de lanzamiento.
