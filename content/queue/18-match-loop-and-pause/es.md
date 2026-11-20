---
title: El bucle de la partida pasa a un motor de juego
description: La animación tablero de la partida ahora corre en un motor de juego, y la partida se pausa cuando sales de la app.
summary: Pasamos el bucle de animación del tablero principal al motor de juego Flame, así que su tiempo se gestiona en un solo lugar. El juego funciona igual que antes. Si sales de la app durante una partida, la partida se pausa y espera a que pulses Reanudar. Sigue en pruebas y llegará pronto a iOS y Android.
slug: match-loop-and-pause
lang: es
category: devlog
translation_of: en
keywords: Claimball, motor de juego, pausa, partida, diario
---
Los jugadores no ven una regla nueva aquí. Es un cambio interno que mantiene estable el tablero de la partida.

## Un solo bucle para el tablero

La animación del tablero funcionaba antes con su propio temporizador. Ahora corre sobre el motor de juego Flame, que controla los fotogramas del tablero desde un solo lugar.

## Sales de la app y vuelves a una pausa

Si entra una llamada, aparece una notificación o cambias a otra app, la partida se pausa. Al volver, pulsa Reanudar para seguir. Mientras no estás, nada se mueve.

## El mismo juego

La puntuación, las reglas, los guardados y las compras no han cambiado. El tablero se ve y se juega igual que antes.

## Sigue en pruebas

Seguimos comprobando el nuevo bucle en teléfonos reales.

## Lo que viene

Claimball sigue en pruebas y llegará pronto a iOS y Android. Todavía no hay fecha de lanzamiento.

## Preguntas frecuentes

### ¿Han cambiado las reglas?
No. La puntuación, las reglas, los guardados y las compras siguen igual. Solo se cambió la forma en que se ejecuta la animación del tablero.

### ¿Qué pasa si salgo durante una partida?
La partida se pausa. Pulsa Reanudar cuando vuelvas.

### ¿Claimball ya está disponible?
Todavía no. Sigue en pruebas y llegará pronto a iOS y Android, y aún no hay fecha de lanzamiento.
