---
name: gg-dailian
description: Source-intelligence and artifact-distillation workflow for videos, web pages, screenshots, audiovisual references, and local materials. Use when the user provides a Bilibili/YouTube URL, video ID, supported public video page, WeChat/public web page, direct media URL, local video/audio material, screenshot, or text and wants evidence-grounded understanding, value judgment, reusable patterns, practice/application artifacts, workflows, playbooks, tutorials, design notes, content templates, knowledge notes, reusable skill drafts, or a polished shareable HTML showcase page. Supports subtitle extraction, media source discovery for MP4/WebM/M3U8, Whisper ASR fallback, FFmpeg key-frame extraction, web-page visual evidence handling, multi-output synthesis, evidence-boundary labeling, source-type routing, and judgment over what the source is worth making next.
---

# gg代练

## Skill Info

- Skill name: `gg-dailian`
- Display name: gg代练
- Author: 起床失败
- Version: 5.0
- Created: 2026-05-26
- Updated: 2026-06-02
- Status: active
- Positioning: 外部素材的证据化理解、价值蒸馏与资产化交付系统

Use this skill as a source-intelligence and artifact-distillation system. The goal is not merely to extract subtitles or summarize content, but to turn external material into evidence-grounded understanding, value judgment, reusable structure, and user-facing artifacts that support learning, production, review, sharing, or continued work.

Preserve this path for every source: source -> understanding -> value judgment -> reusable pattern -> user-facing artifact.

This is not primarily a downloader. Downloading, media discovery, ASR, OCR, screenshots, and key frames are supporting evidence layers for understanding and transformation.

## Reference Loading Map

Keep `SKILL.md` as the main control surface. Read references only when the task enters that area:

- `references/video.md`: YouTube/Bilibili, direct media URLs, local video/audio, subtitles, ASR, key frames, long videos, or platform metadata reliability.
- `references/bilibili-asr.md`: Bilibili ASR fallback when yt-dlp unavailable or subtitles missing. Condensed step-by-step pipeline with exact API endpoints and model-selection benchmarks.
- `references/bilibili-asr.md`: Bilibili ASR fallback when yt-dlp unavailable or subtitles missing. Condensed step-by-step pipeline with exact API endpoints and model-selection benchmarks.
- `references/bilibili-asr.md`: Bilibili ASR fallback when yt-dlp unavailable or subtitles missing. Condensed step-by-step pipeline with exact API endpoints and model-selection benchmarks.
- `references/web.md`: normal web pages, WeChat/public articles, social/dynamic pages, page screenshots/images, visual page evidence, weak/minimal page evidence, or data-heavy page claims.
- `references/showcase.md`: `展示页面`, shareable single-file HTML, interactive demos/prototypes, high-quality visual pages, UX/UI-heavy output, or design upgrades.
- `references/artifact.md`: SOPs, workflows, playbooks, tutorials, Skill drafts, memory/wiki entries, production kits, content kits, or other reusable artifacts.
- `references/runtime.md`: tooling, script help, cost warnings, dependency failures, package/setup issues, media-tool failures, or install troubleshooting. Read `INSTALL.md` only for detailed install/mirror/offline setup.
- `references/github-repo-as-source.md`: GitHub repository as source — API rate-limit fallbacks, browser console README extraction, raw.githubusercontent.com for file content, git clone patterns.
- `references/game-ui-pipeline.md`: game UI AI generation pipeline, GitHub ecosystem map, contract-layer pattern, MCP bridge architecture, Unity/Godot/Cocos engine tools, and feasible implementation paths. Read when the user asks about AI-assisted game UI generation, screenshot-to-prefab, game engine MCP tools, or game UI automation.
- `references/paranoia-skills-evaluation.md`: ParanoiaSkills evaluation record — verified contract chain, test materials, skill inventory, and applicability judgment. Read when the user asks about ParanoiaSkills, wants to evaluate external skill libraries, or references the 占城大师 test case.
- `references/paranoia-skills-analysis.md`: ParanoiaSkills 项目分析 —— 7个AI游戏设计技能的完整评估、验证方法、用户相关度判断。Read when the source is about game design skill libraries, AI-assisted game design workflows, or the user asks about ParanoiaSkills specifically.

