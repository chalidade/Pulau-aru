# Pulau Aru

Satu pulau, satu penghuni. Setiap follower TikTok menjadi warga, dan setiap hari dua komentar dipilih acak untuk menentukan jalan cerita. Game 3D low-poly ini menampilkan kondisi pulau persis seperti di video.

**Main:** https://chalidade.github.io/Pulau-aru/

## Isi pulau
- **Batu Nama**: nama setiap warga diukir di batu dekat pantai.
- **Mercusuar**: satu lampu per follower. Malam hari cahayanya makin terang seiring bertambahnya warga.
- **Kotak surat**: Surat Aru setiap 10 episode.
- **Perahu rusak**: petunjuk misteri "Bagaimana Aru sampai ke pulau ini?".
- **Papan aturan**: aturan keamanan program.
- **Milestone**: festival di 100 penduduk, kapal datang di 1.000, pulau muncul di peta di 10.000.
- Lampu jalan bertambah satu setiap 20 follower.

## Mengelola pulau (kreator)
1. Buka `https://chalidade.github.io/Pulau-aru/?kelola`.
2. Klik tombol pensil (Kelola pulau).
3. Tab **Pulau & GitHub**: tempel fine-grained token GitHub (Contents: Read and write, hanya untuk repo ini). Token disimpan di peramban itu saja.
4. Ubah warga, taruh bangunan, undi komentar, catat episode, tulis surat, buka petunjuk.
5. Klik **Terbitkan**. Perubahan ditulis ke `data/island.json`, dan pengunjung melihatnya dalam 1–2 menit tanpa perlu memuat ulang.

Tanpa token, gunakan **Unduh island.json** lalu unggah manual ke folder `data/`.

## Kontrol
- Desktop: WASD/panah jalan, Shift lari, geser mouse putar kamera, scroll zoom, E interaksi, M peta, H mode rekam, Q/Z putar kamera.
- HP: jempol kiri untuk joystick, geser sisi kanan untuk memutar kamera, cubit untuk zoom, tombol AKSI untuk interaksi.

## Struktur
```
index.html          UI dan importmap
src/main.js         renderer, kamera, input, NPC, siang-malam
src/world.js        generator pulau (seed tetap, semua pengunjung melihat pulau yang sama)
src/models.js       model low-poly: karakter, bangunan, landmark
src/ui.js           panel, HUD, alat kreator
src/data.js         baca/tulis data/island.json
data/island.json    kondisi pulau saat ini
lib/three/          three.js r160 (MIT)
```
Tidak ada build step. Jalankan lokal dengan `python3 -m http.server` lalu buka `http://localhost:8000`.
