# Avalonia Rules

Use this file for Avalonia desktop applications.

## Core Rules

- Prefer MVVM and binding-first UI structure.
- Keep code-behind minimal.
- Use cross-platform abstractions for OS-specific behavior.
- Keep styles, resources, and viewmodels organized by feature or screen.
- Follow the repo’s existing Avalonia project conventions for XAML and startup wiring.

## Avoid

- Platform-specific logic leaking into views.
- Business logic in XAML event handlers.

