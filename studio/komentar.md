# Antrean komentar & request

Tambahkan komentar di sini kalau mau menentukan sendiri apa yang masuk ke episode berikutnya
(bisa diedit langsung di GitHub dari HP). Sesi otomatis memakai yang ada di sini lebih dulu,
lalu menghapusnya setelah dipakai. Format satu baris: `@username: isi komentar`.

## UNTUK EPISODE 26 (Chalid, 9 Nov malam: format CERITA, tetap ramah penonton baru, RUNBOOK 2e)
Riset komentar TikTok Studio 9 Nov (ep25 dapat 20 komentar, kebanyakan request & "aku udah follow"). Screenshot asli
di `studio/episodes/ep26/komentar/` (pakai sebagai kartu `(path, tag)`):
- `karakter-aku.png` @wleeeeeeeeecnt: "nama aku ada tapii,kok gak ada karakter aku?" (keluhan serupa: @selia_032
  "bang ko nama saya gak ada", @ranz.bae1 "jarang kelihatan nih Sayaaa")
- `lift.png` @vcxn.mx: "apartemenya kasih lift dong btw dah follow dah gabung"
- `nelayan.png` @muhamatferos197: "bikin pelabuhan kak aku pengen jadi nelayan dah follow" (cameo, opsional)
- `menteri.png` @araa_yinchan: "aku mau jadi mentri keuangan, sekalian gedung buat rapat" (simpan untuk ep27)

Judul kerja: **"Namamu Ada, Karaktermu Mana?"**
1. **Fitur web baru (inti episode, jawaban komentar 1): "Panggil Karaktermu".** Di menu Batu Nama, setiap nama
   punya tombol "Panggil karakterku": karakter warga dengan tampilan acak tapi tetap (seed dari nama: warna baju,
   rambut, kulit, topi) keluar dari Batu Nama, berjalan ke jalan utama dengan label nama di atas kepala, lalu
   berkeliaran/berkegiatan; kamera mengikuti. Simpan pilihan di perangkat (localStorage) supaya karaktermu tetap ada
   saat kembali. Tambahkan juga link langsung `pulau-aru.web.id/?warga=<nama>`. Ini harus benar-benar jalan di web
   (cek 6b), karena CTA video menyuruh orang mencobanya.
2. **Lift apartemen (komentar 2, payoff lelucon "liftnya belum ada" dari ep22):** lift kaca di sisi Apartemen
   Presiden yang naik-turun di web. Adegan: Presiden 'EGA_ akhirnya naik lift ke penthouse; bodyguard
   Cawetssssss tetap minta "Identitas dulu!" ke lift-nya; Klub Pertama rebutan naik pertama.
3. Cameo: karakter @muhamatferos197 (dipanggil lewat fitur baru) memancing di dermaga di samping _Rayhannn` yang
   lagi-lagi dapat sandal. Pelabuhan sungguhan bisa jadi episode lain.

Struktur:
- 0–3 s cold open: kartu komentar @wleeeeeeeeecnt di atas Batu Nama + Aru melihat batu. Hook (≤18 huruf/baris):
  `NAMAMU ADA,` / `KARAKTERMU MANA?`. Narasi langsung menjelaskan premis: "Di pulau ini, setiap follower jadi warga.
  Tapi ada yang protes..."
- 3–20 s: Aru menekan Batu Nama → karakter wleeeeeeeeecnt keluar dengan label nama, bingung, lalu senang. Dua-tiga
  karakter follower lain menyusul (selia_032, ranz.bae1). Teks: "Sekarang namamu bisa jadi karakter."
- 20–42 s: kartu komentar lift → lift dibangun → adegan presiden + bodyguard + Klub Pertama (jelaskan singkat:
  "si presiden pilihan like", "bodyguard-nya").
- 42–50 s: cameo nelayan baru di dermaga.
- 50–57 s: CTA jelas: "Cari namamu di pulau-aru titik web titik i d, panggil karaktermu." End card: `pulau-aru.web.id`
  + pertanyaan "Karaktermu mau kerja jadi apa di pulau?" (sudah ada yang minta: nelayan, satpam, guru, tukang konter).
- Caption pendek & personal, contoh: "Namamu ada di batu tapi karaktermu nggak ada? Sekarang bisa dipanggil 🥹
  Cari namamu di pulau-aru.web.id. Karaktermu mau kerja jadi apa? #pulaunetizen #alurcerita #indiegame #fyp"
- Isi `state.json → strategy` (lastFormat CERITA, tests[] dengan hook ini). Simpan video ke branch `videos`.

## Traktir (langsung diwujudkan, tanpa undian)
Traktiran dari teer.id/chalidade masuk otomatis ke studio/traktir.json (kalau secret TRAKTEER_API_KEY sudah diisi). Tulis di sini hanya kalau mau menambah manual.

## Presiden / wakil presiden (tanpa undian, potong kuota)

## Komentar warga (opsional; kalau kosong, diambil dari TikTok)

## UMKM (didaftarkan ke Etalase UMKM)
Format: `nama usaha - jenis - link - @username`

## LIVE
Tulis jadwal LIVE berikutnya di sini (misal: Sabtu 20.00 WIB) supaya diumumkan di episode.
