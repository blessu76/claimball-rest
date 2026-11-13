---
title: How a tied match ends in Claimball
description: A tie used to end in a confusing result. Here is how sudden death works now, and what changed in the latest test builds.
summary: In Claimball, a tied match goes to sudden death, where the next point decides it. The player who scores the deciding point takes one tile from the rival if needed, so the board reads 30 to 28 instead of 29 to 29 and the result screen always matches the final numbers.
slug: sudden-death-and-draws
lang: en
category: devlog
keywords: Claimball, sudden death, tie, casual game, journal
published: 2026-11-03T21:05+09:00
---
A Claimball match is 90 seconds on a notebook grid, and most of the time one side simply holds more land when the clock stops. This post is about the other case: the match ends level.

## What happens on a tie

When time runs out with the tile counts equal, the match goes to sudden death. The clock stops and the next point decides the match. If a ball is still in the air at 90 seconds, the match waits for it to land before it counts.

## The bug we fixed

In our test builds, a sudden death could end with the tile counts still level, for example 29 to 29, while the result screen said you lost. The winner was decided correctly, but the numbers on screen did not show it, so it felt wrong.

We first made such a result show as a draw. Then we decided a sudden death should never look like a draw: the player who scores the deciding point now takes one tile from the rival if needed, so the board reads 30 to 28 instead of 29 to 29. The result screen always agrees with the final numbers.

## Also in the latest test builds

The logo and the Max combo number now keep their correct order in right-to-left languages such as Arabic, and the website's Release Notes page lists what changed in each build.

## What is next

Claimball is still in testing and coming soon to iOS and Android. There is no release date yet.

## FAQ

### What happens when a Claimball match ends tied?
When time runs out with the tile counts equal, the match goes to sudden death. The clock stops and the next point decides the match.

### What if the ball is still in the air at 90 seconds?
The match waits for the ball to land before it counts.

### Can a sudden death end looking like a draw?
No. The player who scores the deciding point now takes one tile from the rival if needed, so the board reads 30 to 28 instead of 29 to 29.

### Is Claimball released yet?
Not yet. Claimball is still in testing and coming soon to iOS and Android, with no release date yet.
