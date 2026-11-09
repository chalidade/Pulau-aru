# Pulau Aru: daily episode runbook

> **Catatan Chalid (4 Nov 2026):** durasi video tetap **sekitar 1 menit (55–60 s)** mulai episode 8. Ini menggantikan
> "35–50 s" di bagian 2c dan 3. Aturan retensi lainnya (cold open, hook di detik 0, caption besar, segmen pendek) tetap berlaku:
> isi menit penuh dengan lebih banyak momen, jangan dengan jeda kosong.

Each scheduled run makes **one** episode (about 60 s, portrait 1080×1920), builds what it promises into the game,
and posts it to TikTok **@kita.berkembang**. There are two runs a day (10:00 and 17:00 WIB). Work through the
steps in order. Write everything the audience sees or hears in Indonesian, in the same voice as earlier episodes:
casual, funny, a little anime (jokes, small sad or warm beats, and a hook at the end).

> **Aturan Chalid (6 Nov 2026): setiap video harus ada wujudnya di web.** Semua yang tampil di episode harus bisa
> ditemukan di pulau-aru.web.id. Lihat bagian 6b; episode tidak dikirim sebelum cek ini lulus.

The person who owns all this is Chalid. Message him with `SendUserMessage` for the posting hand-off and final report, or when a step really cannot be done.

---

## 0. Setup (fresh container)

1. Attach and clone both repos, with push access:
   - `chalidade/Pulau-aru` → `/home/claude/pulau-aru` (game, `data/island.json`, `studio/`)
   - `chalidade/vigenco` → `/home/claude/vigenco` (ElevenLabs voice over through GitHub Actions)
2. Set the environment:
   ```
   export STUDIO_WORK=/tmp/studio VIGENCO=/home/claude/vigenco
   ```
3. Start the game server as a **background** command with timeout 7200000:
   ```
   cd /home/claude/pulau-aru && python3 -m http.server 8765
   ```
   If a capture later shows default data (no roads, empty name stone), the server has died. Restart it and recapture.
   - Never stop it with `pkill -f <pattern>`: the pattern also matches your own shell, which then dies with exit 144.
     Use `ps -eo pid,args | awk '/[p]ython3 -m http.server/ {print $1}' | xargs -r kill` instead.
4. Chromium and Playwright are preinstalled; do not reinstall them. PIL, numpy and ffmpeg are present.
5. Commit trailer for every commit:
   ```
   Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
   Claude-Session: <this session's URL>
   ```

## 1. Read where the story is

- `studio/state.json`:
  - `nextEp`
  - president and vice president (term is **1 week**; quotas of 3 and 2 requests without a draw)
  - `openThreads`
  - `usedComments`
  - the last episode summaries
- `data/island.json`:
  - `episodes` (the public chronicle)
  - `buildings`, `roads`, `construct`
  - `followers` (population)
- `studio/komentar.md`: requests queued by Chalid.
  - **Traktir** and **presiden / wapres** requests here happen *without a draw*. Each one counts against the
    president/vice-president quota in `state.json`. A new president or vice president starts a new week and
    a fresh quota.
  - Requests from people who paid through Trakteer (teer.id/chalidade) are realised no matter what, "seperti
    titah dari langit". The island's one rule still holds for them: nothing hurtful, sexual, hateful or targeting
    a real person. If a request breaks it, adapt it into something harmless and say so in the report.

- `studio/traktir.json` (filled hourly by the **Trakteer** workflow): `requests` with `done: false` are paid requests
  (Rp5.000 = 1 request, `qty` = how many). Realise them in this episode, **without a draw**, before or alongside the two
  comments (if there are many, do up to 2 per episode, oldest first). Thank the supporter by name in the episode, then set
  `done: true`. `data/island.json → supporters` (ranking, Monumen Dermawan) is updated by the workflow itself.

## 2. Pick two comments

