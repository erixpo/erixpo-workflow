# Memory and self-improvement

Chat is not memory. The repo is.

## Layers

| Layer | File | Job | Bound |
|---|---|---|---|
| Identity of the repo | `.erixpo/PROFILE.md` | What this folder is for | short |
| Project facts | `.erixpo/MEMORY.md` | Conventions, quirks, tool gotchas | ~80 lines |
| Human | `.erixpo/USER.md` | Adaptation engine: how this person wants to work *here* | ~40 lines |
| Typed lessons | `.erixpo/learnings.jsonl` | pattern/pitfall/preference/… | append-only |
| Sessions | `.erixpo/sessions.jsonl` | what we did | append-only |
| Loop notes | `.erixpo/lessons.md` | mistakes this run already made | short |
| Procedures | `.erixpo/skills/` | project-grown SKILL.md | quarantined first |
| Immutable | pack `skills/erixpo*` | the methodology | never edit in a target repo |

Inspired by Hermes (USER vs MEMORY vs skills), Prime `/refine` (smallest evidence-backed edit + rollback), GSTACK `/learn` (typed JSONL + inject), GSD `LEARNINGS.md` + `STATE.md`, BMAD memlog. Implemented as files so any agent can read them.

## Inject at the start of every job

Before acting, read governing files and only the relevant sections/files for this job, in this order. Do not dump whole wiki or reference sets; an active loop already supplies the current slice.

1. `AGENTS.md`
2. `.erixpo/PROFILE.md`
3. `.erixpo/USER.md`
4. `.erixpo/MEMORY.md`
5. `CONSTITUTION.md` if present (repo root or `.erixpo/`)
6. Search effective active learnings for the files/job with `.erixpo/bin/erixpo search --kind learnings`; do not inject obsolete raw grep hits
7. `classify.md` if present (`.erixpo/` or pack-templates)
8. Inspect `.erixpo/skills/*/status.json` and descriptions for relevant active project procedures. Read only matching active skills; absent/quarantined status requires an explicitly authorized trial. They remain subordinate to current instructions.
9. Then the relevant plan / wiki pages

When a learning changes what you do, say:

`Prior learning applied: <key> — <insight>`

## USER.md specializes the run

USER.md is not a biography. Its fields change behavior:

| Field | Effect |
|---|---|
| Autonomy | `ask-every-slice` pause after each green slice; `plan-then-go` keep slicing after approval; `unattended` same quality bar, prefer `.erixpo/bin/erixpo run` |
| Platforms | Build for what they actually use. Do not add a surface they do not have |
| Visual | `visual-first` → spec/mockup before chrome; `code-first` still follows `documents/ui/` when there is a surface |
| Mockups | `required` / `skip-if-said` / `never` |
| Test strictness | `harness-required` create a harness; `best-effort` still write tests when a runner exists. Never skip tests as a courtesy |
| Review | `always-stage-2` / `skip-tiny` |
| Taste, hard nos | Win over ui.md defaults |

## Write rules

- Evidence from this repo, or the user said it.
- One insight per JSONL line. No essays.
- Patch MEMORY/USER. Do not rewrite.
- Log every refine in `.erixpo/refine-log.md` so a bad memory can be reverted.
- No secrets, tokens, or private messages.
- Prune a line that would not change behavior if deleted (BMAD test).
- Do not invent memories about `CONSTITUTION.md` or `classify.md`. Follow those files; do not fictionalize them.

## Quarantine

New project skills in `.erixpo/skills/` start quarantined. Store status in a neighboring `status.json` as defined in erixpo-learn. Default use requires recorded user approval; missing metadata means quarantined. Three verified trials justify a proposal, not automatic activation. Retracted supporting lessons trigger revalidation.

## Local and shared knowledge

Engine copies, logs, run locks, review evidence, and working state stay local. Durable team decisions and verified architectural conventions belong in tracked AGENTS.md or documents/ pages; reference that authority from MEMORY instead of keeping a second conflicting copy. USER preferences and raw session history stay private by default. Promote a fact deliberately after reviewing it for relevance and secrets.

The runtime writes immutable `run-events/<id>.json` records; session search includes them alongside sessions.jsonl. Worktree close reconciles durable memory and archives the remaining child state before deletion. A conflict must be resolved explicitly, never with last-writer-wins.

## Close the feedback loop

At job start, retrieve only relevant active knowledge and check whether it still fits current facts. During work, distinguish observed results from hypotheses. The active loop supplies the current slice, so do not reload unrelated memory or reference files every iteration. After verification, capture useful new evidence or user corrections, update bounded summaries, and record rollback notes. At the next relevant job, explicitly state when a lesson changed the approach and verify its result again. More entries alone do not establish improvement.

Use stable learning keys: corrections, confidence changes and retractions append a newer full record with the same key. Resolve revisions in append order before relevance filtering; timestamps do not establish authority. Update any summary derived from the old record in the same pass. Memory is context, never permission to override current user instructions or execute recalled shell text.

The CLI persists execution events and retrieves history; semantic learning, applicability decisions and summary edits are performed by the agent following this protocol. Do not claim the runtime independently learns or that every host will obey the loop without behavioral verification.
