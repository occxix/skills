# .NET Framework Rules

Use this file for project-wide C# and .NET framework decisions.

## What Belongs Here

- Top-level architecture confirmation
- Solution and project structure conventions
- Layer boundaries and dependency direction
- Feature/module cohesion rules
- Registration and composition-root rules
- Add-only constraints for shared contracts
- Rules that apply across the whole .NET repo, not just one layer

## What Does Not Belong Here

- Backend-specific CQRS rules
- Build and deployment rules
- Frontend rules
- Low-level style rules
- Logging policy details

## 1. Confirm the Architecture

Before changing the framework structure:

1. Scan the repository layout and existing `.sln` / `.csproj` files.
2. Identify the current architectural shape.
3. Follow the existing structure instead of introducing a new one.
4. If the architecture is still unclear, ask the user before writing files.

### Claude project preference

When the project uses Claude Code, prefer `.claude/CLAUDE.md` over root `CLAUDE.md` when the repo convention allows it.

## 2. Keep the Framework Cohesive

- Keep the project organized around the existing top-level architecture.
- Keep related framework concerns together in the same layer or module.
- Avoid spreading one framework concern across unrelated folders.
- Keep naming, namespace, and folder conventions consistent with the repo.

## 3. Dependency Boundaries

- Prefer upward-only dependency flow when the architecture expects it.
- Keep shared abstractions at the layer where they are owned.
- Avoid direct cross-module coupling unless the current architecture already permits it.
- Use composition-root registration instead of scattered ad hoc wiring.

## 4. Add-Only Changes

- Prefer adding new framework pieces instead of rewriting stable ones.
- Do not modify existing public contracts unless the user explicitly requests it.
- When a change affects a shared boundary, stop and confirm the impact.

## 5. Framework-Level Validation

Before finalizing a framework change, verify:

- The directory shape still matches the architecture.
- The new files fit the existing naming conventions.
- The dependency direction is still coherent.
- The change does not split one framework concern into multiple unrelated locations.

For target-specific project types, see the `Targets/` files under `References/Rules/`.
For C# language details, see `Languages/CSharp.md`.
For project workflow roles, see the `Responsibilities/` files under `References/Rules/`.

For logging rules, see `DotNetLogging.md`.
