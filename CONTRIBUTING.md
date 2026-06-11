# Contributing to gg-dailian

## Public Case Rules

Repository examples, assets, showcases, eval cases, and release notes must use synthetic, public, or explicitly cleared material.

- ✅ Public domain, open-license, or clearly credited public material
- ✅ Synthetic cases created specifically for demonstration
- ✅ Material you own and explicitly clear for public use
- ❌ Confidential or internal project data
- ❌ Copyrighted material without permission
- ❌ Personal data or credentials

When unsure, mark the material as `needs_review` and keep it out of public commits.

## Skill Package Conventions

Each skill is an independently installable package:

- `SKILL.md` — Runtime entrypoint with triggers, workflow, and boundaries
- `references/` — Durable methods and rules (read on demand)
- `templates/` — Reusable output forms
- `examples/` — Reference outputs with source/evidence traceability
- `evals/` — Regression prompts and expected behavior
- `contracts/` — Shared schemas for cross-skill handoff

## Pull Request Guidelines

1. Public examples must be synthetic or cleared
2. SKILL.md frontmatter should match the package name
3. Relative links inside references/, templates/, and examples/ should resolve
4. Run `python scripts/validate_repo.py` before submitting

## Design Principles

- Evidence before opinion
- Feasibility before scope
- Cheapest evidence first
- Source boundaries explicit
- Fail closed: mark unknown, don't guess
