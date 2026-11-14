---
title: Wie wir prüfen, dass die Landemarkierung die Wahrheit sagt
description: Die Landemarkierung ist nur nützlich, wenn sie stimmt. So testen wir, dass sie die Felder zeigt, die wirklich gefärbt werden.
summary: Die Landemarkierung in Claimball hilft nur, wenn sie stimmt, deshalb testen wir, ob sie mit den tatsächlich gefärbten Feldern übereinstimmt. Wir spielen viele vollständige simulierte Partien mit verschiedenen Zufallswerten und vergleichen jede Markierung mit dem Ergebnis. Außerdem brechen wir die Regel absichtlich, um zu bestätigen, dass der Test fehlschlägt. Das Spiel ist noch in der Testphase und kommt bald für iOS und Android.
slug: marker-keeps-its-word
lang: de
category: devlog
translation_of: en
keywords: Claimball, Landemarkierung, Tests, Fairplay, Journal
copy_review: iris 2026-11-14
---
Die Landemarkierung zeigt, wo der Ball landen wird, also muss sie jedes Mal stimmen. So wird sie in den internen TestFlight-Testversionen getestet, die noch nicht öffentlich veröffentlicht sind.

## Ein Versprechen auf dem Bildschirm

Würde die Markierung ein Feld anzeigen und das Spiel ein anderes färben, würdest du ihr nicht mehr trauen, und das Spiel würde sich unfair anfühlen. Die Markierung muss also mit dem übereinstimmen, was wirklich passiert.

## Eine Regel für beides

Markierung und echter Treffer sollen übereinstimmen. Das prüfen wir, indem wir vollständige simulierte Partien spielen, sehr oft und mit verschiedenen Zufallswerten, und jede Markierung mit den tatsächlich gefärbten Feldern vergleichen. Sie müssen jedes Mal übereinstimmen.

## Den Test testen

Ein Test, der nie fehlschlägt, beweist wenig. Deshalb brechen wir die Regel auch absichtlich, etwa indem wir einen Wert leicht verschieben, und stellen sicher, dass der Test es bemerkt und fehlschlägt.

## Auch bei Rivalen und Sonderregeln

Derselbe Vergleich läuft mit jedem KI-Rivalen und mit den Varianten der Tagesaufgabe, da sie Tempo und Verhalten verändern.

## Ehrlich bei den Grenzen

Diese Prüfungen laufen auf simulierten Partien. Das Spielen auf echten Handys ist eine eigene Testrunde.

## Wie es weitergeht

Claimball ist noch in der Testphase und kommt bald für iOS und Android. Ein Erscheinungsdatum gibt es noch nicht.

## Häufige Fragen

### Warum muss die Landemarkierung genau sein?
Würde die Markierung ein Feld anzeigen und das Spiel ein anderes färben, würdest du ihr nicht mehr trauen, und das Spiel würde sich unfair anfühlen.

### Wie testet ihr die Markierung?
Wir spielen sehr oft vollständige simulierte Partien mit verschiedenen Zufallswerten und vergleichen jede Markierung mit den tatsächlich gefärbten Feldern. Sie müssen jedes Mal übereinstimmen.

### Deckt der Test Rivalen und die Tagesaufgabe ab?
Ja. Derselbe Vergleich läuft mit jedem KI-Rivalen und mit den Varianten der Tagesaufgabe, da sie Tempo und Verhalten verändern. Diese Prüfungen laufen auf simulierten Partien, das Spielen auf echten Handys ist eine eigene Testrunde.

### Ist Claimball schon erschienen?
Noch nicht. Es ist noch in der Testphase und kommt bald für iOS und Android, ein Erscheinungsdatum gibt es noch nicht.
