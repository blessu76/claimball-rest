---
title: Bagaimana pertandingan seri berakhir di Claimball
description: Dulu seri berakhir dengan hasil yang membingungkan. Begini cara kerja sudden death sekarang, dan apa yang berubah di build uji terbaru.
summary: Di Claimball, pertandingan seri masuk ke sudden death, tempat poin berikutnya menentukan. Pemain yang mencetak poin penentu mengambil satu petak dari rival jika perlu, sehingga papan menunjukkan 30 lawan 28, bukan 29 lawan 29, dan layar hasil selalu cocok dengan angka akhir.
slug: sudden-death-and-draws
lang: id
category: devlog
translation_of: en
keywords: Claimball, sudden death, seri, game kasual, jurnal
published: 2026-11-03T21:05+09:00
---
Satu pertandingan Claimball berlangsung 90 detik di atas kisi buku catatan, dan biasanya satu pihak sudah menguasai lebih banyak wilayah saat waktu habis. Tulisan ini membahas kasus lainnya: pertandingan berakhir imbang.

## Apa yang terjadi saat seri

Saat waktu habis dengan jumlah petak yang sama, pertandingan masuk ke sudden death. Waktu berhenti dan poin berikutnya menentukan pertandingan. Jika masih ada bola di udara pada detik ke-90, pertandingan menunggu bola itu mendarat sebelum dihitung.

## Bug yang kami perbaiki

Di build uji kami, sudden death bisa berakhir dengan jumlah petak yang masih sama, misalnya 29 lawan 29, sementara layar hasil menyatakan kamu kalah. Pemenangnya ditentukan dengan benar, tetapi angka di layar tidak menunjukkannya, sehingga terasa janggal.

Awalnya kami membuat hasil seperti itu tampil sebagai seri. Lalu kami memutuskan bahwa sudden death tidak boleh terlihat seperti seri: pemain yang mencetak poin penentu sekarang mengambil satu petak dari rival jika perlu, sehingga papan menunjukkan 30 lawan 28, bukan 29 lawan 29. Layar hasil selalu sesuai dengan angka akhir.

## Juga di build uji terbaru

Logo dan angka Kombo maks kini tetap berurutan dengan benar di bahasa yang ditulis dari kanan ke kiri seperti Arab, dan halaman Catatan Rilis di situs web mencantumkan apa yang berubah di setiap build.

## Selanjutnya

Claimball masih dalam tahap uji dan segera hadir di iOS dan Android. Belum ada tanggal rilis.

## FAQ

### Apa yang terjadi saat pertandingan Claimball berakhir seri?
Saat waktu habis dengan jumlah petak yang sama, pertandingan masuk ke sudden death. Waktu berhenti dan poin berikutnya menentukan pertandingan.

### Bagaimana jika bola masih di udara pada detik ke-90?
Pertandingan menunggu bola mendarat sebelum dihitung.

### Bisakah sudden death berakhir tampak seperti seri?
Tidak. Pemain yang mencetak poin penentu sekarang mengambil satu petak dari rival jika perlu, sehingga papan menunjukkan 30 lawan 28, bukan 29 lawan 29.

### Apakah Claimball sudah dirilis?
Belum. Masih dalam tahap uji dan segera hadir di iOS dan Android, dan belum ada tanggal rilis.
