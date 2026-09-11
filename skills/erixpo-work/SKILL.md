---
name: erixpo-work
description: General work inside this repo that is not building a product. Use when the user wants research, writing, ops, automation of a folder, personal-assistant tasks, notes, planning their work, or any non-product job specialized to this repository. Same loop as software — profile, memory, plan, do, check, learn — with a check command that fits the job. Ceremony is light by default.
license: MIT
metadata:
  author: Erixpo
  version: "0.7.0"
---

# erixpo work

Not every `/erixpo` is "build an app". This track is for work **in this folder** that is still real work: research, writing, automation, ops, assistant tasks, personal systems.

For recurring work, specialize to **this folder**. Read governing files and only relevant sections of `.erixpo/PROFILE.md`, `.erixpo/MEMORY.md`, `.erixpo/USER.md`, `AGENTS.md`, and `documents/`; do not load every memory file for a one-shot or iteration. Read [ceremony.md](../erixpo/references/ceremony.md) and [domains.md](../erixpo/references/domains.md) when relevant.

## Ceremony

**Light by default.** Do not invent a SaaS. A Python script does not get a SaaS wiki. No `ARCHITECTURE.md`, no `documents/ui/`, no `progress.html` unless ceremony upgrades or those files already exist.

Check fits the job (fixture script, file proof, or `n/a — human accepts artifact` for light writing only). Dummy `echo` / `exit 0` / `true` are fails.

If the "work" is actually a **new product**, bounce to **erixpo-new**.

If they need a script in a notes repo, scaffold a tiny Python/shell harness ([scaffold.md](../erixpo/references/scaffold.md), light): script + sample fixture + check that exits 0 on the fixture. Not an app. Not Next.js.

## When this track wins

- "summarize these notes"
- "automate the rename in /inbox"
- "draft the weekly update from documents/"
- "research X and file it in the wiki"
- "be my assistant in this repo"
- "plan my work for this project this week"
- any job where the artifact is not a new product stack

## Loop

1. **Orient.** What is this folder for (PROFILE), what does this human prefer (USER), and what relevant facts already exist (MEMORY, wiki)?
2. **Infer first.** Follow [intent.md](../erixpo/references/intent.md). Establish the artifact and observable acceptance. Use [research.md](../erixpo/references/research.md) only for unresolved or stale evidence. A one-shot summary can proceed from provided material without initializing persistent project memory.
3. **Plan short.** For a one-shot light artifact, the request is the plan: deliver and verify it without creating plan/state/stack/PROFILE files or a learning log. The following persistent-file steps apply only to initialized or recurring work. Write `.erixpo/plan.md` with slices (goal, slices, check). Each slice has a check. For non-code jobs the check may be:
   - a script that exits 0
   - "file exists at path P and contains X"
   - "user accepted the draft"
   Write that check as `check:` in `.erixpo/stack.md` so `.erixpo/bin/erixpo` can run it when it is a command. Record `ceremony: light` (unless PROFILE already upgraded) in `.erixpo/state.md`, not `state.yaml`.
4. **Do one slice.** Update the wiki if the folder's knowledge changed, as ceremony requires ([wiki.md](../erixpo/references/wiki.md)); one-shot evidence may remain in the response.
5. **Verify.** Superpowers iron law: no completion claim without fresh evidence. Run the check or show the artifact.
6. **Learn.** After the whole job, or after an explicit correction or verified repeated pitfall, run one `erixpo-learn` pass (one JSONL line, not a novel). An outer-loop iteration is not a finished job.

## Job classes (write into PROFILE if missing)

| Class | Typical artifact | Typical check |
|---|---|---|
| automation | script, Makefile target, folder pipeline | the script exits 0 on a sample |
| research | `documents/` page with sources | page exists, claims are cited |
| writing | draft in repo | user accepted, or lint/spellcheck |
| ops | runbook, checklist, renamed files | command or file proof |
| assistant | notes, reminders file, structured inbox | file updated as specified |
| mixed | whatever PROFILE says | whatever PROFILE.check says |

## Rules

- Do not invent a SaaS stack for a writing repo.
- Do not create twenty empty wiki pages.
- Do not install MCP or third-party skills without asking.
- Secrets stay out of git.
- One worker unless files are disjoint.
