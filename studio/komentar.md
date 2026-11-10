# Antrean komentar & request

Tambahkan komentar di sini kalau mau menentukan sendiri apa yang masuk ke episode berikutnya
(bisa diedit langsung di GitHub dari HP). Sesi otomatis memakai yang ada di sini lebih dulu,
lalu menghapusnya setelah dipakai. Format satu baris: `@username: isi komentar`.

## UNTUK EPISODE 28 (Chalid, 10 Nov siang: dari komentar ep26 + ep27; format CERITA, RUNBOOK 2e)
Screenshot asli di `studio/episodes/ep28/komentar/` (kartu `(path, tag)`):
- `lapangan.png` @.....plengerrr0 (= Presiden 'EGA_ sendiri): "buat lapangan minn buat gotong royong"
  → **jatah terakhir presiden (3/3)**, tanpa undian. Catat di state.json president.requestsUsed = 3.
- `damkar.png` @vcxn.mx: "kak tambahin pemadam kebakaran biar nanti kalo ada kebakaran langsung padam nanti"
  (diminta juga @faaxzy79 6 hari lalu, "tambah pos pemadam kebakaran")
- `npc.png` @joe.harry88: "bang aku mau jadi NPC aja" (cameo)
- `ketua-keuangan.png` @potasganteng_: "gw jdi ketua keuangan ya" (cameo, bentrok lucu dengan Menteri Keuangan araa_yinchan)

Judul kerja: **"Kerja Bakti Pertama Pulau Aru"**. Hangat + lucu, ramah penonton baru (premis di 3 detik pertama).
1. **Lapangan Gotong Royong** (jatah terakhir presiden): lapangan rumput dengan gawang/tiang bendera, papan
   "LAPANGAN GOTONG ROYONG · jatah terakhir Presiden 'EGA_". Adegan: presiden mengumumkan kerja bakti, banyak warga
   (cast warga.json + karakter follower acak) menyapu, mengangkat, menanam; beberapa cast sesuai sifat (Alexandre si
   pahlawan angkat dua karung, whoyss menyembunyikan sapu, Luci si sok tahu memberi instruksi salah, Klub Pertama
   rebutan "aku yang pertama nyapu!").
2. **Pos Pemadam Kebakaran** (komentar @vcxn.mx): pos merah dengan mobil damkar kecil & selang. Payoff lucu yang
   aman: asap dari pembakaran ikan bakar dekat dermaga (bukan kebakaran sungguhan) → damkar meluncur → ternyata
   cuma ikan bakar; ikan bakarnya basah kuyup. Tidak ada yang terluka, tidak ada rumah terbakar.
3. Cameo **@joe.harry88 jadi NPC**: berdiri di pinggir jalan, setiap disapa mengulang satu kalimat yang sama ("Selamat
   datang di Pulau Aru." ... "Selamat datang di Pulau Aru."), di web juga begitu (disapa = kalimat itu saja).
4. Cameo **@potasganteng_ "ketua keuangan"**: mengaku ketua keuangan, Menteri Keuangan araa_yinchan: "Ketua apa?
   Ajukan proposal." (lanjutan gag ep27). Bisa ditambah ke warga.json.
- Struktur kasar: 0–3 s cold open (damkar menyemprot ikan bakar / atau kerja bakti massal) + hook ≤18 huruf/baris
  yang jujur, mis. `KERJA BAKTI` / `SATU PULAU!`; premis: "Di pulau ini, komentar kalian jadi kenyataan." →
  kartu lapangan → kerja bakti → kartu damkar → pos dibangun → payoff ikan bakar → cameo NPC & ketua keuangan →
  end card "Pulau ini butuh apa lagi?" + CTA follow.
- Caption pendek & personal + `pulau-aru.web.id` + #pulaunetizen #alurcerita #indiegame #fyp.
- Web parity: lapangan, pos damkar (+ mobil), NPC joe.harry88, potasganteng_ (spot dekat Gedung Rapat). Simpan video
  ke branch `videos`. Isi `state.json → strategy` (lastFormat CERITA, tests[]).
- **Cek frame gelap** (RUNBOOK 6b): ep27 sempat 1,5 s kamera menembus dinding Gedung Rapat. Jangan ulangi.

## Sisa riset 9 Nov (belum dipakai)
- Pelabuhan sungguhan (@muhamatferos197 "bikin pelabuhan kak", ep26 baru cameo nelayan)

## Traktir (langsung diwujudkan, tanpa undian)
Traktiran dari teer.id/chalidade masuk otomatis ke studio/traktir.json (kalau secret TRAKTEER_API_KEY sudah diisi). Tulis di sini hanya kalau mau menambah manual.

## Presiden / wakil presiden (tanpa undian, potong kuota)

## Komentar warga (opsional; kalau kosong, diambil dari TikTok)

## UMKM (didaftarkan ke Etalase UMKM)
Format: `nama usaha - jenis - link - @username`

## LIVE
Tulis jadwal LIVE berikutnya di sini (misal: Sabtu 20.00 WIB) supaya diumumkan di episode.
