# 11 · Tampilan kartu (embed) lewat webhook

Bukti pengiriman dan balasan agent bisa tampil sebagai **kartu (embed)** Discord yang rapi: bergaris warna di sisi kiri, berjudul, dan field tersusun dalam kolom. Tanpa pengaturan ini, pesan tetap terkirim sebagai teks polos.

## Kenapa perlu webhook

Embed hanya bisa dikirim oleh **bot** atau **webhook**. Sepengetahuanku, Discord tidak menampilkan embed yang dikirim memakai token akun pengguna, jadi pesan semacam itu tidak akan tampil sebagai kartu. Webhook tidak memerlukan bot atau token akun, cukup sebuah URL, dan cocok karena bukti serta balasan selalu dikirim ke **channel pemantau milikmu sendiri**.

Webhook hanya dipakai untuk pesan ke channel pemantau. Pengiriman GM/GN ke channel target tetap memakai credential Discord seperti sebelumnya.

## Cara membuat webhook

1. Di Discord, klik kanan **channel pemantau** → **Edit Channel** (Pengaturan Channel).
2. Menu **Integrations** → **Webhooks** → **New Webhook**.
3. Beri nama (misalnya `GM/GN Agent`), pastikan channel tujuannya benar, lalu klik **Copy Webhook URL**.
4. Buka Google Sheet → sheet **Config** → baris `monitor_webhook_url` → tempel URL di kolom `value`. Jika barisnya belum ada, tambahkan baris baru: `key` = `monitor_webhook_url`, `value` = URL webhook.
5. Selesai. Tidak ada perubahan lain di n8n. Jalankan **Tes Manual** atau **Tes Manual Perintah** untuk melihat hasilnya.

> Kamu butuh izin **Manage Webhooks** di channel itu. Di server milikmu sendiri, izin ini ada.

## Tampilan

### Bukti pengiriman

Satu kartu per tipe (GM dan GN), pesan yang dikirim di bagian atas, dan satu field per channel:

| Bagian | Isi |
|---|---|
| Judul | `☀️ Bukti Pengiriman GM` atau `🌙 Bukti Pengiriman GN` |
| Deskripsi | Teks pesan yang dikirim (sama untuk semua channel) |
| Field per channel | `✅/❌ Nama Server`, mention channel yang bisa diklik, ID, waktu kirim, dan error bila ada |
| Warna sisi | Hijau = semua terkirim, kuning = sebagian, merah = semua gagal |
| Footer | `N dari M terkirim • GM/GN Agent` + waktu |

Jika ada lebih dari 24 channel per tipe, kartu dipecah otomatis. Jika total melebihi batas Discord (10 embed dan sekitar 6.000 karakter per pesan), bukti dikirim dalam beberapa pesan.

### Balasan agent

Satu kartu biru berjudul `🤖 Hasil perintah` berisi jawaban agent, dengan field **Perintah** yang menampilkan perintah `!ai` yang diproses. Jika perintah gagal, kartunya merah berjudul `⚠️ Perintah gagal diproses` beserta alasannya. Jawaban panjang dibagi ke beberapa kartu bernomor.

Karena webhook tidak bisa membalas (*reply*) ke pesan tertentu, kartu tidak lagi tersambung ke pesan perintahmu. Perintah yang diproses ditampilkan di field **Perintah**.

## Tanpa webhook (cadangan)

Jika `monitor_webhook_url` kosong atau bukan URL webhook Discord yang valid, workflow otomatis memakai cara lama: teks polos lewat credential Discord, dengan balasan berupa *reply* ke pesan perintah.

## Keamanan

- URL webhook bekerja seperti kata sandi: siapa pun yang memegangnya bisa mengirim pesan ke channel itu. Simpan hanya di sheet `Config` yang privat dan jangan menempelkannya di chat, issue, atau repo. Validator di repo menolak URL webhook yang ikut ter-commit.
- Jika URL bocor: hapus webhook di pengaturan channel, buat yang baru, dan perbarui `Config`.
- Webhook hanya bisa **mengirim** ke satu channel. Ia tidak bisa membaca pesan atau mengakses channel lain.

## Pemecahan masalah

| Gejala | Penyebab | Solusi |
|---|---|---|
| Bukti masih teks polos | `monitor_webhook_url` kosong atau salah format | Salin ulang URL lewat **Copy Webhook URL** (bentuk `https://discord.com/api/webhooks/<angka>/<token>`) |
| Node *Kirim Bukti* / *Balas* gagal dengan `404` | Webhook sudah dihapus | Buat webhook baru, perbarui `Config` |
| Gagal dengan `429` | Terlalu banyak pesan beruntun ke satu webhook | Otomatis dicoba ulang 3 kali; kurangi jumlah channel per hari bila sering terjadi |
| Gagal dengan `400` | Isi embed melebihi batas Discord | Laporkan sebagai issue beserta jumlah channel dan panjang jawaban |
| Kartu tampil tapi nama pengirim aneh | Nama webhook diatur di Discord | Ubah nama/ikon webhook di pengaturan channel |