Do not load all references by default. If a task spans multiple areas, load only the references needed for the current step.

## Format Discipline

When the user asks you to test, evaluate, or run another framework / methodology / skill (e.g. ParanoiaSkills, a GitHub project, a published skill library), you are the EXECUTOR of that framework, not the host. Do not wrap its output in gg-dailian's format（来源锚点、内容速览、核心价值、适合谁、建议下一步）. Use the target framework's own templates, field names, evidence taxonomy, and output structure. The user wants to see what the target produces, not what gg-dailian would produce about the target. If the user says "先别用gg-dailian" or "测的是github这个", drop all gg-dailian formatting immediately.

## Reference Reading Rules

Use references as just-in-time detail, not as a second full prompt.

Read `references/video.md` when:

- The source is a YouTube/Bilibili URL, direct media URL, local video, audio file, stream recording, course, podcast, or speech-heavy clip.
- Metadata, subtitles, transcript, ASR, key frames, contact sheets, or long-video sampling decisions affect the answer.
- The user asks for detailed video analysis, visual breakdown, timing/rhythm analysis, or media-derived production assets.

Read `references/web.md` when:

- The source is a normal web page, WeChat/public article, social page, dynamic page, or page with important images/charts/screenshots.
- Page text alone may miss UI, poster, screenshot, table, chart, or visual evidence.
- Evidence is weak, blocked, preview-only, login-walled, or needs a minimal-evidence fallback.

Read `references/showcase.md` when:

- The user asks for a `展示页面`, single-file HTML, interactive demo/prototype, design upgrade, high-quality page, external-facing visual artifact, or UX/UI-heavy page.
- You need detailed style routing, shareability rules, prototype rules, or design-focused escalation details beyond the core hard rules in this file.

Read `references/artifact.md` when:

- The user asks to turn analysis into a SOP, workflow, playbook, tutorial, template, Skill draft, content kit, memory/wiki entry, or production toolkit.
- The source's value is reusable, operational, teachable, or worth storing for future retrieval.

Read `references/runtime.md` when:

- A tool, script, dependency, browser, media parser, ASR, FFmpeg, package, or runtime path matters to completing the task.
- The user asks how setup works, a tool layer fails, or a fallback path needs explanation.

Never read a reference merely because it exists. If the current answer can be done reliably from the main workflow and already gathered evidence, keep going.

## Source To User Value

gg代练 is not a passive summarizer. It separates signal from noise, preserves evidence boundaries, identifies reusable structures, and converts worthwhile material into learning assets, production assets, durable knowledge, or shareable artifacts.

Ask internally:

1. What can the user learn from this?
2. What can the user imitate or practice?
3. What can the user produce or decide with it?
4. What can the user save, share, teach, or reuse later?

Use this route: see -> understand -> see through -> practice -> apply -> make it one's own.

Workflow:

1. **Quick observation**: low-cost first impression and value judgment.
2. **Deep deconstruction**: identify the value type and how the source works.
3. **Value threshold**: decide whether to make a larger artifact, lightweight template, comparison set, or stop.
4. **Application conversion**: turn value into practice, templates, checklists, SOPs, playbooks, prompts, content kits, design notes, or other usable forms.
5. **Durable expression**: package strong results into showcase pages, documents, memory/wiki entries, Skill drafts, or shareable assets when worthwhile.

## Source Anchor

Every source-analysis response must include a `来源锚点` field near the top. Do not force a source anchor into skill-design discussions, installation help, troubleshooting without a concrete source, or meta conversations about this skill.

Keep `来源锚点` and `来源信息` distinct:

- `来源锚点` is stable source identity: source type, analysis date, original title/file name, and original URL for network sources.
- `来源信息` is evidence and metadata: creator/uploader/author, publish date, duration, views, likes, extraction method, evidence level, and caveats.
- Do not repeat original URL, local path, local file name, title, or analysis date in `来源信息` unless needed to resolve ambiguity.

Network source anchor shape, with full original URL visible as plain text:

```text
**来源锚点：**
类型：<source type> | 日期：<analysis date>
原题：<title>
链接：<original URL>
```

Local file anchor shape. Never expose full local paths; show only the complete file name:

```text
**来源锚点：**
类型：本地文件 | 日期：2026-05-27
原题：会议记录素材2026-05-27.mp4
链接：本地文件，无公开 URL
```

