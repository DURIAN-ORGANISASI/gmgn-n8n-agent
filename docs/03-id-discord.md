# 03 · Mengambil ID Discord

## Aktifkan Developer Mode

**User Settings > Advanced > Developer Mode = ON.** Setelah itu klik kanan apa pun dan pilih **Copy ID**.

## ID yang dibutuhkan

| ID | Cara mengambil | Dipakai untuk |
|---|---|---|
| Channel pemantau | Klik kanan channel > Copy Channel ID | `Config.monitor_channel_id` |
| URL webhook channel pemantau (opsional) | Edit Channel > Integrations > Webhooks > New Webhook > Copy Webhook URL | `Config.monitor_webhook_url` ([11](11-webhook-embed.md)) |
| User ID kamu | Klik kanan nama/profilmu > Copy User ID | `Config.admin_user_id` |
| Channel target | Klik kanan channel > Copy Channel ID | `Channels.channel_id` |

Nama server dan nama channel **tidak perlu dicatat**. Keduanya diambil otomatis dari Discord memakai ID channel.

## Cara cepat mendapatkan ID channel lewat chat

Setelah sistem berjalan, kamu cukup menempel ID, mention `<#ID>`, atau link channel (`https://discord.com/channels/<SERVER>/<CHANNEL>`) ke perintah `!ai tambah channel ...`. Agent mengambil angka channel dari link tersebut.

## Syarat channel target

- Akun/bot yang dipakai harus anggota server dan punya izin **Send Messages** di channel itu.
- Channel khusus (misalnya hanya untuk pengumuman) akan menghasilkan error `403` di sheet `Logs`.
- Slowmode atau aturan server tertentu bisa menolak pengiriman terjadwal.
