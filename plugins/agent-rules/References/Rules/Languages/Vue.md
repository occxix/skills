# Vue Rules

Use this file for Vue 3 + Vite projects.

## Core Rules

- Use `<script setup>` and the Composition API.
- Keep components small and focused.
- Keep state in Pinia or the project’s established store pattern.
- Route through Vue Router when the project uses routing.
- Keep API access in typed wrappers or composables.

## Avoid

- Options API in new code unless the repo is legacy.
- Direct DOM manipulation or business logic in templates.

