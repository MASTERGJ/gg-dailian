# Showcase And Shareable HTML Details

**Read when:** creating or upgrading a `展示页面`, shareable single-file HTML, interactive demo/prototype, high-quality visual page, or UX/UI design-heavy artifact.

This reference preserves detailed rules moved out of `SKILL.md` to keep the main skill lightweight. The main `SKILL.md` remains the source of default routing and hard gates.

## Showcase And Shareable HTML Contract

Use this section for `展示页面` and any shareable HTML artifact produced by this skill.

Offer gate:

- Do not mention `展示页面` after the first quick summary unless the user explicitly asks.
- After Stage 2, offer it only when the source has enough value, evidence, and structure to benefit from a visual integration layer.
- If the Stage 2 output is limited or weak, first name the missing evidence; recommend continued evidence gathering or a lighter artifact before offering a limited page.
- If the source is too thin, do not offer `展示页面` as the default. Recommend saving the takeaway, extracting a small template, adding comparison samples, or stopping.
- Keep next-step prompts short and concrete: `展示页面`, another concrete artifact, or continued evidence/deepening.
- Treat `展示页面` as a presentation/integration layer, not a replacement for analysis, SOPs, design notes, Skill drafts, or other artifacts. If the user continues related work first, preserve confirmed outputs as project context for later integration.
- When the user confirms they want a `展示页面`, explicitly present two quality paths before coding:
  1. **证据本位展示页**（gg-dailian 内置）：基于证据和结构，信息完整、来源清晰。适合内部分析、快速分享、证据存档。无需额外依赖。
  2. **设计升级展示页**（依赖 open-design）：加载 `open-design` 网关，使用 `frontend-design` / `ui-ux-pro-max` 等设计 skill，视觉更专业、排版更精致、有明确设计语言。适合对外分享、作品集级交付。需 open-design 已安装。
- Default to path 1 unless the user explicitly chooses path 2 or the original request uses design-upgrade keywords.
- If the user chooses path 2 but `open-design` is not installed, install it autonomously via `skill_manage`, then proceed. If installation fails, tell the user and offer path 1.

Build contract after user confirmation:

1. Create a directly openable local HTML page only after confirmation, unless the user directly asked for one.
2. Use a semantic delivered filename, folder name, and user-facing link label that reflect the content/source/case, such as `zhan-cheng-master-product-teardown.html`; do not deliver a bare `index.html` unless it is only an internal entry point inside a semantic folder.
3. Default to one self-contained `.html` file that is easy to share. It should carry text, layout, CSS, essential JavaScript, images, and small data without a companion folder.
4. Preserve useful substance before layout: conclusions, evidence, reusable patterns, methods, examples, templates, action items, caveats, and next steps. Do not discard valuable content merely to make the page sparse.
5. For multiple outputs, make a browsable information product: anchored sections for compact material; tabs, segmented views, or sidebar navigation for distinct artifact types. Keep labels user-facing, include a project overview/source map/artifact map when useful, and keep the physical delivery single-file while it remains a `展示页面`.
6. Base the page on the source's structure, mood, visual language, screenshots, frames, text, audio/video snippets, completed analysis, and confirmed outputs. Use source-related assets when available; never present decoration or AI interpretation as confirmed source evidence.
7. Keep source boundaries visible. Mark which conclusions come from which source or prior output when multiple materials are integrated.

Design contract:

