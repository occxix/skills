# Core Stack Index

Use these rules for application code, APIs, UI, deployment, and platform entry
points.

## Root-Level Rules

- `DotNetRules.md`
- `BackendRules.md`
- `BuildRules.md`
- `DotNetStyle.md`
- `DotNetLogging.md`
- `VueRules.md`

## Language Rules

- `Languages/CSharp.md`
- `Languages/Rust.md`
- `Languages/Go.md`
- `Languages/Java.md`
- `Languages/Python.md`
- `Languages/JavaScript.md`
- `Languages/Vue.md`

## Target Rules

- `Targets/WebApi.md`
- `Targets/Mvc.md`
- `Targets/Razor.md`
- `Targets/WebForms.md`
- `Targets/Console.md`
- `Targets/Wpf.md`
- `Targets/WinForms.md`
- `Targets/Avalonia.md`
- `Targets/Android.md`
- `Targets/BrowserExtension.md`
- `Targets/Aot.md`

## Infrastructure Rules

- `Targets/Docker.md`
- `Targets/GitHubActions.md`

## Core Constraints

- Keep framework and feature code separated.
- Keep endpoints, handlers, and UI surfaces thin.
- Prefer async I/O and avoid blocking hot paths.
- Route target-specific work to the narrowest matching file.
- Prefer `.claude/CLAUDE.md` when Claude Code is the target and the repo supports it.

