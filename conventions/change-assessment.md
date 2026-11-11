# Change Assessment

## Scope and Loading

This personal convention applies to implementation planning and code reviews
across all repositories. Load it after task triage when planning implementation
or assessing a proposed change, and as part of every code review. Reload it when
growing complexity calls for reassessing the approach.

Keep the assessment proportionate to the change. Trivial work does not require
a separate analysis ceremony; material trade-offs need explicit reasoning.
This convention does not replace the target repository's contribution rules.

## Necessity, Proportionality, and Scope

Before implementation, and as part of every code review, assess whether the
change should be made, not only whether it works.

- Establish the need. Identify the actual user impact and supporting evidence.
  Distinguish functional failures, security or accessibility issues, and
  contractual requirements from warnings, cosmetic concerns, and speculative
  future problems. Do not assume a reported issue justifies the proposed
  solution.
- Compare benefit with total cost. Consider runtime and bundle overhead,
  compatibility risk, architectural complexity, duplicated infrastructure,
  testing burden, and long-term maintenance. Passing tests and finding no
  concrete defects do not establish that a change is worth shipping. Equally,
  a small visible symptom can justify substantial work when the evidence
  supports it.
- Consider simpler alternatives - including no change. Check whether existing
  infrastructure can solve the problem, whether a documented limitation is
  acceptable, or whether the work belongs with a future dependency or
  support-policy update. Do not silently drop supported behavior to simplify
  the implementation.
- Separate independently valuable changes. Identify fixes, refactors,
  infrastructure work, and policy decisions that can be reviewed and shipped
  independently. Recommend smaller, coherent PRs when that reduces risk or
  allows a useful fix to proceed without a disputed approach. Do not split
  tightly coupled changes into incomplete or unsafe intermediate states.
- Reassess when complexity grows. If addressing edge cases introduces new
  mechanisms or substantially expands the original scope, revisit the approach
  rather than continuing to patch it by default. Previous effort is not, by
  itself, a reason to continue.
- Report the architectural judgment explicitly. Distinguish confirmed defects
  from concerns about necessity, proportionality, or scope. Support those
  concerns with concrete costs, affected contracts, and realistic alternatives -
  not personal preference. "No confirmed defects" must not automatically become
  a recommendation to approve.

When a material trade-off requires a product, architecture, or compatibility
decision, explain it and seek guidance before implementing or expanding the
work. A recommendation to defer, split, or decline a change is a valid outcome;
it does not authorize changing the user's requested scope or upstream state.
