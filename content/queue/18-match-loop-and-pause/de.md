---
title: Die Spielschleife wandert in eine Spiel-Engine
description: Die Animation des Spielfelds läuft jetzt in einer Spiel-Engine, und ein Spiel pausiert, wenn du die App verlässt.
summary: Wir haben die Animationsschleife des Hauptspielfelds in die Spiel-Engine Flame verlegt, sodass ihr Takt an einer Stelle gesteuert wird. Das Spiel läuft wie bisher. Wenn du die App während eines Spiels verlässt, pausiert das Spiel und wartet, bis du auf Weiter tippst. Die Version ist noch in Tests und kommt bald für iOS und Android.
slug: match-loop-and-pause
lang: de
category: devlog
translation_of: en
keywords: Claimball, Spiel-Engine, Pause, Partie, Journal
copy_review: iris 2026-11-20
---
Spielerinnen und Spieler sehen hier keine neue Regel. Es ist eine interne Änderung, die das Spielfeld stabil hält.

## Eine Schleife für das Spielfeld

Die Animation des Spielfelds lief bisher über einen eigenen Timer. Jetzt läuft sie auf der Spiel-Engine Flame, die die Bilder des Spielfelds an einer Stelle taktet.

## App verlassen, zurück mit Pause

Kommt ein Anruf, erscheint eine Benachrichtigung oder wechselst du in eine andere App, pausiert das Spiel. Wenn du zurückkommst, tippe auf Weiter, um fortzufahren. Solange du weg bist, bewegt sich nichts.

## Gleiches Spiel

Punktestand, Regeln, Speicherstände und Käufe sind nicht verändert. Das Spielfeld sieht aus und spielt sich wie zuvor.

## Noch in Tests

Wir prüfen die neue Schleife weiterhin auf echten Telefonen.

## Was als Nächstes kommt

Claimball ist noch in Tests und kommt bald für iOS und Android. Ein Veröffentlichungstermin steht noch nicht fest.

## Häufige Fragen

### Haben sich die Regeln geändert?
Nein. Punktestand, Regeln, Speicherstände und Käufe bleiben gleich. Geändert wurde nur, wie die Animation des Spielfelds läuft.

### Was passiert, wenn ich während eines Spiels gehe?
Das Spiel pausiert. Tippe beim Zurückkommen auf Weiter.

### Ist Claimball schon erschienen?
Noch nicht. Es ist in Tests und kommt bald für iOS und Android, ein Termin steht aber noch nicht fest.
