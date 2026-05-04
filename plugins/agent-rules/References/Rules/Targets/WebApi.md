# ASP.NET Core Web API Rules

Use this file for ASP.NET Core API projects.

## Core Rules

- Keep endpoints thin and push business logic into the architecture’s service or feature layer.
- Use the project’s existing API style: controllers, minimal APIs, or a mix only when the repo already does that.
- Keep request validation, response shaping, and auth concerns explicit.
- Prefer stable route conventions and versioning when the project already uses them.
- Return the repo’s standard API response shape.

## Avoid

- Putting business logic directly in controllers or endpoint lambdas.
- Mixing unrelated API styles in the same project unless the repo already does so.

