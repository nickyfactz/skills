---
name: repo-work
description: >
  Audit or refactor a repository. Use when the user wants codebase discovery,
  architecture or runtime mapping, technical-debt, reliability, or
  documentation findings, an execution-ready cleanup plan, or implementation
  of an approved cleanup or structural change. Choose audit for inspection and
  reporting; choose refactor for authorized edits.
---

# Repository work

Audit discovers. Refactor resolves.

This skill has one clear mode boundary:

- **Audit** inspects a repository and reports evidence. It leaves repository
  files unchanged.
- **Refactor** implements an authorized cleanup or structural change, then
  verifies the result.
- **Audit -> refactor** is available when the user asks for both or explicitly
  selects an audit finding for implementation. If the user only asks for an
  audit, stop after the report.

When the requested deliverable is unclear, start in audit mode. A finding is
not permission to edit.

## Scope and safety

Use the user's named repository, branch, worktree, and files as the scope. Read
local `AGENTS.md`, `CLAUDE.md`, README files, design notes, ADRs, and task
instructions before making decisions. Preserve existing branch and worktree
state unless the user asks for a commit, merge, push, or cleanup operation.

If `CONTEXT.md` or an equivalent domain glossary exists, use it for domain
naming; read relevant ADRs as decisions to respect, not theoretical designs to
re-litigate. Neither file is required for a general audit.

Audit mode performs read-only inspection and non-mutating checks. Refactor mode
edits only the scoped repository and keeps external systems, credentials,
production data, and irreversible migrations outside the change unless the user
explicitly authorizes them. Report any scope or authorization gap before
crossing it.

## Audit mode

Choose the narrowest useful audit:

- **General audit**: structure, dependencies, runtime paths, interfaces,
  duplication, tests, reliability, security boundaries, configuration, and
  documentation drift.
- **Architecture audit**: add the deepening lens—module depth, interface
  clarity, seam locality, adapter leverage, and the deletion test. Treat the
  interface as the test surface: ask whether important behavior can be proven
  through it. One adapter is a possible seam; repeated independent adapters are
  stronger evidence that the seam is real.
- **Targeted seam audit**: inspect one feature, package, module, service,
  runtime path, or design concern.
- **Regression-risk audit**: focus on behavior preservation, downstream effects,
  validation gaps, lifecycle, concurrency, and failure handling.

### Audit workflow

1. **Scope before scanning.** Read the request and repository guidance. If the
   user named a target, start there. Otherwise use metadata and recent history
   (`git log --oneline`, when available) to find likely hot spots, then widen
   only as needed. Record the audit mode, target, non-goals, and commands that
   will provide evidence.

   **Done when:** the audit has a bounded question, a target area, and a stated
   reason for any wider scan.

2. **Map the repository.** Inspect manifests, lockfiles, workspace/build files,
   scripts, source and test roots, generated-artifact locations, entrypoints,
   background jobs, deployment/runtime configuration, and relevant docs. Map
   applications, packages, modules, adapters, utilities, tests, and generated
   outputs without treating directory names as proof of ownership.

   **Done when:** the report can name the relevant entrypoints, modules,
   boundaries, and validation surfaces.

3. **Trace the seam.** For each important path, follow callers and callees far
   enough to record inputs, outputs, errors, state ownership, dependency
   direction, public exports, and tests. Search for competing implementations,
   wrappers, aliases, fallbacks, stale references, and callers that bypass the
   apparent boundary.

   **Done when:** every major claim has a concrete path, symbol, relationship,
   or command behind it.

4. **Classify the structure.** Use `Keep`, `Merge`, `Move`, `Delete`, or
   `Investigate` for meaningful files, modules, packages, services, or paths.
   Apply the deletion test to suspected shallow layers: would removing the
   layer concentrate complexity in a clearer owner, or merely move it? In the
   architecture lens, also ask whether the interface is simpler than the
   implementation, whether logic lacks locality, and whether a seam creates
   useful leverage for future changes.

   **Done when:** each candidate has a classification, evidence, and confidence
   level—or an explicit evidence gap explaining why it remains `Investigate`.

5. **Assess risk and protection.** Review contracts, mixed responsibilities,
   dependency direction, state/lifecycle ownership, input validation, error
   translation, retries/timeouts/cancellation, idempotency, concurrency,
   resource cleanup, security-sensitive boundaries, tests, builds, and smoke
   checks. Check documentation, examples, scripts, and configuration against
   the observed code.

   **Done when:** the report identifies what currently protects each critical
   flow and what would make a change unsafe or incomplete.

6. **Shape the backlog.** Turn findings into small, ordered refactor cards
   instead of a list of smells. Prefer deletion or consolidation of whole
   obsolete paths, stronger contracts, and coherent seams over broad rewrites
   or cosmetic renames. Keep a proposed interface at the hypothesis level
   during an audit unless the user explicitly requested an implementation-ready
   pre-refactor plan.

   **Done when:** the first recommended card can be executed without repeating
   the discovery work, and each later card has a reason to follow its place in
   the order.

### Audit evidence and cards

Every finding includes:

