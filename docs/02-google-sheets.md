# 02 · Google Sheets dan Service Account

n8n membaca dan menulis sheet lewat **Service Account**. Cara ini tidak memakai OAuth, jadi tidak ada token yang kedaluwarsa.

## A. Siapkan spreadsheet

1. Buka Google Sheets, **File > Import > Upload** [`sheets/gmgn-sheet-template.xlsx`](../sheets/gmgn-sheet-template.xlsx), pilih **Create new spreadsheet**.
2. **File > Save as Google Sheets**. Wajib. Jika judul masih berlabel `.XLSX`, n8n menolak dengan pesan *The document must not be an Office file*. Gunakan file hasil salinan (ID-nya berbeda dari file Excel).
3. Cek format kolom: **Format > Number > Plain text** untuk `Channels!A:A` (channel_id), `Channels!C:D` (jam), `Config!B:B`, `Logs!D:D` dan `Logs!G:G`.
4. Isi sheet **Config**:

| key | value |
|---|---|
| `monitor_channel_id` | ID channel tempat kamu memberi perintah dan menerima bukti |
| `admin_user_id` | ID user Discord kamu |
| `monitor_webhook_url` | (Opsional, disarankan) URL webhook channel pemantau agar bukti dan balasan tampil sebagai kartu embed. Lihat [11](11-webhook-embed.md). Kosongkan untuk teks polos |
| `timezone` | `Asia/Jakarta` (atau `Asia/Makassar`, `Asia/Jayapura`) |
| `gn_time` | Jam GN universal untuk semua channel, format `HH:mm` (default `19:00`) |
| `min_delay_sec` / `max_delay_sec` | Rentang jeda acak antar channel, detik (jaga maksimum di bawah 60) |
| `last_message_id` | **Kosongkan.** Diisi otomatis (diawali huruf `m`) |

5. Sheet **Channels**: ganti baris contoh dengan channel aslimu, atau biarkan kosong lalu tambahkan lewat `!ai`. Scheduler harian saat ini mengirim GM saat workflow mulai (07:00) dan GN pada `Config.gn_time`; kolom `gm_time` / `gn_time` di sheet ini dicatat sebagai referensi.
6. Salin **ID spreadsheet** dari URL: `https://docs.google.com/spreadsheets/d/`**`<ID>`**`/edit`.

Aturan nama: jangan ubah nama sheet maupun nama kolom, karena workflow memakai nama persis ini.

## B. Buat Service Account

1. Buka [Google Cloud Console](https://console.cloud.google.com), buat project (nama bebas).
2. **APIs & Services > Library** → aktifkan **Google Sheets API**.
3. **APIs & Services > Credentials > Create credentials > Service account**, beri nama, selesai.
4. Buka service account itu → tab **Keys > Add key > Create new key > JSON**. File JSON terunduh. **Simpan di luar repo.**
5. Dari file JSON, salin `client_email` (bentuk `nama@project.iam.gserviceaccount.com`).

## C. Bagikan sheet ke Service Account

Di Google Sheet: **Share** → tempel `client_email` → peran **Editor** → Send.

Setiap kali kamu membuat salinan baru file sheet (misalnya hasil *Save as Google Sheets*), share ulang ke email itu. Izin tidak ikut tersalin.

## D. Cek cepat

| Gejala di n8n | Penyebab |
|---|---|
| `Bad request ... must not be an Office file` | File masih .xlsx, lakukan Save as Google Sheets |
| `Forbidden ... caller does not have permission` | Belum di-share ke Service Account, atau ID spreadsheet salah |
| `Requested entity was not found` | ID spreadsheet salah |
| Node membaca data tapi ID berubah menjadi `1.23E+17` | Kolom ID berformat Number |
