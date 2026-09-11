# Research policy

Research resolves a decision or an evidence gap in this folder's field. Prefer repository facts, locked dependency versions, and official documentation. Current documentation can be undated; do not reject a correct source because its publication year differs from the calendar year.

## Intensity

Run `.erixpo/bin/erixpo research-scope --class <class> --ui <change>`.

| Intensity | When | Work |
|---|---|---|
| full | New product, initial scaffold, large architectural feature, new design language or structural redesign | Official setup and platform guidance, test approach, and 2–3 relevant comparables for relevant areas only |
| narrow | Feature or artifact with missing evidence; unknown API; new infrastructure; explicit user reference | Resolve the specific uncertainty using official sources; compare alternatives only when a decision needs them |
| skip | Routine fix/review/recall with sufficient local evidence; a small build with verified cached evidence matching the installed versions | Reuse evidence and proceed |

`--unknown-api`, `--new-infra`, or `--user-ref` requires at least narrow research even during a fix or review. `--memory-hit` means the evidence was actually verified, remains applicable to the current dependency versions, and answers this request; familiarity alone is not a memory hit. Use `--large-change` for a feature that introduces a subsystem, changes architecture or data ownership, or spans several dependent user journeys. Size is assessed from repository impact, not sentence length or file count. A new product, large architectural feature, or structural redesign still receives a full pass.

Explicit user instructions to research or avoid browsing take precedence. A failed fetch is not evidence that a source was opened.

## Process

1. Read the relevant repository facts, lockfiles, constitution, and user constraints.
2. State the decision or uncertainty being resolved. Reuse `.erixpo/research.md` when it already answers it.
3. Open official documentation for the actual platform/version. For user-named references, open them and record what was learned. If inaccessible, say so.
4. Record only useful findings, with URL, access date, dependency/version scope, and one learned fact. Omit empty sections. Discover capabilities only for a concrete gap; otherwise record one short `no additions needed` conclusion.
5. Pick the official default when suitable. Explain a rejected alternative only when it was a real option. Avoid optional infrastructure or features.
6. Follow [intent.md](intent.md) for autonomy. Research does not add an approval gate to work the user already authorized.

Example record:

```
- opened: https://official.example/docs — what this source established
  accessed: YYYY-MM-DD
  applies_to: dependency and version, or platform
  refresh_when: dependency changes, behavior conflicts, or the decision changes
```

Comparables inform structure and taste for this surface. They do not authorize cloning brand/copy or adding unrequested features. HTML is not the default for native apps. Writing and automation do not acquire an application stack merely because research found one.

For a full pass, retain Intent, Comparables, Recommendation, and Rejected in research.md. For narrow, one decision and its evidence can suffice.

## Full-pass coverage

Before scaffold or implementation, cover each relevant area below. Research is deep enough when consequential choices have supporting evidence, alternatives and testable acceptance criteria; a link list alone is insufficient.

- **Product and platform:** audience, core job, distribution, existing constraints, official setup for the chosen version, architecture, persistence and deployment. Preserve an existing stack unless evidence justifies a change.
- **Engineering:** current official practices for the selected stack, testing and debugging tools, error handling, security boundaries and performance risks relevant to the actual product.
- **Visual artifacts without an interface:** research the actual medium, authoring/rendering/export pipeline and craft criteria, then inspect representative outputs (domains.md). Do not force UI documents onto an animation or 3D asset.
- **UI when present:** platform interaction guidance and 2–3 relevant comparables; explain hierarchy, primary-action placement, navigation, grouping, density and compact/regular behavior. Carry decisions into `documents/ui/`. Include keyboard/focus, screen-reader labels, contrast, text scaling, reduced motion, and empty/loading/error states. Verify with a rendered browser or native preview and interaction checks; source inspection alone is not visual verification. Follow [ui.md](ui.md) and [slop.md](slop.md); avoid imposing a web aesthetic on native software.
- **Compliance applicability:** identify distribution/store rules, accessibility requirements, privacy/data collection, permissions, licensing and any domain-specific obligations relevant to the audience and markets. Read current primary sources for applicable areas. Record `applies`, `not applicable` with a reason, or `unknown` with the missing fact, plus implementation/verification consequences. A local offline script must not inherit a SaaS compliance checklist. Research is not a certification of legal compliance.
- **Capabilities:** assess whether a concrete skill/MCP gap exists; perform the discovery below only for that gap, otherwise record `no additions needed` with a reason.