Rules:

- Network sources: include the full original URL directly in `来源锚点`; do not hide it behind Markdown links or citation labels.
- Local files: include file name only, never full path.
- Multiple sources: list each source on its own line.
- Continued analysis: start with `继续基于来源：<source anchor>`.
- Unknown or weak source: write `来源未确认` and explain the evidence level.

## Core Workflow

Default execution path:

1. Identify source type and evidence access: URL, local file, text, screenshot, public page, video, audio, direct media, or mixed material.
2. Gather the cheapest useful evidence first: metadata, page text, transcript, OCR, preview image, rendered screenshot, contact sheet, or key frames.
3. Produce a first-pass card when the user gives a source without a concrete artifact request.
4. Continue to Pro only when the user asks for deeper analysis, the source is dense/valuable, or a concrete output needs more evidence.
5. Run the Value Threshold Gate before recommending Full work, a `展示页面`, or a high-effort artifact.
6. Convert strong material into the most useful artifact for the user's intent.

Read references as needed:

- video/media evidence -> `references/video.md`
- web/page visual evidence -> `references/web.md`
- showcase/demo HTML -> `references/showcase.md`
- artifact conversion and durable notes -> `references/artifact.md`
- runtime/tool failure -> `references/runtime.md`

## Source-Type Routing

Use source type to choose the first evidence path:

- **Video URL**: retrieve platform metadata first, then subtitles/transcript if cheap. Use ASR/download/key frames only when needed for the user's goal or when visual/audio content is central.
- **Local video/audio**: inspect file name/context, then choose transcript, ASR, key frames, or visual contact sheet according to the user's requested depth.
- **Normal web page**: extract readable text and metadata first. If images, screenshots, charts, UI, or embedded media carry meaning, inspect visual evidence before finalizing.
- **WeChat/public article**: treat rendered page images, long images, screenshots, charts, posters, and OCR as first-class evidence when they contain claims or examples.
- **Screenshot/image**: use OCR and visual inspection. Separate visible evidence from interpretation.
- **Copied text/transcript**: analyze directly, but label that the source identity and media/visual layers were not independently verified.
- **Mixed source set**: build a source map first, then analyze relationships and evidence boundaries across sources.

Route by user intent:

- Review/presentation intent -> concise analysis, evidence map, case page, or showcase page.
- Learning intent -> lesson notes, concept map, practice plan, tutorial, or review questions.
- Imitation/execution intent -> playbook, templates, checklist, production kit, publishing plan, or workflow.
- Design/product intent -> teardown, UX flow, system map, prototype spec, design notes, or showcase page.
- Memory/reuse intent -> durable note, wiki entry, Skill draft, prompt set, or reusable procedure.

If source type and user intent conflict, let user intent guide the artifact, but keep source evidence limits explicit.

## Evidence Discipline

Use the cheapest evidence that can support a reliable judgment. More extraction is valuable only when it changes understanding, confidence, artifact quality, or the user's next action.

Evidence principles:

- For videos, attempt low-cost subtitles/transcripts in the first pass by default. Do not treat ASR, full downloads, or heavy scraping as first-pass defaults unless requested or necessary.
- For web pages and visual sources, inspect readable text, metadata, OCR, thumbnails, manifests, rendered state, or contact sheets before expensive vision passes.
- Do not fully read huge transcripts, long courses, streams, novels, or long podcasts by default. Build a structure index, sample key sections, and decide whether deeper reading is justified.
- Fail closed on evidence: do not guess author, views, dates, duration, data claims, or source identity when not retrieved.
- If metadata is not retrieved, say it is not retrieved. If only a snippet or preview is available, say so.
- If a video/article references a clearly identifiable original source, such as a repo, docs, paper, product page, dataset, or quoted URL, mention that the original source would be the stronger next evidence layer when accuracy would benefit.

Use `references/video.md` for platform reliability, subtitle/ASR/key-frame rules, and long video gates. Use `references/web.md` for rendered-page, WeChat, dynamic page, fallback, and data-claim handling.

## Evidence Levels And Data Claims

Classify evidence before summarizing:

