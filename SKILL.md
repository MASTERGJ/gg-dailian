---
name: gg-dailian
description: Source-intelligence and artifact-distillation workflow for videos, web pages, screenshots, audiovisual references, and local materials. Use when the user provides a Bilibili/YouTube URL, video ID, supported public video page, WeChat/public web page, direct media URL, local video/audio material, screenshot, or text and wants evidence-grounded understanding, value judgment, reusable patterns, practice/application artifacts, workflows, playbooks, tutorials, design notes, content templates, knowledge notes, reusable skill drafts, or a polished shareable HTML showcase page. Supports subtitle extraction, media source discovery for MP4/WebM/M3U8, Whisper ASR fallback, FFmpeg key-frame extraction, web-page visual evidence handling, multi-output synthesis, evidence-boundary labeling, source-type routing, and judgment over what the source is worth making next.
---

# gg代练

- Name: `gg-dailian`
- Display: gg代练
- Version: 5.1
- Positioning: 外部素材的证据化理解、价值蒸馏与资产化交付系统

**Core path**: source -> understanding -> value judgment -> reusable pattern -> user-facing artifact.

This is not a downloader. ASR, OCR, key-frame extraction, and screenshots are supporting evidence layers for understanding — not the goal.

---

## Mode Router

Choose output depth by trigger. Jump to any stage when user intent is clear.

| Mode | Triggers | Required output | Forbidden |
|------|----------|----------------|-----------|
| **Fast** | 链接/文件; "看看""分析下""总结下" | `来源锚点` + `证据等级` + `核心价值` (2-4 句) + `适合谁` + `建议下一步` + `证据边界` | 完整证据索引; 展示页; SOP; 长报告 |
| **Pro** | "深入分析""详细拆解""完整复盘"; 用户要求具体产物 | Fast 全部 + `证据索引` + `价值判断` + `可复用模式` + `验证计划/下一步` | 展示页 (除非用户明确要求) |
| **Full** | "展示页""做SOP""写教程""出报告" | Pro 全部 + 展示页/SOP/教程 + `来源/证据追溯` | 跳过价值阈值门; 薄素材强行出大报告 |

**Jump rules**: user directly requests Full → skip Fast/Pro. User says "继续" → escalate one level. Value Threshold Gate must pass before entering Full.

**Density gate**: Fast keeps attention cost low — never a full report. Pro is evidence-based but budget-aware. Full requires confirmed value — warn if slow/costly.

---

## Evidence Gate (required in every analysis)

| Field | Required | Description |
|-------|----------|-------------|
| `evidence_level` | Yes | `完整获取` / `部分获取` / `元信息确认` / `可见内容判断` / `弱线索` |
| `allowed_claims` | Yes | What this evidence supports |
| `forbidden_claims` | Yes | What this evidence cannot support |
| `missing_evidence` | If any | What input would unblock deeper analysis |

Fail closed: never guess author, dates, metrics, or source identity when not retrieved.

---

## Source Anchor

Every analysis opens with source anchor. Network sources show full URL; local files show filename only (never full path).

```
**来源锚点：**
类型: <video_url|web_page|screenshot|local_file> | 日期: <analysis date>
原题: <title>
链接: <URL or 本地文件，无公开 URL>
```

Multiple sources: list each on its own line. Continued analysis: start with `继续基于来源：<anchor>`.

---

## Reference Map

Load references only when the task enters that area. Never load all by default.

| Reference | Read when |
|-----------|-----------|
| `references/video.md` | YouTube/Bilibili, local video/audio, subtitles, ASR, key frames |
| `references/web.md` | Web pages, WeChat articles, dynamic/social pages, visual evidence |
| `references/showcase.md` | 展示页面, HTML, design upgrades, shareable pages |
| `references/artifact.md` | SOPs, workflows, tutorials, Skill drafts, content kits |
| `references/runtime.md` | Tool failures, dependency issues, setup, cost warnings |
| `references/game-ui-pipeline.md` | AI game UI generation, engine MCP tools |

---

## Source-Type Routing

**Video URL**: metadata first → subtitles if cheap → ASR/key-frames only if needed. Long videos: build structure index, sample key segments.

**Local video/audio**: inspect context → transcript/ASR/key-frames per user depth.

