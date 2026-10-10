# 00 · Mulai cepat

Ringkasan satu halaman. Detail tiap langkah ada di dokumen bernomor berikutnya.

## Prasyarat

| Kebutuhan | Keterangan |
|---|---|
| n8n self-hosted | Panduan Railway di [01](01-railway-n8n.md) |
| Akun Google | Untuk Google Sheets dan Service Account |
| Akun Discord | Dengan akses ke channel pemantau dan channel target |
| API key model AI | Gemini (default) atau Groq |
| Python 3.9+ | Hanya untuk skrip bantu di `scripts/` (opsional) |

## Urutan kerja

```text
1. Deploy n8n di Railway ............................ docs/01
2. Salin ID: channel pemantau, user kamu, channel target ... docs/03
3. Import template sheet -> Save as Google Sheets .... docs/02
4. Service Account + share sheet; buat 3 credential .. docs/02, docs/04
   (opsional) webhook channel pemantau untuk tampilan kartu .. docs/11
5. python scripts/set_sheet_id.py <URL_SHEET> ........ docs/05
6. Import dist/gmgn-ai-agent.json, pilih credential .. docs/05
7. Tes (Tes Manual, lalu perintah !ai) ............... docs/07
8. Publish workflow ................................... docs/05
```

## Hasil akhir yang diharapkan

1. Pada jam yang diatur di sheet `Channels`, bot mengirim GM/GN ke tiap channel dengan jeda acak.
2. Ringkasan bukti muncul di channel pemantau, dan baris baru muncul di sheet `Logs`.
3. Kamu bisa mengetik `!ai lihat daftar channel` di channel pemantau dan mendapat daftar lengkap dengan nama server dan channel.

## Jebakan yang paling sering terjadi

- File sheet masih **.xlsx** (pesan error: *must not be an Office file*) → **Save as Google Sheets**.
- Sheet belum dibagikan ke email Service Account (pesan error: *Forbidden*).
- Kolom ID berformat angka sehingga ID dibulatkan → set **Plain text**.
- Workflow belum **Published** sehingga jadwal tidak jalan sendiri.
- Zona waktu server masih UTC → set `GENERIC_TIMEZONE` dan `TZ`.
