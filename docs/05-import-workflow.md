# 05 · Import workflow

## 1. Tanam ID spreadsheet

Workflow di repo memakai placeholder `GANTI_SHEET_ID` supaya tidak ada ID pribadi di Git. Ganti dengan skrip:

```bash
python scripts/set_sheet_id.py "https://docs.google.com/spreadsheets/d/<ID_SPREADSHEET>/edit"
# atau cukup ID-nya:
python scripts/set_sheet_id.py <ID_SPREADSHEET>
```

Hasilnya `dist/gmgn-ai-agent.json` (folder `dist/` diabaikan Git). Tanpa Python: buka `workflows/gmgn-ai-agent.json` di editor teks, Find & Replace `GANTI_SHEET_ID` dengan ID-mu, simpan sebagai file lain.

## 2. Import di n8n

1. **Workflows > ⋯ (kanan atas) > Import from file** → pilih `dist/gmgn-ai-agent.json`.
2. Satu workflow berisi dua alur. Alur scheduler ada di bagian atas canvas, alur AI Agent di bagian bawah.

## 3. Pasang credential di tiap node

Node yang menampilkan peringatan credential perlu dipilihkan credential-nya:

| Jenis node | Credential |
|---|---|
| Semua node Google Sheets (termasuk 7 tool di bawah AI Agent) | Google Service Account (GM/GN) |
| Semua node HTTP Request (termasuk tool `info_channel`, `info_server`, `kirim_sekarang`) | Discord User Token (Header Auth) |
| Google Gemini Chat Model | Google Gemini(PaLM) Api |

Jika node Google Sheets menampilkan peringatan pada kolom *Sheet*, buka dropdown dan pilih ulang sheet yang sesuai (Config, Channels, Messages, atau Logs).

## 4. Tes sebelum Publish

Ikuti [07 · Checklist tes](07-checklist-tes.md). Minimal:

1. Jalankan dari trigger **Tes Manual** (klik panah di samping *Execute workflow* dan pilih trigger itu). Harus terkirim "gm" ke channel aktif, muncul baris di `Logs`, dan bukti masuk ke channel pemantau.
2. Ketik `!ai lihat daftar channel`, lalu jalankan dari **Tes Manual Perintah**. Balasan harus muncul. (Pada operasi normal perintah diproses otomatis pukul 00:01.)

## 5. Publish

Tekan **Publish** (di versi n8n lama: toggle **Active**). Hanya workflow yang dipublish yang dijalankan otomatis oleh trigger jadwal. Menekan *Execute workflow* hanya menjalankan sekali.

## Pembaruan workflow

1. `git pull`, jalankan ulang `set_sheet_id.py`.
2. Import hasilnya sebagai workflow baru, tes, lalu nonaktifkan yang lama. Hindari dua workflow aktif bersamaan karena bisa menghasilkan pengiriman ganda.
3. Jika struktur sheet berubah, lihat [CHANGELOG](../CHANGELOG.md).
