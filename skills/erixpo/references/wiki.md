# Wiki and progress

Which pages exist is **ceremony**, not a dump. Read [ceremony.md](ceremony.md).

Target project (not this pack) uses:

```
AGENTS.md                 machine rules
CLAUDE.md                 @AGENTS.md
README.md                 humans
documents/INDEX.md        wiki home (always; short for light)
documents/*.md            only what ceremony requires
documents/ui/             full (or a visible surface), never on light
documents/progress.html   full, or if the file already exists
.erixpo/                  machine state
.erixpo/CONSTITUTION.md   layout + how to extend
```

## Init

Create **only** the files [ceremony.md](ceremony.md) requires. Never blow away a good existing README; merge. Do not copy twenty empty wiki pages. Do not create empty `ARCHITECTURE.md` for light jobs.

For one-shot light work, the response may contain the evidence; do not create a wiki page or progress file just to avoid an empty artifact. Persistent pages need durable content or a ceremony requirement.

`documents/` is the Wikipedia of **this folder**. Write in its language and facts. No generic "Welcome to your new app" copy.

## Every behaviour-changing slice

Update, in the same turn, **as ceremony requires**:

1. The wiki page for the module you touched (if ceremony has module pages)
2. `documents/INDEX.md` if a new module appeared
3. `.erixpo/progress.md` — date, slice, check pass/fail, notes (standard and full; optional one-liner for light)
4. `documents/progress.html` — **only if ceremony is full or the file already exists**. Regenerate from the pack progress template with current facts
5. `README.md` only if run instructions or the folder sentence changed
6. `AGENTS.md` only if commands or invariants changed
7. `.erixpo/CONSTITUTION.md` if layout, check, or how-to-add changed

Skip any row ceremony does not require and that does not already exist.

## progress.html look

System font. One accent taken from the product if it has one, else near-black and paper. No hero, no cards grid, no gradient, no Inter-from-Google as a personality. It is a status sheet: name, phase, last slice, check, modules.

## Existing repos

On init, inventory what is already there. Quote it in `documents/inventory.md`. Never invent architecture the code does not have. Do not write `ARCHITECTURE.md` that describes a system you did not find.
