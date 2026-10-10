# Kebijakan keamanan

## Melaporkan celah

Jangan membuka issue publik untuk celah keamanan. Gunakan **Security > Report a vulnerability** (GitHub Private Vulnerability Reporting) pada repo ini, atau hubungi pemilik repo lewat profil GitHub `akndrn000`.

Sertakan langkah reproduksi, dampak, dan versi. Hapus token dan data pribadi dari laporan.

## Prinsip

- Repo ini **tidak boleh** berisi token Discord, API key, private key Service Account, atau ID pribadi. CI (`scripts/validate_workflow.py`) memeriksa pola rahasia pada workflow.
- Semua rahasia disimpan di *Credentials* n8n.
- Jika sebuah token pernah ter-commit atau terkirim ke tempat publik, anggap bocor: **cabut dan buat ulang** segera, bukan hanya menghapus commit.

## Catatan tentang token akun Discord

Memakai token akun pengguna untuk mengotomatisasi akun (self-bot) melanggar Terms of Service Discord dan dapat menyebabkan akun diblokir. Proyek ini menyediakan jalur bot resmi (`Bot <token>`) dan menyarankannya. Penggunaan token akun pribadi menjadi tanggung jawab pengguna sepenuhnya.

## Versi yang didukung

Hanya rilis terbaru di branch `main` yang mendapat perbaikan keamanan.
