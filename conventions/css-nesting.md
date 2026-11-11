# CSS Nesting

## Purpose

Capture a personal implementation and review check for repeated parent selectors.
Apply it when authoring or reviewing related CSS rules, subject to the target
repository's contribution rules and supported CSS toolchain.

## Prefer grouped parent and child rules

When a parent state has its own declarations and related descendant styling,
prefer nesting the descendant rule inside that parent instead of repeating the
full parent selector:

```css
@media (forced-colors: active) {
  .root:where([data-disabled]) {
    color: GrayText;

    .checkIcon {
      color: GrayText;
      border-color: GrayText;
    }
  }
}
```

This keeps the state and its slot treatment together without repeating
`.root:where([data-disabled])`.

## Safeguards

- Preserve the selector relationship, cascade layer, source order, and effective
  specificity. Do not accidentally turn a descendant into a direct child.
- Keep state qualifiers in `:where(...)` where the owning package requires it.
- Do not introduce nesting solely to wrap a single child rule when the parent
  has no declarations; follow the repository's flattening guidance.
- Do not group selectors when their states, layers, or ordering intentionally
  differ. Native nesting can change specificity for selector lists; verify
  equivalence rather than assuming a mechanical rewrite is harmless.
- Use the repository formatter and CSS lint, and validate the affected rendered
  states. A structural CSS refactor should not change appearance or behavior.
- The `GrayText` values above illustrate an already-authorized contrast fix,
  not permission to add forced-colors overrides to other components.

This is a personal workbench check, not a new shared repository policy.