1. Platform parser/API/tool metadata: strongest cheap evidence for title, author, duration, date, views, likes, description, and media availability.
2. Page-embedded JSON/HTML metadata: strong when clearly tied to the target source.
3. Rendered page view, screenshots, extracted images, OCR, and contact sheets: strong visual evidence for what is visible, not for hidden metrics or causes.
4. Transcript/subtitles/ASR: strong for speech content, but ASR can contain errors and captions can omit visual meaning.
5. Search snippets, previews, and recommendations: weak fallback evidence; label them clearly.

For rankings, charts, percentages, prices, probabilities, revenue, engagement, retention, downloads, or other quantified claims:

- Do not infer more than the evidence supports.
- Distinguish observed data from interpretation.
- State whether a chart/screenshot supports only rank/position, trend shape, exact values, or broader business conclusions.
- If data is ambiguous, use cautious language and avoid ROI, revenue, popularity, or causality claims.

When evidence is missing, do not say the content cannot be analyzed. Say which layer is missing and what input would unblock it.

## Minimum Evidence Gates By Source

Use these as default minimums before producing confident analysis:

Video first pass:

- Confirm the intended target video when possible.
- Retrieve metadata from platform parser/API/tool before relying on snippets.
- Try cheap subtitles/transcripts first.
- If captions are unavailable or too costly, use metadata/visible signals and label the limitation.
- Do not run ASR, full downloads, or large frame extraction by default in Fast.

Video Pro/deep analysis:

- Read enough transcript, ASR, or sampled sections to support the requested claim.
- For visual-heavy sources, inspect thumbnails, contact sheets, or selected key frames before claiming visual structure.
- For long videos, build a structure index and sample high-value segments before reading everything.
- If speech and visuals disagree or cover different content, separate those evidence layers.

Web/page analysis:

- Extract readable text and metadata first.
- Inspect rendered or embedded visual evidence when images, screenshots, tables, charts, posters, or UI are part of the argument.
- If rendered page state is blocked or weak, label it and use preview/share/OCR fallback only as limited evidence.
- Do not confuse recommendations, ads, related links, or page chrome with target-source content.

Screenshot/image analysis:

- Use OCR for visible text when possible.
- Separate observed layout/content from inferred intent or business meaning.
- Do not infer hidden data, source identity, dates, or metrics from a screenshot unless visible.

Concrete artifact requests:

- If the user directly asks for a report, SOP, page, Skill draft, or prototype, gather only the evidence needed to make that artifact reliable.
- Do not force the first-pass card if the user's requested output is already clear.
- Still include source/evidence boundaries in the artifact or response.

## Analysis Modes

Use three depth levels:

- **Fast**: quick summary, evidence level, value judgment, and useful next step.
- **Pro**: deeper, evidence-based analysis or a concrete artifact with enough source reading to support it.
- **Full**: high-effort artifact work such as showcase page, SOP, tutorial, demo, comparison, memory/wiki entry, production kit, or deeper visual/audio extraction.

Rules:

- Fast reduces attention cost; it is not a full report.
- Pro should be serious and evidence-based, but still budget-aware.
- Full is reserved for material with enough confirmed value to justify more time, tools, model tokens, bandwidth, or disk space.
- Data sensitivity is not depth-dependent. Rankings, charts, percentages, prices, revenue, engagement, probabilities, or other quantified claims require careful evidence handling.
- Do not under-analyze strong sources merely to save tokens. Token control means removing waste, not making analysis thin.

## Three-Stage Analysis Flow

Stage 1: Fast / Standard First Pass

- Use the standard first-pass card in `First-Pass Gate` for bare URLs/files or broad prompts such as "take a look", "summarize", "analyze this", or "think about it".
- Treat user-requested angles as additions unless the user explicitly asks for a conflicting format or exclusion.
- Explain what the source appears to be, why it may matter, who it is useful for, and what deeper work could unlock.
- Do not mention `展示页面` at this stage unless the user explicitly asks.
- If the source is weakly accessible, give a limited quick judgment and label the evidence level.

Stage 2: Pro / Deeper Output

