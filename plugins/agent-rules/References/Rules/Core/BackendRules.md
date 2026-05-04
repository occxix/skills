## Mandatory Enforcement Rules
Before generating any code, the AI assistant must:

First completely read the entire content of this file
Confirm understanding of all architecture and coding specifications
Immediately reject or propose a correction plan for any code that violates this file

Any output that violates this rule is deemed invalid.

# Backend Layer Rules

This is the Backend layer (API / Services / Features / Infrastructure).

## Strict Constraints
- Must **100% follow** "Interface + Implementation + Add-Only, Never Modify" principle.
- All business operations must use **MediatR CQRS** (Command/Query/Handler pattern).
- Every public service must be exposed through an **interface**.
- Database access is **only allowed through repositories** — never use DbContext directly outside Infrastructure.
- All endpoints must return `Result<T>` / `ApiResponse<T>` or `PaginatedResponse<T>`.
- Use FluentValidation for all input validation.
- Every module must provide `AddXXXModule()` extension method for registration.

## Forbidden Practices
- Never modify existing business interfaces in Features/*.
- Do not create new static classes for business logic.
- Do not add direct references between modules — only through interfaces or MediatR.
- No synchronous database calls — all must be async.

Apply these rules on top of Agents.md when working in Backend layer.

For analysis, planning, implementation, and verification flow, also read the relevant files under `References/Rules/Responsibilities/`.
For application-entry patterns, also read the relevant files under `References/Rules/Targets/`:

- `WebApi.md`
- `Mvc.md`
- `Razor.md`
- `WebForms.md`
- `Console.md`
