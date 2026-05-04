# C# Language Rules

Use this file for C# language-level conventions.

## Core Rules

- Use `PascalCase` for types, members, and namespaces.
- Use `camelCase` for locals and parameters.
- End async methods with `Async`.
- Use `required`, `init`, records, `with`, nullable reference types, and file-scoped namespaces when the repo already supports them.
- Prefer `async/await + Task` for I/O work.

## Avoid

- Bare `catch (Exception)` unless the repo has a top-level handler.
- Style that conflicts with the project’s existing C# conventions.