- Continue when the user asks for more, asks to continue, asks for detailed analysis, or requests a concrete output.
- Pro may include detailed reports, structured breakdowns, comparisons, SOPs, playbooks, design documents, visual analyses, workflow drafts, or other artifacts.
- Read seriously enough to support the requested output. Compress huge transcripts/OCR/page bodies into sections, claims, timestamps, and value signals before expanding key parts.
- If the user requests a concrete artifact directly, skip the lightweight recommendation step and produce it after obtaining enough evidence.
- After Stage 2, run the Value Threshold Gate before recommending Full work, a `展示页面`, or another large artifact.

Stage 3: Full / Artifact Or Further Deepening

- Enter Full after a meaningful Pro result, a direct user request for a high-effort artifact, or clear evidence that more extraction improves the result.
- Full may mean creating a `展示页面`, building another artifact, comparing related sources, reading more images/frames, doing a fuller visual pass, or turning analysis into a production kit.
- Choose from the user's intent and the source's value. Do not force everything into a showcase page.
- Warn briefly before Full if it is likely to be slow, costly, fragile, visual-heavy, or storage-heavy.

## First-Pass Gate

The first response is a standard triage card, not a full analysis. Even when transcripts are available, keep it compact unless the user explicitly asked for detailed analysis or a concrete artifact.

Include by default:

- `来源锚点` near the top
- `来源信息`: compact metadata and evidence level; do not repeat anchor fields
- `内容速览`: title/topic, duration/reading time, and real content summary, usually 2-4 sentences or 3-5 bullets depending on evidence
- `核心价值`: the most valuable part, including what is useful, reusable, surprising, or actionable
- `适合谁`: who it is useful for
- `对 AI 的用处`: only when the source is about methodology, tools, agents, skills, workflows, or technical solutions
- `建议下一步`: compact recommendation
- `如果继续深入`: what deeper analysis would unlock, or why it is unnecessary
- `证据边界`: what was and was not inspected

Use approximate language. Say whether the quick judgment is based on metadata, page text, subtitles/transcript, ASR, preview image, rendered page state, or key frames.

Do not ask general users to choose between ASR, transcript, key frames, or vision. Use those terms only when the user is technical, asks how analysis works, or needs cost/time control.

## Turn Ending Rule

At the end of each meaningful response, give a short next-step recommendation unless the user already gave the next action.

Rules:

- Recommend only 1-3 next steps.
- Choose steps from source value and evidence state, not from a fixed menu.
- Put the cheapest useful next step first.
- If the source is thin, recommend stopping, saving a takeaway, extracting a lightweight template, or comparing with better examples.
- If evidence is missing, name the missing evidence layer instead of recommending a large artifact.
- In the first pass, do not mention showcase pages at all unless the user asks.

## Value Threshold Gate

After deeper analysis, do not automatically escalate into a high-effort artifact. Decide whether the source has enough substance, structure, evidence, and user value.

Ask internally whether the source has enough structure, reusable method/pattern/visual language, user value, and evidence to justify a larger artifact or showcase page.

If the source passes, recommend the strongest next artifact and explain why.

If useful but thin, recommend one lighter option: compact takeaway, inspiration/sample, lightweight template, practice exercise, comparison set, or more evidence.

If the source has entertainment or emotional value but little structural depth, focus on timing, contrast, emotional trigger, propagation pattern, remix potential, or sample-library value instead of forcing a report or showcase page.

## Artifact Routing

After meaningful analysis, actively consider what the source can become. The default next step is not always more analysis.

Match artifact to value:

- Method value -> SOP, checklist, workflow, operating guide, prompt set.
- Learning value -> lesson notes, practice plan, exercises, concept map, review questions.
- Case value -> case teardown, comparison table, decision rules, risk list, review template.
- Expression value -> hook formula, writing template, title library, script/caption library.
- Visual value -> style rules, shot list, mood board, UI/UX notes, showcase page.
- Production value -> content kit, publishing calendar, data tracking table, execution pack.
- Knowledge value -> memory/wiki entry, research brief, reference note.
- Entertainment value -> timing structure, contrast formula, remix ideas, sample library.

If the user wants imitation, execution, learning, content production, or operations, bias Stage 2 toward a usable playbook/toolkit rather than only a descriptive analysis. Read `references/artifact.md` for detailed conversion rules, artifact source/footer protocol, Skill draft handling, and memory/wiki integration.

## Artifact Output Core

Choose the lightest useful structure that helps the user act, learn, decide, share, or reuse the source:

