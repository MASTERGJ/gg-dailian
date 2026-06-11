# Artifact Conversion And Distillation Details

**Read when:** turning analysis into SOPs, workflows, playbooks, tutorials, Skill drafts, memory/wiki entries, production kits, or other reusable artifacts.

This reference preserves detailed rules moved out of `SKILL.md` to keep the main skill lightweight. The main `SKILL.md` remains the source of default routing and hard gates.

## Artifact Source And Evidence Footer Protocol

Use this for reports, product analysis pages, market/case teardown pages, showcase pages, internal wiki-style pages, and any artifact that contains analytical conclusions, data signals, screenshots, quotes, source-derived claims, or AI-assisted synthesis.

The default rule: serious analysis artifacts should include a lightweight source/evidence area. This is not an academic bibliography. Its purpose is to establish credibility, preserve traceability, and make the artifact usable as a knowledge node.

Why this matters:

- It shows the artifact is grounded in inspected material instead of unsupported generation.
- It helps readers trace back, verify, continue research, or understand evidence limits.
- It reduces anxiety around AI hallucination, especially in internal reports, product analysis, market analysis, and leadership-facing pages.
- It separates source evidence from agent interpretation, so the reader can tell what was observed and what was inferred.

Risks to manage:

- A large reference block can damage visual polish or immersion.
- Overly detailed references can expose internal paths, private documents, or unnecessary process traces.
- Source lists can invite detailed scrutiny, so data and claims must be handled carefully.

Design rules:

1. Prefer productized light sourcing over academic citation. Use labels like `资料来源`, `Sources`, `证据范围`, `Evidence scope`, or `资料来源与证据边界`.
2. For shareable showcase pages, place sources near the bottom or in a visually quiet expandable/details area unless the page's purpose requires source-first reading.
3. Do not dump raw local paths, long file-system paths, internal working filenames, or process language. For local materials, show source type and readable file name or category only.
4. Public URLs may be included when they are useful for follow-up reading and safe to expose, but avoid turning a polished page into a wall of links. Use concise labels or a collapsed source list when there are many.
5. For internal or private materials, cite source categories and evidence boundaries instead of exposing confidential paths, for example `internal prototype notes`, `captured UI screenshots`, `DataEye trend screenshots`, or `gameplay key frames`.
6. Do not treat AI as an evidence source. AI can be described as the analysis or synthesis method only when relevant. Real sources are articles, screenshots, videos, datasets, documents, logs, interviews, product builds, or other inspected material.
7. Include evidence boundaries when data or screenshots support conclusions. State what was confirmed and what was not, such as `榜单截图只支持排名位置判断，不推导收入、留存或 ROI`.
8. If the artifact is a brand/landing/worldview/purely immersive page, sources may be omitted or greatly minimized when they would harm the intended experience and the page does not make serious analytical or data-backed claims.
9. If the artifact is an analysis report, product teardown, market brief, data-backed showcase, or internal knowledge page, omitting all sources is usually a quality problem.

Useful lightweight footer shapes: a compact `资料来源与证据边界` paragraph, or a short grouped list such as market signals, gameplay evidence, system evidence, and analysis boundaries.

## Output Layout Discipline

Keep first-pass reports easy to scan. Do not squeeze adjacent fields into the same paragraph.

Rules:

1. Put `来源锚点`, `标题`, `来源信息`, `时长/阅读成本`, `内容总结`, `最有价值的部分`, `适合谁`, `对 AI 的用处`, `建议下一步`, and `如果继续深入` on separate blocks.
2. Leave one blank line between top-level blocks.
3. Keep `来源信息` to one compact metadata line when possible.
4. Use bullets only inside content sections that need multiple points; avoid nested bullets in normal output.
5. If a field is unavailable, write it briefly in that field instead of merging it into another field.
6. Format `来源锚点` as 3 short metadata lines after the label: `类型：... | 日期：...`, `原题：...`, and `链接：...`.
7. In normal user-facing Markdown, bold top-level field labels consistently, such as `**来源锚点：**`, `**标题：**`, and `**来源信息：**`.
8. Inside `来源锚点`, keep sublabels plain, such as `类型：`, `原题：`, and `链接：`. Do not bold some top-level labels while leaving others plain.

## Artifact Language Separation

Final artifacts must be separated from collaboration and work-process language.

Use this rule for showcase pages, reports, docs, briefs, demos, playbooks, memory entries, Skill drafts, and any other deliverable the user may read, share, or reuse.

Core rule: collaboration language is for aligning work with the user; artifact language is for the artifact's external reader. Do not let collaboration language enter the final artifact body.

Common contamination patterns:

- Mentioning the working process: `MD`, `报告里`, `已有材料`, `这版`, `这个页面`, `展示页`, `我/我们刚才`, `应该被放在第一层`.
- Explaining the agent's construction choices inside the artifact: `这不是图片陈列`, `我把...串起来`, `这里用来说明`.
- Addressing the user instead of the artifact's reader, unless the artifact is explicitly a personal note or chat transcript.

