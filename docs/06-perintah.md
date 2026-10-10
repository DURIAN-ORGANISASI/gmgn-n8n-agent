# 06 · Daftar perintah `!ai`

Ketik di **channel pemantau**. Awalan `!ai` wajib. Pesan tanpa awalan itu, atau dari user selain `admin_user_id`, diabaikan.

Bahasa bebas boleh. Contoh di bawah hanya pola yang paling umum. Balasan tampil sebagai kartu embed jika webhook sudah diatur ([11](11-webhook-embed.md)), selain itu sebagai teks polos.

> **Waktu pemrosesan:** perintah tidak dibalas langsung. Semua perintah yang menumpuk sepanjang hari diproses sekaligus pukul **00:01** (berurutan dari yang terlama), dan balasan muncul setelah itu. Kata "sekarang" pada `kirim ... sekarang` berarti saat pemrosesan itu berlangsung. Untuk menguji tanpa menunggu, jalankan trigger **Tes Manual Perintah** di n8n.
>
> Maksimal 100 pesan terbaru di channel pemantau dibaca per hari (batas Discord). Pesan sistem berawalan 🤖 ikut terhitung.

## Membaca

| Perintah | Hasil |
|---|---|
| `!ai lihat daftar channel` | Daftar channel: `Server › #channel • ID • GM • GN • Aktif/Nonaktif` |
| `!ai tampilkan daftar pesan` | Isi sheet `Messages` |
| `!ai tampilkan bukti pengiriman terakhir` | Maksimal 5 entri terbaru dari `Logs` (diubah dengan menyebut jumlah) |

## Mengelola channel

| Perintah | Perilaku |
|---|---|
| `!ai tambah channel <ID>` | Validasi ID ke Discord, lalu simpan dengan jam default **GM 07:00** dan **GN 19:00** |
| `!ai tambah channel <ID> gm jam 08:00 gn jam 21:30` | Simpan dengan jam yang disebut |
| `!ai tambah channel <ID1> <ID2> <ID3>` | Tambah banyak sekaligus. Dipisah spasi, koma, baris baru, `<#ID>`, atau link channel |
| `!ai ubah jam gm channel <ID> jadi 06:45` | Hanya `gm_time` yang berubah. Jam `7.15` otomatis jadi `07:15` |
| `!ai stop channel <ID>` | `aktif` = FALSE. Baris **tidak dihapus** |
| `!ai aktifkan lagi channel <ID>` | `aktif` = TRUE |

Aturan penambahan:

- Channel yang sudah ada tidak diduplikasi. Jika statusnya nonaktif dan kamu menambahkannya lagi, agent mengaktifkannya kembali.
- Jam yang ditulis di samping sebuah ID hanya berlaku untuk ID itu. Jam tanpa ID tertentu berlaku untuk semua ID di pesan yang sama. Catatan: jam ini tersimpan di kolom `gm_time` / `gn_time`, sedangkan scheduler harian saat ini memakai jam mulai (cron 07:00) untuk GM dan `Config.gn_time` untuk GN.
- Pada penambahan banyak channel, hasil dikelompokkan: **Ditambahkan**, **Sudah ada (dilewati)**, **Gagal**, ditutup ringkasan jumlah.
- Agent membaca ulang sheet setelah selesai dan hanya melaporkan "Ditambahkan" untuk ID yang benar-benar ada.

## Pesan custom

| Perintah | Hasil |
|---|---|
| `!ai tambah pesan gm "gm legends" bobot 8` | Baris baru di `Messages` (tipe gm) |
| `!ai tambah pesan gn "gn frens"` | Bobot default 10 |

## Kirim manual

`!ai kirim gm sekarang ke <ID>` mengirim pesan saat itu juga, mencatat ke `Logs` (tipe `manual`), dan melaporkan bukti dalam satu baris: server, mention channel, ID, tipe, waktu, dan teks pesan di akhir.

## Yang sengaja tidak bisa dilakukan

- Menghapus baris channel. Agent hanya menonaktifkan, dan menyarankan penghapusan manual di sheet jika ada baris ganda.
- Menyimpan ID yang tidak valid atau tidak ditemukan di Discord.
- Mengarang nama server/channel.
