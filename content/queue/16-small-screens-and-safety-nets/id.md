---
title: Ponsel kecil, teks besar, dan jaring pengaman
description: Sebelum melangkah lebih jauh, kami memeriksa layar Claimball di ponsel sempit dengan teks besar, dan menambahkan jaring pengaman agar satu berkas bermasalah tidak menghentikan aplikasi.
summary: Sebelum melangkah lebih jauh, kami memeriksa layar menu, statistik, dan peringkat Claimball di ponsel sempit dengan teks diperbesar 50 persen, dalam bahasa Inggris, Arab, dan Korea. Kami juga menambahkan penjaga kesalahan global dan nilai cadangan yang aman, sehingga aplikasi tetap terbuka jika satu item tersimpan tidak bisa dibaca. Masih dalam tahap pengujian dan segera hadir di iOS dan Android.
slug: small-screens-and-safety-nets
lang: id
category: devlog
translation_of: en
keywords: Claimball, aksesibilitas, layar kecil, keandalan, jurnal
---
Game yang terbuka dengan buruk atau teksnya terpotong tidak menyenangkan, sebagus apa pun aturannya. Ini adalah satu putaran pemeriksaan pada build uji internal TestFlight, yang belum dirilis ke publik.

## Layar sempit, teks besar

Kami menguji menu, layar statistik, dan layar peringkat pada lebar ponsel yang sempit dengan teks diperbesar 50 persen, dalam bahasa Inggris, Arab, dan Korea, dan memastikan tidak ada yang meluap atau bertumpuk.

## Jaring pengaman untuk kesalahan

Jika ada hal tak terduga yang salah, penjaga kesalahan global menangkapnya alih-alih membiarkan aplikasi jatuh.

## Tetap terbuka meski data simpanan tidak terbaca

Jika satu item tersimpan tidak bisa dibaca saat dimulai, game beralih ke nilai bawaan yang aman untuk item itu dan tetap terbuka, alih-alih berhenti di layar kosong.

## Terjemahan

Pemeriksaan terjemahan berjalan pada setiap build dan menandai teks yang hilang atau rusak. Terjemahannya sendiri dibuat dengan AI dan belum ditinjau oleh penutur asli.

## Selanjutnya

Claimball masih dalam tahap pengujian dan segera hadir di iOS dan Android. Belum ada tanggal rilis.

## FAQ

### Bagaimana kalian memeriksa layar kecil dan teks besar?
Kami menguji menu, layar statistik, dan layar peringkat pada lebar ponsel yang sempit dengan teks diperbesar 50 persen, dalam bahasa Inggris, Arab, dan Korea, dan memastikan tidak ada yang meluap atau bertumpuk.

### Bagaimana jika ada yang salah di aplikasi?
Jika ada hal tak terduga yang salah, penjaga kesalahan global menangkapnya alih-alih membiarkan aplikasi jatuh. Jika satu item tersimpan tidak bisa dibaca saat dimulai, game beralih ke nilai bawaan yang aman untuk item itu dan tetap terbuka.

### Apakah terjemahannya sudah ditinjau?
Pemeriksaan terjemahan berjalan pada setiap build dan menandai teks yang hilang atau rusak. Terjemahannya sendiri dibuat dengan AI dan belum ditinjau oleh penutur asli.

### Apakah Claimball sudah dirilis?
Belum. Masih dalam tahap pengujian dan segera hadir di iOS dan Android, dan belum ada tanggal rilis.
