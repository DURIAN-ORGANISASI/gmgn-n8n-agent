<div align="center">

<img src="assets/brand.svg" alt="GM/GN n8n Agent" width="84" height="84">

# GM/GN AI Agent for n8n

<p>
  <img src="https://img.shields.io/badge/n8n-self--hosted-FF6D5A?style=flat&logo=n8n&logoColor=white" alt="n8n self-hosted">
  <img src="https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=flat&logo=railway&logoColor=white" alt="Railway">
  <img src="https://img.shields.io/badge/Data-Google%20Sheets-188038?style=flat&logo=googlesheets&logoColor=white" alt="Google Sheets">
  <img src="https://img.shields.io/badge/Discord-REST%20API-5865F2?style=flat&logo=discord&logoColor=white" alt="Discord REST API">
  <img src="https://img.shields.io/badge/AI-Gemini%20%7C%20Groq-6688FF?style=flat" alt="Gemini or Groq">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-2DAD87?style=flat" alt="MIT License"></a>
</p>

<p><strong>Automatiskan pesan Good Morning dan Good Night ke banyak channel Discord.</strong><br>
Jadwal deterministik di n8n, konfigurasi di Google Sheets, dan perintah administrasi melalui chat.</p>

<p><a href="README.md">🇮🇩 Bahasa Indonesia</a> · <a href="README.en.md">🇬🇧 English</a></p>

<p>
  <a href="#-fitur">Fitur</a> ·
  <a href="#-cara-kerja">Arsitektur</a> ·
  <a href="#-mulai-cepat">Mulai cepat</a> ·
  <a href="#-instalasi-di-railway">Deploy Railway</a> ·
  <a href="#-setup-credential">Credential</a> ·
  <a href="#-perintah">Perintah</a> ·
  <a href="#-keamanan-dan-disclaimer">Keamanan</a> ·
  <a href="#-faq">FAQ</a>
</p>

</div>
---

