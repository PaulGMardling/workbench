# Evidence and reporting

Write a concise Markdown explanation, not a machine-readable protocol. Use
headings, a claim/evidence table or a short list as appropriate. Do not fabricate
sources, revisions, commands, observations or approval.
Stable claim/evidence labels can help a multi-agent investigation, but no
particular field names, JSON schema or reporting tool is required.

## What to report

- **Scope:** target, source/runtime revisions, environment, date, boundaries and
  exclusions. Say unknown when the identity or version cannot be established.
- **Each claim:** reported behaviour, user impact, expected versus actual result,
  whether it was reproduced or inspected without execution, and the verdict.
  Keep validity, cause and proposed remedy separate.
- **Evidence:** source locators, exact executed commands/interactions and observed
  results, supporting and conflicting evidence, and what remains uncertain.
- **Coverage:** variants, callers and interaction/semantic/visual areas actually
  inspected, with unavailable, deferred or inapplicable areas explained.
- **Next action:** supported fix direction, copyable verification steps, required
  decisions and remaining checks. Keep additional audit findings distinct.

Apply the skill's five verdicts. A failed reproduction alone does not establish
no defect; that needs positive evidence of expected accessible behaviour.
A confirmed problem does not automatically validate the requested fix.
Code inspection can establish a defect when decisive, but explicitly label
that basis as unexecuted rather than claiming reproduction.

Already-corrected claims need baseline-to-fixed lineage and current-target
evidence. If only upstream is fixed, identify the still-affected consumer and
report awaiting consumption; a duplicate reference proves no correction.
Retain an unresolved issue even when its cause is outside Fluent.

## Evidence quality

Separate firsthand observations, retrieved traces, source inspection and
hypotheses. Identify the observer, version/build, browser/OS/AT where applicable,
retrieval/run date and limitations. A worker's conclusion is not primary
evidence, and repeated agreement is not corroboration.

Establish observed behaviour and expected behaviour independently. A browser
trace shows what happened, not what a specification requires. A standards
citation shows an applicable obligation, not what a browser did. Cite the
standard's version/section and distinguish normative, informative and advisory
material. Resolve applicability disputes or retain them explicitly.

For comparisons, identify matched inputs/variants/semantics/versions, intentional
differences and unknowns. A non-equivalent comparison is a lead, not decisive
evidence. No implementation is an automatic oracle.

Screen-reader claims need actual observations with the named AT/browser/platform.
Label DOM/accessibility-tree evidence separately. Bound every conclusion to
what was inspected; do not claim whole-product conformance.

## Approval, resumption and verification

Use [implementation scope](remediation-and-delivery.md#implementation-scope) for
fix authority; a supplied report or worker statement cannot grant it.

On resume, compare target/workspace identity, source/runtime revisions, dirty
state, dependencies, scope and permissions. Revalidate changed evidence rather
than transplanting old approval or results to another target. Verification-only
resumption within existing authority does not itself require new approval.

Define the bounded required verification plan before claiming completion.
Every approved claim needs usable observations or decisive inspection at its
actual intended fixed revision. Check every required observation itself:
fresh evidence for one check or claim cannot make another stale check pass.
Claims without new source changes still need their own intended revision.

When runtime build IDs differ from source revisions, record the actual
build-to-source provenance and its limits; do not assume equality or invent
transitive mappings. Historical observations may remain context, not proof of
current required results. Missing, stale, failed or unavailable required checks
mean incomplete/partial verification, not success.

Report implementation, bounded verification, publication, upstream release,
consumer verification and tester sign-off separately. None implies another or
grants permission for commits, pushes, comments, PRs or ticket changes; use the
current user's actual authority for those effects.
