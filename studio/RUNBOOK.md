# Pulau Aru: daily episode runbook

Each scheduled run makes **one** episode (about 60 s, portrait 1080×1920), builds what it promises into the game,
and posts it to TikTok **@kita.berkembang**. There are two runs a day (10:00 and 17:00 WIB). Work through the
steps in order. Write everything the audience sees or hears in Indonesian, in the same voice as earlier episodes:
casual, funny, a little anime (jokes, small sad or warm beats, and a hook at the end).

The person who owns all this is Chalid. Message him with `SendUserMessage` only for the final report, or when a
step really cannot be done.

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

Use **Claude in Chrome**. Load the `chrome-browser` skill, then use Chalid's logged-in Chrome.

- **Where to read comments:** open `https://www.tiktok.com/tiktokstudio/comment`, or the latest videos on
  `https://www.tiktok.com/@kita.berkembang`. Read the comments on the 1–3 newest videos with `get_page_text`,
  scrolling to load more.
- **What to choose:** two comments that are unique, funny, surprising or random. They do not need to make sense.
  - Prefer comments that answer the previous episode's question.
  - Never reuse anything in `usedComments`.
  - Skip comments that are hateful, sexual, about minors, doxxing, or political about real people.
- **Credit:** use the commenter's display handle exactly as shown.
- **Screenshots:** take one of each chosen comment if possible (`computer` with `zoom` and `save_to_disk`).
  Otherwise the compositor draws the card from text.
- **Order of sources:** queued items in `komentar.md` come first.
- **If Chrome is not connected:** use `komentar.md`. If that is empty as well, re-use an open thread from
  `state.json` as the episode's driver. Say in the report that no new comments could be read.

## 2b. Community and money (every episode, lightly)

The account is not eligible for TikTok's pay-per-view programme in Indonesia, so the plan is: grow the audience, then earn
from Trakteer requests, TikTok LIVE gifts, and small-business (UMKM) features. Keep it warm, never pushy:
- **Supporters:** when someone traktir'd, thank them on screen ("Terima kasih @nama!") and show their request happening.
  The Monumen Dermawan (east of the stage, (57,46)) and the "Papan Dermawan" ranking update automatically.
- **Call to action:** every 2nd–3rd episode, close with ONE of these on the end card (rotate, never all at once):
  "Request tanpa undian: traktir Rp5.000 di teer.id/chalidade" · "Punya usaha? Komentar #UMKMPulauAru nama - jenis - link"
  · "Ikut LIVE bangun pulau" (only if Chalid has announced a LIVE time in komentar.md).
- **UMKM:** collect comments containing `#UMKMPulauAru` (and entries in komentar.md). Accept only real small businesses with
  a shop / Instagram / WhatsApp business / website link; reject gambling, illegal loans, investment schemes, adult or
  prohibited goods, and anything that looks like a scam. Add at most 1–2 per episode to `island.json → umkm` as
  `{name, kind, link, by, ep, place: "pasar" | "kopdes"}`; give them a short moment in the episode ("Lapak baru di pasar:
  …"). They appear on the Papan UMKM board (by the market, (86,75)) and in the "Etalase UMKM" menu. Free while the island
  is starting out; never promise sales or results.
- Caption: always include `pulau-aru.web.id`; add `teer.id/chalidade` when the episode shows a supporter's request.

## 2c. Retention rules (most important; viewers were leaving at 0:01–0:02)

TikTok decides in the first 1–2 seconds. Every episode must follow these:
1. **Cold open, no intro.** Second 0 shows the most surprising, funny or dramatic moment of THIS episode (a flash-forward),
   with a voice line starting at 0.0–0.1 s and a two-line **`hook`** text on screen from frame 0
   (e.g. `('KOMENTAR KALIAN', 'JADI JALAN ASPAL!', 0, 2.9)`). Never open on a slow aerial, a fade-in, a title card or
   "Episode N"; the episode number is a small badge (automatic). No `fade_in` on the first segment.
2. **The first frame must be readable on a phone**: a close shot of a character or the new thing, never a tiny landscape.
   Never start the cold open on a camera cut (skip the first frames after a cut with `from`).
3. **Promise a payoff** in the hook or the first line ("…tapi lihat apa yang terjadi di akhir", "siapa yang jatuh?"), and
   deliver it near the end. The end card asks a question that makes people comment.
4. **Shorter:** 35–50 s total (`TOTAL`). Cut dead air: lines start at 0.1 s into each segment, no segment longer than
   ~7 s, most 2.5–5 s. Skip the population stat unless it is a milestone.
5. **Something changes every 2–3 s**: a cut, a pop-in card, a title, a reaction, the crowd cheering. Captions are big
   word-by-word (`CAPTIONS = 'pop'`, default) and every cut gets a small zoom punch (automatic).
6. **Show the viewers' comments early** (people stay to see their own): the draw segment comes within the first ~10 s,
   first card at ~0.4 s (`CARD_T`).
7. Write lines short and spoken: one idea per line, max ~12 words, humour over exposition.

## 3. Write the episode

- 35–50 s, in 7–9 segments, starting with the cold open (see 2c). Roughly:
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

## 7. Post to TikTok (public)

1. Make an upload copy under 10 MB:
   ```
   ffmpeg -i final.mp4 -c:v libx264 -preset medium -crf 26 -maxrate 1200k -bufsize 2400k -c:a aac -b:a 128k -movflags +faststart /mnt/user-data/outputs/pulau-aru-ep<N>.mp4
   ```
2. In Chrome, open `https://www.tiktok.com/tiktokstudio/upload`.
   - Use `find` to locate the file input, then `file_upload` with the path above. Never click the input itself.
   - Wait for processing.
3. Write the caption in Indonesian, under ~300 characters:
   - one line about what happened
   - credit `@user1 @user2`
   - "Komentar = nasib pulau. Kunjungi pulau-aru.web.id"
   - hashtags `#pulauaru #pulaunetizen #fyp`
4. Set visibility to **Everyone**. Turn on the **AI-generated content** label: the voices are AI.
5. Click Post, then confirm on the profile that the video appears.
   - This posting is authorised by Chalid's standing instruction for this workflow. Do not post anything else.
   - Never change account settings.
6. If Chrome is unavailable or the upload fails twice:
   - Send the file with `SendUserFile` and push a notification.
   - Give the ready-to-paste caption in the report, so Chalid can post by hand.

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