Required cleanup pass before delivery:

1. Search the artifact for process markers such as `MD`, `报告里`, `这版`, `页面`, `展示页`, `已有`, `我`, `我们`, `刚才`, `应该被`, `不是图片陈列`.
2. Keep them only when they are part of an explicit source/caveat section and genuinely useful to the reader.
3. Rewrite contaminated text from the source or product object's perspective.
4. Final artifact body should answer the external reader's questions: what it is, why it matters, what evidence supports it, what pattern can be reused, and what caveats remain.

## Artifact And Material Value Methodology

The user does not need to know which artifact or material treatment is professionally appropriate. The agent owns that judgment.

For every meaningful source or project, decide three things before producing the artifact: analysis object -> best artifact role -> high-value material treatment.

### 1. Identify the analysis object

Classify what the source primarily is, not only its file format:

- **Product/game case**: gameplay, system design, market performance, monetization, retention, onboarding, UI/UX, prototype reconstruction.
- **Market/business material**: rankings, trend curves, revenue, users, categories, competitors, channels, cost, conversion, growth, risk.
- **Visual/UI material**: screenshots, screen flows, layout systems, component states, interaction feedback, visual hierarchy.
- **Content/social material**: hook, title, script, rhythm, emotion, propagation, account positioning, reusable content format.
- **Tutorial/course/workflow**: method, steps, prerequisites, mistakes, practice path, operating checklist.
- **Opinion/report/article**: argument structure, evidence quality, assumptions, implications, reusable framework.
- **Entertainment/viral sample**: emotional trigger, timing, contrast, character, meme/remix potential.

### 2. Choose the artifact role

Pick the output that best serves the object and the user's likely need:

- Product/game case -> teardown report, system map, UX flow, prototype spec, mechanism playbook, showcase page.
- Market/business material -> decision memo, market brief, evidence board, competitor table, risk/opportunity map.
- Visual/UI material -> UX blueprint, annotated source image, component anatomy, style rules, redesign notes.
- Content/social material -> hook library, script template, post format, content calendar, imitation guide.
- Tutorial/workflow -> SOP, checklist, practice plan, lesson notes, prompt/toolkit.
- Opinion/report/article -> argument map, executive brief, critique, knowledge note.
- Entertainment/viral sample -> rhythm teardown, remix kit, sample library, creative prompts.

### 3. Treat materials by value

Do not process all material equally. Assign each item a job:

- **Main evidence**: directly supports the core conclusion; should shape structure and be presented clearly.
- **Mechanism evidence**: explains how the object works; use in diagrams, flows, annotated screenshots, or focused sections.
- **Context evidence**: helps establish market, source, time, audience, category, or credibility; keep concise.
- **Texture material**: helps mood, tone, visual language, or examples; use sparingly.
- **Low-value/noise**: repeated logos, QR codes, decorative images, weak snippets, unrelated recommendations, generic screenshots; exclude unless they reveal distribution, monetization, or trust signals.

When building a serious analysis report, product teardown, market brief, or showcase page:

1. Start from the strongest conclusion the material can support.
2. Select only the materials that make that conclusion clearer, more credible, or more reusable.
3. Let high-value charts, rankings, UI screenshots, probability tables, price panels, or system diagrams influence the artifact's structure.
4. Do not bury important evidence in captions.
5. Do not inflate low-value material just because it is available.
6. If the best artifact is not what the user originally named, proceed with the user's requested artifact but improve its structure using this judgment.

## Production Judgment Depth

The first-pass `建议下一步` must be a production judgment, not a shallow menu of artifact names.

When recommending what to do next, include:

1. **Recommended artifact**: the single most useful next artifact, such as summary, report, SOP, playbook, tutorial, demo, prompt, Skill draft, memory entry, content kit, or showcase page.
2. **Why this artifact**: what structure, method, visual pattern, workflow, argument, data, or reuse value in the source supports that choice.
3. **Depth level**: whether it should be a light note, detailed breakdown, execution playbook, reusable toolkit, showcase page, or long-term knowledge entry.
4. **Expected contents**: concrete modules the artifact would contain, such as workflow steps, checklist, title library, shot list, prompt set, data table, calendar, metrics, code demo, visual rules, risk list, or iteration path.
5. **What not to do**: briefly say what would be overkill or low value when relevant.

If the user asks for imitation, account/content planning, marketing cases, operational strategy, or practical execution, bias Stage 2 toward an actionable playbook/toolkit instead of only a descriptive analysis. A high-value output may include:

- core formula
- reusable templates
- title/hook/script library
- shooting or production checklist
- publishing calendar
- data tracking table
- from-imitation-to-original iteration path
- quick-start checklist

Before creating a `展示页面`, check whether the completed Stage 2 output is actionable enough for the user's goal:

