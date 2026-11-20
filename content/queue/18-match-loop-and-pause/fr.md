---
title: La boucle de partie passe dans un moteur de jeu
description: L'animation du plateau de la partie tourne désormais dans un moteur de jeu, et la partie se met en pause quand vous quittez l'app.
summary: Nous avons déplacé la boucle d'animation du plateau principal vers le moteur de jeu Flame, pour que son rythme soit géré à un seul endroit. Le jeu se joue comme avant. Si vous quittez l'app pendant une partie, elle se met en pause et attend que vous appuyiez sur Reprendre. Le jeu est encore en test et arrive bientôt sur iOS et Android.
slug: match-loop-and-pause
lang: fr
category: devlog
translation_of: en
keywords: Claimball, moteur de jeu, pause, partie, journal
copy_review: iris 2026-11-20
---
Les joueurs ne voient aucune nouvelle règle ici. C'est un changement interne qui garde le plateau de la partie stable.

## Une seule boucle pour le plateau

L'animation du plateau tournait avant sur son propre minuteur. Elle tourne maintenant sur le moteur de jeu Flame, qui cadence les images du plateau depuis un seul endroit.

## Quitter l'app, revenir à une pause

Si un appel arrive, qu'une notification s'affiche ou que vous passez à une autre app, la partie se met en pause. Au retour, appuyez sur Reprendre pour continuer. Pendant votre absence, rien ne bouge.

## Le même jeu

Le score, les règles, les sauvegardes et les achats n'ont pas changé. Le plateau se présente et se joue comme avant.

## Toujours en test

Nous vérifions encore la nouvelle boucle sur de vrais téléphones.

## La suite

Claimball est toujours en test et arrive bientôt sur iOS et Android. Il n'y a pas encore de date de sortie.

## Questions fréquentes

### Les règles ont-elles changé ?
Non. Le score, les règles, les sauvegardes et les achats ne changent pas. Seule la manière dont l'animation du plateau tourne a été déplacée.

### Que se passe-t-il si je quitte pendant une partie ?
La partie se met en pause. Appuyez sur Reprendre à votre retour.

### Claimball est-il déjà sorti ?
Pas encore. Il est en test et arrive bientôt sur iOS et Android, sans date de sortie pour le moment.
