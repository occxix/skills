# .NET Logging Rules

Use this file when a .NET project needs logging setup or logging-related constraints.

## Core Rules

- Use `Microsoft.Extensions.Logging` as the abstraction.
- Use dependency injection to obtain `ILogger<T>`.
- Use structured logging with placeholders, not string interpolation.
- Log important entry, exit, and error paths with contextual values.
- Support runtime log level configuration through `appsettings.json`.
- Use environment-specific config files such as `appsettings.Development.json` and `appsettings.Production.json`.

## Recommended Setup

- Development: console logging with detailed output.
- Production: structured logging provider such as Serilog when the project already uses it.
- Keep log levels adjustable per namespace.

## Good Practice

```csharp
logger.LogInformation("Processing order {OrderId} for user {UserId}", orderId, userId);
```

## Avoid

```csharp
logger.LogInformation($"Processing order {orderId} for user {userId}");
```

