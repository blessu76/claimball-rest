---
title: Loop pertandingan pindah ke mesin game
description: Animasi papan pertandingan sekarang berjalan di mesin game, dan pertandingan dijeda saat kamu keluar dari aplikasi.
summary: Kami memindahkan loop animasi papan pertandingan utama ke mesin game Flame, sehingga pewaktuannya diatur di satu tempat. Gamenya tetap berjalan seperti sebelumnya. Jika kamu keluar dari aplikasi saat pertandingan berlangsung, pertandingan dijeda dan menunggu kamu menekan Lanjut. Game ini masih dalam pengujian dan segera hadir untuk iOS dan Android.
slug: match-loop-and-pause
lang: id
category: devlog
translation_of: en
keywords: Claimball, mesin game, jeda, pertandingan, jurnal
---
Pemain tidak melihat aturan baru di sini. Ini perubahan di dalam yang membuat papan pertandingan tetap stabil.

## Satu loop untuk papan

Animasi papan dulu berjalan dengan timer sendiri. Sekarang berjalan di mesin game Flame, yang mengatur bingkai papan dari satu tempat.

## Keluar dari aplikasi, kembali dalam keadaan jeda

Jika ada panggilan masuk, notifikasi muncul, atau kamu pindah ke aplikasi lain, pertandingan dijeda. Saat kembali, tekan Lanjut untuk meneruskan. Selama kamu pergi, tidak ada yang bergerak.

## Gamenya sama

Skor, aturan, penyimpanan, dan pembelian tidak berubah. Papan terlihat dan dimainkan seperti sebelumnya.

## Masih diuji

Kami masih memeriksa loop baru ini di ponsel sungguhan.

## Yang berikutnya

Claimball masih dalam pengujian dan segera hadir untuk iOS dan Android. Belum ada tanggal rilis.

## Pertanyaan umum

### Apakah aturannya berubah?
Tidak. Skor, aturan, penyimpanan, dan pembelian tetap sama. Yang berubah hanya cara animasi papan dijalankan.

### Apa yang terjadi jika saya keluar saat pertandingan?
Pertandingan dijeda. Tekan Lanjut saat kamu kembali.

### Apakah Claimball sudah dirilis?
Belum. Game ini masih dalam pengujian dan segera hadir untuk iOS dan Android, dan belum ada tanggal rilis.
