# 08 · Pemecahan masalah

## Google Sheets

| Pesan / gejala | Penyebab | Solusi |
|---|---|---|
| `Bad request ... This operation is not supported for this document. The document must not be an Office file` | File sheet masih format Excel | **File > Save as Google Sheets**, pakai ID file baru, share ulang ke Service Account |
| `Forbidden - perhaps check your credentials? The caller does not have permission` | Sheet belum di-share ke Service Account, atau ID salah | Share sebagai **Editor** ke `client_email`; cocokkan ID di node dengan URL |
| `Requested entity was not found` | ID spreadsheet salah | Jalankan ulang `set_sheet_id.py` dengan ID yang benar |
| Aktivasi API | Sheets API belum aktif di project Google Cloud | Aktifkan di APIs & Services > Library |
| Channel ID berubah jadi `1.23E+17` | Kolom berformat Number | Set Plain text, ketik ulang ID |
| Baris `Logs` tidak bertambah | Header `Logs` tidak sama | Samakan 9 header: `waktu, server, nama_channel, channel_id, tipe, pesan, message_id, status, error` (kolom `link` sudah dihapus; hapus manual jika masih ada) |
| Sheet berisi baris ganda untuk satu channel | Penambahan manual atau race lama | Hapus baris ganda manual. Pengiriman tetap hanya sekali per channel |

## Discord

| Pesan / gejala | Penyebab | Solusi |
|---|---|---|
| `HTTP 401` di `Logs` | Token salah atau kedaluwarsa | Perbarui credential `Discord User Token` |
| `HTTP 403` | Tidak punya izin kirim/baca di channel | Cek izin channel dan keanggotaan server |
| `HTTP 404` pada Info Channel | ID salah atau akun tidak punya akses | Periksa ID; nama server akan tertulis `(server tidak diketahui)` |
| `HTTP 429` | Terlalu cepat / rate limit | Naikkan `min_delay_sec` dan `max_delay_sec`, kurangi jumlah channel per menit |
| Bukti tidak muncul di channel pemantau | `monitor_channel_id` salah atau tidak ada izin kirim | Periksa `Config` |
| Mention `<#ID>` tampil sebagai teks mentah | Akun tidak punya akses ke channel itu | Normal; ID tetap tertulis di sebelahnya |

## Jadwal

| Gejala | Penyebab | Solusi |
|---|---|---|
| Tidak terkirim sendiri | Workflow belum **Published**, atau n8n mati pada jam mulai (07:00) | Tekan Publish; pastikan service n8n tidak tidur |
| Jam bergeser beberapa jam | Zona waktu server UTC | Set `GENERIC_TIMEZONE` dan `TZ`; cek `Config.timezone` |
| GM terkirim tapi GN tidak | Jam GN hari ini sudah lewat saat workflow mulai, atau `Config.gn_time` bukan `HH:mm` | Perbaiki `gn_time`; GN yang terlewat tidak dikejar |
| Channel tidak ikut terkirim | `aktif` bukan `TRUE`, ID bukan 17-20 digit, atau baris ganda | Perbaiki sel di sheet |
| Execute manual tidak mengirim | Tidak ada channel aktif yang valid (output *Susun Pengiriman Hari Ini* kosong) | Cek sheet `Channels`; gunakan trigger **Tes Manual** |
| Eksekusi scheduler terlihat "berjalan" berjam-jam | Normal: node *Tunggu Jam Kirim* menunggu `gn_time` | Tunggu; eksekusi tersimpan di database dan lanjut sendiri |
| "Node was not executed" pada *Loop Over Items* | Tidak ada item yang diteruskan | Bukan error, lihat baris di atas |
| Executions kosong | `EXECUTIONS_DATA_SAVE_ON_SUCCESS=none` | Hapus variabel itu |

## Kartu embed / webhook

Lihat tabel pemecahan masalah di [11 · Tampilan kartu (embed)](11-webhook-embed.md#pemecahan-masalah).

## AI Agent

| Gejala | Penyebab | Solusi |
|---|---|---|
| `404 ... model is no longer available` | Model Gemini sudah dipensiunkan | Pilih model terbaru di dropdown node *Google Gemini Chat Model* |
| `429 / quota exceeded` | Batas kuota model | Tunggu reset, atau ganti model/penyedia |
| Badge merah di Chat Model | Credential model belum dipilih | Buka node, pilih credential |
| Agent tidak memanggil tool / jawaban berantakan | Model terlalu kecil | Ganti ke model yang lebih besar |
| Balasan muncul dua kali | Dua workflow aktif bersamaan | Nonaktifkan salah satu |
| Agent tidak merespons | Belum lewat 00:01 (perintah diproses sekali sehari), tidak berawalan `!ai`, `admin_user_id` salah, atau workflow belum Published | Tunggu 00:01, atau jalankan **Tes Manual Perintah**; periksa `Config` dan status Publish |
| Balasan berisi "Perintah gagal diproses" | Model/kuota error setelah 3 percobaan | Lihat tab Executions; ganti model atau ulangi perintahnya besok / via Tes Manual Perintah |
| Perintah lama diproses ulang | `last_message_id` terhapus | Biarkan satu run mengisi ulang; run pertama hanya menyimpan penanda |
| Perintah yang gagal tidak diulang | Penanda sudah maju sebelum perintah diproses | Ketik ulang perintahnya |
| `Max iterations` tercapai | Perintah sangat besar (banyak channel) | Pecah perintah menjadi beberapa pesan |

## Cara melaporkan masalah

Sertakan: versi n8n, model AI yang dipakai, nomor tes di [07](07-checklist-tes.md), teks error di node yang merah, dan baris `Logs` yang relevan. **Hapus token dan ID pribadi dari lampiran.**
