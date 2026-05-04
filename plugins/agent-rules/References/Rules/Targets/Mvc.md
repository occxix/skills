# ASP.NET MVC Rules

Use this file for ASP.NET MVC projects.

## Core Rules

- Keep controllers thin and move domain or application logic out of actions.
- Use view models for UI shaping.
- Keep view logic in views, filters, or reusable components, not in controllers.
- Respect the project’s route, filter, and layout conventions.
- Use antiforgery protection and proper validation where the project expects it.

## Avoid

- Business logic in controllers.
- View-specific concerns leaking into shared services.

