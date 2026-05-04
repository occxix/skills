# .NET Style Rules

This file is a transition layer. Prefer `Languages/CSharp.md` for new guidance.

Use this file for repo-wide C# naming and code-style defaults.

## Naming

- Types, classes, methods, and properties use `PascalCase`.
- Local variables and parameters use `camelCase`.
- Async methods end with `Async`.
- Interfaces start with `I`.

## Modern C#

- Prefer primary constructors, `required` members, `init` properties, records, and nullable reference types when the repo already uses them.
- Use file-scoped namespaces and global usings when the repo already follows that pattern.

## Async and Exceptions

- Use `async/await + Task` for I/O work.
- Catch only specific exceptions that can be handled meaningfully.

## General Guidance

- Prefer readability and consistency with the existing repo over personal style preferences.
- Follow the repository’s established formatting and analyzer conventions.
