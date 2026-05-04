# .NET AOT Rules

Use this file for trimming, NativeAOT, and publish-time compatibility work.

## Core Rules

- Prefer reflection-safe code paths.
- Avoid runtime code generation unless the project explicitly supports it.
- Favor source generators and compile-time metadata when available.
- Test publish and runtime behavior under the target AOT configuration.
- Keep serialization, activation, and plugin loading AOT-friendly.

## Avoid

- Unbounded reflection, dynamic assembly loading, and implicit runtime type discovery.