**Web page**: extract text+metadata first → inspect visual evidence (images, charts, screenshots) before finalizing.

**WeChat/article**: rendered images, long-images, and OCR are first-class evidence.

**Screenshot/image**: OCR + visual inspection. Separate observed from inferred.

**Copied text**: analyze directly, but label that source identity was not verified.

**Mixed sources**: build source map first, then cross-reference.

**Route by user intent**:
- Review/pitch → concise + evidence map
- Learning → lesson notes, practice plan
- Imitation/execution → playbook, templates, checklist
- Design/product → teardown, UX flow, system map
- Memory/reuse → durable note, Skill draft

---

## Evidence Discipline

- **Cheapest evidence first**: before vision passes, try metadata, OCR, transcripts, contact sheets.
- **Long content**: build structure index, sample key sections. Don't read everything by default.
- **Data claims**: rankings, charts, percentages → distinguish observed data from interpretation. Don't infer revenue/causality from screenshots.
- **Missing evidence**: say which layer is missing, not "cannot be analyzed."

**Evidence levels**:
1. Platform metadata (strongest cheap evidence)
2. Page-embedded JSON/HTML
3. Rendered page/screenshots/OCR (strong for visible, not hidden)
4. Transcript/ASR (strong for speech, may miss visual)
5. Search snippets/previews (weak — label clearly)

---

## Value Threshold Gate

After Pro analysis, decide: does this source have enough substance for a larger artifact?

- **Pass** → recommend strongest next artifact, explain why
- **Thin but useful** → compact takeaway, template, comparison set
- **Entertainment/emotional** → timing, contrast, remix potential — don't force a report

---

## Artifact Routing

Match output to value type:

| Value type | Artifact |
|-----------|----------|
| Method | SOP, checklist, workflow, prompt set |
| Learning | Lesson notes, practice plan, concept map |
| Case | Teardown, comparison table, risk list |
| Expression | Hook formula, writing template, script library |
| Visual | Style rules, mood board, showcase page |
| Production | Content kit, publishing calendar |
| Knowledge | Memory/wiki entry, research brief |
| Entertainment | Timing structure, contrast formula, remix ideas |

Choose the lightest useful structure. Don't over-package thin sources.

---

## Showcase Pages

Read `references/showcase.md` before generating. Never mention showcase pages in first-pass Fast.

**Two paths**:
1. **证据本位展示页** (default): evidence-based, source-clear, single-file HTML. For internal sharing, quick evidence archival.
2. **设计升级展示页** (requires open-design): professional visual design via `frontend-design` / `ui-ux-pro-max` skills.

**Hard rules**:
- Single self-contained `.html` with inline CSS/JS
- Images as `data:image/...` URLs
- No local-path references (`./`, `../`, `file://`, `C:\`)
- UTF-8, sanitized source text
- Visual QA before delivery
- Never overwrite delivered page during upgrades

---

## External Methodology Testing

When user asks to test an external project/methodology (e.g., "测一下这个 GitHub 项目"), do NOT wrap output in gg-dailian's format (来源锚点, 核心价值, etc.). Apply the external tool's own templates, fields, and output structure strictly.

---

## Platform Pitfalls

**知乎**: zse-ck anti-bot blocks all HTTP paths. Browser screenshot + OCR can get partial content. After 3+ failed methods, ask user for screenshot/text — don't loop.

**GitHub repos**: API rate limits → use browser console for README extraction or raw.githubusercontent.com for file content.

---

## Runtime & Tool Boundaries

1. Try built-in path first
2. Try 2-4 high-value alternatives if needed
3. Produce best limited analysis with evidence boundaries
4. Ask user for substitute input only when no self-service path remains

Warn before slow/costly operations: long video processing, many vision calls, large downloads.

---

## Quality Gates (check before finalizing)

**Evidence**: source identity clear? evidence level stated? missing layers named? claims vs interpretation separated?

**Value**: does output say why it matters? what can be learned/reused? is next step source-driven?

**Artifact**: format matches user's job? substance before polish? lighter output when source is thin?

**Showcase**: warranted by value? retains source boundaries? no local-path references? visual QA done?

**Output**: adapt to user level. No specialist vocabulary for general audience. Token control = removing waste, not making analysis thin.
