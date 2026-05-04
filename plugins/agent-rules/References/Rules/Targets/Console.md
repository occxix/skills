# Console App Rules

Use this file for console apps, worker processes, and CLI tools.

## Core Rules

- Keep startup, command parsing, and business logic separated.
- Use dependency injection when the repo already uses it.
- Make exit codes and error handling explicit.
- Prefer structured output and clear command names.
- Respect cancellation tokens for long-running work.

## Avoid

- Monolithic `Main` methods.
- Mixing CLI parsing, orchestration, and business logic in one class.

