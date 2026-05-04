## Mandatory Enforcement Rules
Before generating any code, the AI assistant must:

First completely read the entire content of this file
Confirm understanding of all architecture and coding specifications
Immediately reject or propose a correction plan for any code that violates this file

Any output that violates this rule is deemed invalid.

# Vue + Vite Layer Rules

This is the Vue 3 + Vite frontend layer (Vue + Vite project).

## Strict Constraints
- Always use **Vue 3 Composition API** with `<script setup>` syntax (Options API is only allowed for legacy components).
- All components must be written as **Single-File Components (SFC)** with clear separation of `<template>`, `<script setup>`, and `<style>`.
- State management must use **Pinia** (never use Vuex unless it's a legacy project).
- Routing must use **Vue Router 4+** with composition API style (`useRouter`, `useRoute`).
- All API calls must go through **typed Axios / fetch wrappers** or Pinia actions — never use raw `fetch` or `axios` directly in components.
- Use **TypeScript** strictly (`<script setup lang="ts">`).
- Styling must use the project's design system (Tailwind CSS, UnoCSS, or scoped CSS variables). Prefer utility-first classes.
- Environment variables must be accessed via `import.meta.env.VITE_xxx` and validated.
- Use Vite's built-in features: `defineConfig`, plugins (`@vitejs/plugin-vue`, `vite-plugin-vue-devtools`, etc.).
- Components should be small and focused. Use `defineAsyncComponent` for lazy loading heavy components.
- All props must be defined with `defineProps` + TypeScript interfaces and proper defaults.

## Forbidden Practices
- Do not use `this` in `<script setup>` or mix Options API with Composition API.
- Never perform DOM manipulation directly (no `document.getElementById`, no jQuery).
- Do not put business logic or API calls directly in `<template>` or `@click` handlers — delegate to composables or stores.
- No hard-coded strings for routes, API endpoints, or magic numbers — use constants or composables.
- Do not commit `node_modules`, `.vite/`, or `dist/` folders.
- Avoid deep nesting of components (keep component tree shallow).
- Never use `v-html` unless content is fully sanitized.

## Vite-Specific Best Practices
- Always configure `vite.config.ts` with proper plugins and aliases (`@/*` → `src/*`).
- Use `vite-plugin-vue-inspector` during development for better debugging.
- Enable `strict` mode in `tsconfig.json` and Vite's TypeScript checking.
- All builds must pass `vite build --mode production` without warnings.

Apply these rules on top of Agents.md / AGENTS.md when working in any Vue + Vite related files (`.vue`, `vite.config.ts`, `src/` frontend folder, etc.).