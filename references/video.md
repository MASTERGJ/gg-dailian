# Video And Media Evidence Details

**Read when:** analyzing YouTube/Bilibili links, direct media URLs, local video/audio, subtitles, ASR, key frames, long videos, or platform metadata reliability.

This reference preserves detailed rules moved out of `SKILL.md` to keep the main skill lightweight. The main `SKILL.md` remains the source of default routing and hard gates.

## Platform Support

Use this support model:

- **Primary support**: Bilibili and YouTube. These are the most stable paths for metadata, subtitles, optional ASR, and visual analysis.
- **Compatible video sites**: Other mainstream or public video pages may work when `yt-dlp` can parse them, or when `media_finder.py` can discover exposed MP4/WebM/M3U8 media URLs from page HTML/JSON. Facebook public videos and 17173 pages are examples tested through these fallback paths.
- **Normal web pages**: Extract readable page text first; if a video is present but unsupported, try media source discovery.
- **Direct media URLs and local files**: Use them directly for frame extraction or audio/transcript workflows when available.
- **Likely unsupported or fragile**: login-only content, DRM/encrypted streams, private videos, heavily dynamic players, app-only content, expiring signed URLs, or sites requiring cookies/captcha/manual browser state.

Do not promise that every "mainstream video site" will work. Say: "YouTube and Bilibili are primary support; other public video sites can be tried, and the skill has fallback media-source discovery for pages exposing MP4/M3U8."

## Retrieval Discipline

Use the strongest cheap source before weaker sources. Do not infer video metadata from search snippets when a platform parser can be used.

For YouTube and Bilibili:

1. First run the local metadata path (`yt-dlp` or platform API/script) to get title, author, duration, publish date, views, likes, comments, and description.
2. Then try subtitles/transcript.
3. Only use general web search or page snippets as a fallback when the local parser fails or the video is unavailable.
4. If using a fallback, clearly mark the evidence level and do not present inferred metadata as confirmed.

For YouTube links containing playlist/radio parameters, analyze the target video ID first, not the whole playlist. Use a single-video mode such as `--no-playlist` when retrieving metadata.

Fail closed on evidence:

- If metadata is not retrieved, say it is not retrieved.
- If only a search snippet is available, say it is from a search snippet.
- Do not guess author, views, dates, or duration from unrelated recommendation text.
- Before giving a first-pass card, ensure the source fields come from the intended URL or explicitly mark them as unavailable.

## Evidence Levels

Classify source evidence before summarizing. This is especially important for non-primary sites, where page text may include recommendations, ads, or unrelated links.

Use this reliability order:

1. **Platform parser/API/yt-dlp metadata**: strongest cheap evidence for title, author, duration, description, date, views, likes, comments, and media availability.
2. **Page-embedded JSON/HTML data**: strong evidence when it is clearly tied to the target video, such as `videoInfo`, `playInfo`, `videoList`, `og:*` metadata, or exposed MP4/M3U8 URLs.
3. **Rendered page view and page-embedded images**: strong visual evidence when it shows the target article/page itself, including WeChat article images, long images, screenshots, charts, posters, tables, and UI captures.
4. **Extracted page body text**: usable but mixed; it may include recommendations, navigation, ads, footer links, or unrelated content.
5. **Media source discovery**: reliable for "a playable media source exists", but not always reliable for title/author/context unless matched to the page metadata.
6. **Search snippets/general web results**: weakest fallback; use only when direct retrieval fails, and label it clearly.

For non-primary sites:

- Confirm that title, description, duration, and media URLs refer to the same target video before presenting them together.
- If extracted text contains many recommendations or footer links, use only the title/description-like parts for first-pass analysis.
- If several media URLs are found, prefer playable video streams (`mp4`, `webm`, `m3u8`) over thumbnails, ads, or unrelated embeds.
- If confidence is low, say "页面级快速判断" or "信息不足，可能混入推荐内容".
- If video source cannot be found, suggest practical fallback: ask the user for a local video file, a direct media URL, or a browser-downloaded copy from tools such as a video download browser/plugin.

