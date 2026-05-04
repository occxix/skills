# Rust Rules

Use this file for Rust projects.

## Core Rules

- Prefer explicit ownership and borrow boundaries.
- Keep modules small and focused.
- Use `Result` and `Option` intentionally.
- Prefer `clippy`-friendly, idiomatic Rust.
- Keep async runtime choices consistent with the existing project.

## Avoid

- Overuse of `unwrap()` and `expect()`.
- Hidden global state or unclear ownership.