The scheduled runs work **without Chalid's laptop** (cloud mode, chosen by Chalid on 2026-11-04). Sources, in order:
1. `studio/komentar.md`: anything Chalid queued comes first.
2. `studio/traktir.json`: paid requests (see 1).
3. **Fresh TikTok comments via Apify:** dispatch the workflow and wait for it (2–5 min):
   ```
   gh api -X POST repos/chalidade/Pulau-aru/actions/workflows/tiktok-comments.yml/dispatches -f ref=main
   ```
   Poll `gh api repos/chalidade/Pulau-aru/actions/workflows/tiktok-comments.yml/runs?per_page=1` until it completes,
   then `git pull` and read `studio/comments.json` (`comments[]`: user, name, text, likes, video). If the run fails
   because `APIFY_TOKEN` is not set (or Apify errors), say so in the report and carry on with the next source.
4. Claude in Chrome, **only if** its tools are present and connected in this session (Chalid's laptop happens to be on):
   `https://www.tiktok.com/tiktokstudio/comment`, read with `get_page_text`.
5. Nothing new available: drive the episode from an open thread in `state.json` and ask Chalid in the report to
   queue comments in `komentar.md` (he can edit it on GitHub from his phone).

Choosing:
- Two comments that are unique, funny, surprising or random; they do not need to make sense. Prefer ones answering
  the previous episode's question, and ones with likes.
- Never reuse anything in `usedComments`. Skip hateful, sexual, about-minors, doxxing, or real-politics comments.
- Credit the commenter's handle exactly.
- **Comment cards must show the real username and profile photo (Chalid, 5 Nov 2026).** Best: a real screenshot of the
  comment (Claude in Chrome on TikTok Studio, cropped to the one comment) passed to `COMMENTS` as `(path, tag)`.
  Otherwise draw the card with the exact `user` from `studio/comments.json` and its `avatar` file (downloaded by the
  comments workflow into `studio/avatars/`): `(user, text, tag, avatar)`. Never invent a username or photo; if neither
  is available, say so in the report.

## 2b. Community and money (every episode, lightly)

The account is not eligible for TikTok's pay-per-view programme in Indonesia, so the plan is: grow the audience, then earn
from Trakteer requests, TikTok LIVE gifts, and small-business (UMKM) features. Keep it warm, never pushy:
- **Supporters:** when someone traktir'd, thank them on screen ("Terima kasih @nama!") and show their request happening.
  The Monumen Dermawan (east of the stage, (57,46)) and the "Papan Dermawan" ranking update automatically.
- **Call to action:** every 2nd–3rd episode, close with ONE of these on the end card (rotate, never all at once):
  "Request tanpa undian: traktir Rp5.000 di teer.id/chalidade" · "Punya usaha? Komentar #UMKMPulauAru nama - jenis - IG/WA"
  · "Ikut LIVE bangun pulau" (only if Chalid has announced a LIVE time in komentar.md).
- **UMKM (warung milik usaha sungguhan, permintaan Chalid 4 Nov 2026):** people with a small business comment
  `#UMKMPulauAru nama usaha - jenis - kontak` (contact = `IG: namaakun`, `WA: 08xxxx`, a shop link or a website; also
  entries in komentar.md). Pick at most 1–2 per episode. Accept only real small businesses; reject gambling, illegal loans,
  investment schemes, adult or prohibited goods, and anything that looks like a scam.
  - Turn the contact into an **https** link: `IG: seblakbundaarsy` → `https://www.instagram.com/seblakbundaarsy/`,
    `WA: 0812…` → `https://wa.me/62812…` (drop the leading 0), shop or website links as given (https only).
  - Build it on the island as its own stall: `island.json → buildings` gets
    `{type: "warungumkm", x, y, r, label: "<nama usaha>", link: "<https link>", kind: "<jenis>", by: "<username>", ep}`,
    in a row along a street near the market (east street `y 77–78`) or the main street. The sign shows `label`.
  - Also add `{name, kind, link, by, ep, place: "pasar"}` to `island.json → umkm` (Papan UMKM board and Etalase UMKM menu).
  - **Any building with a `link`** (not only `warungumkm`) is clickable on pulau-aru.web.id: tapping it, or walking up and
    pressing the action button, opens a sheet with a button to the Instagram, WhatsApp order chat or website.
  - In the episode: a short moment ("Lapak baru: Seblak Bunda Arsy! Ketuk warungnya di pulau-aru.web.id untuk pesan"),
    a `title` card with the business name and `@username`. Free while the island is starting out; never promise sales.
  - CTA rotation (end card, every 2nd–3rd episode): "Punya usaha? Komentar #UMKMPulauAru nama - jenis - IG/WA, warungmu
    kami bangun di pulau".
- Caption: always include `pulau-aru.web.id`; add `teer.id/chalidade` when the episode shows a supporter's request.

## 2c. Retention rules (most important; viewers were leaving at 0:01–0:02)

TikTok decides in the first 1–2 seconds. Every episode must follow these:
1. **Cold open, no intro.** Second 0 shows the most surprising, funny or dramatic moment of THIS episode (a flash-forward),
   with a voice line starting at 0.0–0.1 s and a two-line **`hook`** text on screen from frame 0
   (e.g. `('KOMENTAR KALIAN', 'JADI JALAN ASPAL!', 0, 2.9)`). Never open on a slow aerial, a fade-in, a title card or
   "Episode N"; the episode number is a small badge (automatic). No `fade_in` on the first segment.
   The hook sits at y≈600 (`HOOK_Y`), below TikTok's "Following | For You" tabs and inside the 3:4 profile-grid crop,
   so it is also the readable thumbnail. Keep each hook line **≤ 18 characters** so it renders big (long lines shrink
   to fit the width). Frame the shot so the face sits below the hook (y 800–1300), not behind it.
2. **The first frame must be readable on a phone**: a close shot of a character or the new thing, never a tiny landscape.
   Never start the cold open on a camera cut (skip the first frames after a cut with `from`).
3. **Promise a payoff** in the hook or the first line ("…tapi lihat apa yang terjadi di akhir", "siapa yang jatuh?"), and
   deliver it near the end. The end card asks a question that makes people comment.
4. **Tight, about 1 minute:** 55–60 s total (`TOTAL`, see Chalid's note at the top). Cut dead air: lines start at 0.1 s into each segment, no segment longer than
   ~7 s, most 2.5–5 s. Skip the population stat unless it is a milestone.
5. **Something changes every 2–3 s**: a cut, a pop-in card, a title, a reaction, the crowd cheering. Captions are big
   word-by-word (`CAPTIONS = 'pop'`, default) and every cut gets a small zoom punch (automatic).
6. **Show the viewers' comments early** (people stay to see their own): the draw segment comes within the first ~10 s,
   first card at ~0.4 s (`CARD_T`).
7. Write lines short and spoken: one idea per line, max ~12 words, humour over exposition.

## 2e. Strategi viral (analisa TikTok Studio, 9 Nov 2026; berlaku mulai ep25)

Data: `studio/analytics/`. 7.000 dari 7.020 follower datang dari SATU video ("Kini Aru punya teman", 68K views,
21,6 s rata-rata tonton, 97% For You). Video itu menjual **premis**: Aru sendirian di pulau, setiap follower jadi
warga, komentar mengatur cerita. Sejak ep7, views turun ke 400–1.000 karena episode jadi sinetron politik penuh nama
yang tidak dipahami penonton baru (93% penonton datang dari For You = orang yang belum kenal pulau ini).
Ep15 dapat 13K views tapi rata-rata cuma 3,3 s: hook-nya tidak cocok dengan isi, jadi algoritma berhenti mendorong.

Aturan:
1. **Ramah penonton baru.** Setiap video harus bisa dinikmati orang yang belum pernah melihat channel ini. Dalam
   3 detik pertama premis harus jelas lewat hook/narasi: "pulau ini diatur komentar kalian" atau "follow = jadi warga".
   Nama tokoh dan lore boleh, tapi jadi bumbu; jelaskan siapa dia dalam 2–3 kata saat pertama muncul
   ("si bodyguard", "presiden pilihan like").
2. **Rotasi format.** `state.json → strategy.lastFormat` mencatat format terakhir; gantian:
   - **KONSEP** (minimal 1x sehari, biasanya run pagi): menjual premis ke penonton baru. Contoh: "7 hari lalu Aru
     sendirian → sekarang 7.000 warga", "komentarmu jadi bangunan", "namamu terukir di batu kalau follow",
     before/after pulau, satu komentar random yang jadi sesuatu yang absurd. Emosional/hangat + lucu, sedikit nama.
   - **CERITA**: episode lanjutan dengan pemeran warga (aturan 2d), tetap memakai aturan 1.
3. **Hook = janji yang ditepati.** Teks hook harus menggambarkan apa yang benar-benar terjadi di video, bukan
   clickbait politik ("PRESIDEN MUNDUR?!" tanpa payoff jelas = 3 detik lalu digeser).
4. **Gaya visual awal.** Video viral memakai ilustrasi 2D bergaya buku cerita (pantai senja, Aru kecil). Untuk
   episode KONSEP boleh membuka 2–4 detik dengan kartu bergaya ilustrasi/hangat, lalu masuk ke 3D. Catat di
   `strategy.tests` apakah dipakai, supaya bisa dibandingkan.
5. **Caption pendek dan personal** (1–2 kalimat, gaya video awal: "Kini Aru punya teman. hayuk join pulau dan atur
   alur cerita."), lalu `pulau-aru.web.id` dan hashtag. Jangan ringkasan cerita panjang. Kata kunci yang dicari
   penonton: "alur cerita", "pulau netizen", "netizen city", "diatur netizen"; masukkan salah satunya di caption.
6. **Ajakan follow yang jelas** di akhir episode KONSEP: "Follow, namamu jadi warga. Komentar, ceritanya kamu yang
   atur." (Episode CERITA tetap pakai pertanyaan untuk komentar.)
7. **Catat eksperimen**: tulis di `state.json → strategy.tests[]` `{ep, format, hook, opening, captionStyle}` supaya
   analisa berikutnya (tarik data TikTok Studio → `studio/analytics/<tanggal>.csv`) bisa melihat apa yang menang.

## 2d. Pemeran warga (studio/warga.json)
Chalid wants the island to feel alive through recurring residents with fixed personalities (iseng, pahlawan,
introvert, sok tahu, menyebalkan, kocak, ...). `studio/warga.json` is the cast list. In every episode, give 1-3 of
them a small supporting part that matches their `sifat` and use their `kalimat` lines (one line each is enough).
Keep traits consistent across episodes, keep them friendly (teasing is fine, never mean), and when a new
follower asks to join, you may add them to warga.json with a new trait. **Cameo rule (Chalid, 8 Nov):** whenever the camera is in a public place, let 1-3 random residents from warga.json
appear in frame doing a small funny bit true to their trait (vary who appears from episode to episode).
Running gags: **Klub Warga Biasa** (ALIF HR vs NOVA), the over-serious bodyguard, and **Klub Pertama**
(three residents who all commented 'pertama') argue over who was first whenever anything opens.

## 3. Write the episode

- 55–60 s, in 10–13 segments, starting with the cold open (see 2c). Roughly:
  - hook or stat (population from `island.json`)
  - a character beat with the president or vice president, Aru, or residents
  - the comment draw (`undian`) with the two comments
  - building or doing request 1
  - request 2
  - a funny or warm beat
  - Aru's mystery thread, briefly, every other episode or so
  - the end card with a question for the comments
- Close an open thread when it fits; for example, the school and pharmacy can finish.
- Keep continuity with earlier episodes. Use real usernames only for the people involved.
- Voice: create `vigenco/voiceover/pulau-ep<N>/lines.json`, copying `voiceover/pulau-ep6/lines.json` for the format
  and settings. Fixed voices:

  | Role | Voice | ID |
  |---|---|---|
  | narrator | Kira | `gmnazjXOFoOcWA59sd5m` |
  | presiden | Putra | `RWiGLY9uXI70QL540WNd` |
  | wapres / aru | Dakocan | `plgKUYgnlZ1DCNh54DwJ` |
  | warga (female) | Cahaya | `iWydkXKoiVtvdn4vLKp9` |
  | warga2 / penjual | Putri Maharani | `I7sakys8pBZ1Z5f0UhT9` |

  Keep `useLibrary: false`.
- Commit and push to vigenco `main`. The **Voice over** workflow renders the mp3s and `result.json`
  (durations and word timings) and commits them back in 1–3 minutes. Poll with
  `git pull` until `result.json` contains every line id.
- Write numbers and URLs as speech: "pulau aru titik web titik i d". The screen shows the real text.

## 4. Build the requests into the game

Everything the episode shows must really exist at pulau-aru.web.id afterwards.

- **New building:**
  - Add a model to `BT` in `src/models.js`. Low-poly boxes, cones and spheres, built in metres around the origin.
    A person is about 1.55 m tall: a house is about 2× that, and big public buildings 2.5–3.5×. `scale: k`
    enlarges a model; `w`/`h` is the footprint in cells.
  - Then add an entry to `data/island.json → buildings`: `{type, x, y, r, by, ep}`.
    - `r` turns it in quarter turns. The door faces +y at r=0, west at r=1... use r=1 or r=3 to face a north–south street.
  - Never logos or brands of real organisations. Use your own generic signs.
- **Proportions (Chalid asked for realistic scale):** a person is ~1.46 m. A small one-storey building (warung, kiosk,
  pharmacy, post) is at least ~2× a person tall with a door taller than a person; houses ~2.2×; schools, hospitals,
  police stations, mosques 3× or more; lamps ~1.6×. Build at a comfortable size and use `scale: k` with a footprint
  (`w`/`h`) that covers the scaled model. Check with `python3 studio/lib/measure.py` (height/human column) and
  `python3 studio/lib/overlap.py` (no clashes except road x road) before capturing.
- **Placement:** run `python3 studio/lib/mapdump.py` and look at `$STUDIO_WORK/map.png`. The town is planned:
  - Main street: `x 54–55`, from the stage `(53,44)` south to the pier.
  - Cross street: `y 52–53`.
  - East street to the market: `y 77–78`.
  - Put new buildings in rows along a street, on grass (tile 3), off road cells, and not on the camp (east, around (66,66)).
  - New streets: add straight two-lane rectangles to `roads.segments`, as `[x0, y0, x1, y1]` inclusive.
  - Buildings stand on levelled pads automatically, and trees around them are cleared.
- **Construction:** `construct: [{type, by, ep, x, y}]` puts a work site with a "SEGERA DIBANGUN" sign at (x,y).
  When it is finished, remove it from `construct` and add the real building.
- **Other kinds of requests:**
  - People or roles: president/VP live in `island.json` (`president`, `vicePresident`).
  - Behaviours: `src/activities.js`.
  - World features: `src/main.js` / `src/world.js`.
- **Check your work:**
  - `node --check` every edited JS file.
  - Look at the result with `python3 studio/lib/look.py name "x,z,yaw,pitch,dist"`. x,z are world coords
    (cell − 56 + .5). Fix anything sunken, floating or clipping.
- **Record the episode:** append it to `island.json → episodes` (`{ep, date, picks, text}`; Indonesian, 2–4 short
  lines). Add credited usernames to `residents` if they are missing.
- **Push:**
  - **Push the game code first** (`src/…`).
  - **Push `data/island.json` only after the capture.** A local edit during a capture changes what the camera sees.
  - Always `git pull --rebase` before pushing. The follower sync commits to `data/island.json` every 30 min.

## 4a. Live story events

Whatever the episode stages only for the camera must also be visible in the live game, or viewers who open the
website will not find it. `island.json → event` drives a live scene: `{"type":"demo","ep":13}` puts 8 residents with
placards next to the `spanduk` (optional `"signs": ["PEMILU!", "SUARA|WARGA!", …]`, `|` = line break). When the story
resolves (e.g. the election happens), remove `event` or replace it. New kinds of events go in `assignDemo`/`stepDemo`
in `src/main.js`.

## 4b. Rooms inside buildings (unlock one per episode)

Rooms exist for masjid, sekolah, rumahsakit, rumah, rumahpresiden, warteg, kedaikopi, apotik (`src/interiors.js`).
All start locked ("Lihat … (terkunci)" + toast "Segera dibuka"). Each episode opens **one** room as a beat, in this
order unless a comment asks for another: **masjid (ep14) → sekolah → rumahpresiden → rumahsakit → rumah → warteg →
kedaikopi → apotik**.
- Open it: add the type to `island.json → interiors` (e.g. `"interiors": ["masjid"]`). Track it in `state.json → rooms`.
- Preview locally before it is open: `?buka=semua` or `?buka=masjid,sekolah`.
- Capture: `window.__room.enter('masjid')` puts the player inside (camera set for you); `window.__room.exit()`
  returns. Inside, people are real resident names (newest followers; sekolah's blackboard lists the 8 newest — use
  that as a "selamat datang murid baru" shout-out). Rumah presiden seats the current president and VP.
- Story beat: Aru unlocks the door ("Hari ini masjid resmi dibuka!"), walk-in shot, 2–3 s inside, a resident line.

## 5. Capture

- Copy `studio/lib/shots_template.py` to `studio/episodes/ep<N>/shots.py`.
  - Shot folders: `e<N>c1`, `e<N>c2`…
  - Frames = seconds × 30.
  - Base each shot on the line timings: segment length = start of the voice line + its duration + 0.3 s.
- Use `window.__look(x, z, yaw, pitch, dist, showPlayer)` and `window.__camTarget`, plus:
  - `__beforeRender(dt, T)` for per-frame animation and camera moves
  - `__cheer` to make the crowd cheer
  - `__vpTalk`, `P.npcs` (roles: president, vicepresident, listen, sell, shop, fish, chop, build, sit, wander, climb, kopdes)
  - `P.roads.userData.reveal(f)` to animate paving
  - `P.LM`, `P.WD`
- Good framings (bad framings put the camera inside a crowd or a tree, so check every new shot first):
  - The stage from above: pitch 0.9–1.0, dist 6–8.
  - Aerial: pitch 0.9–1.1, dist 40–75.
  - Two-person dialogue: see the explainer example `c8`, which searches for a tree-free spot.
- First check every shot as a single frame at `DPR=1` (a `prev` entry). Then run the full capture at `DPR=2`
  as a **background** command (timeout 7200000). It runs at about 1–1.5 s per frame; 60 s of footage takes 35–45 min.

## 6. Compose

- Copy `studio/lib/compose_template.py` to `studio/episodes/ep<N>/compose.py`.
- Edit `SEGS`. Each segment has:
  - `seq`, `mood` (cheer, hype, mystery, sail, dusk, sad, cliff, ending)
  - `lines` [(start s, id)]
  - optional overlays: `title`, `stat`, `banner`, `place`, `decree`, `cheer`, `market`, `fade_in`/`fade_out`
  - `endcard` on the last segment, with the end-card question text in `end_layer`
- Set `COMMENTS`: key = the word in the narrator's draw line at which the card pops; value = (user, text, 'TERPILIH').
  Also set `UNDIAN_BG` and `DECREE` if used.
- Run with `EP=<N>`:
  - `plan` (timeline must total 60 s; the last segment absorbs the remainder)
  - `preview t1,t2,…` (look at the JPGs)
  - `render`
  - `audio`
  - `final`
- Check four or five frames of the final MP4 before posting: text not clipped, nothing covering faces,
  the comment cards readable.

## 6b. Web parity check (WAJIB, never skip)

**Rule from Chalid (6 Nov 2026): every video must be represented on the website.** A viewer who opens
pulau-aru.web.id right after watching must find everything the episode showed: new buildings, signs, rooms opened,
crowds/events, NPC jobs, president/VP changes. Viewers noticed when the ep13 protest existed only in the video.
1. List every visible thing in the episode that is new or story-relevant (read your `shots.py`).
2. For each item, anything that was only staged in `shots.py` (`__pose`, `__placard`, crowd spots, props added in JS,
   hidden NPCs, forced time of day excepted) must become real game state before you deliver:
   a building or `label` in `island.json`, an `event` (section 4a), an opened room (4b), or a new NPC role in code.
3. Push code + `data/island.json`, `git pull` so the checkout equals `main` (what Pages serves; the container
   can't reach pulau-aru.web.id), restart the local server and take plain `look.py` shots of each item **with no
   shot-script JS at all**. Look at them. If something is missing, fix and repeat.
4. Send one parity screenshot (contact sheet) to Chalid together with the episode in step 7, captioned
   "Sudah ada di web: …". Do not send the episode until this passes.

## 7. Deliver for posting (Chalid posts it from his phone)

Cloud mode has no access to TikTok, so Chalid posts by hand. Make that a 30-second job for him:
1. Make a phone-friendly copy (under ~15 MB):
   ```
   ffmpeg -i final.mp4 -c:v libx264 -preset medium -crf 25 -maxrate 1500k -bufsize 3000k -c:a aac -b:a 128k -movflags +faststart $STUDIO_WORK/pulau-aru-ep<N>.mp4
   ```
2. **WAJIB, jangan dilewati (video ep16 & ep17 hilang 7 Nov karena langkah ini gagal): simpan salinan di branch `videos`.**
   `gh release` is blocked for these sessions (HTTP 403), so commit the file to the orphan branch `videos` instead:
   ```
   git clone -q --no-checkout --filter=blob:none https://github.com/chalidade/Pulau-aru.git /tmp/vids && cd /tmp/vids
   git checkout -q videos && cp $STUDIO_WORK/pulau-aru-ep<N>.mp4 episodes/ && git add episodes && git commit -m "Ep <N> video" && git push origin videos
   ```
   Download link for Chalid (and for later sessions): `https://github.com/chalidade/Pulau-aru/raw/videos/episodes/pulau-aru-ep<N>.mp4`.
   Keep the file under ~10 MB (`-crf 25 -maxrate 1100k`), which also fits the Chrome TikTok upload.
3. Send it with `SendUserFile` (status `proactive`). In the message, also give the download link
   `https://github.com/chalidade/Pulau-aru/raw/videos/episodes/pulau-aru-ep<N>.mp4` so Chalid can always download it from his phone.
4. Send a `SendUserMessage` that starts with **"Episode <N> siap diposting"**, followed by the caption in a code block
   ready to paste. Caption: Indonesian, under ~300 characters, one line about what happened, credit `@user1 @user2`,
   "Komentar = nasib pulau. Kunjungi pulau-aru.web.id", hashtags `#pulauaru #pulaunetizen #fyp`. Add one line
   reminding him to turn on the AI-generated content label.
5. If Claude in Chrome happens to be connected in this run, you may post it yourself through TikTok Studio upload
   instead (file_upload only accepts files under 10 MB in /mnt/user-data/uploads/ or attachments, not outputs/; visibility Everyone; AI label on), then
   still send the file and link. This posting is authorised by Chalid for this workflow; post nothing else, change
   no settings.

## 8. Wrap up

- Update `studio/state.json`:
  - `nextEp` + 1
  - add the used comments
  - adjust president/vice-president quota and week
  - refresh `openThreads`
  - append `{ep, title, posted, summary}`
- Remove the used entries from `komentar.md`.
- Commit and push `studio/` and `data/island.json`.
- Report to Chalid in 4–6 lines with `SendUserMessage`:
  - the episode title
  - the two comments chosen and why
  - what was built in the game
  - the TikTok link, or what still needs a manual post
- Attach the video with `SendUserFile`.
