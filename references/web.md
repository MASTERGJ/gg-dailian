# Web Page And Visual Evidence Details

**Read when:** analyzing normal web pages, WeChat/public articles, social pages, dynamic pages, screenshots, page images, or weak/minimal page evidence.

This reference preserves detailed rules moved out of `SKILL.md` to keep the main skill lightweight. The main `SKILL.md` remains the source of default routing and hard gates.

## Data Analysis Handling Protocol

Data-like information is a high-sensitivity layer in every analysis artifact. This is not a `Pro` vs `Full` depth choice; even a `Fast` or `Pro` report must handle meaningful data seriously.

In serious analysis tasks, data sensitivity is a default professional capability, not an extra user request. The user should not need to remind the agent to notice, evaluate, or prioritize important data.

Default responsibilities:

- Do not wait for the user to point out which data matters.
- Do not require the user to ask for "data analysis" when the task is product analysis, market analysis, business teardown, growth review, monetization analysis, or other serious analytical work.
- The agent must decide which data signals affect the core conclusion and treat them accordingly.
- If data changes the argument, it should shape the structure, conclusion, comparison, or visual presentation.
- If data is low-value, repetitive, unclear, or incompatible, it can be minimized or excluded; seriousness means good judgment, not forcing every number into the artifact.

The goal is not to mechanically label every number. The goal is to notice valuable data, understand it, decide whether it matters to the argument, and present it with the right weight.

Treat these as data signals: rankings, revenue, downloads, DAU/MAU, retention, conversion, CPM/CPI/ROI, ad spend, views, likes, comments, shares, growth curves, percentages, probabilities, prices, costs, time windows, durations, sample sizes, cohort claims, chart/table values, and any quantified business/product claim.

Operational rules:

1. **Scan for data-bearing evidence**. In reports, case studies, product analysis, market analysis, and commercial teardown, proactively look for charts, rankings, tables, dashboards, price/probability panels, trend curves, and quantified claims. Do not let them become decorative screenshots.
2. **Decide what matters**. Not every number deserves emphasis. Prioritize data that affects the core conclusion, reveals scale, timing, ranking, growth, monetization pressure, user behavior, probability design, or business viability.
3. **Read the data carefully before interpreting**. Check metric name, unit, axis, category, platform, geography, time window, sample scope, and whether the value is exact, quoted, estimated from an image, or inferred.
4. **Use data to strengthen the argument when it has value**. Valuable data should shape the analysis, section structure, comparison, or visual presentation. Do not bury important data in captions or generic prose.
5. **Avoid false precision and false causality**. Do not turn a curve into exact numbers unless readable. Do not turn correlation into causation. Do not compare incompatible metrics or time windows without explaining the limitation.
6. **Choose presentation by analytical value**. Use a concise table, data card, chart callout, timeline, before/after comparison, or evidence note only when it helps the reader understand the point. Do not add labels or badges for their own sake.
7. **Separate observation from interpretation in wording**. Example: `截图显示榜单进入头部位置` is observation; `说明市场验证已经成立` is interpretation. Both can be used, but do not blur them.
8. **If data is weak or unreadable, say less rather than pretending precision**. Use cautious wording such as `趋势提示`, `材料显示`, `文章称`, `截图可见`, `大致可见`, or `待验证` only where useful.

Minimum behavior by artifact type:

- **Quick analysis**: mention the most important data signals if they materially change the value judgment or next step.
- **Serious report / case study / product teardown**: identify the important data signals, explain why they matter, and integrate them into the argument.
- **Showcase page**: make valuable data legible and visually meaningful. For example, a ranking screenshot should support market validation; a probability table should support random-mechanism analysis; a price panel should support monetization or pacing analysis.
- **Execution artifact**: convert relevant data into thresholds, assumptions, risks, tuning targets, or validation metrics when appropriate.

## Web Page Visual Evidence Protocol

For web pages, WeChat public-account articles, long-image posts, reports, product pages, dashboards, and UI-heavy material, treat accessible images as source content, not decoration.

Rules:

1. In Stage 1 quick summaries, do not call model vision by default. Use low-cost visual signals when available: cover/share image metadata, alt text, preview images, page-render state, OCR text, image count/type, or thumbnails. Mention image text or visual claims only when they are available from these low-cost paths and change the summary, value judgment, or recommended next step.
2. In Stage 2 deeper output, inventory accessible high-signal visuals before finalizing the analysis. Use rendered screenshots, page image assets, contact sheets, OCR, or user-provided screenshots as available, then select the smallest useful visual set for model inspection.
3. OCR or transcribe image text when it carries claims, steps, labels, numbers, titles, interface copy, or evidence. Interpret charts, UI flows, poster structure, visual hierarchy, and composition when relevant to the user's goal.
4. Do not spend attention on decorative icons, avatars, repeated logos, spacer images, ads, or duplicated thumbnails unless they affect source meaning, credibility, style imitation, or user-facing production.
5. If page images are blocked, lazy-loaded, too small, expired, login-only, or hidden behind a security wall, label the missing visual layer clearly. Ask for screenshots only after built-in/browser/page/metadata/preview attempts are unavailable or insufficient.
6. Use evidence labels such as `完整正文 + 页面图片确认`, `正文确认 + 图片未确认`, `页面可见内容判断`, or `封面/预览图判断` so the user knows whether images were actually inspected.

