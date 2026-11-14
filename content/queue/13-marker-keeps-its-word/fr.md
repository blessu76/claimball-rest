---
title: Comment nous vérifions que le repère d'atterrissage dit vrai
description: Le repère d'atterrissage n'est utile que s'il est juste. Voici comment nous testons qu'il montre bien les cases qui sont réellement peintes.
summary: Le repère d'atterrissage de Claimball n'aide que s'il est juste, alors nous testons qu'il correspond aux cases réellement peintes. Nous jouons de nombreuses parties complètes simulées avec différentes graines aléatoires et comparons chaque repère au résultat, et nous brisons aussi la règle exprès pour confirmer que le test échoue. Le jeu est encore en test et arrive bientôt sur iOS et Android.
slug: marker-keeps-its-word
lang: fr
category: devlog
keywords: Claimball, repère d'atterrissage, tests, fair-play, journal
---
Le repère d'atterrissage montre où la balle va tomber, il doit donc être juste à chaque fois. Voici comment il est testé dans les versions de test internes TestFlight, qui ne sont pas encore publiées.

## Une promesse à l'écran

Si le repère indiquait une case et que le jeu en peignait une autre, vous cesseriez de vous y fier et le jeu paraîtrait injuste. Le repère doit donc correspondre à ce qui se passe réellement.

## Une règle pour les deux

Le repère et l'impact réel sont censés concorder. Nous le vérifions en jouant des parties complètes simulées, un grand nombre de fois avec différentes graines aléatoires, et en comparant chaque repère aux cases réellement peintes. Ils doivent concorder à chaque fois.

## Vérifier la vérification

Un test qui n'échoue jamais prouve peu de choses. Nous brisons donc aussi la règle exprès, par exemple en décalant légèrement une valeur, et nous nous assurons que le test s'en aperçoit et échoue.

## Aussi avec les rivaux et les règles spéciales

La même comparaison tourne avec chaque rival IA et avec les variantes du Défi quotidien, puisqu'ils changent la vitesse et le comportement.

## Honnêtes sur les limites

Ces vérifications portent sur des parties simulées. Jouer sur de vrais téléphones est une autre série de tests.

## Et ensuite

Claimball est encore en test et arrive bientôt sur iOS et Android. Il n'y a pas encore de date de sortie.

## FAQ

### Pourquoi le repère d'atterrissage doit-il être exact ?
Si le repère indiquait une case et que le jeu en peignait une autre, vous cesseriez de vous y fier et le jeu paraîtrait injuste.

### Comment testez-vous le repère ?
Nous jouons un grand nombre de parties complètes simulées avec différentes graines aléatoires et comparons chaque repère aux cases réellement peintes. Ils doivent concorder à chaque fois.

### Le test couvre-t-il les rivaux et le Défi quotidien ?
Oui. La même comparaison tourne avec chaque rival IA et avec les variantes du Défi quotidien, puisqu'ils changent la vitesse et le comportement. Ces vérifications portent sur des parties simulées, et jouer sur de vrais téléphones est une autre série de tests.

### Claimball est-il déjà sorti ?
Pas encore. Le jeu est encore en test et arrive bientôt sur iOS et Android, et il n'y a pas encore de date de sortie.
