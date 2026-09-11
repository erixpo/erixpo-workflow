---
name: erixpo-init
description: Initialize erixpo in a new or existing repository. Use when the user says erixpo init, set this project up, or when AGENTS.md and documents/ are missing. Maps the repo, classifies domain AND ceremony, writes AGENTS.md, a ceremony-sized wiki, PROFILE/MEMORY/USER, CONSTITUTION, and .erixpo state without dumping empty pages or overwriting blindly.
license: MIT
metadata:
  author: Erixpo
  version: "0.7.0"
---

# erixpo init

Run this on a greenfield folder or on a repo that already has code.

Read [domains.md](../erixpo/references/domains.md), [ceremony.md](../erixpo/references/ceremony.md), [scaffold.md](../erixpo/references/scaffold.md), [wiki.md](../erixpo/references/wiki.md).

## Steps

1. **Map.** List languages, manifests, apps, tests, docs, CI, notes, scripts, workflows. Write `documents/inventory.md` from evidence. Quote. Do not guess a stack the files do not support.

2. **Classify domain AND ceremony.** Write `.erixpo/PROFILE.md` (`class`, `ceremony`, `surfaces`, `one_liner`, `check`). Ceremony is `full` | `standard` | `light` — pick from [ceremony.md](../erixpo/references/ceremony.md) (class × surface × request). Do not assume software or web.

3. **Say what you understood** in chat, short. If domain, surface, or audience is ambiguous, one question.

4. **USER.md when needed.** For full/standard work, if USER is empty, ask **2–3** working-style questions (not 20): (1) autonomy — ask / plan-then-go / unattended; (2) platforms they actually use; (3) visual-first vs code-first, **or** test strictness (pick the one that matches this folder). Fill the USER template; do not rewrite its shape (that template is owned elsewhere). If they say "you pick" / unattended / just go, write defaults: `plan-then-go`, `harness-required`, `always-stage-2`. For recurring light work, create USER only when those preferences affect the workflow.

5. **Create project brain** if missing, from `.erixpo/pack-templates/` or this pack's `templates/`. Copy **only what ceremony requires**. A one-shot light job does not initialize a persistent brain. For recurring or explicit light init, start with the small baseline needed by the workflow: `AGENTS.md`, `.erixpo/PROFILE.md`, `.erixpo/state.md`, and `.erixpo/stack.md`; add `CLAUDE.md`, `documents/INDEX.md`, inventory, or `CONSTITUTION.md` only when the folder contract or an actual artifact needs them. Create `.erixpo/USER.md`, `MEMORY.md`, `lessons.md`, `learnings.jsonl`, `sessions.jsonl`, or `refine-log.md` only when durable context, a handoff, or learning requires it. Other templates stay in pack-templates for later promotion.

   The baseline `AGENTS.md` says what this folder is for, how to run it, and what is forbidden. `.erixpo/stack.md` has a real `check:` line, or explicitly `n/a — human accepts artifact` for light writing jobs only. Dummy `echo` / `exit 0` / `true` are fails. Full and standard ceremony retain their required artifacts below.

   Then seed wiki per [ceremony.md](../erixpo/references/ceremony.md). Visible surface: seed **`documents/ui/LANGUAGE.md` only** (voice + anti-slop). Do not copy blank token/layout tables — that looks like a fake design system. Fill the rest in the first UI slice with real numbers.

6. **Do not overwrite** a non-trivial existing README or AGENTS.md. Propose a diff. Merge facts.

7. **README.** If there is none, write a short honest one. If there is one, leave it unless it is empty scaffolding.

8. After init, if the user already stated a goal in the same message, return to the erixpo router with that goal. Do not wait for them to type `/erixpo` again.

9. Write `.erixpo/init-manifest.txt` listing every file **you created** (not files that already existed), one `SHA256<TAB>relative-path` entry per file. Refresh a recorded hash only when erixpo intentionally updates that owned artifact. Purge preserves files whose current hash differs. Uninstall `--purge-docs` may only delete names on that list plus `.erixpo/`. Never list the user's pre-existing README or source.

## AGENTS.md must contain

- One-paragraph **folder** truth (not "what this software is")
- Install / run / test / lint / check commands you actually verified or marked unverified
- Directory map
- Invariants: secrets, no unapproved deps, done = check, worktrees isolate, stage-2 different session, follow `CONSTITUTION.md`, ceremony in PROFILE, no `documents/ui/` dump on non-surfaces
- Pointer to `documents/` and `.erixpo/`

Stack section is optional if class is writing / assistant / research with no runtime.

## Anti-patterns

- Generic Next.js AGENTS.md on a Swift repo, notes vault, or personal-ops folder
- Twenty empty wiki pages, blank token tables, leftover `{{PRODUCT}}`
- Coding features during init unless they said keep going
- Assuming the folder is a software product or that the surface is web
- `echo ok` / `exit 0` / `true` as check
