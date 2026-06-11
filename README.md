# gg-dailian

gg代练 — A verifiable agent-skill for source intelligence and artifact distillation. Turns external material (videos, web pages, screenshots, audiovisual references, local materials) into evidence-grounded understanding, value judgment, reusable structure, and user-facing artifacts.

[简体中文](README.zh-CN.md) · [English](README.en.md) · [SKILL.md](SKILL.md) · [License](LICENSE)

---

## What This Is

gg-dailian is a public agent skill for AI-assisted source intelligence work. It turns media analysis, web research, visual evidence processing, and artifact creation into reusable agent instructions, references, schemas, templates, examples, and evals.

It is not a prompt collection. It is a compact operating system for serious source work, with evidence boundaries, source-type routing, value threshold gates, and artifact output contracts:

```
source → understanding → value judgment → reusable pattern → user-facing artifact
```

## What Makes It Different

- **Evidence-first**: judgments point back to sources, screenshots, timestamps, and extraction methods
- **Source-type routing**: video, web page, screenshot, text — each gets a tailored evidence path
- **Value-gated**: not every source deserves a full artifact. Thin sources get compact takeaways
- **Artifact-driven output**: SOPs, playbooks, tutorials, showcase pages, knowledge notes, skill drafts
- **Agent portable**: Markdown-skill-capable agents can adapt the package
- **Public/private safe**: public examples stay synthetic or cleared; real projects stay local

## Quick Start

### 1. Pick your source type

| Source | What you get |
|--------|-------------|
| YouTube / Bilibili URL, local video | Evidence-linked analysis, transcript/ASR, key frames, value judgment |
| Web page, WeChat article | Readable text extraction, visual evidence, source credibility check |
| Screenshot / image | OCR, visual inspection, layout analysis |
| Mixed source set | Source map, cross-referenced analysis |

### 2. Try a minimal prompt

```
Use gg-dailian to analyze this video into timestamped evidence, core value, reusable patterns, and next step recommendation.
```

```
Use gg-dailian to extract key claims from this article into a knowledge note with evidence boundaries.
```

### 3. Install

Copy the skill folder into your agent's skill directory:

```bash
cp -r gg-dailian/ ~/.hermes/skills/
# or
cp -r gg-dailian/ ~/.claude/skills/
```

## Skill Architecture

| Layer | Path | Purpose |
|-------|------|---------|
| Runtime entrypoint | `SKILL.md` | Agent instructions, triggers, workflow, boundaries |
| Methodology | `references/` | Source-type routing, evidence rules, artifact rules, runtime troubleshooting |
| Templates | `templates/` | Reusable output forms and structures |
| Examples | `examples/` | Reference outputs with source/evidence traceability |
| Quality | `evals/` | Regression prompts and expected behavior |
| Contracts | `contracts/` | Shared schemas for cross-skill handoff |
| Scripts | `scripts/` | Media finder, web analyzer, video subtitle, ASR helpers |

## Source → Value Pipeline

1. **Quick observation**: low-cost first impression and value judgment
2. **Deep deconstruction**: identify value type and how the source works
3. **Value threshold**: decide artifact scale based on source substance
4. **Artifact conversion**: turn value into practice, templates, checklists, SOPs
5. **Durable expression**: package strong results into showcase pages, documents, knowledge notes

## Use Cases

- Video content analysis with evidence indexing
- Web page research with visual evidence validation
- Screenshot-based UI/UX inspection
- Mixed-source competitive analysis
- Knowledge base curation from scattered materials
- Shareable showcase page generation

## Repository Layout

```
gg-dailian/
├── SKILL.md              # Agent entrypoint
├── README.md             # You are here
├── README.zh-CN.md       # 中文说明
├── LICENSE               # MIT
├── references/           # Methodology documents
│   ├── video.md          # Video/audio source handling
│   ├── web.md            # Web page visual evidence
│   ├── showcase.md       # Showcase HTML rules
│   ├── artifact.md       # Artifact conversion rules
│   └── runtime.md        # Tooling and troubleshooting
├── templates/            # Reusable output forms
├── examples/             # Reference outputs
├── evals/                # Quality regression tests
├── contracts/            # Shared schemas
├── scripts/              # Helper scripts
└── assets/               # README visuals
```

## Design Principles

- Evidence before opinion
- Cheapest evidence first
- Source boundaries explicit
- Artifact format matches user intent
- Fail closed on evidence: don't guess what wasn't retrieved

## License

Skill documents and tooling are released under the MIT License.
