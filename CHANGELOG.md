# Changelog

Format mengikuti [Keep a Changelog](https://keepachangelog.com/id/1.1.0/) dan [Semantic Versioning](https://semver.org/lang/id/).

## [2.0.0] - 2026-10-09

Versi pertama berbasis n8n (menggantikan bot Python `gmgn-bot`).

### Ditambahkan
- Satu workflow n8n dengan dua alur: Scheduler GM/GN dan AI Agent perintah `!ai`.
- Penyimpanan konfigurasi di Google Sheets (`Config`, `Channels`, `Messages`, `Logs`).
- Scheduler harian (cron 07:00): GM dikirim saat workflow mulai, GN pada `Config.gn_time` (default 19:00), zona waktu dari `Config`.
- Satu pesan GM dan satu pesan GN (acak berbobot) dipakai sama untuk semua channel pada hari itu.
- Tampilan kartu (embed) untuk bukti pengiriman dan balasan agent lewat `Config.monitor_webhook_url`; tanpa webhook otomatis kembali ke teks polos. Dokumentasi: `docs/11-webhook-embed.md`.
- AI Agent berjalan sekali sehari pukul 00:01 (cron) memproses perintah yang menumpuk; trigger **Tes Manual Perintah** untuk pengujian. Agent mencoba ulang saat error dan membalas pesan error, bukan berhenti diam-diam.
- Nama server dan channel diambil otomatis dari Discord (tanpa kolom label atau guild_id).
- Bukti pengiriman ke channel pemantau (satu baris per entri: server, mention channel, ID, tipe, waktu, teks pesan di akhir) dan ke sheet `Logs`. Kolom `link` tidak dipakai.
- Tambah banyak channel sekaligus (ID, `<#ID>`, atau link channel), dengan verifikasi pasca-simpan.
- Validasi ID channel ke Discord sebelum disimpan.
- Trigger **Tes Manual** untuk menguji pengiriman tanpa menunggu jam.
- Skrip `set_sheet_id.py`, `validate_workflow.py`, `make_template.py` dan CI validasi.
- Dokumentasi lengkap di `docs/` dan diagram di `assets/`.

### Catatan
- Kolom `gm_time` / `gn_time` per channel di sheet `Channels` disimpan sebagai referensi dan belum dibaca scheduler harian.

### Keamanan
- Hanya `admin_user_id` dengan awalan `!ai` yang diproses; agent tidak punya tool hapus.
- Penanda pembacaan pesan disimpan dengan awalan `m` agar ID 19 digit tidak dibulatkan oleh Sheets.
