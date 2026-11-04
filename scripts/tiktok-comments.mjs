// Latest comments on @kita.berkembang's newest videos, via Apify (no laptop needed).
// Needs the repo secret APIFY_TOKEN. Writes studio/comments.json: { fetchedAt, videos: [{url, desc}], comments: [{user, text, likes, at, video}] }
import fs from 'node:fs';
const token = process.env.APIFY_TOKEN, user = process.env.TIKTOK_USER || 'kita.berkembang', nVideos = +(process.env.VIDEOS || 3);
if (!token) { console.log('::error::APIFY_TOKEN belum diisi (GitHub → Settings → Secrets → Actions).'); process.exit(1); }
const run = async (actor, input) => {
  const r = await fetch(`https://api.apify.com/v2/acts/${actor}/run-sync-get-dataset-items?token=${token}&timeout=240`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(input) });
  if (!r.ok) throw new Error(`${actor} ${r.status}: ${(await r.text()).slice(0, 300)}`);
  return r.json();
};
const vids = await run('clockworks~tiktok-scraper', { profiles: [user], resultsPerPage: nVideos, profileScrapeSections: ['videos'], profileSorting: 'latest', shouldDownloadVideos: false, shouldDownloadCovers: false });
const videos = vids.map(v => ({ url: v.webVideoUrl || v.url, desc: (v.text || '').slice(0, 140), at: v.createTimeISO || '' })).filter(v => v.url)
  .sort((a, b) => String(b.at).localeCompare(String(a.at))).slice(0, nVideos);
console.log(`[comments] ${videos.length} video`);
const items = videos.length ? await run('clockworks~tiktok-comments-scraper', { postURLs: videos.map(v => v.url), commentsPerPost: 80, maxRepliesPerComment: 0 }) : [];
const comments = items.map(c => ({ user: c.uniqueId || c.user?.uniqueId || c.username || '', name: c.user?.nickname || c.nickname || '', text: c.text || c.comment || '', likes: c.diggCount ?? c.likes ?? 0, at: c.createTimeISO || '', video: c.videoWebUrl || c.postUrl || '' }))
  .filter(c => c.text && c.user && c.user !== user);
fs.writeFileSync('studio/comments.json', JSON.stringify({ fetchedAt: new Date().toISOString(), videos, comments }, null, 1) + '\n');
console.log(`[comments] ${comments.length} komentar`);
