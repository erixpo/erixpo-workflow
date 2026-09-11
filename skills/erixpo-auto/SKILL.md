---
name: erixpo-auto
description: Autonomous build loop for an approved erixpo plan. Use when the user says erixpo auto (or go/continue/keep building about an approved .erixpo/plan.md). Same quality bar as .erixpo/bin/erixpo run (templates/PROMPT.md). One slice per iteration with tests, UI spec, self-review, check, wiki per ceremony. USER.md autonomy wins; tests are not optional.
license: MIT
metadata:
  author: Erixpo
  version: "0.7.0"
---

# erixpo auto

This is the build phase. No more product interview unless a slice is blocked on a decision.

Interactive `/erixpo auto` and unattended `.erixpo/bin/erixpo run` use the **same** quality bar. The detailed worker contract is [PROMPT.md](../../templates/PROMPT.md), installed at `.erixpo/pack-templates/PROMPT.md`; it is specialist, not factory ([craft.md](../erixpo/references/craft.md)). USER.md taste and autonomy win. Tests still run. Do not narrate the workflow in chat.

## Preconditions

- `.erixpo/plan.md` exists and status is `approved` (or the user just said "go" on the plan you showed).
- `AGENTS.md` exists. If not, run init first.
- A check command is written in `.erixpo/stack.md` or `AGENTS.md`. If missing, infer from the repo and confirm once.
- Isolation: if the tree is dirty or this is `.erixpo/bin/erixpo run`, isolate first (`.erixpo/bin/erixpo isolate` / [worktrees.md](../erixpo/references/worktrees.md)). Do not chew the user's WIP.
- Search `.erixpo/sessions.jsonl` for this module before coding.
- `.erixpo/classify.md` exists with `request_class` and `jobs:`. If missing, run `.erixpo/bin/erixpo classify <sentence>` and write the file **before** product code.
- If `USER.md` still has empty autonomy / test / review lines, write defaults: `plan-then-go`, `harness-required`, `always-stage-2`. Do not skip tests because USER was blank.
- Run `.erixpo/bin/erixpo capabilities` and paste into classify `capabilities:` only when a concrete capability gap exists and that field is empty.

## Loop

Follow [PROMPT.md](../../templates/PROMPT.md) for worker policy and [memory.md](../erixpo/references/memory.md) for targeted retrieval. Read only relevant governing files and references for the current slice; the active loop already supplies the current slice context.

Until every approved slice is complete and fresh checks pass, or a budget/failure stop is reached:

0. Read the plan, `documents/` as ceremony requires, git status, and only relevant memory/procedure sections. Search sessions when the current job needs prior context.
1. If check already passes AND **all approved slices** are done (plan status): stop (interactive: delivery note below; unattended: print `ERIXPO_DONE` and exit).
2. Have the worker follow PROMPT.md for exactly the next incomplete slice, fresh tests/checks, research, UI, self-review, docs, and learning timing. Preserve skip/narrow/full research semantics and read references only when relevant.
3. After the worker exits, require the approved slice identities and check commands to be unchanged; do not accept deleted, newly invented, or newly skipped slices. Run the fresh project check and approved completed-slice checks.
4. A worker or check failure is not success: repair only that failure, preserve logs/evidence, and stop after the existing failure/no-progress limits. Do not append sessions or learnings merely because an iteration ends.
5. Mark the current slice done only after fresh verification, preserving its approved title/check and avoiding optional extras. Continue according to USER autonomy; an unattended worker exits so the outer loop can restart it.

No completion claim without fresh test/check output in this iteration.

Stop and ask only when:

- a product decision was not in the plan **and** USER is `ask-every-slice` (otherwise: narrow research, official default, record why)
- the check cannot be run
- you would need to add a dependency or MCP the user did not approve **and** USER is `ask-every-slice`
- iteration cap reached

Do **not** stop to ask "may I add tests?"

## After the plan is green

Write a short delivery note in chat and in `.erixpo/progress.md`. Suggest two-stage `/erixpo review` as the next human action (stage 1 mechanical, stage 2 a fresh session). `skip-tiny` in USER.md may skip stage-2 on a tiny diff; `always-stage-2` never does.

If this ran in a worktree, do **not** merge. After stage-2 says `ship` **and** they say close/merge, tell them:

```bash
.erixpo/bin/erixpo close --id <id>
```

Do not start optional extras. Do not close/prune the worktree yourself.

## CLI

If `.erixpo/bin/erixpo` is on PATH in this project, you may run:

```bash
.erixpo/bin/erixpo run --max 20
```

That is the same loop driven from outside the chat. Prefer it when they walk away or USER.md autonomy is `unattended`. The worker prompt is `templates/PROMPT.md` in the source pack and `.erixpo/pack-templates/PROMPT.md` after install; both must match this skill's contract.

## Runtime contract

The CLI reads max_iterations/max_seconds from budget.md (overridden by --max/--timeout), captures worker/check logs, and writes verification.json plus canonical state.md. Worker failure never counts as success. Three consecutive worker failures, three check failures, or three iterations without slice progress stop the run. Terminal events remain searchable through erixpo search. Guidance fields about dependencies are worker instructions, not a sandbox.
