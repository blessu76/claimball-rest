---
title: Comment se termine un match nul dans Claimball
description: Une égalité se terminait autrefois sur un résultat déroutant. Voici comment fonctionne désormais la mort subite, et ce qui a changé dans les dernières versions de test.
summary: Dans Claimball, un match à égalité passe en mort subite, où le point suivant décide. Le joueur qui marque le point décisif prend une case au rival si nécessaire, de sorte que le plateau affiche 30 à 28 au lieu de 29 à 29 et que l'écran de résultat correspond toujours aux chiffres finaux.
slug: sudden-death-and-draws
lang: fr
category: devlog
translation_of: en
keywords: Claimball, mort subite, égalité, jeu casual, journal
published: 2026-11-03T21:05+09:00
copy_review: iris 2026-11-14
---
Un match de Claimball dure 90 secondes sur une grille de cahier, et la plupart du temps un camp détient simplement plus de terrain quand le chrono s'arrête. Cet article parle de l'autre cas : le match se termine à égalité.

## Ce qui se passe en cas d'égalité

Quand le temps est écoulé avec le même nombre de cases, le match passe en mort subite. Le chrono s'arrête et le point suivant décide du match. Si une balle est encore en l'air à 90 secondes, le match attend qu'elle retombe avant de compter.

## Le bug que nous avons corrigé

Dans nos versions de test, une mort subite pouvait se terminer avec des cases encore à égalité, par exemple 29 à 29, alors que l'écran de résultat indiquait que vous aviez perdu. Le vainqueur était bien désigné, mais les chiffres à l'écran ne le montraient pas, ce qui donnait une impression d'injustice.

Nous avons d'abord fait afficher ce résultat comme un match nul. Puis nous avons décidé qu'une mort subite ne devait jamais ressembler à un match nul : le joueur qui marque le point décisif prend désormais une case au rival si nécessaire, de sorte que le plateau affiche 30 à 28 au lieu de 29 à 29. L'écran de résultat correspond toujours aux chiffres finaux.

## Aussi dans les dernières versions de test

Le logo et le nombre du Combo max conservent désormais leur ordre correct dans les langues qui s'écrivent de droite à gauche, comme l'arabe, et la page Notes de version du site liste ce qui a changé dans chaque version.

## La suite

Claimball est toujours en phase de test et arrive bientôt sur iOS et Android. Il n'y a pas encore de date de sortie.

## Questions fréquentes

### Que se passe-t-il quand un match de Claimball se termine à égalité ?
Quand le temps est écoulé avec le même nombre de cases, le match passe en mort subite. Le chrono s'arrête et le point suivant décide du match.

### Et si la balle est encore en l'air à 90 secondes ?
Le match attend que la balle retombe avant de compter.

### Une mort subite peut-elle se terminer comme un match nul ?
Non. Le joueur qui marque le point décisif prend désormais une case au rival si nécessaire, de sorte que le plateau affiche 30 à 28 au lieu de 29 à 29.

### Claimball est-il déjà sorti ?
Pas encore. Il est toujours en test et arrive bientôt sur iOS et Android, et il n'y a pas encore de date de sortie.
