# WPF Rules

Use this file for WPF desktop applications.

## Core Rules

- Prefer MVVM and data binding.
- Keep code-behind minimal and UI-focused.
- Use `ICommand`, `INotifyPropertyChanged`, and resource dictionaries where the repo already follows that style.
- Marshal UI updates onto the UI thread correctly.
- Keep reusable UI logic out of XAML event handlers.

## Avoid

- Business logic in code-behind.
- UI coupling that makes viewmodels impossible to test.

