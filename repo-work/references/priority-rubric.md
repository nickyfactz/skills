# Priority rubric

## Impact

- **High**: likely to reduce recurring defects, complexity, runtime cost, or
  maintenance overhead on an important path.
- **Medium**: materially improves maintainability or safety without affecting a
  critical path.
- **Low**: mostly cleanup, consistency, or convenience.

## Effort

- **Low**: localized change with a limited blast radius.
- **Medium**: crosses a few modules, tests, docs, or configuration files.
- **High**: broad structural change, interface migration, or many dependent
  callers.

## Risk

- **Low**: behavior-preserving and easy to validate.
- **Medium**: touches core paths or shared contracts.
- **High**: affects public APIs, persistence, concurrency, security, or critical
  workflows.

## Confidence

- **High**: supported by direct file-level or runtime evidence.
- **Medium**: strong indicator, but some paths or ownership are unclear.
- **Low**: plausible hypothesis that needs confirmation.
