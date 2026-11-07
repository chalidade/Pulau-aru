# Antrean komentar & request

Tambahkan komentar di sini kalau mau menentukan sendiri apa yang masuk ke episode berikutnya
(bisa diedit langsung di GitHub dari HP). Sesi otomatis memakai yang ada di sini lebih dulu,
lalu menghapusnya setelah dipakai. Format satu baris: `@username: isi komentar`.

## Traktir (langsung diwujudkan, tanpa undian)
Traktiran dari teer.id/chalidade masuk otomatis ke studio/traktir.json (kalau secret TRAKTEER_API_KEY sudah diisi). Tulis di sini hanya kalau mau menambah manual.

## Presiden / wakil presiden (tanpa undian, potong kuota)

## Komentar warga (opsional; kalau kosong, diambil dari TikTok)

### UNTUK EPISODE 16 (pagi 7 Nov, dipilih Chalid; pakai DUA komentar ini, jangan diundi)
Screenshot asli (pakai sebagai kartu komentar, `COMMENTS` = (path, tag)):
`studio/episodes/ep16/komentar-ega.jpg` dan `studio/episodes/ep16/komentar-kopi.jpg`.

1. **'EGA_💥💥** (akun @.....plengerrr0, mantan wapres @EGA_91 di cerita): "aku nyalon min, janji saya kalau terpilih
   saya akan menjadi pemimpin yang baik minn" (**3 like**), lalu membalas sendiri: "wakil saya @King indo" (**2 like**).
   **Hasil pemilu (dicek di TikTok Studio 7 Nov 07:55 WIB):** komentar EGA adalah komentar dengan like terbanyak di
   video ep 15 → **EGA_ PRESIDEN**. Peringkat kedua seri 2 like (balasan EGA yang menunjuk King indo, dan @vcxn.mx
   "aku kak plis udah follow" yang bukan pencalonan) → **King indo WAKIL PRESIDEN**. Plot twist: wapres yang mundur
   di ep 15 sekarang jadi presiden ("namanya strategi!"), janjinya "jadi pemimpin yang baik" ditulis di papan.
   Lantik keduanya di mimbar, isi `island.json` president/vicePresident, kuota baru 3/2, Papan Pemilu jadi papan hasil,
   hapus `event.carry` 'EGA_ NYALON'. Ruangan berikutnya sesuai urutan: **rumahpresiden** (EGA & King indo duduk di kursinya).
2. **wibu cilik pelenger** (akun @sapta.rajo.ghaisa): "kakak aku tukang jualan kopidong udah follow".
   Wujudkan: gerobak/lapak kopi miliknya (label mis. "Kopi Dong" / "Kopi Wibu Cilik") di dekat mimbar atau Papan Pemilu,
   dia jualan kopi untuk warga yang merayakan pelantikan (NPC peran `sell`), dan masukkan ke residents kalau belum ada.
   Harus ada juga di web (lihat 6b RUNBOOK).


## UMKM (didaftarkan ke Etalase UMKM)
Format: `nama usaha - jenis - link - @username`

## LIVE
Tulis jadwal LIVE berikutnya di sini (misal: Sabtu 20.00 WIB) supaya diumumkan di episode.
