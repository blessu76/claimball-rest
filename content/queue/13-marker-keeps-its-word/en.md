---
title: How we check that the landing marker tells the truth
description: The landing marker is only useful if it is right. Here is how we test that it shows the tiles that really get painted.
summary: The Claimball landing marker only helps if it is right, so we test that it matches the tiles that really get painted. We play many full simulated matches with different random seeds and compare every marker with the result, and we also break the rule on purpose to confirm the test fails. It is still in testing and coming soon to iOS and Android.
slug: marker-keeps-its-word
lang: en
category: devlog
keywords: Claimball, landing marker, testing, fair play, journal
---
The landing marker shows where the ball will land, so it has to be right every time. This is how it is tested in the TestFlight internal test builds, which are not released to the public yet.

## A promise on screen

If the marker said one tile and the game painted another, you would stop trusting it, and the game would feel unfair. So the marker has to match what really happens.

## One rule for both

The marker and the real hit are meant to agree. We check this by playing full simulated matches, many times over with different random seeds, and comparing every marker with the tiles that were actually painted. They must agree every time.

## Checking the check

A test that never fails proves little. So we also break the rule on purpose, for example by nudging a value slightly, and make sure the test notices and fails.

## Rivals and special rules too

The same comparison runs with each AI rival and with the Daily Challenge variants, since they change speed and behavior.

## Still honest about limits

These checks run on simulated matches. Playing on real phones is a separate round of testing.

## What is next

Claimball is still in testing and coming soon to iOS and Android. There is no release date yet.

## FAQ

### Why does the landing marker have to be accurate?
If the marker said one tile and the game painted another, you would stop trusting it, and the game would feel unfair.

### How do you test the marker?
We play full simulated matches many times over with different random seeds and compare every marker with the tiles that were actually painted. They must agree every time.

### Does the test cover rivals and the Daily Challenge?
Yes. The same comparison runs with each AI rival and with the Daily Challenge variants, since they change speed and behavior. These checks run on simulated matches, and playing on real phones is a separate round of testing.

### Is Claimball released yet?
Not yet. It is still in testing and coming soon to iOS and Android, and there is no release date yet.
