---
title: Cómo termina un empate en Claimball
description: Antes un empate acababa con un resultado confuso. Así funciona ahora la muerte súbita y qué cambió en las últimas versiones de prueba.
summary: En Claimball, una partida empatada pasa a muerte súbita, donde el siguiente punto la decide. Quien anota el punto decisivo le quita una casilla al rival si hace falta, así que el tablero marca 30 a 28 en lugar de 29 a 29 y la pantalla de resultado siempre coincide con los números finales.
slug: sudden-death-and-draws
lang: es
category: devlog
translation_of: en
keywords: Claimball, muerte súbita, empate, juego casual, diario
published: 2026-11-03T21:05+09:00
---
Una partida de Claimball dura 90 segundos sobre una cuadrícula de cuaderno, y casi siempre un bando simplemente tiene más terreno cuando se para el reloj. Esta entrada trata del otro caso: la partida termina igualada.

## Qué pasa en un empate

Cuando se acaba el tiempo con el mismo número de casillas, la partida pasa a muerte súbita. El reloj se detiene y el siguiente punto decide la partida. Si todavía hay una pelota en el aire a los 90 segundos, la partida espera a que caiga antes de contar.

## El error que corregimos

En nuestras versiones de prueba, una muerte súbita podía terminar con las casillas aún igualadas, por ejemplo 29 a 29, mientras la pantalla de resultado decía que habías perdido. El ganador se decidía bien, pero los números en pantalla no lo reflejaban, y por eso parecía injusto.

Primero hicimos que ese resultado se mostrara como un empate. Después decidimos que una muerte súbita nunca debe parecer un empate: ahora quien anota el punto decisivo le quita una casilla al rival si hace falta, así que el tablero marca 30 a 28 en lugar de 29 a 29. La pantalla de resultado siempre concuerda con los números finales.

## También en las últimas versiones de prueba

El logotipo y el número del Combo máx. ahora mantienen el orden correcto en idiomas que se escriben de derecha a izquierda, como el árabe, y la página de Notas de la versión del sitio web enumera lo que cambió en cada versión.

## Lo que viene

Claimball sigue en pruebas y llegará pronto a iOS y Android. Aún no hay fecha de lanzamiento.

## Preguntas frecuentes

### ¿Qué pasa cuando una partida de Claimball termina en empate?
Cuando se acaba el tiempo con el mismo número de casillas, la partida pasa a muerte súbita. El reloj se detiene y el siguiente punto decide la partida.

### ¿Y si la pelota sigue en el aire a los 90 segundos?
La partida espera a que la pelota caiga antes de contar.

### ¿Puede una muerte súbita terminar pareciendo un empate?
No. Quien anota el punto decisivo ahora le quita una casilla al rival si hace falta, así que el tablero marca 30 a 28 en lugar de 29 a 29.

### ¿Ya se ha lanzado Claimball?
Todavía no. Claimball sigue en pruebas y llegará pronto a iOS y Android, sin fecha de lanzamiento por ahora.
