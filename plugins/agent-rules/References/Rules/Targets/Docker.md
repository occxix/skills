# Docker Rules

Use this file for Dockerfiles and container image design.

## Core Rules

- Use multi-stage builds.
- Run containers as non-root unless the project explicitly requires otherwise.
- Keep images slim and reproducible.
- Avoid baking secrets into images.
- Prefer clear, deterministic build steps.

## Avoid

- Single-stage production images for app workloads.
- Dockerfiles that depend on hidden local state.

