# ASP.NET Web Forms Rules

Use this file for legacy ASP.NET Web Forms projects.

## Core Rules

- Preserve the page lifecycle and the existing code-behind structure.
- Keep event handlers thin and move reusable logic into services or helpers that fit the project.
- Avoid migrating the project to MVC or Razor unless the user explicitly asks for that change.
- Treat designer-generated files as framework-managed surface area.
- Be careful with ViewState, postbacks, and control IDs.

## Avoid

- Large code-behind methods.
- Structural changes that fight the existing Web Forms model.