- title and category
- file or directory path, symbol, and caller/callee relationship when useful
- observed evidence and the command or source that supports it
- why it matters to behavior, clarity, testability, reliability, or change cost
- recommendation and affected paths
- expected impact, effort, risk, and confidence
- validation needed before or after a refactor

Useful categories include structure, modularity, duplication, abstraction,
interface or service design, state management, validation, reliability,
testing, documentation drift, dependency/runtime bloat, performance, security
boundaries, dead code, migration debt, and configuration.

Use [audit-report-template.md](references/audit-report-template.md) when a
structured report will help. Use [priority-rubric.md](references/priority-rubric.md)
for consistent impact, effort, risk, and confidence labels.

## Refactor mode

Refactor mode is write-capable, but it still begins with a bounded audit of the
seam being changed.

### Refactor workflow

1. **Confirm the change envelope.** Read the selected audit card, issue, plan,
   ADR, or user request. Record the objective, target design, non-goals,
   behavior to preserve, accepted behavior changes, affected files/symbols/
   callers, public contracts, compatibility constraints, deletion targets,
   validation plan, and rollback risks. If no usable plan exists, create a
   short one before editing.

   **Done when:** the intended end state and the boundaries of the work are
   explicit enough to review.

2. **Baseline and trace.** Check repository status and run the most relevant
   existing tests, checks, or smoke paths before invasive edits. Reconfirm
   entrypoints, callers, exports, dependencies, tests, docs, scripts, configs,
   generated references, and competing paths for the selected seam.

   **Done when:** current behavior and any pre-existing failures are recorded,
   and the migration surface is known.

3. **Protect behavior.** Prefer targeted tests, characterization tests,
   contract tests, regression cases, or critical-flow smoke checks. Test
   observable behavior rather than freezing poor implementation details. If a
   protection gap cannot be closed safely, record it as a risk before editing.

   **Done when:** important preserved behavior has a passing check or a named,
   accepted validation gap.

4. **Define the contract and slices.** Give the target owner clear inputs,
   outputs, errors, invariants, and lifecycle. Keep framework, vendor,
   persistence, network, filesystem, shell, and UI details at adapters when
   they are not the actual domain boundary. Choose a migration order that
   avoids a half-old, half-new path.

   **Done when:** each slice has a small purpose, affected callers, a removal
   condition for old code, and a validation check.

5. **Execute the slices.** Add or adjust safety tests, isolate mixed
   responsibilities, normalize contracts, migrate callers, consolidate one
   owned implementation, and delete obsolete wrappers, aliases, flags, dead
   code, duplicate paths, and stale exports. Validate after each meaningful
   slice before widening the change.

   **Done when:** the target behavior is implemented, all known callers use the
   intended path, and every removed or retained compatibility path is
   explained.

6. **Finish the seam.** Update imports, tests, documentation, examples,
   comments, scripts, configuration, generated references, and dependency
   entries that describe or reach the changed structure. Search for stale
   symbols and old paths after the edits.

   **Done when:** the repository has no known stale references caused by the
   refactor and the final diff matches the change envelope.

7. **Prove and classify.** Run relevant formatting, linting, typechecking,
   unit/integration/end-to-end tests, builds, dependency checks, and smoke
   checks. Separate refactor-caused failures from pre-existing and environmental
   failures. Never report an unrun check as passing.

   **Done when:** validation results, remaining risks, and behavior changes are
   explicit and reproducible.

### Refactor heuristics

- Delete or consolidate before adding an abstraction.
- Give each important concept one clear owner and each public contract a named,
  explicit shape.
- Keep policy independent from low-level details; wire concrete dependencies at
  the setup/composition layer when that improves clarity or testability.
- Validate and normalize at boundaries, then let internal code rely on the
  stated contract.
- Keep state and lifecycle ownership visible. Treat broad catches, silent
  fallbacks, ambient globals, hidden caches, boolean-control flags, and
  unstructured important data as risks to resolve or justify.
- Keep compatibility only for a named caller, public requirement, or migration
  window, and record its removal condition.
- Prefer existing platform or repository capabilities over new dependencies and
  ceremony when they solve the problem adequately.

Use [refactor-execution-template.md](references/refactor-execution-template.md)
to capture the change envelope. Use
[docs-sync-checklist.md](references/docs-sync-checklist.md) when the refactor
changes structure, setup, ownership, or usage guidance.

## Report format

### Audit report

1. Scope, mode, method, and commands
2. Executive summary and top recommendation
3. Architecture/runtime snapshot and repository map
4. Keep / Merge / Move / Delete / Investigate classification
5. Evidence-backed findings and risk gaps
6. Testing, validation, and documentation drift
7. Prioritized refactor cards
8. Unknowns and evidence needed

### Refactor report

1. Execution plan: objective, target, non-goals, behavior constraints, and
   validation plan
2. Impact map: files/modules, contracts, callers, tests/docs/configs, and
   deleted or consolidated paths
3. Changes applied
4. Validation results, including failures and checks not run
5. Intentional behavior changes, or `none`
6. Remaining risks and follow-ups

For a combined audit-to-refactor session, report the audit decision first, then
the implementation and proof for the selected card. Stop after the audit when
the user has not authorized a change.