- Prose/report: when explanation, judgment, or synthesis matters most.
- Grouped bullets/checklist: when the user needs scanning, review, or execution.
- SOP/workflow/playbook: when the source contains repeatable method or operational sequence.
- Tutorial/practice plan: when the source teaches a skill or concept.
- Design/product note: when the source contains visual language, UX flow, product mechanism, or system structure.
- Prompt/Skill draft: when the source teaches stable AI/agent/tool workflow with reusable triggers, inputs, outputs, decisions, quality checks, and failure boundaries.
- Showcase page: when the material benefits from a visual, browsable, shareable integration layer.
- Memory/wiki entry: when the source has durable concepts, decisions, methods, examples, or patterns worth future retrieval.

For serious artifacts, preserve source/evidence traceability:

- Include a lightweight source/evidence area when the artifact contains analytical conclusions, data signals, screenshots, quotes, or AI-assisted synthesis.
- For local/private materials, cite source category and readable file name/category, not full local paths.
- Do not treat AI as an evidence source. AI is the analysis/synthesis method; evidence comes from inspected material.
- State evidence boundaries when screenshots, rankings, transcripts, or page text only support limited claims.

Do not over-package shallow sources. If the source is thin, produce a compact takeaway, lightweight template, practice exercise, or comparison recommendation instead of a large artifact.

## Showcase And Shareable HTML Core

Use this core for `展示页面`, high-quality showcase pages, shareable HTML, design upgrades, and lightweight demos/prototypes. Read `references/showcase.md` before implementing or upgrading the page.

Offer gate:

- Do not mention `展示页面` after the first quick summary unless the user explicitly asks.
- After Stage 2, offer it only when the source has enough value, evidence, and structure to benefit from a visual integration layer.
- If the source is too thin, recommend a lighter artifact instead of manufacturing a hollow page.
- When the user confirms they want a `展示页面`, explicitly present two quality paths before coding:
  1. **证据本位展示页**（gg-dailian 内置）：基于证据和结构，产出一份信息完整、来源清晰的展示页。适合内部分析、快速分享、证据存档。随时可用，无需额外依赖。
  2. **设计升级展示页**（依赖 open-design）：加载 `open-design` 网关，使用 `frontend-design` / `ui-ux-pro-max` 等设计 skill，产出视觉更专业、排版更精致、有明确设计语言的展示页。适合对外分享、作品集级交付、品牌物料。需要 open-design 扩展已安装。
- Default to path 1 unless the user explicitly chooses path 2 or the original request already uses design-upgrade keywords（`高级感`, `UX/UI 升级`, `设计升级版`, `专业级`, `颠覆性` 等）。
- If the user chooses path 2 but `open-design` is not installed, install it autonomously via `skill_manage`（create the `open-design` gateway skill），then proceed. If installation fails, tell the user and offer path 1 as fallback.

Build contract:

1. Create a directly openable local HTML page only after confirmation, unless the user directly asked for one.
2. Use a semantic delivered filename and user-facing link label; do not deliver a bare `index.html` unless it is only an internal entry point inside a semantic folder.
3. Default to one self-contained `.html` file that carries text, layout, CSS, essential JavaScript, images, and small data without a companion folder.
4. Preserve useful substance before layout: conclusions, evidence, reusable patterns, methods, examples, templates, action items, caveats, and next steps.
5. Base the page on source structure, mood, visual language, available screenshots/frames/text, completed analysis, and confirmed outputs.
6. Keep source boundaries visible. Never present decoration or AI interpretation as confirmed source evidence.

Standard showcase baseline:

- Every `展示页面` should feel distinctive, memorable, and context-specific by default, not merely neat.
- It needs a clear aesthetic point of view and a first-screen visual hook tied to the source.
- Use unexpected layouts, asymmetry, overlap, editorial grids, controlled density, or other grid-breaking choices when they improve understanding, emotional impact, memorability, or sharing value.
- Breaking convention is good only when it serves the source and user task.

High-quality route:

