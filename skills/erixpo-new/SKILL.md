---
name: erixpo-new
description: Start a new product with erixpo. Interview the user (surface is mandatory, never default to web), research current best stack for this job, present 2-4 choices, write a plan with slice 0 scaffold when the folder has no project, wait for approval. Use when the user wants a new app, site, SaaS, script, desktop, mobile, robot software, wiki, assistant, or any greenfield work.
license: MIT
metadata:
  author: Erixpo
  version: "0.7.0"
---

# erixpo-new

Greenfield or "I want to build X". Do not jump to code.

Read [intent.md](../erixpo/references/intent.md) and [ceremony.md](../erixpo/references/ceremony.md) up front. Load [domains.md](../erixpo/references/domains.md), [scaffold.md](../erixpo/references/scaffold.md), [judgment.md](../erixpo/references/judgment.md) on demand when the phase needs them — do not preload all five.

## Phase A — Infer, then at most one question

Follow [intent.md](../erixpo/references/intent.md). Infer job, surface, `like X`, must-have from the sentence and this folder. **Do not default to web.** Do not open with a form.

If surface is still unknown **and** files do not decide it, ask **one** question. If they already named a surface, skip that question. A reference alone may not establish a platform. Ask further focused questions only when an unresolved constraint changes a consequential decision; do not treat the initial one-question rule as a ban on necessary clarification.

Follow the adaptation contract in domains.md for any project, including robotics, graphics, animation and unfamiliar tools. Application interface: load `erixpo-ui` only when the work includes one; standalone visual artifacts use domain-specific composition and preview/export checks instead of app UI ceremony. Write `documents/ui/` before product chrome. HTML mockups only when surface is web (or last-resort wire). Native uses `documents/ui/mapping.md`.

If the folder has **no project** (empty or nearly empty): the plan's **slice 0 is scaffold** ([scaffold.md](../erixpo/references/scaffold.md)). Acceptance: the smallest valid project/artifact opens, builds, renders or runs in its actual toolchain and its domain-appropriate `check:` runs. Before UI chrome and before feature slices.

## Phase B — Research

Follow [research.md](../erixpo/references/research.md) (**full** for new). Open current official sources for the actual versions: official init, platform guide, **comparables** (2–3 similar products for this surface, plus any `like X`), test runner. Complete the full-pass coverage in that protocol for relevant areas only: domain-specific craft/engineering, UI layout/accessibility when an interface is present, and applicable compliance. Discover skills/MCP capabilities only when a concrete gap exists; otherwise record one short `no additions needed`. Omit empty research sections. Write the evidence and decisions in `.erixpo/research.md`, including concrete project-local installation proposals when useful; obtain authorization before adding third-party capabilities.

Do not use memorized defaults. Novelty is optional. The reframe is not.

## Phase C — Choices

USER `ask-every-slice`: 2–4 options + "write your own" for expensive decisions; wait.

Otherwise: pick the **official default**, write why + the rejected non-obvious option, put it in the plan. Still wait for **go** unless they already said go / you pick / unattended.

## Phase D — Plan

Write `.erixpo/plan.md` from the rich template (same content as pack `templates/erixpo/plan.md`):

- Product in one paragraph
- **Ceremony** field
- Non-goals
- Chosen stack
- **Slice 0 scaffold** if greenfield (acceptance = official project opens/builds and check runs)
- UI spec pointer (`documents/ui/`) if there is a surface; **UI change-type** per slice
- Slices in order (each slice has acceptance + **Tests to add** + UI tokens/components touched + check that **runs tests**)
- Edge cases to handle in v1
- Test plan pointer (`.erixpo/test-plan.md`)
- Suggested extras the user did **not** ask for as a separate optional list

Show the plan. Keep optional extras separate. Follow intent.md: wait for **go** only when execution is not already authorized; prior "go", "you pick" or unattended authorization carries forward. Unapproved extras do not block approved work.

Update `.erixpo/state.md` (not `state.yaml`) to `phase: planned`. On approval: `phase: approved`, then immediately load `erixpo-auto`.