- If the user wants review or presentation, a visual analysis page may be enough.
- If the user wants imitation, execution, learning, content production, or operations, upgrade the content into a playbook/toolkit before or while making the page.
- Do not merely beautify a shallow analysis when the user actually needs a usable production artifact.
- If the source is too thin for a meaningful page, recommend a lighter artifact or comparison set instead of manufacturing a hollow showcase.

## Value Gap Prevention

When the user states an execution intent after the first pass, reinterpret the source through that intent before continuing. Signals include imitation, account/content templates, operations, topics/titles/scripts, methodology, team use, tutorial/SOP, or execution package requests.

In these cases, the main job is no longer to describe the source. The main job is to extract what can be reused, turned into decisions, or executed.

Use this depth ladder:

1. **Description**: what the source says or shows.
2. **Deconstruction**: how it is structured, why it works, and what patterns repeat.
3. **Production kit**: templates, libraries, checklists, calendars, prompts, metrics, examples, and iteration rules the user can apply.

Do not stop at level 1 when the user's intent is level 3.

Before finalizing a Stage 2 result or turning it into a `展示页面`, check whether the output directly helps the user act and whether it lacks templates, checklists, case libraries, steps, or evaluation criteria.

If the answer reveals a gap, add the missing production modules before packaging or presenting the result.

For content/account imitation, a high-value Stage 2 output should usually include:

- source style formula
- reusable content structure
- title/hook library
- caption/script templates
- visual or shooting rules
- topic calendar
- publishing rhythm
- metrics and review table
- imitation-to-original upgrade path
- quick-start checklist

The `展示页面` should then present this production kit clearly. It should not turn a low-action analysis into a visually polished but low-value page.

## Application Artifact Conversion

After meaningful analysis, actively consider what the source can become for the user. The default next step is not always more analysis; it may be a usable artifact.

Match artifact type to source value:

- Method value -> SOP, checklist, workflow, operating guide, prompt set.
- Learning value -> lesson notes, practice plan, exercises, concept map, review questions.
- Case value -> case teardown, comparison table, decision rules, risk list, review template.
- Expression value -> hook formula, writing template, title library, script/caption library.
- Visual value -> style rules, shot list, mood board, UI/UX notes, showcase page.
- Production value -> content kit, publishing calendar, data tracking table, execution pack.
- Knowledge value -> memory/wiki entry, research brief, reference note.
- Entertainment value -> timing structure, contrast formula, remix ideas, sample library.

The practical test is simple: if the user wanted to act tomorrow, what would they need in hand? Add that missing structure when the source can support it.

## Memory and LLM Wiki Integration

This skill can act as an ingestion and pre-processing layer for memory systems, LLM Wiki-style knowledge bases, AI second brains, or long-term agent memory.

Use this when the user asks about memory, knowledge bases, LLM Wiki, wiki entries, durable notes, long-term recall, or saving analysis for future use.

Recommended role split:

- gg代练: read the source, produce a grounded summary, label evidence level, identify useful concepts, suggest links, and create a clean entry draft.
- Memory/wiki system: store durable entries, preserve source anchors, maintain backlinks, support future retrieval, and manage updates or contradictions over time.

When preparing content for a memory or wiki system, include only useful durable fields: title, source anchor, evidence level, core conclusions, reusable method, related topics, follow-up actions, and limitations.

Before creating a memory entry, decide whether the source is worth storing:

- Suitable for memory: reusable workflows, stable concepts, methods, examples, decisions, design patterns, prompt patterns, source summaries worth future retrieval, or material the user explicitly wants to keep.
- Not ideal for memory: one-off entertainment, weak snippets with no durable value, duplicate entries, unverified claims, transient news unless date-stamped, or raw transcript dumps.

Rules:

1. Do not dump raw transcripts or long page text into memory unless the user asks.
2. Preserve source anchors and evidence levels so future agents know what was confirmed.
3. Separate durable knowledge from one-off task output.
4. Flag contradictions, stale claims, and weak evidence instead of silently merging them into memory.
5. If the target memory system has its own schema, adapt the entry to that schema.
6. If evidence is weak but the user still wants storage, label it as a weak or provisional memory entry.
7. Prefer compact entries that future agents can retrieve and act on, not decorative summaries.

## Output Templates

Use templates as information contracts, not rigid prose. For first-pass analysis, follow the standard card in `First-Pass Gate`; adapt wording, order, and density to the source and user goal without dropping traceability, evidence level, summary, value judgment, or next-step guidance.

For artifact outputs, choose only the modules that matter:

- workflow/skill: reusable pattern, input, process, output, generalization value
- demo/prototype: demonstrable mechanism, minimum useful version, key UI/interactions, scope control
- design/playbook: design goal, core mechanism, user/player experience, system structure, executable suggestions
- content/marketing kit: style formula, hooks/titles, script/caption templates, production checklist, publishing rhythm, metrics

Do not force every module into every artifact. If a section does not help the user act, learn, decide, share, or reuse the source, omit it.