> [!WARNING]
> **Baca dulu: risiko Terms of Service Discord.** Versi awal proyek ini ([`gmgn-bot`](https://github.com/akndrn000/gmgn-bot)) memakai *token akun pengguna* (self-bot). Itu melanggar ToS Discord dan akun bisa diblokir. Workflow di repo ini memakai Discord REST API dengan credential **Header Auth** yang kamu isi sendiri. Kamu bebas mengisinya dengan `Bot <token>` untuk bot resmi (sangat disarankan jika bot bisa diundang ke channel target). Pakai token akun pribadi sepenuhnya risiko kamu sendiri. Detail di [Keamanan dan disclaimer](#-keamanan-dan-disclaimer).

![Ilustrasi alur GM/GN AI Agent](assets/hero.id.svg)

## ✨ Fitur

- **Jadwal harian otomatis.** Workflow mulai tiap hari pukul 07:00 (cron, mengikuti zona waktu n8n). GM dikirim saat itu juga ke semua channel aktif, GN dikirim pada jam universal `gn_time` di sheet `Config` (default 19:00). Zona waktu bisa diatur (WIB, WITA, WIT).
- **Satu pesan untuk semua channel.** Setiap hari satu pesan GM dan satu pesan GN dipilih acak (berbobot) dari sheet `Messages` ("gm", "gm all", "gm buddy", dan variasi lain), lalu dipakai **sama** untuk semua channel terdaftar. Semua pesan bisa kamu ubah atau tambah.
- **Kontrol lewat chat dengan AI Agent.** Ketik `!ai ...` di channel pemantau. Agent memahami bahasa sehari-hari: tambah channel, matikan channel, tambah pesan, kirim manual. Perintah dikumpulkan sepanjang hari dan diproses **sekali sehari pukul 00:01**, balasannya muncul setelah itu.
- **Tambah banyak channel sekaligus.** Tempel beberapa ID, mention `<#ID>`, atau link `discord.com/channels/...` dalam satu pesan.
- **Bukti pengiriman otomatis.** Setiap pengiriman dicatat ke sheet `Logs` dan dikirim ke channel pemantau.
- **Tampilan kartu (embed).** Dengan satu URL webhook di sheet `Config`, bukti dan balasan agent tampil sebagai kartu Discord yang rapi: judul, warna status (hijau/kuning/merah), dan field per channel berisi nama server, mention channel yang bisa diklik, ID, serta waktu. Tanpa webhook, tampil sebagai teks polos satu baris per entri. Lihat [`docs/11`](docs/11-webhook-embed.md).
- **Nama server dan channel otomatis.** Cukup simpan ID channel. Nama server dan channel selalu diambil langsung dari Discord.
- **Jadwal deterministik.** Pengiriman terjadwal dijalankan kode biasa tanpa AI, jadi tidak bergantung pada tebakan model. AI hanya dipakai untuk memahami perintahmu.
- **Aman dari kirim ganda.** Satu run per menit dan baris channel ganda di sheet otomatis dilewati.
- **Validasi ID channel.** Agent memeriksa channel ke Discord sebelum menyimpan, sehingga ID karangan model tidak masuk ke sheet.
- **Jeda acak antar channel.** Rentang jeda (detik) diatur di sheet `Config`.
- **Ganti model AI dengan mudah.** Default Gemini Flash-Lite. Bisa diganti Groq (Llama) atau model lain yang mendukung tool calling.

## 📸 Tampilan

<div align="center">
<img src="assets/discord-preview.id.svg" alt="Ilustrasi tampilan di Discord" width="760"/>
<br/><sub>Ilustrasi kartu embed dengan nama server dan ID fiktif. Tampilan asli dapat sedikit berbeda.</sub>
</div>

## 🧠 Cara kerja

<div align="center">
<img src="assets/architecture-map.id.svg" alt="Arsitektur sistem" width="900"/>
</div>

Satu workflow n8n berisi dua alur yang saling bebas:

| Alur | Trigger | Pakai AI? | Tugas |
|---|---|---|---|
| **1. Scheduler** | Cron `0 7 * * *` (sekali sehari, node *Mulai 07:00*) | Tidak | Menyusun antrean pengiriman hari ini dari `Config`, `Channels`, `Messages`; GM langsung, GN menunggu `gn_time`; mencatat ke `Logs`; mengirim bukti ke channel pemantau |
| **2. AI Agent** | Cron `1 0 * * *` (sekali sehari, node *Mulai 00:01*) | Ya | Membaca semua pesan `!ai` yang menumpuk sejak kemarin di channel pemantau, memanggil tool (Sheets dan Discord), lalu membalas satu per satu |
| *Tes Manual* | Manual | Tidak | Memaksa kirim "gm" ke semua channel aktif sekarang juga, untuk pengujian |
| *Tes Manual Perintah* | Manual | Ya | Memproses perintah `!ai` yang sudah ada sekarang juga, tanpa menunggu 00:01 |

Alur 2 memanggil model AI hanya untuk perintah `!ai` yang menumpuk. Membaca pesan tidak memakai AI, jadi kuota gratis model cukup untuk pemakaian normal.

![Diagram scheduler harian](assets/scheduler-flow.id.svg)

Detail teknis tiap node ada di [`docs/09-arsitektur.md`](docs/09-arsitektur.md).

## 🚀 Mulai cepat

Prasyarat: n8n self-hosted (panduan Railway tersedia), akun Google, akun Discord, dan API key model AI (Gemini atau Groq).

1. **Deploy n8n** di Railway → [panduan di bawah](#-instalasi-di-railway) · [`docs/01`](docs/01-railway-n8n.md)
2. **Kumpulkan ID Discord** (channel pemantau, ID user kamu, channel target) → [`docs/03-id-discord.md`](docs/03-id-discord.md)
3. **Siapkan Google Sheet** dari template → [`docs/02-google-sheets.md`](docs/02-google-sheets.md)
4. **Buat credential di n8n** (Google Service Account, Discord Header Auth, Gemini/Groq) → [panduan di bawah](#-setup-credential) · [`docs/04`](docs/04-credentials.md)
5. *(Opsional, disarankan)* **Webhook channel pemantau** agar bukti dan balasan tampil sebagai kartu → [`docs/11-webhook-embed.md`](docs/11-webhook-embed.md)
6. **Import workflow** → [`docs/05-import-workflow.md`](docs/05-import-workflow.md)
7. **Tes** dengan checklist → [`docs/07-checklist-tes.md`](docs/07-checklist-tes.md), lalu **Publish** workflow.

Ringkasan perintah untuk langkah 5:

```bash
git clone https://github.com/akndrn000/gmgn-n8n-agent.git
cd gmgn-n8n-agent

# 1) tanam ID spreadsheet-mu ke workflow (hasil di dist/, tidak ikut ter-commit)
python scripts/set_sheet_id.py "https://docs.google.com/spreadsheets/d/<ID_SPREADSHEET>/edit"

# 2) import dist/gmgn-ai-agent.json di n8n: Workflows > ... > Import from file
```

Panduan satu halaman ada di [`docs/00-mulai-cepat.md`](docs/00-mulai-cepat.md).

## 🚂 Instalasi di Railway

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

### Jumlah eksekusi

Workflow ini hanya punya dua jadwal harian:

| Trigger | Waktu | Eksekusi per hari |
|---|---|---|
| Mulai 00:01 (AI Agent, memproses perintah yang menumpuk) | sekali sehari | 1 |
| Mulai 07:00 (Scheduler GM dan GN) | sekali sehari | 1 |
| **Total** | | **2 per hari (±60 per bulan)** |

- Jumlahnya sangat kecil, jadi aman untuk n8n self-hosted di Railway maupun kuota n8n Cloud.
- Eksekusi scheduler terlihat "berjalan" berjam-jam karena menunggu jam GN (19:00). Ini normal.
- Jaga ukuran database dengan `EXECUTIONS_DATA_PRUNE=true` (sudah bawaan template).

Detail dan variabel lain: [`docs/01-railway-n8n.md`](docs/01-railway-n8n.md).

## 🔑 Setup credential

Workflow memakai empat jenis credential. Peta lengkapnya:

<div align="center">
<img src="assets/credentials-map.id.svg" alt="Peta credential ke node" width="860"/>
</div>

Cara membuat credential di n8n (berlaku untuk semuanya): menu kiri **Overview** (atau **Credentials**) → tombol **Create** → **Create Credential** → cari jenisnya → isi field → **Save**. Beri nama persis seperti di bawah supaya mudah dikenali saat memilihnya di node.

### 1. Google Service Account (akses ke Google Sheets)

**A. Buat Service Account di Google Cloud**

1. Buka [console.cloud.google.com](https://console.cloud.google.com) → pilih atau buat **project** baru.
2. Menu **APIs & Services → Library** → cari **Google Sheets API** → **Enable**.
3. Menu **APIs & Services → Credentials → Create credentials → Service account**. Isi nama (bebas) → **Create and continue** → lewati langkah peran → **Done**.
4. Klik service account yang baru dibuat → tab **Keys → Add key → Create new key → JSON → Create**. File `.json` terunduh. **Simpan di luar repo dan jangan dibagikan.**
5. Buka file JSON dengan editor teks. Kamu butuh dua nilai: `client_email` dan `private_key`.

**B. Bagikan Google Sheet ke Service Account**

Buka Google Sheet → **Share** → tempel `client_email` → peran **Editor** → **Send**. Ulangi bila kamu membuat salinan sheet baru.

**C. Isi credential di n8n**

| Field | Isi |
|---|---|
| Jenis | **Google Service Account API** |
| Nama credential | `Google Service Account (GM/GN)` |
| Region | Global |
| Service Account Email | nilai `client_email` |
| Private Key | nilai `private_key`, salin utuh dari `-----BEGIN PRIVATE KEY-----` sampai `-----END PRIVATE KEY-----` |
| Impersonate a User, Set up for use in HTTP Request node | biarkan mati |

Banner hijau *Connection tested successfully* hanya membuktikan key valid. Akses ke sheet tertentu baru terbukti saat node membaca sheet.

### 2. Discord (Header Auth)

| Field | Isi |
|---|---|
| Jenis | **Header Auth** |
| Nama credential | `Discord User Token` (ganti `Discord Bot Token` bila memakai bot resmi) |
| Name | `Authorization` |
| Value | lihat pilihan di bawah |

**Pilihan A: bot resmi (disarankan, sesuai ToS)**

1. Buka [discord.com/developers/applications](https://discord.com/developers/applications) → **New Application** → beri nama.
2. Menu **Bot** → **Reset Token** → salin token (hanya tampil sekali).
3. Masih di menu **Bot**, aktifkan **Message Content Intent**. Tanpa ini, isi pesan perintah `!ai` terbaca kosong.
4. Menu **OAuth2 → URL Generator**: centang scope `bot`, lalu izin **View Channels**, **Send Messages**, **Read Message History**. Buka URL yang dihasilkan untuk mengundang bot ke server.
5. Isi **Value** dengan `Bot <token>` (kata `Bot`, spasi, token).
6. Bot hanya bisa mengirim ke server tempat ia diundang. Jika channel target ada di server orang lain yang tidak mengizinkan bot, pilihan A tidak bisa dipakai.

**Pilihan B: token akun pengguna (melanggar ToS Discord, risiko ban)**

Isi **Value** dengan token yang sama dengan `DISCORD_USER_TOKEN` di bot lama, **tanpa** awalan `Bot`. Gunakan akun cadangan bila memungkinkan dan jangan pernah membagikan token.

### 3. Model AI

**Gemini (default)**

1. Buka [aistudio.google.com/apikey](https://aistudio.google.com/apikey) → **Create API key** → salin.
2. n8n: jenis **Google Gemini(PaLM) Api** → isi **API Key**, **Host** biarkan default → Save.
3. Di node **Google Gemini Chat Model**, pilih credential tersebut dan pilih model dari dropdown. Workflow memakai `models/gemini-3.5-flash-lite`. Jika muncul error `404 ... model is no longer available`, pilih model Flash/Flash-Lite terbaru yang ada di dropdown.

**Groq (alternatif)**

1. Buka [console.groq.com/keys](https://console.groq.com/keys) → **Create API Key** → salin.
2. n8n: jenis **Groq** → isi **API Key** → Save.
3. Di canvas hapus node **Google Gemini Chat Model**. Klik **+** pada port **Chat Model** di node **AI Agent GM/GN** → pilih **Groq Chat Model** → pilih credential dan model yang mendukung *tool calling* (keluarga Llama 70B).

### 4. Pasang credential ke node setelah import

1. Setelah [import workflow](docs/05-import-workflow.md), node yang membutuhkan credential menampilkan peringatan.
2. Klik dua kali node → kolom **Credential to connect with** → pilih credential yang sesuai (lihat peta di atas).
3. Untuk tool di bawah **AI Agent GM/GN** (7 tool Sheets dan 3 tool HTTP), lakukan hal yang sama satu per satu.
4. Klik **Execute step** pada satu node Google Sheets (misalnya *Get Config*). Jika data muncul, credential dan izin sheet benar.

Detail tambahan dan pemecahan masalah: [`docs/04-credentials.md`](docs/04-credentials.md).

## 💬 Perintah

Semua perintah diketik di **channel pemantau** dan harus diawali `!ai`. Hanya pesan dari `admin_user_id` yang diproses.

> [!NOTE]
> Perintah **tidak dibalas langsung**. Semua perintah yang kamu ketik sepanjang hari diproses sekaligus pukul **00:01**, dan balasannya muncul setelah itu. Pengiriman GM (07:00) dan GN (19:00) berjalan terpisah sesuai jadwal. Untuk mengujinya sekarang, jalankan trigger **Tes Manual Perintah** di n8n.

```text
!ai lihat daftar channel
!ai tambah channel 123456789012345678 gm jam 07:00 gn jam 21:30
!ai tambah channel 111111111111111111 222222222222222222 333333333333333333
!ai ubah jam gm channel 123456789012345678 jadi 06:45
!ai stop channel 123456789012345678
!ai aktifkan lagi channel 123456789012345678
!ai tambah pesan gm "gm legends" bobot 8
!ai kirim gm sekarang ke 123456789012345678
!ai tampilkan bukti pengiriman terakhir
```

Daftar lengkap beserta perilaku yang diharapkan: [`docs/06-perintah.md`](docs/06-perintah.md).

## 📊 Struktur data (Google Sheets)

![Skema Google Sheets](assets/sheets-schema.id.svg)

| Sheet | Kolom | Fungsi |
|---|---|---|
| `Config` | `key`, `value`, `keterangan` | `monitor_channel_id`, `admin_user_id`, `monitor_webhook_url` (opsional), `timezone`, `gn_time`, `min_delay_sec`, `max_delay_sec`, `last_message_id` |
| `Channels` | `channel_id`, `aktif`, `gm_time`, `gn_time` | Channel target. Nama server dan channel diambil otomatis. Scheduler harian memakai `Config.gn_time`; kolom jam per channel disimpan sebagai referensi |
| `Messages` | `tipe`, `teks`, `bobot` | Pesan `gm` / `gn`. Bobot lebih besar berarti lebih sering muncul |
| `Logs` | `waktu`, `server`, `nama_channel`, `channel_id`, `tipe`, `pesan`, `message_id`, `status`, `error` | Bukti pengiriman, diisi otomatis |

Template siap pakai: [`sheets/gmgn-sheet-template.xlsx`](sheets/gmgn-sheet-template.xlsx). Sumber datanya CSV di [`sheets/csv/`](sheets/csv).

> [!IMPORTANT]
> Kolom ID dan jam **harus berformat Plain Text**. ID Discord 18-19 digit akan dibulatkan jika Google Sheets menganggapnya angka. Setelah import, simpan sebagai **Google Sheets asli** (*File > Save as Google Sheets*). n8n tidak bisa membaca file yang masih berformat Excel (.xlsx).

## 📁 Struktur repo

```text
gmgn-n8n-agent/
├── README.md
├── assets/                    # logo dan diagram SVG bilingual
├── workflows/
│   └── gmgn-ai-agent.json     # workflow n8n (placeholder GANTI_SHEET_ID)
├── sheets/
│   ├── gmgn-sheet-template.xlsx
│   └── csv/                   # sumber data template: Config, Channels, Messages, Logs
├── docs/                      # panduan lengkap (00 sampai 11)
├── scripts/
│   ├── set_sheet_id.py        # tanam ID spreadsheet ke workflow
│   ├── validate_workflow.py   # cek struktur, rahasia, sintaks JS
│   └── make_template.py       # bangun xlsx dari CSV
├── .github/                   # CI, template issue dan PR
├── .env.example               # variabel untuk n8n di Railway
├── CHANGELOG.md · CONTRIBUTING.md · SECURITY.md · LICENSE
└── requirements.txt
```

## 🔧 Kustomisasi

| Ingin | Caranya |
|---|---|
| Ganti model ke Groq | Hapus node *Google Gemini Chat Model*, tambah *Groq Chat Model*, sambungkan ke port **Chat Model** di *AI Agent GM/GN*. Lihat [`docs/04-credentials.md`](docs/04-credentials.md) |
| Ubah gaya pesan | Edit sheet `Messages` atau minta lewat `!ai tambah pesan ...` |
| Ubah format tampilan | Edit *system message* di node *AI Agent GM/GN* dan kode di node *Rangkum Bukti* |
| Ubah jam pemrosesan perintah | Ekspresi cron di node *Mulai 00:01 (proses perintah)* |
| Ubah jam mulai harian (jam GM) | Ekspresi cron di node *Mulai 07:00 (sekali sehari)*, mis. `30 6 * * *` untuk 06:30 |
| Ubah jam GN | Ubah `gn_time` di sheet `Config` |

## 🔒 Keamanan dan disclaimer

![Batas keamanan dan aliran data](assets/security-boundaries.id.svg)

- **Jangan pernah** menaruh token, API key, atau private key di repo, sheet, maupun chat. Semua rahasia hanya di *Credentials* n8n (terenkripsi dengan `N8N_ENCRYPTION_KEY`).
- Hanya pesan dari `admin_user_id` yang berawalan `!ai` yang diproses. Balasan sistem berawalan 🤖 agar tidak terbaca ulang sebagai perintah.
- Gunakan akun cadangan untuk pengujian. Gunakan jeda acak yang wajar dan jangan mengirim ke terlalu banyak channel dengan frekuensi tinggi.
- Pesan massal dan otomatis dapat melanggar aturan komunitas tertentu. Patuhi aturan tiap server.
- Proyek ini tidak berafiliasi dengan Discord, n8n, Google, maupun Railway. Dipakai dengan risiko sendiri, tanpa jaminan.

Kebijakan pelaporan celah keamanan: [`SECURITY.md`](SECURITY.md).

## 🔐 Privasi dan data

| Data | Disimpan di | Catatan |
|---|---|---|
| ID channel, jam, pesan, log kirim | Google Sheet milikmu | Tidak ada server pihak ketiga milik proyek ini |
| Token Discord, API key model, private key Service Account | *Credentials* n8n (terenkripsi `N8N_ENCRYPTION_KEY`) | Tidak pernah masuk sheet, chat, atau repo |
| Isi perintah `!ai` dan data sheet yang relevan | Dikirim ke penyedia model AI yang kamu pilih | Tinjau kebijakan data penyedia; paket gratis sebagian penyedia dapat memakai input untuk peningkatan produk |
| Riwayat eksekusi | Database Postgres n8n kamu | Dibersihkan otomatis (`EXECUTIONS_DATA_PRUNE`) |

Repo ini tidak mengumpulkan telemetri apa pun. Workflow di repo sudah disanitasi: tanpa ID spreadsheet, ID credential, token, maupun ID Discord pribadi.

## ❓ FAQ

<details>
<summary><b>Kenapa Google Sheets menolak dengan "The document must not be an Office file"?</b></summary>

File masih berformat Excel. Buka di Google Sheets, pilih *File > Save as Google Sheets*, lalu pakai ID file hasil salinan itu (dan share ulang ke Service Account).
</details>

<details>
<summary><b>Kenapa "Forbidden / The caller does not have permission"?</b></summary>

Sheet belum dibagikan ke email Service Account sebagai **Editor**, atau ID spreadsheet di workflow bukan ID file yang dibagikan.
</details>

<details>
<summary><b>Jadwal tidak jalan padahal sudah benar?</b></summary>

Pastikan workflow sudah **Published/Active**, `GENERIC_TIMEZONE` dan `TZ` di Railway bernilai `Asia/Jakarta`, dan `Config.gn_time` berformat teks `HH:mm`. Scheduler hanya jalan sekali sehari pukul 07:00 (cron); jika n8n mati pada jam itu, pengiriman hari itu terlewat. Gunakan trigger **Tes Manual** untuk memastikan pengiriman dan pencatatan berfungsi.
</details>

<details>
<summary><b>Apakah AI bisa salah mengirim ke channel yang salah?</b></summary>

Pengiriman terjadwal tidak melibatkan AI. Untuk perintah lewat chat, agent wajib memvalidasi ID ke Discord sebelum menyimpan, dan hanya menonaktifkan (tidak menghapus) channel. Tetap periksa balasan agent, terutama saat memakai model kecil.
</details>

Lebih lengkap: [`docs/08-pemecahan-masalah.md`](docs/08-pemecahan-masalah.md).

## 🧭 Roadmap

- [ ] Jam GM/GN per channel (membaca kolom `gm_time` / `gn_time` di sheet `Channels`)
- [ ] Perintah `!ai ringkasan hari ini` (jumlah terkirim/gagal)
- [ ] Notifikasi otomatis saat pengiriman gagal berulang
- [ ] Dukungan mode bot resmi (bot token) dengan contoh konfigurasi lengkap
- [ ] Versi Telegram sebagai tempat perintah

Ide lain? Buka [issue](https://github.com/akndrn000/gmgn-n8n-agent/issues/new/choose).

## 🤝 Kontribusi

Pull request dipersilakan. Baca [`CONTRIBUTING.md`](CONTRIBUTING.md) dan jalankan `python scripts/validate_workflow.py` sebelum mengirim PR.

## 📄 Lisensi

[MIT](LICENSE) © 2026 akndrn000
