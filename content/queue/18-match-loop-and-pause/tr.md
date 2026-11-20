---
title: Maç döngüsü bir oyun motoruna taşındı
description: Maç tahtasının animasyonu artık bir oyun motorunda çalışıyor ve uygulamadan çıkınca maç duraklatılıyor.
summary: Ana maç tahtasının animasyon döngüsünü Flame oyun motoruna taşıdık, böylece zamanlaması tek bir yerde yönetiliyor. Oyun eskisi gibi oynanıyor. Bir maç sırasında uygulamadan çıkarsanız maç duraklatılır ve Devam düğmesine basmanızı bekler. Oyun hâlâ test aşamasında ve yakında iOS ve Android için gelecek.
slug: match-loop-and-pause
lang: tr
category: devlog
translation_of: en
keywords: Claimball, oyun motoru, duraklatma, maç, günlük
copy_review: iris 2026-11-20
---
Oyuncular burada yeni bir kural görmeyecek. Bu, tahtanın istikrarlı kalmasını sağlayan içeride yapılmış bir değişiklik.

## Tahta için tek döngü

Tahtanın animasyonu eskiden kendi zamanlayıcısında çalışıyordu. Artık Flame oyun motorunda çalışıyor ve tahtanın karelerini tek bir yerden yönetiyor.

## Uygulamadan çıkınca maç duraklar

Bir arama gelirse, bildirim çıkarsa veya başka bir uygulamaya geçerseniz maç duraklatılır. Geri döndüğünüzde kaldığınız yerden devam etmek için Devam düğmesine basın. Siz uzaktayken hiçbir şey hareket etmez.

## Aynı oyun

Puan, kurallar, kayıtlar ve satın almalar değişmedi. Tahta eskisi gibi görünüyor ve eskisi gibi oynanıyor.

## Hâlâ test ediliyor

Yeni döngüyü gerçek telefonlarda kontrol etmeye devam ediyoruz.

## Sırada ne var

Claimball hâlâ test aşamasında ve yakında iOS ve Android için gelecek. Henüz bir yayın tarihi yok.

## Sık sorulan sorular

### Kurallar değişti mi?
Hayır. Puan, kurallar, kayıtlar ve satın almalar aynı kaldı. Yalnızca tahtanın animasyonunun nasıl çalıştığı taşındı.

### Maç sırasında çıkarsam ne olur?
Maç duraklatılır. Geri döndüğünüzde Devam düğmesine basın.

### Claimball yayınlandı mı?
Henüz değil. Test aşamasında ve yakında iOS ve Android için gelecek, ama henüz bir yayın tarihi yok.
