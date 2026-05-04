# WinForms Rules

Use this file for WinForms desktop applications.

## Core Rules

- Keep event handlers thin.
- Respect designer-generated code and partial classes.
- Keep UI-thread interactions explicit.
- Move shared behavior into services or presenter-style classes when the project already uses them.
- Preserve the existing form layout and naming conventions.

## Avoid

- Large methods inside form event handlers.
- UI logic that cannot be reused or tested.

