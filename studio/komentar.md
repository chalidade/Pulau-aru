# Antrean komentar & request

Tambahkan komentar di sini kalau mau menentukan sendiri apa yang masuk ke episode berikutnya
(bisa diedit langsung di GitHub dari HP). Sesi otomatis memakai yang ada di sini lebih dulu,
lalu menghapusnya setelah dipakai. Format satu baris: `@username: isi komentar`.

## UNTUK EPISODE 19 (sore 7 Nov, permintaan Chalid; JANGAN ambil komentar lain)
**"Warga Baru Pulau Aru"**: episode perkenalan 14 warga baru yang minta ikut, masing-masing dengan sifat uniknya.
Semua data ada di `studio/warga.json` (nama, sifat, julukan, peran, kalimat khas, pose, tempat, screenshot asli di
`studio/episodes/ep19/warga/*.png` untuk kartu komentar). Arahan:
- Format: Aru (atau presiden 'EGA_) menyambut rombongan warga baru di dermaga/alun-alun; tiap warga muncul cepat
  (2-4 detik) dengan kartu namanya + julukan + satu kalimat khas, langsung memperagakan sifatnya.
  Contoh: Alexandre "Serahkan padaku!" menolong ember jatuh; whoyss ketahuan menukar papan nama; Klub Pertama
  (D..A..B..Y a..j..a, princes_nay, Letisya) ribut siapa yang pertama dan Letisya menang pakai 'catatan jam';
  dell_ cuma bilang "hm." di ujung dermaga; senar muliya gitarnya putus; inyuu mencari tombol save.
- Hook (detik 0): mis. "14 WARGA BARU, SATU PULAU" / "SIAPA YANG PALING NYEBELIN?". Tetap ~55-60 detik: kalau
  14 terlalu padat, tampilkan semuanya di montase kartu dan beri adegan sungguhan ke 6-8 yang paling lucu.
- End card: "Kamu mirip siapa? Tulis di komentar", dan bahwa mereka akan muncul di cerita berikutnya.
- **Wajib ada di web (6b):** masukkan ke-14 orang ke residents di island.json, tempatkan di 'tempat' masing-masing,
  dan saat warga disapa di game tampil julukan + salah satu kalimat khasnya (tambahkan kolom sifat ke data warga).
- Ruangan berikutnya sesuai urutan RUNBOOK 4b tetap boleh dibuka.

## Traktir (langsung diwujudkan, tanpa undian)
Traktiran dari teer.id/chalidade masuk otomatis ke studio/traktir.json (kalau secret TRAKTEER_API_KEY sudah diisi). Tulis di sini hanya kalau mau menambah manual.

## Presiden / wakil presiden (tanpa undian, potong kuota)

## Komentar warga (opsional; kalau kosong, diambil dari TikTok)

## UMKM (didaftarkan ke Etalase UMKM)
Format: `nama usaha - jenis - link - @username`

## LIVE
Tulis jadwal LIVE berikutnya di sini (misal: Sabtu 20.00 WIB) supaya diumumkan di episode.
