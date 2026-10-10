# Kontribusi

Terima kasih sudah ingin membantu. Panduan singkat:

## Alur kerja

1. Fork repo, buat branch: `git checkout -b fitur/nama-singkat`.
2. Ubah workflow di n8n, lalu **Export** dan simpan ke `workflows/gmgn-ai-agent.json`.
3. **Sanitasi sebelum commit** (wajib):
   - Ganti semua ID spreadsheet menjadi `GANTI_SHEET_ID`.
   - Kosongkan `id` pada setiap blok `credentials` (nama boleh tetap).
   - Pastikan tidak ada token, API key, atau ID pribadi (channel, user, server) di file mana pun.
4. Jalankan pemeriksaan:
   ```bash
   pip install -r requirements.txt
   python scripts/validate_workflow.py
   python scripts/make_template.py   # jika menyentuh sheets/csv
   ```
5. Perbarui `CHANGELOG.md` dan dokumen terkait di `docs/`.
6. Buka Pull Request memakai template yang tersedia.

## Gaya

- Dokumentasi dalam Bahasa Indonesia, kalimat singkat, contoh nyata.
- Nama node memakai Bahasa Indonesia seperti yang sudah ada.
- Kode di node Code: JavaScript polos, beri komentar untuk keputusan yang tidak jelas.
- Jangan menambah dependensi ke skrip kecuali perlu.

## Perubahan yang diterima dengan senang hati

Perbaikan bug, dokumentasi, contoh konfigurasi, tes tambahan di checklist, dan dukungan model AI lain. Untuk perubahan besar (misalnya mengganti tempat perintah ke platform lain), buka issue diskusi dulu.
