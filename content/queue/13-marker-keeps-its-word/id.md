---
title: Cara kami memastikan penanda pendaratan berkata jujur
description: Penanda pendaratan hanya berguna jika benar. Begini cara kami menguji bahwa penanda itu menunjukkan petak yang benar-benar terwarnai.
summary: Penanda pendaratan Claimball hanya membantu jika benar, jadi kami menguji bahwa penanda itu cocok dengan petak yang benar-benar terwarnai. Kami memainkan banyak pertandingan simulasi penuh dengan seed acak yang berbeda dan membandingkan setiap penanda dengan hasilnya, dan kami juga sengaja merusak aturan untuk memastikan pengujian itu gagal. Game ini masih dalam pengujian dan segera hadir di iOS dan Android.
slug: marker-keeps-its-word
lang: id
category: devlog
translation_of: en
keywords: Claimball, penanda pendaratan, pengujian, permainan adil, jurnal
---
Penanda pendaratan menunjukkan di mana bola akan mendarat, jadi harus benar setiap kali. Begini cara mengujinya di build uji coba internal TestFlight, yang belum dirilis untuk umum.

## Janji di layar

Jika penanda menunjuk satu petak dan game mewarnai petak lain, kamu akan berhenti memercayainya, dan game terasa tidak adil. Jadi penanda harus sesuai dengan apa yang benar-benar terjadi.

## Satu aturan untuk keduanya

Penanda dan pukulan sungguhan seharusnya sama. Kami memeriksanya dengan memainkan pertandingan simulasi penuh, berkali-kali dengan seed acak yang berbeda, dan membandingkan setiap penanda dengan petak yang benar-benar terwarnai. Keduanya harus sama setiap kali.

## Menguji pengujian

Pengujian yang tidak pernah gagal tidak membuktikan banyak hal. Jadi kami juga sengaja merusak aturan, misalnya menggeser sebuah nilai sedikit, dan memastikan pengujian itu menyadarinya dan gagal.

## Rival dan aturan khusus juga

Perbandingan yang sama dijalankan dengan setiap rival AI dan dengan varian Tantangan Harian, karena semuanya mengubah kecepatan dan perilaku.

## Jujur soal batasan

Pemeriksaan ini dijalankan pada pertandingan simulasi. Bermain di ponsel sungguhan adalah putaran pengujian yang terpisah.

## Selanjutnya

Claimball masih dalam pengujian dan segera hadir di iOS dan Android. Belum ada tanggal rilis.

## Tanya jawab

### Mengapa penanda pendaratan harus akurat?
Jika penanda menunjuk satu petak dan game mewarnai petak lain, kamu akan berhenti memercayainya, dan game terasa tidak adil.

### Bagaimana kalian menguji penanda?
Kami memainkan pertandingan simulasi penuh berkali-kali dengan seed acak yang berbeda dan membandingkan setiap penanda dengan petak yang benar-benar terwarnai. Keduanya harus sama setiap kali.

### Apakah pengujian mencakup rival dan Tantangan Harian?
Ya. Perbandingan yang sama dijalankan dengan setiap rival AI dan dengan varian Tantangan Harian, karena semuanya mengubah kecepatan dan perilaku. Pemeriksaan ini dijalankan pada pertandingan simulasi, dan bermain di ponsel sungguhan adalah putaran pengujian yang terpisah.

### Apakah Claimball sudah dirilis?
Belum. Game ini masih dalam pengujian dan segera hadir di iOS dan Android, dan belum ada tanggal rilis.
