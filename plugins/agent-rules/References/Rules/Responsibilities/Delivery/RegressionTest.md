# Regression Test Rules

Use this file when guarding against previously fixed bugs or behavior drift.

## Core Rules

- Capture the exact behavior that must not break again.
- Write the smallest test that reproduces the historical failure.
- Keep the regression case easy to understand from the test name and data.
- Tie the test to the bug scenario, not just the implementation detail.

## Output

- Repro case
- Guard test
- Expected behavior