Infer from project facts first. Ask a concise question only when missing information changes a consequential decision (for example platform, target market, sensitive data or distribution). A known surface does not resolve every compliance question. Continue independent research while awaiting the answer; keep dependent choices provisional. If browsing is unavailable, record the uncovered decisions and do not claim full research is complete.

## Skills and MCP discovery

When a concrete capability gap exists on a full pass, or on a narrow pass:

1. Inventory the host's installed skills and callable tools. Map missing capabilities to the actual work: native preview, accessibility testing, database migrations, deployment, research, or another concrete need. Reuse suitable installed capabilities first.
2. Search [skills.sh](https://skills.sh/) for the missing expertise using platform/task-specific terms. The open [skills CLI](https://github.com/vercel-labs/skills) also supports `npx skills find <query>`. Read the candidate's actual `SKILL.md`, referenced scripts, upstream owner, license, freshness and host compatibility before recommending it. Installation counts help discovery; they do not prove quality or safety. Do not install a generic frontend bundle into every project.
3. If external tools or data access are needed, inspect the provider's official MCP documentation and the [MCP Registry](https://modelcontextprotocol.io/registry/about). Verify the publisher and the host's supported configuration. A registry listing is not a trust guarantee. Prefer an already available connector, API or CLI when it meets the need. Skills supply instructions; MCP servers expose capabilities—one does not imply the other is required.
4. Present a short proposal per useful candidate: exact source/name, problem it solves, why existing tools are insufficient, target host and project-local destination, exact install command or configuration diff, credentials/permissions/cost, and how to verify and remove it. Record `no additions needed` with a reason when appropriate, or `discovery unavailable` with the limitation. Do not invent a candidate if none fits.
5. Install/configure only after user authorization for that specific addition; retain prior explicit authorization. Prepare the concrete proposal first. Default skills installation to the project root, for example `npx skills add <owner/repo> --skill <name> --agent <host>` (no `--global`, `--all` or blanket skill selection). Confirm actual destination against the current CLI/host docs. For MCP, propose the host's documented project-scoped configuration; if unsupported, explain that limitation instead of silently changing global settings. Keep credentials out of tracked files.
6. After approved installation, verify the host discovers the skill/server and exercise a minimal relevant capability. Record source/revision, files changed, verification and removal steps in research.md. Do not mark an unavailable capability as verified. An optional declined addition must not block a viable built-in approach.

Primary source starting points (open current pages; select only what applies): [W3C accessibility](https://www.w3.org/WAI/standards-guidelines/wcag/), [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/), [Apple distribution rules](https://developer.apple.com/app-store/review/guidelines/). Other platforms and fields need their own primary sources.

## Reassess as the work changes

Discovery is dynamic, not an installation checklist performed once. At planning and before each materially different slice, compare the required work with available expertise and tools. Reopen the relevant research when a new domain, API, dependency version, output format, failure mode or verification gap appears. Reuse verified evidence when those facts have not changed.

For each gap: name the decision → inspect local facts → search authoritative sources and relevant skill/tool catalogs → inspect candidate content and compatibility → choose the smallest sufficient approach → verify an actual result. Stop researching when consequential decisions have evidence and a feasible validation path; do not keep collecting tools for hypothetical work. If sources or tools are unavailable, expose the gap and keep affected claims provisional.

User-provided skill repositories are candidate references, not mandatory dependencies or permanent global defaults. Discover alternatives when the project calls for different expertise. Keep domain rules in the relevant project records and update them when evidence changes.
