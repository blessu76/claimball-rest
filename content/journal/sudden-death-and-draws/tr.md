---
title: Claimball'da berabere biten bir maç nasıl sona erer
description: Beraberlik eskiden kafa karıştıran bir sonuçla bitiyordu. Ani ölüm şimdi nasıl işliyor ve son test derlemelerinde ne değişti.
summary: Claimball'da berabere biten bir maç ani ölüme gider ve bir sonraki sayı maçı belirler. Belirleyici sayıyı atan oyuncu gerekirse rakipten bir karo alır; böylece tahta 29-29 yerine 30-28 gösterir ve sonuç ekranı her zaman son sayılarla uyumlu olur.
slug: sudden-death-and-draws
lang: tr
category: devlog
translation_of: en
keywords: Claimball, ani ölüm, beraberlik, rahat oyun, günlük
published: 2026-11-03T21:05+09:00
copy_review: iris 2026-11-14
---
Bir Claimball maçı defter ızgarasında 90 saniye sürer ve çoğu zaman süre dolduğunda bir taraf daha fazla araziye sahip olur. Bu yazı diğer durumla ilgili: maç berabere bitiyor.

## Beraberlikte ne olur

Süre dolduğunda karo sayıları eşitse maç ani ölüme gider. Süre durur ve bir sonraki sayı maçı belirler. 90. saniyede top hâlâ havadaysa maç, sayılmadan önce topun yere inmesini bekler.

## Düzelttiğimiz hata

Test derlemelerimizde ani ölüm, karo sayıları hâlâ eşitken (örneğin 29'a 29) bitebiliyor, sonuç ekranı ise kaybettiğini söylüyordu. Kazanan doğru belirleniyordu ama ekrandaki sayılar bunu göstermiyordu, bu yüzden yanlış hissettiriyordu.

Önce böyle bir sonucu beraberlik olarak gösterdik. Sonra ani ölümün asla beraberlik gibi görünmemesine karar verdik: belirleyici sayıyı atan oyuncu gerekirse rakipten bir karo alıyor, böylece tahta 29'a 29 yerine 30'a 28 gösteriyor. Sonuç ekranı artık her zaman son sayılarla uyumlu.

## Son test derlemelerinde ayrıca

Logo ve Maks kombo sayısı, Arapça gibi sağdan sola yazılan dillerde artık doğru sırasını koruyor ve web sitesinin Sürüm notları sayfası her derlemede nelerin değiştiğini listeliyor.

## Sırada ne var

Claimball hâlâ test aşamasında ve iOS ile Android için çok yakında geliyor. Henüz bir çıkış tarihi yok.

## Sık sorulan sorular

### Bir Claimball maçı berabere bitince ne olur?
Süre dolduğunda karo sayıları eşitse maç ani ölüme gider. Süre durur ve bir sonraki sayı maçı belirler.

### 90. saniyede top hâlâ havadaysa ne olur?
Maç, sayılmadan önce topun yere inmesini bekler.

### Ani ölüm berabere gibi görünerek bitebilir mi?
Hayır. Belirleyici sayıyı atan oyuncu artık gerekirse rakipten bir karo alır; böylece tahta 29-29 yerine 30-28 gösterir.

### Claimball çıktı mı?
Henüz değil. Claimball hâlâ test aşamasında ve iOS ile Android için çok yakında geliyor; henüz bir çıkış tarihi yok.
