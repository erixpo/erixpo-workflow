# AGENTS.md

_Fill this during `/erixpo init`. Delete this italic line._

## Product

[One paragraph. What this folder is for. Who it is for.]

## Stack

_Omit this section if class is writing / assistant / research with no runtime._

- Language / runtime:
- App surface:
- Data:
- Tests:

## Commands

```bash
# install
# dev
# test   (this is the erixpo check unless .erixpo/stack.md overrides it)
# check  (same as test unless PROFILE.check is a different proof)
# build
# lint
```

Mark any command unverified until you have run it.

## Layout

```
[top-level map]
documents/          wiki (ceremony in PROFILE — do not dump ui/ on non-surfaces)
.erixpo/            machine state
.erixpo/CONSTITUTION.md   layout + how to extend this folder
```

## Invariants

- Follow `.erixpo/CONSTITUTION.md`. Ceremony lives in `.erixpo/PROFILE.md`. Do not dump `documents/ui/` on jobs with no surface.
- Do not commit secrets or `.env`.
- Do not add dependencies or MCP servers the user did not approve.
- Update `documents/` when behaviour changes, as ceremony requires.
- "Done" means the check command exits 0 (or the light-writing PROFILE check is satisfied).
- Unattended loops isolate in a worktree. Do not merge onto the user's branch until they say so. After ship, `.erixpo/bin/erixpo close --id` removes the tree.
- Stage-2 review is a different session from the implementer.

## erixpo

This folder uses erixpo workflow. Router skill: `/erixpo`.

## Memory

This repo keeps durable memory in `.erixpo/PROFILE.md`, `.erixpo/MEMORY.md`, `.erixpo/USER.md`, and `.erixpo/learnings.jsonl`. Read governing files first, then only relevant sections and effective lessons/procedures for the job; do not load every memory file for each one-shot or iteration. After the whole job, run one learn pass if a verified reusable fact appeared; also learn after an explicit user correction or verified repeated pitfall. An outer-loop iteration is not a finished job, and immutable `.erixpo/run-events/` are runtime evidence, not job sessions.
