---
title: 透過 iCloud 在其他裝置上繼續遊玩
description: 你的進度、星星、成就與無障礙設定，會在 iPhone 與 iPad 上跟著你的 iCloud 帳號走。以下說明哪些會同步、哪些不會。
slug: continue-with-icloud
lang: zh-Hant
category: devlog
translation_of: en
keywords: Claimball, iCloud, 跨裝置繼續遊玩, 休閒遊戲, 日誌
published: 2026-11-09T18:00+09:00
---
第 7 版是 TestFlight 內部測試版，讓你可以在另一台裝置上接續上次的進度。目前尚未對外正式發布。

## 會跟著 iCloud 帳號走的內容

在 iPhone 與 iPad 上，你的進度、星星、成就、免費試玩狀態與無障礙設定，都會跟著你的 iCloud 帳號走，並在背景默默完成同步。如果 iCloud 已關閉或處於離線狀態，遊戲就只會在裝置上保留自己的副本。

## 只留在裝置上的內容

有些內容刻意不透過 iCloud 共享：完整解鎖的購買項目（由 App Store 負責記錄）、每日挑戰的嘗試次數，以及震動與音效設定。

## 購買時的謹慎處理

如果購買項目被退款，或透過「家人共享」被收回，遊戲就會重新上鎖。不過在你登出或離線時，遊戲會小心避免誤鎖。

## 接下來

Claimball 仍在測試中，即將登陸 iOS 與 Android，目前尚無上市日期。每個版本都列在[版本說明](/releases/)頁面。
