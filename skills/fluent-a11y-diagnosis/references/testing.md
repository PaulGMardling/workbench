# Bounded accessibility testing

Read the sections relevant to the current runtime investigation, not a mandatory
full checklist. The [skill](../SKILL.md) defines verdicts,
[evidence guide](evidence-contract.md) defines reporting/verification quality, and
[implementation scope](remediation-and-delivery.md#implementation-scope) defines
source-edit authority. This reference supplies practical diagnostic recipes.

## 1. Agree the boundary and discover capabilities

Name the affected component, user task, reported configuration and
revision. The target may be a Fluent website/page or public library generation,
including v0, v8 or v9; do not assume a dependency chain.
Include relevant variants and callers: for example, the reported
controlled state, a caller supplying labels, or a portal host affecting focus.
Select these because they exercise an affected contract or credible failure
path, not because they exist in the package. Record exclusions. Do not silently
audit the whole package or product.

Before any execution, record both availability and authorization for:

- Reading the original report, source, callers, tests and standards.
- Browser control, accessibility-tree inspection, screenshots and console logs.
- Existing test runners, diagnostic fixture writes, local servers and actual AT.
- Authenticated app access, playground use, evidence storage and external transfer.

Discover the host's available tool schemas rather than inventing tool names,
payloads, commands or selectors. Inspect existing project instructions and
scripts before choosing a runner. Tool availability is not permission; permission
to diagnose is not permission to change source, start a server or write fixtures.
Never run tests, builds, scripts or installs in a protected primary checkout.
Execute bounded checks only in an authorized task workspace. If none exists,
report the blocker and supply the manual recipe; do not provision one implicitly.

Do not auto-install dependencies, browsers, AT or extensions. A missing dependency
is a blocker to report, not authorization to install it. Do not upload source,
private examples, traces or user data to public playgrounds or other services.
Use authorized local or already-approved examples with non-sensitive data.
Diagnostic fixture permission does not permit a production component patch.

### Shared browser and AT safety

Establish who owns the browser, page and AT session before sending input. Prefer
an authorized dedicated page/profile with synthetic data. Do not navigate away
from the user's work, close unrelated tabs, clear shared storage, change their
global accessibility settings or toggle their AT without permission. Keyboard
automation can reach browser chrome, OS shortcuts or other applications; stop
if focus leaves the intended surface unexpectedly. Avoid destructive actions and
authenticated submissions. Agree on any recording, redact sensitive content and
save artifacts only at an authorized location. Restore only settings and
resources this run changed; do not terminate someone else's server or AT.

## 2. Establish expectations independently of the repro

For each claim, write the user task, alleged barrier, expected behavior, actual
behavior to observe, proposed remedy and alternatives that could explain it.
Use applicable W3C WAI sources as the primary standards references:

| Source | Authority and use |
| --- | --- |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Normative success criteria and conformance requirements. Record the version, criterion, level, exceptions and applicability; do not silently substitute it for a different contracted version. |
| [WAI-ARIA 1.2](https://www.w3.org/TR/wai-aria-1.2/) | Normative role/state/property requirements where applicable. Read the relevant role definition and requirements, not only an example. ARIA does not supply keyboard behavior by itself. |
| [Understanding WCAG](https://www.w3.org/WAI/WCAG22/Understanding/) | Informative explanations of intent, benefits, examples and techniques; not additional normative requirements. |
| [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) | Advisory patterns and examples for interaction and semantics. Explain why a pattern fits; deviation alone does not establish a WCAG failure. |
| [WAI Easy Checks](https://www.w3.org/WAI/test-evaluate/preliminary/) | Informative starting checks, explicitly not a comprehensive evaluation. |

Use version-matched native HTML and component contracts where relevant, and
record conflicts with the report or example. A request to match another Fluent
generation is not itself a normative obligation. If using a numeric threshold,
retrieve the applicable primary criterion, verify its conditions and exceptions,
and record that source alongside the measurement. Do not guess thresholds or
turn an advisory recommendation into a conformance requirement.

Ask what observation would disprove the initial diagnosis. For example, would
correct behavior in the same component without a caller's event handler locate
the problem in the caller, or would only a fresh build change the result?
Changing configuration is a separate discriminating experiment, not a faithful
reproduction. A real barrier in a story, browser or AT remains a real problem
even when it does not justify a shared-component patch.

## 3. Preserve the scenario and prove the harness is live

First verify the reported behavior in its original environment, if accessible.
Isolate it in a standalone story, authorized fixture or approved playground when
that helps distinguish causes. For a website or Docs bug, the page/wrapper may
be the target: do not remove it and conclude there is no issue. Docs wrappers can
change focus, layout, events and announcements; an isolated repro complements
rather than replaces the original.

### Optional sister-component comparison

Compare implementations only to answer a specific diagnostic or fix question;
cross-generation comparison is not a prerequisite for verifying every report.
A sister component can help explain a difference. Inspect each actual
implementation/version rather than assuming equivalent internals. Record
relevant focus-management libraries, native APIs, polyfill setup, browser
support and intended interaction contracts. A difference is an observation,
not proof that either implementation is defective or must copy the other.

Explain in ordinary language what was compared, which inputs matched,
intentional differences and unknowns, and whether the comparison supports a
verdict. Match or explicitly account for:

- Actual source/build revision, resolved package versions and dependency graph
  for the selected targets; no fixed set of Fluent generations is required.
- Props, slots, controlled/uncontrolled state, initial values, data and the exact
  action sequence; relevant disabled, loading, error and empty states.
- Consumer callbacks, native semantics, labels, descriptions, relationship IDs,
  localization and directionality.
- Theme/provider configuration, CSS/reset order, fonts, portal/container
  placement, focus management and relevant application wrappers.
- Browser, OS, AT, viewport, zoom, input mode and relevant settings.

Say when versions are unknown. A URL or branch name does not prove which
bundle is running. Non-equivalent comparisons are leads, not decisive evidence
of a regression or correct fix. In particular, do not add `preventDefault`,
focus handlers, labels, live regions, CSS overrides or state resets that repair
the alleged bug in the baseline. Explain every necessary harness adaptation.

### Freshness and errors

Before trusting a standalone or playground observation:

1. Confirm the selected story/route and rendered code, props and styles match the
   intended example. Confirm the preview frame, not the editor or Docs wrapper,
   receives input.
2. Verify a known visible input/state change reaches that preview. If permitted,
   use a harmless fixture-only marker or existing build/version indicator to
   distinguish the current render from cached or stale output. Preserve the
   faithful scenario after this probe.
3. Check compilation/runtime errors, console messages and relevant resource
   failures. Detect blank previews, error boundaries, failed imports, unsupported
   dependencies, missing styles and stale hot reload.
4. Record the observed build identity and freshness evidence. Reset to the
   documented initial state and rerun the claimed sequence.

A changed editor buffer does not prove a changed runtime. If freshness or a
healthy render cannot be established, stop that experiment and label it blocked;
do not interpret an error page or absent widget as evidence about accessibility.

For baseline/fixed comparisons, label both identities explicitly and keep them
distinct in artifacts. After authorised remediation, repeat the same
inputs and observations against the actual fixed revision with equivalent
configuration. Do not compare an old deployed baseline with an unrelated
dependency upgrade and attribute the result to one patch. Verify the baseline
still exposes the claimed behavior and the fixed case does not merely hide the
widget, suppress the event or skip the failing assertion. If the baseline cannot
be obtained, disclose that limit instead of inventing a before/after result.

## 4. Run a small scenario-specific smoke matrix

Use only rows relevant to affected variants/callers. Explain what was inspected,
what failed, and what was unavailable, deferred or inapplicable. Inspection is
not a passing result. Split partially exercised areas rather than hiding gaps;
no prescribed coverage field or status vocabulary is required.

| Area | Practical checks | Evidence and user impact |
| --- | --- | --- |
| Keyboard and focus | Enter and leave by keyboard; traverse in both directions; activate with applicable keys; exercise pattern-specific navigation, dismissal and focus return. Inspect initial, visible and unobscured focus, order, disabled items, portals and rerenders where relevant. | Record the action sequence and focused element before/after, alongside visible focus evidence. Explain if someone cannot reach, operate, escape or resume their task. |
| Names, roles, relationships and state | Compare visible purpose with computed name/description and role. Check label association, relationship targets, required owned structures where applicable, expanded/selected/checked/disabled/invalid states and their updates. Distinguish focus from selection. | Capture relevant DOM and accessibility-tree excerpts, including referenced elements and state transitions. Explain ambiguity, missing context or misleading state; valid attributes alone do not prove a usable task. |
| Dynamic announcements | Trigger relevant validation, loading, result, selection and status updates, including repeated updates. Check whether focus should move or information should be conveyed without moving it; inspect timing and live-region setup. | Separate DOM/tree changes from actual AT observations. Explain what information a nonvisual user misses, hears too late or hears repeatedly. Do not assume every change requires a live region. |
| Contrast and forced colors | Inspect applicable text, controls, icons, boundaries, focus and selected/error states. Measure relevant rendered foreground/background combinations with an available authorized tool. Exercise actual forced-colors mode when available. | Record colors, measurement method, state and applicable criterion. Screenshots alone are not contrast measurements. Distinguish emulation from the OS mode; explain lost meaning or discoverability. |
| Reflow, text resize and zoom | Use criterion-appropriate viewport/text-resize/zoom conditions for the scenario, including popup positioning and scrolling. Look for clipped content, overlapping controls, lost labels, hidden focus or unavailable actions. | Record viewport, zoom/resize method and observed task outcome. Browser zoom, OS scaling and a smaller viewport are not interchangeable evidence. Explain what becomes unreadable or inoperable. |
| Motion and timing | Where present, inspect animation, auto-updates, pause/stop controls, time limits and relevant reduced-motion settings. Avoid exposing a person to potentially harmful flashing content; use safe inspection and report unavailable visual checks. | Record which motion/settings were exercised and the applicable requirement. Explain distraction, discomfort or lost time to act; reduced-motion support alone is not a blanket WCAG requirement or conformance proof. |

Keyboard expectations depend on the actual widget and modality. Do not impose a
blanket focus trap on nonmodal popups: evaluate reachable content, predictable
order, appropriate dismissal and a way to leave. A modal dialog has different
focus-management expectations; verify its actual modality, applicable contracts
and the advisory [dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
instead of assuming any popup is modal. Similarly, not every item in a composite
widget needs a separate Tab stop; test its applicable navigation model.

Automated semantic checks and existing focused unit/browser tests can supplement
these rows when available and authorized. Limit selectors to the affected
component, variants and relevant callers. Record rule exclusions and runner
versions. Neither a clean scanner nor simulated key events replace manual
keyboard, visual or actual AT checks that the claim requires.

### Actual assistive technology

Screen-reader speech claims require an actual named AT/browser/OS combination,
versions, interaction mode, settings relevant to the scenario, a healthy rendered
target and authorization to operate that session. Confirm the AT is running,
focus is on the intended page and the tester knows the relevant navigation
commands. Record the actual commands and observed output, distinguishing quoted
speech from a tester's paraphrase. A speech log can help if supported and
authorized; do not claim to have heard output merely because a DOM live region
or accessibility-tree node changed.

If actual AT or a capable operator is unavailable, say so and leave the speech
claim unresolved. Provide a manual recipe with the
target version, platform prerequisites, initial state, specific navigation and
activation sequence, expected semantic information, observations to capture and
reset instructions. Do not invent exact spoken wording; voice and verbosity
settings vary. A result on one combination does not establish all-platform
behavior. Test another combination only when it discriminates a credible
platform explanation within the agreed boundary, or leave it explicitly deferred.

## 5. Copyable claim recipe

Use this short outline when a copyable recipe helps; adapt it to the scenario.
It is not a required form, executed test or reason to install a runner.

```text
Scenario and user task; relevant variants and exclusions:
Target source/runtime revision and environment; missing prerequisites:
Permitted workspace/resources, setup and freshness check:
Numbered interaction steps; exact existing command where applicable:
Expected result and applicable contract; pass/fail condition:
Actual observations and evidence locators (only after execution):
Limits, alternative explanations and next check:
Reset steps; bounded stop condition and resources owned by this run:
```

For approved fix verification, duplicate the recipe for the fixed identity and
retain the original baseline evidence. Include a focused regression assertion
at the correct layer without weakening the original scenario. Diagnosis alone
does not authorize adding that test to project files.

## 6. Failure paths and evidence handoff

Set a bounded run budget before execution. If tooling fails, record the exact
command/interaction and error, then try only an authorized, bounded alternative
that answers the same question. Do not loop indefinitely, broaden the audit,
install a missing tool or change source to force a result. Stop and report when
permissions, authentication, browser ownership, build identity, harness health,
AT availability or required dependencies block a trustworthy observation.
Provide the remaining manual steps and prerequisites. A blocked or
not-reproduced experiment does not establish that there is no defect.

Keep relevant traces, screenshots and measurements at actual authorised
locators, then report observations, counterevidence and remaining checks using
the evidence guide. For example: "After Tab, focus moves to the body instead of
the next action; this interrupts the user's task." Explain what that observation
establishes and what still needs investigation. Do not turn the recipe or a
blocked experiment into a claim of successful execution.