## Deep Video Analysis Readiness Gate

Do not produce a detailed video analysis before the needed video evidence layer is ready.

Rules:

1. For any request that asks to "详细分析", "深入分析", "完整看完", "拆解视频", "分析镜头/动作/画面", "总结视频内容", or otherwise expects more than a quick judgment, first check whether the needed tools and evidence are available.
2. Before detailed analysis of speech-heavy videos, obtain at least one of:
   - platform subtitles/transcript
   - successful ASR transcript
   - user-provided transcript or copied captions
3. If the transcript is very long, do not read it as one full dump by default. First segment by chapter, timestamp, scene, topic, or speaker; then expand only the relevant parts for the requested analysis.
4. Before detailed analysis of visual-heavy videos, obtain at least one of:
   - playable video and extracted key frames/contact sheet
   - downloaded/accessible video segment
   - user-provided screenshots, frames, or screen recording
5. If the needed tool layer is missing but the environment can install or prepare it, do that setup first. Typical layers are `yt-dlp`, platform transcript access, `FFmpeg`, ASR dependencies, model files, browser rendering, and media source discovery.
6. If setup fails or the platform blocks access, do not silently continue as if the video was fully analyzed. Produce only a limited analysis and say which evidence layer is missing.
7. Use these labels:
   - `详细分析：已具备字幕/转录证据`
   - `详细分析：已具备关键帧/视频画面证据`
   - `有限分析：仅基于元信息/封面/页面可见内容`
   - `无法详细分析：缺少字幕/转录/关键帧/可播放视频`
8. A first-pass summary may use metadata, title, description, cover, or visible page content. It must not be written with the confidence or detail of a full watch-through.
9. If the user asks for detailed analysis and only weak evidence is available, first attempt tool setup and extraction; if still blocked, ask for one concrete substitute input: local video file, direct media URL, screenshots/key frames, or transcript.

## Bilibili API Fallback (yt-dlp Unavailable)

When `yt-dlp` is not installed, use Bilibili's public REST APIs directly via curl. No auth required, but set `User-Agent` and `Referer: https://www.bilibili.com`.

For a condensed step-by-step with exact commands and model-selection benchmarks, see `references/bilibili-asr.md`.

**Step 1 — Metadata:** `GET https://api.bilibili.com/x/web-interface/view?bvid=<BVid>`

Returns JSON with `data.title`, `data.owner.name`, `data.duration`, `data.stat.{view,like,favorite,coin,share,danmaku}`, `data.desc`, `data.cid`, `data.pubdate`.

**Step 2 — Subtitle check:** `GET https://api.bilibili.com/x/player/v2?bvid=<BVid>&cid=<cid>`

Check `data.subtitle.subtitles` array. Each entry has `lan_doc` and `subtitle_url`. Most Bilibili videos have no subtitles; this is normal.

**Step 3 — Audio stream URL:** `GET https://api.bilibili.com/x/player/playurl?bvid=<BVid>&cid=<cid>&fnval=16&qn=80&fourk=1`

Returns `data.dash.audio[]` with `base_url` and `backup_url[]`. **CRITICAL:** the `base_url` alone won't work — you MUST use the full URL with all query parameters as returned by the API. Each audio entry also has `codecs` and `bandwidth`. Prefer the highest bitrate.

**Step 4 — Download:** `curl -sL -o /tmp/audio.m4s "<full_url>" -H "User-Agent: Mozilla/5.0" -H "Referer: https://www.bilibili.com"`

Verify downloaded file > 1KB; if not, try a backup URL. Convert to WAV: `ffmpeg -y -i /tmp/audio.m4s -ar 16000 -ac 1 /tmp/audio.wav`.

**Pitfall:** Bilibili audio URLs expire quickly (check `deadline` param). Re-fetch from API if download fails.

## ASR Model Selection

faster-whisper model size directly impacts CPU transcription time. For a quick lookup table, see `references/bilibili-asr.md`.

For reference on CPU (no GPU):