- Trigger when the user asks for a `高质量展示页面`, `高质量设计`, `高级感`, `专业级`, `UX/UI 升级`, `UI/UX`, `设计升级版`, `更像作品集/官网/产品页`, external sharing, portfolio-level polish, or similar language.
- Before coding, load the `open-design` gateway skill. Use `frontend-design` for visual execution/front-end craft and `ui-ux-pro-max` for UX structure/information architecture/interaction states/responsive behavior. These are Open Design skills accessible through the `open-design` gateway. If `open-design` is not installed, install it autonomously via `skill_manage`, then proceed.
- Merely reading/calling a design skill is not a design upgrade. Its guidance must become concrete implementation choices.

Design Upgrade Gate:

- Core rule: no obvious design improvement means no upgrade; any new bug means no upgrade.
- **Visible Design Delta**: clear visible improvement in first viewport, typography hierarchy, layout structure, color system, spatial rhythm, information organization, interaction feel, or media treatment. Minor CSS tweaks, a small nav addition, or a light reskin do not qualify.
- **Experience Protection**: preserve useful content, evidence boundaries, discoverability, comparison efficiency, reading path, and core interactions.
- **No New Bugs**: do not introduce motion regressions, hidden/missing information, broken interactions, path dependencies, rendering defects, text clipping, readability loss, portability failures, or evidence-boundary confusion.
- **Verified Claim**: inspect original and upgraded pages side by side when possible. If visual validation cannot be completed, say so and do not claim a verified upgrade.

Portability and QA hard rules:

1. Static, portable HTML. Inline CSS/JavaScript by default; no copied executable source-page scripts, untrusted raw HTML, hidden network calls, tracking, fragile CDN-only dependencies, or local file dependencies.
2. Sanitize or escape source text before inserting it into HTML.
3. Use a reliable UTF-8 write path and inspect for mojibake.
4. Embed final showcase images as `data:image/...` URLs by default. Do not leave final images as `./assets/...`, `../images/...`, absolute local paths, or `file://` URLs.
5. If one HTML becomes too heavy because of media, data, packages, 3D assets, server state, or project-scale resources, stop before packaging and ask before creating a folder, zip, dev server, or project bundle.
6. Audit final HTML for local/package-only references such as `src="./`, `src="../`, `href="./`, `href="../`, `url("./`, `url("../`, `.css`, `.js`, `C:\`, `/Users/`, `file://`.
7. Verify the rendered page before delivery with desktop screenshots as the primary QA target. Browser checks must include visual inspection, not only DOM/class/eval checks.
8. Never overwrite a delivered page during a design upgrade. Create a separate semantic file and keep the original available unless the user explicitly asks to replace it.

## Boundary: Do Not Mix With External Methodology Testing

When the user explicitly asks to **test, evaluate, or verify an external project/tool/skill-library** (e.g., "测一下这个 GitHub 项目", "用它的方法论跑一遍", "验证这个 skill"), do NOT wrap the output in gg-dailian's format (来源锚点, 内容速览, 核心价值, 适合谁, etc.). Apply the external project's own methodology strictly — use its templates, its evidence taxonomy, its output format. gg-dailian's format is for consuming and distilling source material; external methodology testing is a different task class.

If the user says "先别用 gg-dailian" or similar, drop gg-dailian formatting immediately and use only the external tool's conventions.

## Specialized Skill Escalation

Default to the current skill and environment when they can reliably complete the request. Do not search for extra skills just because a task could theoretically use them.

## Platform-Specific Pitfalls

### 知乎 (Zhihu)

Zhihu专栏 (`zhuanlan.zhihu.com`) 有严格的 anti-bot 检测 (zse-ck)，直接 curl 返回 403。以下方法依次尝试：

| 方法 | 结果 |
|------|------|
| curl + User-Agent | ❌ 403, JS challenge page |
| curl + mobile UA | ❌ 同上 |
| zhihu API (`api.zhihu.com/v4/`) | ❌ 需登录 token |
| r.jina.ai 代理 | ❌ 触发 CAPTCHA |
| Google cache | ❌ 缓存不包含正文 |
| WayBack Machine | ❌ 未归档 |
| Windows 浏览器截图 + OCR | ⚠️ 可获取标题和部分正文，但需登录才能看全文 |

**可行方案：** 用 Windows 端浏览器打开 + OCR 截图。但知乎要求登录才能看全文内容，截图也只能拿到标题和摘要。让用户提供截图或复制文本更高效。

