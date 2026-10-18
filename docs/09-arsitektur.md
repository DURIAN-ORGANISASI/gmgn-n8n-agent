# 09 · Arsitektur

<div align="center">
<img src="../assets/architecture-map.id.svg" alt="Arsitektur" width="900"/>
</div>

Satu workflow, dua alur, satu sumber data (Google Sheets). Tidak ada state tersembunyi di n8n, kecuali penanda pembacaan pesan yang juga disimpan di sheet `Config`. Kedua alur berjalan sekali sehari: perintah pukul 00:01, pengiriman GM pukul 07:00 dan GN pukul 19:00.

## Alur 1: Scheduler (tanpa AI)

Trigger **Mulai 07:00 (sekali sehari)** memakai ekspresi cron `0 7 * * *` (mengikuti `GENERIC_TIMEZONE`). Satu eksekusi menyusun seluruh pengiriman hari itu, lalu menunggu sampai tiap pengiriman jatuh tempo.

| Node | Tipe | Fungsi |
|---|---|---|
| Mulai 07:00 (sekali sehari) | Schedule Trigger (cron) | Memulai alur tiap hari. GM dikirim pada saat ini |
| Tes Manual | Manual Trigger | Memaksa kirim `gm` ke semua channel aktif (pengujian) |
| Get Config / Get Messages / Get Channels | Google Sheets (read) | Membaca pengaturan, pesan, dan channel |
| Susun Pengiriman Hari Ini | Code | Memilih **satu pesan GM dan satu pesan GN** (acak berbobot) yang dipakai sama untuk semua channel. Membuat antrean: tiap channel aktif dan valid mendapat satu item GM (waktu = sekarang) dan satu item GN (waktu = `Config.gn_time`, default 19:00). GN yang jamnya sudah lewat dilewati. Menghitung jeda acak, membuang ID tidak valid dan baris ganda, mengurutkan: semua GM dulu, lalu GN |
| Loop Over Items | Split In Batches (1) | Memproses item satu per satu |
| Tunggu Jam Kirim | Wait | Menunggu sampai waktu item (GM: langsung, GN: sampai `gn_time`) |
| Wait Acak | Wait | Jeda acak (detik) antar pengiriman |
| Info Channel | HTTP GET `/channels/{id}` | Nama channel dan `guild_id` |
| Info Server | HTTP GET `/guilds/{id}` | Nama server |
| Kirim ke Discord | HTTP POST `/channels/{id}/messages` | Mengirim pesan |
| Susun Log | Code | Menyusun baris log (status, nama server dan channel, error) |
| Simpan Log | Google Sheets (append) | Menulis ke `Logs`. Tidak menghentikan alur bila gagal |
| Teruskan Data | Code | Membawa data kirim apa adanya dan menandai kegagalan simpan log |
| Rangkum Bukti | Code | Menyusun bukti. Jika `Config.monitor_webhook_url` valid: kartu embed per tipe (GM/GN) dengan satu field per channel; jika tidak: teks polos satu baris per entri. Dipecah ke beberapa pesan bila melebihi batas Discord (10 embed, sekitar 6.000 karakter) |
| Kirim Bukti ke Channel Pemantau | HTTP POST | Mengirim ke URL webhook, atau ke API channel pemantau bila webhook tidak diisi. Mencoba ulang 3 kali bila gagal |

Keputusan desain:

- **Tanpa AI** untuk jadwal: perilaku deterministik, murah, dan tidak terpengaruh limit model.
- **Satu eksekusi per hari** menekan jumlah eksekusi n8n (lihat tabel kuota). Konsekuensinya, eksekusi itu tetap "berjalan" selama menunggu GN dan disimpan di database oleh n8n, sehingga tahan restart selama database dan volume utuh.
- **Jam GM = jam mulai cron.** Mengubah jam GM berarti mengubah ekspresi cron di node trigger. **Jam GN universal** berada di `Config.gn_time`. Kolom `gm_time` / `gn_time` per channel di sheet `Channels` saat ini tidak dibaca scheduler.
- **Pesan sama untuk semua channel.** Pemilihan acak berbobot (`bobot` di `Messages`, nilai kosong atau tidak valid dianggap 1) dilakukan sekali per tipe per hari, bukan per channel. Yang acak antar channel hanya jeda waktu kirim.
- **Jam dinormalisasi**: `7.15`, `07:15`, `07:15:00`, dan `7:15 AM` dibaca sama.
- **Pesan kosong**: jika `Messages` tidak punya pesan untuk suatu tipe, entri tetap diteruskan dan tercatat `GAGAL` dengan keterangan jelas.
- **Kegagalan satu channel** tidak menghentikan channel lain (respons HTTP error tidak melempar exception).
- **Kelemahan yang diketahui**: jika n8n mati tepat pada 07:00, pengiriman hari itu terlewat dan tidak dikejar; GN yang jamnya sudah lewat saat workflow mulai juga dilewati.

## Alur 2: AI Agent

Trigger **Mulai 00:01 (proses perintah)** memakai cron `1 0 * * *`. Perintah yang kamu ketik sepanjang hari menumpuk di channel pemantau dan diproses sekaligus saat trigger ini jalan. Trigger **Tes Manual Perintah** menjalankan alur yang sama kapan saja untuk pengujian.

