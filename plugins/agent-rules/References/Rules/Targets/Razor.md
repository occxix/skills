# Razor Rules

Use this file for Razor Pages or server-rendered Razor projects.

## Core Rules

- Keep page handlers or component code thin.
- Use page models, view models, or components to structure UI logic.
- Keep markup and behavior aligned with the project’s established Razor conventions.
- Use antiforgery, validation, and route conventions when the repo already relies on them.

## Avoid

- Putting non-UI business logic directly in page handlers or `.cshtml` files.