## Minimum Evidence Analysis Protocol

When a source exposes only minimal information, still analyze what is visible, but never pretend full access.

Rules:

1. First try structured content: title, author, date, body, transcript, metadata, media URL, or platform parser output.
2. If structured content is unavailable, inspect visible evidence: page title, meta tags, share card, cover image, thumbnail, first frame, screenshots, file name, URL text, embedded JSON, or rendered page state.
3. Produce a limited analysis when meaningful evidence exists.
4. Clearly label the evidence level with one of these exact values: `完整正文/字幕确认`, `元信息确认`, `页面可见内容判断`, `封面/关键帧判断`, or `文件名/URL弱线索`.
5. Use cautious wording such as: "基于当前可见信息，这更像是……" or "还不能确认完整内容，但可以初步判断……".
6. Only write `来源未确认` when neither metadata nor meaningful visible content can be obtained.
7. Never treat parser failure as content failure.
8. For dynamic pages such as 微信视频号、抖音、快手、小红书, report access layers as a single compact line: `访问层：页面可访问 / 静态信息 / 动态详情 / 可见画面/封面 / 视频内容`. Mark unavailable layers as `未确认`.
9. If full playback or transcript is unavailable for video sources, try thumbnail, cover, preview, first frame, or screenshot analysis before stopping.

## Dynamic Social Page Preview Fallback

Use this for dynamic social pages such as 小红书、抖音、快手、微信视频号, and similar app-first/share-card pages.

Default posture:

- Act as the user's helper, not as a tool that makes the user gather evidence first.
- When the user asks for deeper analysis, visual analysis, imitation, account templates, design breakdowns, or showcase pages, first use the skill's built-in or documented evidence paths that fit the source.
- If built-in paths are unavailable, fail, or do not cover the source, then attempt every reasonable evidence path available in the current environment.
- Ask the user for screenshots, copied text, local media, or direct media URLs only after tool/browser/page/metadata/preview extraction paths are unavailable, blocked, or insufficient.
- If a needed tool is missing but the environment can install or use an alternative, try that setup or alternative path before asking the user.
- Keep the effort bounded: if a few high-value attempts still cannot obtain better evidence, produce a clearly labeled limited analysis instead of endlessly debugging access.

Purpose:

- Treat share metadata and preview images as an intermediate evidence layer between plain text extraction and true in-app/browser viewing.
- Use it to avoid stopping too early when body extraction, rendered screenshots, or playback are blocked.
- Never present preview evidence as equivalent to seeing the full app page.

When normal page extraction is weak, blocked, or mostly boilerplate:

1. Start with the built-in/documented path: use `web_analyzer.py` for readable text, `media_finder.py` when media may be exposed, and the existing browser/screenshot path when available.
2. Inspect the final redirected URL and confirm it still points to the intended source.
3. Try to obtain a rendered page screenshot with available browser tools or local browsers when visual evidence matters. Do this before asking the user for a screenshot.
4. If the rendered screenshot is useful, use it as `页面可见内容判断` and clearly say it is from browser rendering, not necessarily the native app view.
5. If rendered screenshot returns a security block, login wall, blank shell, or generic error page, say so and do not treat that screenshot as source content.
6. Extract share metadata when available: `<title>`, `description`, `og:title`, `og:description`, `og:image`, `twitter:image`, and embedded JSON preview fields.
7. If preview images are available and local tools can fetch them, download them as source-related assets.
8. When multiple preview images exist, create or inspect a contact sheet before visual analysis.
9. Use preview images for visual style, composition, color, subject, and content-template analysis.
10. If the built-in paths do not expose enough evidence, use bounded autonomous troubleshooting such as alternate URL resolution, targeted search, browser user-agent variation, or lightweight HTML/JSON inspection.
11. Clearly label the evidence as `页面元信息 + 分享预览图证据` or `封面/预览图判断`.
12. Preserve the limitation: comments, full author profile, dynamic UI state, hidden text, full video playback, and in-app-only interactions remain unconfirmed unless actually accessed.
13. If built-in paths, browser rendering, share metadata, preview images, media discovery, and bounded autonomous troubleshooting are also unavailable or insufficient, ask for one concrete substitute input: screenshot, copied text, local media file, or direct media URL.

Do not overclaim:

- Preview images may be compressed, cropped, reordered, expired, watermarked, or incomplete.
- `meta description` may be truncated, mixed with tags, or shaped for sharing rather than full reading.
- `og:image` often represents share-card/preview assets, not necessarily every original image.
- This evidence can support quick judgment, visual style analysis, and account/content-template imitation; it cannot prove performance metrics, comments, creator intent, or complete narrative order.

## Platform-Specific Anti-Bot Notes

For sites with aggressive anti-bot protection that block even the Dynamic Social Page Fallback, see
platform-specific references for known workarounds:

- **知乎 (zhuanlan.zhihu.com)**: `references/zhihu-antibott.md` — zse-ck JS challenge, all HTTP paths blocked, try browser screenshot + OCR or ask user to copy.
