---
title: Cómo comprobamos que el marcador de aterrizaje dice la verdad
description: El marcador de aterrizaje solo sirve si acierta. Así probamos que muestra las casillas que de verdad se pintan.
summary: El marcador de aterrizaje de Claimball solo ayuda si acierta, así que probamos que coincide con las casillas que de verdad se pintan. Jugamos muchas partidas completas simuladas con distintas semillas aleatorias y comparamos cada marcador con el resultado, y además rompemos la regla a propósito para confirmar que la prueba falla. Todavía está en pruebas y llegará pronto a iOS y Android.
slug: marker-keeps-its-word
lang: es
category: devlog
translation_of: en
keywords: Claimball, marcador de aterrizaje, pruebas, juego limpio, diario
---
El marcador de aterrizaje muestra dónde caerá la bola, así que tiene que acertar siempre. Así se prueba en las versiones de prueba internas de TestFlight, que todavía no se han publicado.

## Una promesa en pantalla

Si el marcador indicara una casilla y el juego pintara otra, dejarías de fiarte de él y el juego parecería injusto. Por eso el marcador tiene que coincidir con lo que realmente ocurre.

## Una regla para ambos

El marcador y el golpe real deben coincidir. Lo comprobamos jugando partidas completas simuladas, muchísimas veces y con distintas semillas aleatorias, y comparando cada marcador con las casillas que realmente se pintaron. Tienen que coincidir siempre.

## Comprobar la comprobación

Una prueba que nunca falla demuestra poco. Por eso también rompemos la regla a propósito, por ejemplo moviendo un valor un poco, y nos aseguramos de que la prueba lo detecta y falla.

## También con rivales y reglas especiales

La misma comparación se ejecuta con cada rival de IA y con las variantes del Desafío diario, ya que cambian la velocidad y el comportamiento.

## Sinceros sobre los límites

Estas comprobaciones se hacen con partidas simuladas. Jugar en teléfonos reales es otra ronda de pruebas distinta.

## Qué viene ahora

Claimball sigue en pruebas y llegará pronto a iOS y Android. Todavía no hay fecha de lanzamiento.

## Preguntas frecuentes

### ¿Por qué tiene que ser preciso el marcador de aterrizaje?
Si el marcador indicara una casilla y el juego pintara otra, dejarías de fiarte de él y el juego parecería injusto.

### ¿Cómo prueban el marcador?
Jugamos partidas completas simuladas muchísimas veces con distintas semillas aleatorias y comparamos cada marcador con las casillas que realmente se pintaron. Tienen que coincidir siempre.

### ¿La prueba incluye a los rivales y el Desafío diario?
Sí. La misma comparación se ejecuta con cada rival de IA y con las variantes del Desafío diario, ya que cambian la velocidad y el comportamiento. Estas comprobaciones se hacen con partidas simuladas, y jugar en teléfonos reales es otra ronda de pruebas distinta.

### ¿Ya se ha lanzado Claimball?
Todavía no. Sigue en pruebas y llegará pronto a iOS y Android, y aún no hay fecha de lanzamiento.