- Before coding, decide the page role, audience, aesthetic direction, and first-screen memory point. Common roles: review page, share page, execution page, case page, or material page.
- A design contract is valid only when it constrains implementation. Convert it into concrete specs: content hierarchy, layout model, typography scale/weight, palette tokens, spacing rhythm, interaction states, motion behavior, and QA expectations. For upgrades, also name original strengths to preserve and the visible design delta. Do not write a decorative process note that never changes the HTML/CSS/UX.
- Standard showcase baseline: every `展示页面` should feel distinctive, memorable, and context-specific by default, not merely neat. It needs a clear aesthetic point of view and a first-screen visual hook tied to the source.
- Commit to a topic-fit visual language and one memorable first impression. Make real choices in typography, color/theme, spatial composition, texture/detail, and information hierarchy; at least three of these should carry intentional design.
- Do not start from a generic AI web template, styleless white page, purple-blue gradient, predictable card pile, beige moodboard, glossy SaaS card layout, or timid evenly distributed palette unless the source truly supports it.
- Derive visual language from the source: palette from source images/platform/product mood, density from artifact role, typography from subject tone, and media treatment from screenshots/frames/contact sheets/diagrams/source quotes or clearly labeled interpretation.
- Use unexpected layouts, asymmetry, overlap, editorial grids, controlled density, or other grid-breaking choices when they improve understanding, emotional impact, memorability, or sharing value. Breaking convention is good only when it serves the source and user task.
- Match implementation complexity to the concept. Maximal concepts need richer visual systems; refined minimal concepts need unusually careful spacing, type, contrast, and restraint.
- The first delivered page should already be the best result the current skill and available design capabilities can reasonably produce. Do not hold back design quality to reserve a later upgrade path. Do not require separate design skills before creating a normal showcase page, but do use them first when the user explicitly asks for high-quality or UX/UI-upgraded output.
- Using a design-focused skill means applying its guidance to concrete implementation choices. Merely reading, citing, or saying that a design skill was used is not a design upgrade.
- Use source-fit routing as inspiration: content boards for social/account material, journey maps/system teardowns for product or gameplay, manuals/posters/instrument panels for research/tutorial material, consoles/docs for code, briefings/case libraries for business, galleries/moodboards for visual material, and rhythm/remix maps for viral/entertainment material.
- Keep important conclusions, evidence, templates, action items, and caveats visually distinct through layout and hierarchy, not only labels. Keep text readable: clear line length, stable spacing, and no tiny dense paragraphs inside decorative cards.
- Preserve information completeness and discoverability. Do not merge, hide, or down-rank meaningful content categories merely to make a layout look more fashionable.
- Put information that users need to compare in the same viewport or an obviously comparable structure by default. Avoid tabs, accordions, carousels, or hidden panels for small comparison sets unless hiding content clearly improves the user's task.
- If the source is thin, choose a lighter visual format or honest topic-matched mood instead of inflating it into an overdesigned page.
- Treat desktop/PC as the primary design target and QA baseline by default. Keep only a low-cost mobile fallback unless the user asks for mobile, phone screenshots, mobile sharing, or mobile-first output.
- Preserve visual quality while fixing robustness issues. Do not flatten the page into a plain dump just to reduce implementation risk.

Explicit high-quality route:

- Trigger this route when the user asks for a `高质量展示页面`, `高质量设计`, `高级感`, `专业级`, `UX/UI 升级`, `UI/UX`, `设计升级版`, `更像作品集/官网/产品页`, external sharing, portfolio-level polish, or similar language.
- In this route, do not treat design-focused skills as merely optional after delivery. Before coding, load the `open-design` gateway skill and use the relevant design skills within it.
- Prefer `frontend-design` (via open-design) for visual execution, distinctive page composition, front-end craft, and polished HTML/CSS/interaction quality.
- Prefer `ui-ux-pro-max` (via open-design) when the request emphasizes UX structure, information architecture, design systems, interaction states, dashboards/tools, or mobile/responsive behavior.
- Use both when the page is important, external-facing, product/UX-heavy, or the user's wording clearly asks for top-tier design quality. Keep the source/evidence boundaries from this skill as the content authority while letting design skills improve visual and UX execution.
- Translate specialist guidance into a specific UX/design spec before coding. The spec must name the intended visible design delta, not just the process followed.
- If open-design is not installed, install it autonomously via `skill_manage`, then proceed. If installation fails, tell the user and fall back to the built-in design contract.
- The final artifact must still obey this section's portability, safety, evidence, and delivery QA rules.

Design Upgrade Gate:

