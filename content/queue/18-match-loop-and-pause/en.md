---
title: The match loop moves to a game engine
description: The match board now runs its animation on a game engine, and a match pauses when you leave the app.
summary: We moved the animation loop of the main match board onto the Flame game engine, so its timing is handled in one place. The game plays as before. If you leave the app during a match, the match pauses and waits for you to press Resume. It is still in testing and coming soon to iOS and Android.
slug: match-loop-and-pause
lang: en
category: devlog
keywords: Claimball, game engine, pause, match, journal
copy_review: iris 2026-11-20
---
Players do not see a new rule here. This is a change under the hood that keeps the match board steady.

## One loop for the board

The board's animation used to run on its own timer. It now runs on the Flame game engine, which drives the board's frames from one place.

## Leave the app, come back to a pause

If a call comes in, a notification pops up or you switch to another app, the match pauses. When you come back, press Resume to carry on. Nothing moves while you are away.

## Same game

Scoring, rules, saves and purchases are not changed. The board looks and plays the same as before.

## Still being tested

We are still checking the new loop on real phones.

## What is next

Claimball is still in testing and coming soon to iOS and Android. There is no release date yet.

## FAQ

### Did the rules change?
No. Scoring, rules, saves and purchases are not changed. Only the way the board's animation runs was moved.

### What happens if I leave during a match?
The match pauses. Press Resume when you come back.

### Is Claimball released yet?
Not yet. It is still in testing and coming soon to iOS and Android, and there is no release date yet.
