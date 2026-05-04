## Mandatory Enforcement Rules
Before generating any code, the AI assistant must:

First completely read the entire content of this file
Confirm understanding of all architecture and coding specifications
Immediately reject or propose a correction plan for any code that violates this file

Any output that violates this rule is deemed invalid.

# Build / Infrastructure Layer Rules

This is the Build / Infrastructure / Deployment layer.

## Strict Constraints
- All CI/CD pipelines must use GitHub Actions (or the project's chosen tool).
- Dockerfiles must be **multi-stage** builds and run as non-root user.
- Versioning must strictly follow **SemVer**.
- No hard-coded secrets or credentials — use GitHub Secrets, Azure Key Vault, or environment variables.
- All configuration must be done through `appsettings.json` + environment-specific files or `IOptions<T>`.
- Build scripts must be idempotent and support clean rebuilds.
- Use `dotnet format` + analyzers in every build step.

## Forbidden Practices
- Never commit secrets, certificates, or sensitive files.
- Do not use `BuildServiceProvider()` in Program.cs or extension methods.
- No custom MSBuild targets that bypass standard .NET build process unless approved.

Apply these rules on top of Agents.md when working in Build / Infrastructure layer.

For analysis, planning, implementation, and verification flow, also read the relevant files under `References/Rules/Responsibilities/`.
For platform-specific build targets, also read the relevant files under `References/Rules/Targets/`:

- `GitHubActions.md`
- `Docker.md`
- `Aot.md`