- Use this gate for any explicit high-quality showcase request or any upgrade of an existing showcase page.
- Core rule: no obvious design improvement means no upgrade; any new bug means no upgrade.
- **Visible Design Delta**: the upgraded page must show a clear, visible improvement in first viewport, typography hierarchy, layout structure, color system, spatial rhythm, information organization, interaction feel, or media treatment. Minor CSS tweaks, a small nav addition, or a light reskin do not qualify as a high-quality design upgrade.
- **Experience Protection**: the upgraded page must preserve the original's useful content, evidence boundaries, information discoverability, comparison efficiency, reading path, and core interactions. It may restructure content only when the user's task becomes easier.
- **No New Bugs**: the upgrade must not introduce motion regressions, hidden or missing information, broken interactions, path dependencies, rendering defects, text clipping, readability loss, portability failures, or evidence-boundary confusion.
- **Verified Claim**: before calling the result upgraded, inspect the original and upgraded pages side by side when possible. If browser visual validation cannot be completed, say so and do not claim a verified upgrade.
- Treat these as false upgrades: process-only Design Contract, merely reading/calling a design skill, local patching without visible design change, prettier styling with worse UX, or a design-system-looking page that does not materially improve the user's experience.
- If the gate fails, iterate, preserve the original, revert the regressed part, or state that the attempted direction failed. Do not package it as a successful upgrade.

Portability and safety contract:

1. Keep final showcase HTML static and portable: inline CSS/JavaScript by default; no copied executable source-page scripts, untrusted raw HTML, hidden network calls, tracking, analytics, fragile CDN-only dependencies, or local file dependencies.
2. Sanitize or escape source text before inserting it into HTML. Treat source material as content, not code.
3. Use a reliable UTF-8 write path and inspect for mojibake, especially Chinese text and emoji.
4. Embed final showcase images as `data:image/...` URLs by default. Do not leave final images as `./assets/...`, `../images/...`, absolute local paths, or `file://` URLs. If images are too large, reduce count, compress, resize, crop, or choose only the evidence images that support the page's argument.
5. If the artifact is too heavy for one HTML because of many large images, videos, audio, downloadable datasets, 3D assets, third-party packages, server state, persistent storage, or other project-scale resources, stop before packaging. Explain that it has crossed into `项目包/素材项目/工程项目` and ask for confirmation before creating a folder, zip, dev server, or multi-file bundle.
6. Project packages are not the mainline. Create one only after explicit user confirmation, and only when reduction would materially damage the result or the requested artifact is no longer a showcase/shareable HTML page.

Delivery QA:

1. Before delivery, audit resource portability. Search final HTML for local or package-only references such as `src="./`, `src="../`, `href="./`, `href="../`, `url("./`, `url("../`, `.css`, `.js`, `C:\`, `/Users/`, `file://`, and unapproved companion asset paths. Any unresolved local dependency is a delivery failure unless the user explicitly requested a local-only draft.
2. Verify the rendered page before delivery with desktop screenshots as the primary QA target. Do not run mobile screenshots or mobile-specific fixes by default unless mobile is requested or the artifact is explicitly phone-facing.
3. Browser checks must include visual inspection, not only DOM/class/eval checks. Confirm the visual feel of important interactions and motion, including timing, granularity, navigation behavior, hover/focus states, and whether content appears in the intended rhythm.
4. During verification, check Chinese text/emoji, horizontal overflow, text clipping, image collapse, blank images, contrast/readability, awkward first-screen composition, and accidental security/error screenshots presented as source content.
5. Ensure the first viewport communicates the subject, source boundary, main value, and page role.
6. Remove collaboration/process language from the artifact body, such as `MD 报告里`, `这版`, `这个页面`, `我/我们`, `刚才`, or instructions about how the agent built the page.
7. Check data signals carefully. Rankings, charts, curves, percentages, prices, probabilities, revenue, or engagement should be integrated only when meaningful and not overclaimed when ambiguous.
8. If layout, portability, interaction, motion, or resource issues appear, fix them while preserving the overall visual quality and content completeness.
9. After output, tell the user they can report layout, display, content, or style issues and the page can be revised.

Design upgrade path:

