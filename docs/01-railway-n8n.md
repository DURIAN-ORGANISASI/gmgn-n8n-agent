# 01 · Deploy n8n di Railway

Panduan dari nol sampai n8n bisa dibuka di browser. Perkiraan waktu: 10 menit.

**1. Buat akun dan project**

1. Buka [railway.com](https://railway.com) → **Login** (paling mudah dengan akun GitHub).
2. Pilih paket yang tersedia (trial atau berbayar). n8n berjalan 24 jam dan memakai kredit terus-menerus; cek harga dan kredit terbaru di halaman Railway.
3. Di dashboard klik **New Project** → **Deploy a Template**.
4. Ketik `n8n` di kolom pencarian, pilih template **n8n** yang membuat dua service: **Postgres** dan **n8n** (hindari varian dengan worker/Redis kecuali memang butuh). Klik **Deploy**.
5. Tunggu sampai kotak **Postgres** dan **n8n** di canvas berstatus **Online** (bisa beberapa menit pada deploy pertama).

**2. Buka akses publik**

1. Klik kotak **n8n** → tab **Settings** → bagian **Networking**.
2. Klik **Generate Domain** jika belum ada domain. Hasilnya `https://<nama>.up.railway.app`. Salin.

**3. Atur variabel**

1. Di kotak **n8n** buka tab **Variables**. Biarkan variabel bawaan template (database, port, proxy, pembersihan eksekusi) apa adanya.
2. Klik **Raw Editor** dan **tambahkan** baris berikut di bagian bawah (jangan menghapus yang sudah ada):

   ```env
   GENERIC_TIMEZONE=Asia/Jakarta
   TZ=Asia/Jakarta
   ```

3. Cek `WEBHOOK_URL`. Nilainya harus domain dari langkah 2 dengan awalan `https://`. Jika kosong atau berikon peringatan kuning, isi `https://${{RAILWAY_PUBLIC_DOMAIN}}`.
4. Cek `DB_POSTGRESDB_HOST`. Jika berikon peringatan, pastikan nilainya merujuk ke service Postgres di project yang sama (misalnya `${{Postgres.PGHOST}}`).
5. Klik tombol **Deploy** pada banner perubahan dan tunggu proses selesai.

**4. Pastikan data tersimpan permanen (Volume)**

Di canvas, kotak **n8n** harus punya ikon volume (misalnya `n8n-volume-xxxx`) dengan mount path `/home/node/.n8n`. Jika belum ada: klik kanan canvas → **Volume** → hubungkan ke service n8n → mount path `/home/node/.n8n`. Tanpa volume, kunci enkripsi dan pengaturan bisa hilang saat redeploy.

**5. Buat akun owner**

1. Buka domain dari langkah 2. Halaman pembuatan akun owner muncul.
2. Isi email, nama, dan kata sandi kuat, lalu simpan di password manager. Lewati penawaran fitur berbayar bila ada.

**6. Cadangkan kunci enkripsi**

Di kotak **n8n** buka tab **Console**, jalankan `cat /home/node/.n8n/config`, lalu salin nilai `encryptionKey` ke password manager. Tanpa key ini, semua credential tidak bisa dibaca jika data n8n dipulihkan ke instance baru.

> Jangan mengisi `N8N_ENCRYPTION_KEY` dengan nilai acak baru pada n8n yang sudah pernah berjalan. n8n akan menolak start jika nilainya berbeda dengan yang tersimpan.

**7. Pemeriksaan akhir**

- Tab **Deployments → View Logs** menampilkan baris *Editor is now accessible via* dan tidak ada error berulang.
- Zona waktu benar: di n8n, node *Schedule Trigger* atau waktu eksekusi sesuai WIB.

## Jumlah eksekusi

Workflow ini hanya punya dua jadwal harian:

| Trigger | Waktu | Eksekusi per hari |
|---|---|---|
| Mulai 00:01 (AI Agent, memproses perintah yang menumpuk) | sekali sehari | 1 |
| Mulai 07:00 (Scheduler GM dan GN) | sekali sehari | 1 |
| **Total** | | **2 per hari (±60 per bulan)** |

- Jumlahnya sangat kecil, jadi aman untuk n8n self-hosted di Railway maupun kuota n8n Cloud.
- Eksekusi scheduler terlihat "berjalan" berjam-jam karena menunggu jam GN (19:00). Ini normal.
- Jaga ukuran database dengan `EXECUTIONS_DATA_PRUNE=true` (sudah bawaan template).

## Referensi variabel

Biasanya tersedia otomatis (jumlah dan namanya bisa berbeda antar versi template):

`DB_TYPE`, `DB_POSTGRESDB_HOST`, `DB_POSTGRESDB_PORT`, `DB_POSTGRESDB_DATABASE`, `DB_POSTGRESDB_USER`, `DB_POSTGRESDB_PASSWORD`, `EXECUTIONS_DATA_PRUNE`, `EXECUTIONS_DATA_PRUNE_MAX_COUNT`, `N8N_DEFAULT_BINARY_DATA_MODE`, `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS`, `N8N_EXPRESS_TRUST_PROXY`, `N8N_PROXY_HOPS`, `PORT`, `WEBHOOK_URL`.

**Jangan dihapus.** Ikon peringatan kuning di samping variabel (biasanya `DB_POSTGRESDB_HOST` dan `WEBHOOK_URL`) berarti nilainya merujuk ke variabel atau service lain yang perlu dicek:

- `DB_POSTGRESDB_HOST` harus mengarah ke service Postgres di project yang sama, misalnya `${{Postgres.PGHOST}}`.
- `WEBHOOK_URL` harus berisi domain publik dengan awalan `https://`. Buat domain di **Settings > Networking > Generate Domain** jika belum ada.

### Variabel yang perlu kamu tambahkan

| Variabel | Nilai | Alasan |
|---|---|---|
| `GENERIC_TIMEZONE` | `Asia/Jakarta` | Zona waktu workflow |
| `TZ` | `Asia/Jakarta` | Zona waktu proses |

Lihat [`../.env.example`](../.env.example).

### Soal `N8N_ENCRYPTION_KEY`

- Jika n8n **sudah pernah berjalan**, jangan mengisi key acak baru. n8n akan menolak start (*mismatching encryption keys*) jika nilainya berbeda dengan yang tersimpan.
- Ambil key yang sedang dipakai dari tab **Console**: `cat /home/node/.n8n/config`, salin `encryptionKey`, simpan di password manager. Opsional: tambahkan sebagai variabel dengan nilai persis sama sebagai cadangan.

### Riwayat eksekusi

Jangan menaruh `EXECUTIONS_DATA_SAVE_ON_SUCCESS=none` saat pengujian, karena eksekusi yang sukses tidak akan terlihat di tab **Executions**. Pembersihan otomatis (`EXECUTIONS_DATA_PRUNE`) sudah cukup menjaga ukuran database.
