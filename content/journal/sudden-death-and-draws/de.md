---
title: Wie ein Unentschieden in Claimball endet
description: Früher endete ein Gleichstand mit einem verwirrenden Ergebnis. So funktioniert Sudden Death jetzt, und das hat sich in den neuesten Testversionen geändert.
summary: In Claimball geht ein Match mit Gleichstand in Sudden Death, wo der nächste Punkt entscheidet. Wer den entscheidenden Punkt holt, nimmt dem Rivalen bei Bedarf ein Feld ab, sodass das Brett 30 zu 28 statt 29 zu 29 zeigt und der Ergebnisbildschirm immer zu den Endzahlen passt.
slug: sudden-death-and-draws
lang: de
category: devlog
translation_of: en
keywords: Claimball, Sudden Death, Gleichstand, Casual-Spiel, Journal
published: 2026-11-03T21:05+09:00
---
Ein Claimball-Match dauert 90 Sekunden auf einem Heftraster, und meistens hat eine Seite einfach mehr Land, wenn die Uhr stehen bleibt. In diesem Beitrag geht es um den anderen Fall: Das Match endet gleichauf.

## Was bei einem Gleichstand passiert

Läuft die Zeit bei gleicher Feldanzahl ab, geht das Match in Sudden Death. Die Uhr bleibt stehen, und der nächste Punkt entscheidet das Match. Ist bei 90 Sekunden noch ein Ball in der Luft, wartet das Match, bis er gelandet ist, bevor es zählt.

## Der Fehler, den wir behoben haben

In unseren Testversionen konnte ein Sudden Death mit weiterhin gleicher Feldanzahl enden, zum Beispiel 29 zu 29, während der Ergebnisbildschirm anzeigte, dass du verloren hast. Der Gewinner wurde korrekt ermittelt, aber die Zahlen auf dem Bildschirm zeigten es nicht, und deshalb fühlte es sich falsch an.

Zuerst haben wir ein solches Ergebnis als Unentschieden anzeigen lassen. Dann haben wir entschieden, dass ein Sudden Death nie wie ein Unentschieden aussehen darf: Wer den entscheidenden Punkt holt, nimmt dem Rivalen jetzt bei Bedarf ein Feld ab, sodass das Brett 30 zu 28 statt 29 zu 29 zeigt. Der Ergebnisbildschirm stimmt immer mit den Endzahlen überein.

## Außerdem in den neuesten Testversionen

Das Logo und die Zahl für die maximale Kombo behalten jetzt in Sprachen, die von rechts nach links geschrieben werden, wie Arabisch, ihre richtige Reihenfolge, und die Seite mit den Versionshinweisen der Website listet auf, was sich in jedem Build geändert hat.

## Wie es weitergeht

Claimball befindet sich weiterhin im Test und erscheint bald für iOS und Android. Ein Veröffentlichungsdatum gibt es noch nicht.

## FAQ

### Was passiert, wenn ein Claimball-Match unentschieden endet?
Läuft die Zeit bei gleicher Feldanzahl ab, geht das Match in Sudden Death. Die Uhr bleibt stehen, und der nächste Punkt entscheidet das Match.

### Was ist, wenn der Ball bei 90 Sekunden noch in der Luft ist?
Das Match wartet, bis der Ball gelandet ist, bevor es zählt.

### Kann ein Sudden Death wie ein Unentschieden enden?
Nein. Wer den entscheidenden Punkt holt, nimmt dem Rivalen jetzt bei Bedarf ein Feld ab, sodass das Brett 30 zu 28 statt 29 zu 29 zeigt.

### Ist Claimball schon erschienen?
Noch nicht. Es ist weiterhin im Test und erscheint bald für iOS und Android, ein Veröffentlichungsdatum gibt es noch nicht.
