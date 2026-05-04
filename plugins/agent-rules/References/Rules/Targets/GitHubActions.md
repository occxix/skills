# GitHub Actions Rules

Use this file for GitHub Actions workflows.

## Core Rules

- Keep workflows deterministic and idempotent.
- Use clear job boundaries for restore, build, test, and publish steps.
- Cache dependencies when it improves reliability and speed.
- Pin action versions deliberately.
- Keep secrets out of workflow files.

## Avoid

- Hidden side effects between jobs.
- Overly clever workflow logic that is hard to debug.

