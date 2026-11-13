---
title: Small phones, big text and a safety net
description: Before going further, we checked Claimball's screens on a narrow phone with large text, and added a safety net so one bad file cannot stop the app.
summary: Before going further, we checked Claimball's menu, stats and ranking screens on a narrow phone with text scaled up by 50 percent, in English, Arabic and Korean. We also added a global error guard and a safe fallback so the app still opens if one saved item cannot be read. It is still in testing and coming soon to iOS and Android.
slug: small-screens-and-safety-nets
lang: en
category: devlog
keywords: Claimball, accessibility, small screens, reliability, journal
---
A game that opens badly or cuts off its text is not fun, however good the rules are. This is a round of checks in the TestFlight internal test builds, which are not released to the public yet.

## Narrow screens, large text

We test the menu, the stats screen and the ranking screen on a narrow phone width with text scaled up by 50 percent, in English, Arabic and Korean, and make sure nothing overflows or overlaps.

## A safety net for errors

If something unexpected goes wrong, a global error guard catches it instead of letting the app fall over.

## Opens even when a save is unreadable

If one saved item cannot be read at startup, the game falls back to a safe default for that item and still opens, rather than stopping at a blank screen.

## Translations

A translation check runs on every build and flags missing or broken text. The translations themselves were made with AI and have not yet been reviewed by native speakers.

## What is next

Claimball is still in testing and coming soon to iOS and Android. There is no release date yet.

## FAQ

### How do you check small screens and large text?
We test the menu, the stats screen and the ranking screen on a narrow phone width with text scaled up by 50 percent, in English, Arabic and Korean, and make sure nothing overflows or overlaps.

### What if something goes wrong in the app?
If something unexpected goes wrong, a global error guard catches it instead of letting the app fall over. If one saved item cannot be read at startup, the game falls back to a safe default for that item and still opens.

### Have the translations been reviewed?
A translation check runs on every build and flags missing or broken text. The translations themselves were made with AI and have not yet been reviewed by native speakers.

### Is Claimball released yet?
Not yet. It is still in testing and coming soon to iOS and Android, and there is no release date yet.
