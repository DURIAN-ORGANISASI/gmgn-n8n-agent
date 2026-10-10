# 10 · Migrasi dari bot Python (`gmgn-bot`)

Versi awal proyek ini adalah bot Python (`gmgn-bot`) yang berjalan terus-menerus dengan token akun pengguna. Versi n8n menggantikannya.

## Perbandingan

| Aspek | `gmgn-bot` (Python) | `gmgn-n8n-agent` |
|---|---|---|
| Proses | Skrip Python yang berjalan terus-menerus | Workflow n8n (dua jadwal harian) |
| Konfigurasi | Berkas konfigurasi di server (`config.json`) | Google Sheets, bisa diubah tanpa deploy |
| Pesan | Daftar pesan dengan kelangkaan (*rarity*) di kode | Sheet `Messages` dengan kolom `bobot` |
| Kontrol | Lewat kode dan perintah bot | `!ai ...` dipahami AI Agent |
| Bukti kirim | - | Sheet `Logs` + ringkasan di channel pemantau |
| Jam per channel | - | `gm_time` dan `gn_time` per baris channel |

Kolom bertanda `-` adalah fitur yang dijamin ada di versi n8n; cek `gmgn-bot` sendiri untuk perilaku lama.

## Langkah migrasi

1. Catat channel dan jam dari konfigurasi bot lama.
2. Isi sheet `Channels` (`channel_id`, `aktif`, `gm_time`, `gn_time`). Alternatifnya, tempel semua ID sekaligus lewat `!ai tambah channel ...`.
3. Pindahkan daftar pesan ke sheet `Messages`. Kelangkaan (*rarity*) di kode lama dipetakan ke kolom `bobot`: makin umum, makin besar bobotnya.
4. Selesaikan [pengaturan](00-mulai-cepat.md) dan tes di server pribadi.
5. **Hentikan service bot lama** (stop atau remove di Railway) sebelum Publish workflow, supaya tidak ada pengiriman ganda.
6. Setelah stabil beberapa hari, arsipkan repo lama atau tandai sebagai *legacy*.

## Catatan token

Jika bot lama memakai token akun pengguna, pertimbangkan beralih ke bot resmi (lihat [04](04-credentials.md)). Ganti token akun lama jika pernah tersimpan di tempat yang tidak aman.