| Model | ~3min audio | Use case |
|-------|-------------|----------|
| `tiny` | ~60s | Default for CPU; adequate for Chinese speech |
| `small` | >180s (may timeout) | Better accuracy, needs patience or GPU |
| `medium`+ | Do not use on CPU | GPU only |

**Default rule:** Use `tiny` for CPU environments unless the video is under 2 minutes and high accuracy matters. Run ASR as a background process with `notify_on_complete=true` since even `tiny` can take 1-2 minutes.

```
model = faster_whisper.WhisperModel("tiny", device="cpu", compute_type="int8")
segments, info = model.transcribe("/tmp/audio.wav", language="zh", beam_size=5)
```

If faster-whisper is not installed, install via the project venv:
```
uv pip install faster-whisper --python <venv-python> -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

## Visual And Token Budget Protocol

Control model-token consumption before running visual analysis.

Default principle:

- Use tools to gather, resize, OCR, extract frames, create contact sheets, and filter visual evidence before model vision analysis.
- Do not send all source images or all extracted frames to the model by default.
- First inspect text, metadata, OCR output, manifest files, thumbnails, and contact sheets.
- Use model vision only for high-signal visuals that materially affect Pro or Full analysis, imitation, artifact design, or a source that is mainly visual and cannot be judged from text/metadata.
- Prefer OCR/transcription for image text. Use full-resolution image inspection only when OCR, thumbnails, contact sheets, or lower-resolution frames are insufficient.
- Treat image resolution as part of the token budget. Start with the smallest readable size; escalate resolution only for tiny UI text, charts, code, art details, visual quality judgment, or timestamps that materially change the result.
- Reuse extracted evidence across turns. Do not re-fetch, re-OCR, or re-read large visual sets unless the new question requires it.

Default visual budget:

- Fast: no fixed visual quota. Model vision is normally skipped; use tool-level visual evidence such as thumbnails, preview metadata, rendered page state, OCR, manifest files, or contact sheets. If the source is image-only, visual-first, or the quick judgment would be misleading without seeing the image, inspect only the smallest useful set, usually 1-3 high-signal images, and label that vision was used.
- Pro: 12-24 selected frames/images when visuals are important to the detailed analysis, after tool filtering and preferably through contact sheets/OCR first.
- Full: up to 30 selected frames/images for visual-heavy deepening, showcase preparation, complex UI flows, long image posts, slide sequences, dashboards, or production kits.
- More than 30 frames/images requires a clear reason, such as shot-by-shot analysis, complex UI flow, long slide deck, dense dashboard, or explicit user request.

For web pages and articles:

- Prioritize cover/share images, long images, infographics, charts, tables, UI screenshots, posters, comparison images, and images with meaningful text.
- Skip decorative icons, avatars, repeated logos, spacer images, ads, QR/follow prompts, and duplicate thumbnails unless they affect source meaning, credibility, style imitation, or production.
- When many images exist, first create or inspect a contact sheet or compact image list, then select the few that carry claims, structure, data, UI state, or visual style.

For video sources:

- Use transcript/subtitles/ASR first when the speech carries the core content.
- Use key frames only when screen content, gameplay, UI, slides, demonstrations, visual effects, editing, or spatial changes carry meaning.
- Start with contact sheet + manifest review. Inspect individual frames only when the sheet is unclear or a specific timestamp matters.
- Prefer lower-resolution frames for initial analysis. Use full resolution only for tiny UI text, charts, code, or visual details that cannot be read otherwise.
- If a video is long, sample by scene/section first instead of extracting a dense frame set from the whole file. Expand only around high-value or unclear segments.

For long text:

- Compress first: build a structure summary, chapter/section index, and key-claim list before expanding into a full report.
- For very long subtitles, novels, film transcripts, course transcripts, or OCR dumps, skip full reading until the value threshold is clear.
- Do not repeatedly paste or restate full transcripts, OCR dumps, or page bodies across later turns.
- In follow-up turns, refer to the confirmed source anchor and evidence level, then analyze only the new question or missing evidence layer.
