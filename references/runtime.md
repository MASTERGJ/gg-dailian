# Runtime Tooling And Failure Details

**Read when:** tooling, scripts, cost/friction warnings, dependency failures, package/setup issues, install troubleshooting, or when a tool layer fails.

This reference preserves detailed rules moved out of `SKILL.md` to keep the main skill lightweight. The main `SKILL.md` remains the source of default routing and hard gates.

## Runtime And Install Boundary

Keep ordinary source analysis focused on the user's material. Do not load or explain install/dependency details unless the user is installing the skill, asking how setup works, or a required runtime dependency fails.

Rules:

1. Before saying a task cannot be done, check whether the current environment exposes files, shell commands, browser rendering, package installation, or the needed media tools.
2. If a built-in path exists and tools are available, use it directly. If setup is missing but can be prepared in the current environment, prepare it unless the user said not to.
3. Keep troubleshooting bounded: try the built-in path plus 2-4 high-value alternatives, then produce the best limited analysis and name the missing evidence layer.
4. Do not make the user solve tooling problems unless no reasonable self-service path remains.
5. Do not phrase dependency or download failure as "the content cannot be analyzed". Say which layer failed and what substitute input would unblock analysis, such as local media, screenshots, copied text, direct media URL, or transcript.
6. For install, dependency, mainland-China mirror, FFmpeg, Python package, model download, or offline setup details, read `INSTALL.md` only when that path is actually relevant.
7. If the user only asks how to use the skill, give a short onboarding: accepted inputs, quick judgment -> deeper analysis -> optional artifacts, evidence honesty, and 2-3 example prompts.

## Cost and Friction Warnings

When the user wants to continue deeper, decide the next technical step yourself, but warn before proceeding if it is likely to be slow, costly, fragile, or storage-heavy.

Warn in plain user-facing terms, not tool jargon:

- Long audio/video may take several minutes.
- Visual analysis may consume many model tokens or require reading many frames.
- Downloading video may use network bandwidth and disk space.
- Some platforms may block access, require cookies/login, or provide incomplete data.
- ASR/transcription quality may be imperfect for noisy audio, mixed languages, music, or domain terms.

Keep the warning short and actionable: name the likely cost, recommend the cheapest useful next step, and avoid over-explaining minor costs.

If the extra cost is minor, do not over-explain. Just proceed.

## Proactive Deep-Dive Prompting

If a source appears unusually valuable, the agent should proactively suggest deeper analysis, but should not automatically start expensive work unless the user already asked for it.

Recommend further digging when the source has one or more strong value signals:

- reusable workflow, method, prompt pattern, production pipeline, or decision framework
- dense visual evidence such as UI flows, gameplay systems, charts, dashboards, slide sequences, or long images
- strong case-study value, unusual execution detail, or transferable creative pattern
- material that can become a concrete artifact: SOP, playbook, tutorial, design note, demo plan, prompt kit, memory/wiki entry, or showcase page
- missing evidence that would materially change the conclusion if obtained

The prompt should be specific and cost-aware: say what deeper work could unlock, name the cheapest useful next step, mention meaningful time/token/bandwidth/storage cost, and offer a lighter alternative when the source is promising but not yet proven.

Do not pressure the user into deeper work. If the source is thin, entertaining but shallow, weakly accessible, or only useful as a small inspiration sample, recommend a compact takeaway, lightweight template, comparison sample, or stopping point instead.

## Tooling

All scripts are in `scripts/`. Keep this section as a routing guide, not a full parameter manual. When uncommon options are needed, run the relevant script with `--help` instead of relying on memorized parameters.

Default routes:

- `video_subtitle.py`: main entry for video metadata, subtitles, optional ASR, optional vision, and report signals.
- `web_analyzer.py`: readable text from normal web pages.
- `media_finder.py`: fallback for pages that appear to contain exposed MP4/WebM/M3U8 media when normal extraction fails.
- `video_vision.py` and `video_asr.py`: direct specialist tools when the user specifically needs frame extraction or ASR.

Common commands:

```bash
python scripts/video_subtitle.py <url-or-id> -f text-only
python scripts/video_subtitle.py <url-or-id> -f text-only --asr
python scripts/video_subtitle.py <url-or-id> -V --vision-max-frames 24
python scripts/video_subtitle.py <url-or-id> -R
```

Use vision only when text is insufficient and screen content, gameplay, UI, slides, visual effects, dashboards, code, or demonstrations carry meaning. After vision extraction, inspect `contact_sheet.jpg` and `manifest.json` before selecting individual frames.

## Script Help And Runtime Limits

Do not maintain a full option table in this file. The scripts expose their own help:

```bash
python scripts/video_subtitle.py --help
python scripts/video_vision.py --help
python scripts/web_analyzer.py --help
python scripts/media_finder.py --help
```

Remember the practical limits: ASR may take minutes, vision uses bandwidth/disk/model tokens, restricted Bilibili videos may need cookies, and missing Python packages or FFmpeg are runtime setup issues. For dependency installation, mirrors, offline setup, or detailed troubleshooting, read `INSTALL.md` only when needed.

## Known Hard Platform Blocks

These platforms use strong anti-bot measures that reliably block automated HTTP/API access. Do not spend more than 2-3 attempts bypassing them — produce a limited analysis and name the missing layer.

### Zhihu (知乎专栏 / zhuanlan.zhihu.com)

- **Block type**: 403 + zse-ck bot detection (JavaScript challenge)
- **Attempts that failed**: direct curl, mobile UA, desktop Chrome UA, zhuanlan API (`/api/posts/`, `/api/columns/p/`), jina.ai proxy (captcha wall), Google cache (empty/mangled), archive.org (no snapshot)
- **What may work**: real browser with login cookies, user-provided screenshot/copy-paste
- **Fallback**: use screenshot + OCR via desktop automation if browser is available, or ask user for copied text
- **Evidence label**: `页面截图OCR判断（未登录）` or `用户提供文本`
