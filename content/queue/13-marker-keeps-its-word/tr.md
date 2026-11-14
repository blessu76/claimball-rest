---
title: Düşüş işaretçisinin doğru söylediğini nasıl denetliyoruz
description: Düşüş işaretçisi ancak doğruysa işe yarar. Gerçekten boyanan karelerle örtüştüğünü nasıl test ettiğimizi anlatıyoruz.
summary: Claimball düşüş işaretçisi ancak doğruysa işe yarar; bu yüzden gerçekten boyanan karelerle örtüştüğünü test ediyoruz. Farklı rastgele tohumlarla çok sayıda tam simüle maç oynatıp her işaretçiyi sonuçla karşılaştırıyor, testin başarısız olduğunu doğrulamak için kuralı bilerek bozuyoruz. Hâlâ test aşamasında; yakında iOS ve Android'de.
slug: marker-keeps-its-word
lang: tr
category: devlog
translation_of: en
keywords: Claimball, düşüş işaretçisi, test, adil oyun, günlük
copy_review: iris 2026-11-14
---
Düşüş işaretçisi topun nereye ineceğini gösterir; bu yüzden her seferinde doğru olmak zorundadır. Bu, henüz herkese açık olmayan TestFlight iç test sürümlerinde şöyle test ediliyor.

## Ekranda verilmiş bir söz

İşaretçi bir kareyi gösterip oyun başka bir kareyi boyasaydı ona güvenmeyi bırakırdın ve oyun haksız hissettirirdi. Bu yüzden işaretçinin gerçekte olanla örtüşmesi gerekir.

## İkisi için tek kural

İşaretçi ile gerçek vuruşun uyuşması amaçlanır. Bunu, farklı rastgele tohumlarla defalarca tam simüle maç oynatıp her işaretçiyi gerçekten boyanan karelerle karşılaştırarak denetliyoruz. Her seferinde uyuşmak zorundalar.

## Denetimi denetlemek

Hiç başarısız olmayan bir test pek bir şey kanıtlamaz. Bu yüzden kuralı bilerek bozuyoruz, örneğin bir değeri hafifçe kaydırıyoruz ve testin bunu fark edip başarısız olduğundan emin oluyoruz.

## Rakiplerde ve özel kurallarda da

Aynı karşılaştırma her yapay zekâ rakiple ve Günlük meydan okuma varyantlarıyla da çalışır; çünkü bunlar hızı ve davranışı değiştirir.

## Sınırlar konusunda hâlâ dürüstüz

Bu denetimler simüle maçlarda çalışıyor. Gerçek telefonlarda oynamak ayrı bir test turu.

## Sırada ne var

Claimball hâlâ test aşamasında ve yakında iOS ve Android'de. Henüz bir çıkış tarihi yok.

## Sık sorulan sorular

### Düşüş işaretçisi neden doğru olmak zorunda?
İşaretçi bir kareyi gösterip oyun başka bir kareyi boyasaydı ona güvenmeyi bırakırdın ve oyun haksız hissettirirdi.

### İşaretçiyi nasıl test ediyorsunuz?
Farklı rastgele tohumlarla defalarca tam simüle maç oynatıyor ve her işaretçiyi gerçekten boyanan karelerle karşılaştırıyoruz. Her seferinde uyuşmak zorundalar.

### Test rakipleri ve Günlük meydan okumayı da kapsıyor mu?
Evet. Aynı karşılaştırma her yapay zekâ rakiple ve Günlük meydan okuma varyantlarıyla da çalışır; çünkü bunlar hızı ve davranışı değiştirir. Bu denetimler simüle maçlarda çalışıyor; gerçek telefonlarda oynamak ayrı bir test turu.

### Claimball yayınlandı mı?
Henüz değil. Hâlâ test aşamasında ve yakında iOS ve Android'de; henüz bir çıkış tarihi yok.