| Node | Fungsi |
|---|---|
| Get Config1 → Siapkan Polling | Membaca `monitor_channel_id`, `admin_user_id`, `last_message_id` |
| Ambil Pesan Baru | `GET /channels/{monitor}/messages?after=<last_id>` (maksimal 100 pesan, batas Discord; pada run pertama hanya 1 pesan untuk mengambil penanda) |
| Ambil Perintah | Menyaring pesan: penulis = `admin_user_id` dan awalan `!ai`. Diurutkan dari yang terlama |
| Cari ID Terbaru → Simpan Cursor | Menyimpan ID pesan terbaru ke `Config.last_message_id` (diawali `m`) |
| AI Agent GM/GN | Memahami perintah, memanggil tool. Mencoba ulang sampai 3 kali bila model error, dan bila tetap gagal tidak menghentikan perintah berikutnya |
| Susun Balasan | Menyusun balasan: kartu embed biru berjudul "Hasil perintah" dengan field Perintah (kartu merah bila gagal), atau teks polos bila webhook tidak diisi. Jawaban panjang dipecah ke beberapa kartu |
| Balas ke Channel Pemantau | Mengirim ke URL webhook, atau sebagai *reply* ke pesan perintah (diawali 🤖) bila webhook tidak diisi. Mencoba ulang 3 kali |

**Tool** yang tersedia untuk agent:

| Tool | Jenis | Fungsi |
|---|---|---|
| `lihat_channel`, `tambah_channel`, `ubah_channel` | Google Sheets | Membaca, menambah, dan mengubah `Channels` (tambah memakai *append or update* berdasarkan `channel_id`) |
| `lihat_pesan`, `tambah_pesan` | Google Sheets | Membaca dan menambah `Messages` |
| `lihat_log`, `tambah_log` | Google Sheets | Membaca `Logs` dan mencatat pengiriman manual |
| `info_channel`, `info_server` | HTTP GET | Validasi channel serta nama channel dan server |
| `kirim_sekarang` | HTTP POST | Kirim pesan manual |

Keputusan desain:

- **Batch harian, bukan real-time.** n8n tidak mempertahankan koneksi WebSocket Discord, jadi pesan dibaca lewat REST sekali sehari. Konsekuensinya balasan baru muncul setelah 00:01, dan jumlah eksekusi n8n sangat kecil.
- **Perintah diproses berurutan** dari yang terlama, satu per satu, sehingga penulisan ke sheet tidak saling menimpa.
- **Penanda disimpan dengan awalan `m`** (`m1558...`) agar Google Sheets tidak mengubah ID 19 digit menjadi angka dan membulatkannya. Kode membuang semua karakter non-digit saat membaca.
- **Run pertama aman**: jika `last_message_id` kosong, tidak ada perintah yang diproses; hanya penanda yang disimpan, jadi riwayat lama tidak dieksekusi.
- **Filter ganda**: awalan `!ai` dan `admin_user_id`. Balasan sistem berawalan 🤖 tidak lolos filter, sehingga tidak ada loop.
- **Penghapusan tidak tersedia**: agent hanya menonaktifkan channel. Ini membatasi dampak kesalahan model.
- **Penambahan banyak channel** dilakukan satu per satu (tidak paralel) agar penulisan ke sheet tidak saling menimpa, lalu diverifikasi dengan membaca ulang sheet.
- `maxIterations` agent diset 60 agar perintah dengan banyak channel tidak terpotong.

## Kuota dan beban

| Sumber | Perkiraan |
|---|---|
| Google Sheets API (baca) | Alur 1: 3 baca per hari; Alur 2: 1 baca per hari, ditambah baca/tulis tool saat memproses perintah. Jauh di bawah batas bawaan per pengguna per menit |
| Discord REST | 1 request baca per hari untuk perintah + pengiriman sesuai jumlah channel. Jeda acak mengurangi risiko rate limit |
| Model AI | Hanya saat ada perintah. Sekitar 2-5 request per perintah, beruntun pada 00:01. Jika kuota per menit kecil, retry otomatis membantu; perintah sangat banyak sebaiknya dipecah ke beberapa hari |
| Eksekusi n8n | 2 per hari (satu per alur), sekitar 60 per bulan |

## Model ancaman singkat

| Risiko | Mitigasi |
|---|---|
| Orang lain memberi perintah | Hanya `admin_user_id` + awalan `!ai` |
| Model mengarang ID | Validasi `info_channel` sebelum simpan; aturan di system prompt |
| Kebocoran token | Hanya di Credentials n8n; CI memeriksa pola rahasia di repo |
| Kehilangan data akibat model | Tidak ada tool hapus; semua perubahan terlihat di sheet |
| Perintah gagal diproses | Penanda disimpan sebelum agent berjalan, jadi perintah yang gagal tidak diulang otomatis; balasan error muncul di channel pemantau dan perintah bisa diketik ulang |
| Pengiriman ganda | Satu run per hari, dedup baris `channel_id`, satu workflow aktif |