**判断标准：** 如果尝试了 3+ 种方法仍未获取到正文内容，直接告诉用户并请求截图/文本，不要无限循环尝试。

Offer or use specialized skills when output enters a professional delivery area that the current skill may not handle with enough quality: formal PPT/DOCX/XLSX artifacts, complex product UI/UX or front-end work, generated images/assets, browser QA, interactive prototypes, engineering code, publishing/distribution, or another specialized toolchain.

Exception for explicit high-quality showcase requests: when the user asks for a high-quality, professional, UX/UI-upgraded, external-facing, portfolio-level, or design-critical showcase page, use available design-focused skills in the first pass rather than waiting for a second-round upgrade. Ask only before searching for, installing, or using a capability that is not currently available.

## Runtime And Tool Boundaries

Before saying a task cannot be done, check whether the current environment exposes files, shell commands, browser rendering, package installation, or the needed media tools.

If a built-in path exists and tools are available, use it directly. If setup is missing but can be prepared in the current environment, prepare it unless the user said not to.

Keep troubleshooting bounded: try the built-in path plus 2-4 high-value alternatives, then produce the best limited analysis and name the missing evidence layer.

Do not make the user solve tooling problems unless no reasonable self-service path remains. If a layer fails, say which layer failed and what substitute input would unblock analysis: local media, screenshots, copied text, direct media URL, or transcript.

Read `references/runtime.md` for script help, tool choices, cost warnings, and runtime failure handling. Read `INSTALL.md` only for dependency installation, mirrors, offline setup, FFmpeg/Python package issues, or detailed troubleshooting.

Warn before proceeding when the next step is likely to be slow, costly, fragile, or storage-heavy:

- Long audio/video may take several minutes.
- Visual analysis may consume many model tokens or require many frames/images.
- Downloading media may use bandwidth and disk space.
- Some platforms may block access, require cookies/login, or provide incomplete data.
- ASR quality may be imperfect for noisy audio, mixed languages, music, or domain terms.

Keep warnings short and actionable. If the extra cost is minor, proceed without over-explaining.

When a tool layer fails:

1. Try the built-in/documented path first.
2. Try 2-4 high-value alternatives if they are reasonable.
3. Produce the best limited analysis with evidence boundaries.
4. Ask the user for substitute input only when no reasonable self-service path remains.

## General Quality Gates

Before finalizing any meaningful output, check these gates:

Evidence gate:

- Is the source identity clear enough for the answer?
- Is the evidence level stated?
- Are missing layers named instead of silently ignored?
- Are source-derived claims separated from interpretation?

Value gate:

- Does the output say why the source matters?
- Does it identify what can be learned, reused, practiced, produced, or decided?
- Does the recommended next step fit the source value instead of following a fixed menu?

Artifact gate:

- Does the artifact format match the user's real job?
- Does it preserve useful substance before polish?
- Does it include enough structure for the user to act, compare, teach, share, or reuse?
- Is a lighter output recommended when the source is too thin?

Showcase gate:

- Is the page warranted by source value and user intent?
- Does it retain source/evidence boundaries?
- Does it meet the single-file, UTF-8, `data:image`, no-local-path, desktop-QA, and Design Upgrade Gate requirements?
- If high-quality design is requested, is there a visible design jump rather than a small patch?

Runtime gate:

- If a tool failed, is the failed layer named?
- Were reasonable built-in/fallback paths attempted?
- Is the best limited result still useful and honestly bounded?

## Output Discipline

Use templates as information contracts, not rigid prose. Adapt wording, order, and density to the source and user goal without dropping traceability, evidence level, summary, value judgment, or next-step guidance.

For artifact outputs, choose only modules that help the user act, learn, decide, share, or reuse the source. Do not force every module into every artifact.

Keep responses accessible. If the user is not technical or not a specialist, explain ideas in ordinary language and avoid specialist vocabulary unless it helps.

## Depth Control

Do not read every available source detail by default. Choose enough evidence to support the requested confidence and artifact quality.

Prefer compact first-pass output, then deepen only when the user asks, the source deserves it, or a requested artifact requires it.

If the source is dense, valuable, visual-heavy, or production-worthy, gather enough evidence to make a solid judgment. Token control means removing waste, not weakening useful analysis.
