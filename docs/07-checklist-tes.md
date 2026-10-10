# 07 · Checklist tes

Jalankan berurutan. Gunakan **server pribadi** untuk uji coba. Ganti `ID` dengan ID channel tesmu.

## A. Alur otomatis (tanpa AI)

| # | Aksi | Hasil yang benar |
|---|---|---|
| A1 | Execute dari trigger **Tes Manual** | Pesan gm terkirim ke channel aktif, **sama persis untuk semua channel**, baris `Logs` berstatus `TERKIRIM`, bukti masuk ke channel pemantau |
| A2 | Periksa bukti di channel pemantau | Dengan webhook: kartu "Bukti Pengiriman GM" berisi pesan dan satu field per channel (nama server, mention, ID, waktu), warna hijau bila semua terkirim. Tanpa webhook: satu baris teks per entri |
| A2b | Kosongkan `monitor_webhook_url`, ulangi A1 | Bukti tampil sebagai teks polos (cadangan) |
| A2c | Isi `monitor_webhook_url` dengan URL webhook yang salah format | Bukti tampil sebagai teks polos, tidak error |
| A3 | Set `Config.gn_time` = 2 menit dari sekarang, Execute dari **Mulai 07:00** (bukan Tes Manual) | GM terkirim segera ke tiap channel aktif; GN menunggu sampai `gn_time` lalu terkirim |
| A4 | Set `aktif` = FALSE, ulangi A1 | Tidak ada pesan terkirim ke channel itu |
| A5 | Isi `channel_id` tidak valid (5 digit), ulangi A1 | Baris dilewati tanpa error |
| A6 | Dua channel aktif | Keduanya terkirim dengan jeda acak |
| A7 | Dua baris dengan `channel_id` sama | Hanya satu pesan terkirim |
| A8 | Hapus semua baris `gm` di `Messages`, jalankan A1 | Tercatat `GAGAL` dengan keterangan sheet tidak punya pesan bertipe gm |

## B. Perintah AI

Agent diproses sekali sehari pukul 00:01. Untuk tes, ketik perintah lalu jalankan trigger **Tes Manual Perintah** (jalankan sekali dulu untuk mengisi penanda `last_message_id`; run pertama tidak memproses apa pun).

| # | Perintah | Hasil yang benar |
|---|---|---|
| B1 | `!ai lihat daftar channel` | Kartu "Hasil perintah" berisi daftar berformat dan field Perintah (teks polos bila tanpa webhook) |
| B2 | `!ai tampilkan daftar pesan` | Isi `Messages` tampil |
| B3 | `!ai tampilkan bukti pengiriman terakhir` | Maksimal 5 entri |
| B4 | `!ai tambah channel ID` | Tersimpan dengan jam default 07:00 dan 19:00 |
| B5 | `!ai tambah channel ID2 gm jam 7.15` | Jam tersimpan `07:15` |
| B6 | `!ai ubah jam gn channel ID jadi 21:30` | Hanya `gn_time` berubah |
| B7 | `!ai stop channel ID` lalu `!ai aktifkan lagi channel ID` | `aktif` FALSE lalu TRUE, baris tidak terhapus |
| B8 | `!ai tambah pesan gm "gm legends" bobot 8` | Baris baru di `Messages` |
| B9 | `!ai kirim gm sekarang ke ID` | Terkirim, balasan memuat bukti satu baris, baris `manual` di `Logs` |
| B10 | Tambah 3 ID dalam satu pesan | Tiga channel tersimpan, hasil dikelompokkan |

## C. Penolakan dan keamanan

| # | Aksi | Hasil yang benar |
|---|---|---|
| C1 | `!ai tambah channel 12345` | Ditolak (ID tidak valid), tidak disimpan |
| C2 | `!ai tambah channel 111111111111111111` (ID karangan 18 digit) | Ditolak, channel tidak ditemukan |
| C3 | `!ai tambah channel ID gm jam 25:99` | Ditolak atau ditanyakan ulang |
| C4 | Tambah ID yang sudah ada | Tidak ada baris ganda |
| C5 | Ketik `lihat daftar channel` tanpa `!ai` | Tidak ada respons |
| C6 | User lain mengetik `!ai lihat daftar channel` | Diabaikan |
| C7 | `!ai hapus semua channel` | Tidak ada baris yang terhapus (hanya dinonaktifkan atau agent bertanya) |

## D. Ketahanan

| # | Aksi | Hasil yang benar |
|---|---|---|
| D1 | Dua perintah `!ai` berurutan, lalu **Tes Manual Perintah** | Keduanya dibalas, berurutan |
| D2 | `!ai tolong matikan channel ID dulu` | Dipahami sebagai stop |
| D3 | Ketik 3 perintah `!ai` di jam berbeda, **Publish**, biarkan lewat 00:01 | Ketiganya dibalas berurutan setelah 00:01, `last_message_id` bergerak, tidak ada balasan ganda keesokan harinya |
| D4 | Buka tab **Executions** | Eksekusi tercatat, tidak ada node merah yang berulang |

Catat hasil tes yang gagal bersama: nomor tes, teks balasan di Discord, dan node yang merah di n8n. Lampirkan ke issue.

Setelah selesai, nonaktifkan channel tes di sheet agar tidak ikut terkirim.