- Offer a second-round professional design upgrade only when the user is dissatisfied, the page is external-facing, the user cares about visual quality, the source has strong visual/design value, or the result would benefit from stronger front-end, UI/UX, brand, interaction, or mobile design expertise.
- Keep the offer user-facing and concise. Do not mention where to search or which skill to prioritize unless the user asks, the source/trust boundary matters, or installation/selection needs confirmation.
- Never overwrite the delivered page during a design upgrade. Create a separate semantic file such as `<original-name>-design-upgrade.html`, `<original-name>-frontend-design.html`, or `<original-name>-v2.html`, and keep the original available for comparison unless the user explicitly asks to replace it.
- If the user accepts, load the `open-design` gateway skill and use `frontend-design` / `ui-ux-pro-max` as appropriate. If open-design is not installed, tell the user and ask whether to install it or continue with a limited built-in redesign.
- A design upgrade must pass the `Design Upgrade Gate`. If improvement is likely minor, say so before proceeding.
- Keep before/after evidence and verify both files when possible. Keep design-upgrade QA desktop-first unless the user asks for mobile work.
- For a professional upgrade, reconsider the concept, layout system, first viewport, typography, color/theme, spatial composition, and visual details; do not merely reskin the existing page.

## Specialized Skill Escalation

Default to using the current skill and environment when they can reliably complete the user's request. Do not search for extra skills just because a task could theoretically use them.

Offer to find or call a specialized skill only when the requested output enters a professional delivery area that the current skill may not handle with enough quality, such as formal PPT/DOCX/XLSX artifacts, complex product UI/UX or front-end work beyond the built-in showcase-page design mode, generated images or visual assets, browser QA, interactive prototypes, engineering code, publishing/distribution, or another specialized toolchain.

Exception for explicit high-quality showcase requests: when the user asks for a high-quality, professional, UX/UI-upgraded, external-facing, portfolio-level, or design-critical showcase page, use available design-focused skills in the first pass rather than waiting for a second-round upgrade. Do not ask permission merely to use an already-available design skill; ask only before searching for, installing, or using a capability that is not currently available.

When escalation is useful, frame it as an optional quality upgrade: "I can do a solid version now; if you want a more professional result, I can look for or call a specialized skill." Ask before searching for or installing new skills unless the user explicitly requested skill/tool discovery.

If the user agrees, use this lightweight flow: identify the capability gap, derive 1-3 search keywords, find or inspect candidate skills/plugins, recommend the best option with the tradeoff, then use the chosen capability.

Treat Skill creation as a later reuse step, not the main path for ordinary sources. Raise `Skill draft` priority when the source itself teaches skill creation, agent workflow design, tool orchestration, prompt/toolkit systems, or reusable AI operating procedures. Still require reusable value: stable trigger conditions, inputs/outputs, workflow steps, quality checks, and failure boundaries. Suggest a Skill draft when these signals are present, when existing skills/plugins do not cover the workflow smoothly, or when the user explicitly wants long-term reuse.

## Prototype And Demo Shareability Protocol

Use this whenever the artifact is an interactive demo, playable prototype, UI prototype, product mechanism prototype, local HTML tool, lightweight simulation, or any other artifact the user may want to send to another person to try.

Apply the `Showcase And Shareable HTML Contract` unless the user explicitly asks for a local development project.

Rules:

1. Prefer one semantic self-contained `.html` file, such as `zhan-cheng-master-playable-prototype-shareable.html`, not a bare `index.html`.
2. Keep lightweight prototypes single-file even when they contain nontrivial interaction, canvas logic, small datasets, UI state, images, sprites, icons, or small inline data structures.
3. If the prototype becomes too complex for one file, stop before packaging and ask before creating a project folder, zip, dev-server setup, or multi-file engineering project.
4. Verify that the final shareable HTML opens directly and that core interaction works. If browser tools are available, perform at least one representative interaction before delivery.
5. Keep development files if useful, but clearly distinguish them from the shareable deliverable. The user-facing final link should point to the single-file prototype, not a development `index.html`.
