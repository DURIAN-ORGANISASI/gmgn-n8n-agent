# 04 · Credentials di n8n

Workflow memakai empat jenis credential. Peta lengkapnya:

<div align="center">
<img src="../assets/credentials-map.svg" alt="Peta credential ke node" width="860"/>
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

1. Setelah [import workflow](05-import-workflow.md), node yang membutuhkan credential menampilkan peringatan.
2. Klik dua kali node → kolom **Credential to connect with** → pilih credential yang sesuai (lihat peta di atas).
3. Untuk tool di bawah **AI Agent GM/GN** (7 tool Sheets dan 3 tool HTTP), lakukan hal yang sama satu per satu.
4. Klik **Execute step** pada satu node Google Sheets (misalnya *Get Config*). Jika data muncul, credential dan izin sheet benar.

### Soal limit

Model hanya dipanggil saat ada perintah `!ai`, sekitar 2 sampai 5 request per perintah. Kuota gratis model Flash/Flash-Lite maupun Groq umumnya cukup. Cek angka limit akunmu sendiri di dashboard penyedia, karena angkanya berubah-ubah dan berbeda antar akun.
