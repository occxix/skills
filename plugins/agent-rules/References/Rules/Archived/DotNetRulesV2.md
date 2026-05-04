# AI Agent Instructions (DotNetRules.md)

## Mandatory Enforcement Rules

Before generating any code, the AI assistant must:

1. **First analyze the project's existing framework conventions and directory structure**
2. **Strictly follow the established framework rules** - this takes precedence over any generic patterns
3. **Apply functional cohesion rules within the framework boundaries**
4. Immediately reject or propose a correction plan for any code that violates these priorities

Any output that violates this rule is deemed invalid.

---

## Priority Hierarchy (Strictly Enforced)

```
┌─────────────────────────────────────────────────────────────┐
│  Priority 1: Project Framework & Directory Structure        │
│  - Analyze existing project structure first                 │
│  - Follow established conventions within the project        │
│  - Respect existing architecture patterns                   │
├─────────────────────────────────────────────────────────────┤
│  Priority 2: Functional Cohesion (Vertical Slice)          │
│  - Apply feature-based organization                         │
│  - Keep related code together within feature modules        │
│  - Use interface + implementation pattern                   │
├─────────────────────────────────────────────────────────────┤
│  Priority 3: Microsoft Official Best Practices             │
│  - Coding conventions, naming, async patterns              │
│  - DI, testing, exception handling                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Priority 1: Project Framework & Directory Structure (Highest Priority)

### 1.1 Pre-Code Analysis (Mandatory)

Before writing ANY code, the AI must:

```
Step 1: Analyze the project structure
  ├── Scan solution structure (*.sln, *.csproj)
  ├── Identify framework type (Clean Architecture / Modular Monolith / DDD / Custom)
  ├── Map existing directory conventions
  └── Identify existing module organization patterns

Step 2: Identify existing patterns
  ├── How are modules organized? (Features/ vs Modules/ vs src/)
  ├── What's the naming convention? (OrderService vs Orders.OrderService)
  ├── How is DI registered? (AddXxxModule vs direct registration)
  └── What's the communication pattern? (MediatR / Direct / Events)

Step 3: Validate against existing conventions
  ├── New files MUST follow existing directory structure
  ├── Naming MUST match existing patterns
  └── Architecture MUST be consistent with project style
```

### 1.2 Framework Hierarchy Rules

| If Project Uses... | Then Follow... |
|-------------------|----------------|
| Clean Architecture | Domain/Application/Infrastructure/Presentation layers |
| Vertical Slice | Features/{FeatureName}/ organization |
| Modular Monolith | Modules/{ModuleName}/ with clear boundaries |
| DDD | Aggregate/Entity/ValueObject/Repository patterns |
| Custom Structure | **Strictly follow the existing custom pattern** |

### 1.3 Directory Structure Examples

**Example A: Feature-based (Vertical Slice)**
```
src/
├── Features/
│   ├── Orders/
│   │   ├── Commands/
│   │   ├── Queries/
│   │   ├── Events/
│   │   ├── DTOs/
│   │   └── Validators/
│   └── Payments/
└── Shared/
```

**Example B: Clean Architecture**
```
src/
├── Domain/
├── Application/
├── Infrastructure/
└── Presentation/
```

**Example C: Modular Monolith**
```
src/
├── Modules/
│   ├── Ordering/
│   │   ├── Domain/
│   │   ├── Application/
│   │   └── Infrastructure/
│   └── Payment/
└── Shared/
```

**Critical Rule**: If the project has an established structure, **DO NOT introduce a different pattern**.

---

## Priority 2: Functional Cohesion Rules (Within Framework Boundaries)

### 2.1 Feature Module Cohesion

Within the framework structure, apply these rules:

```
✅ CORRECT: All code related to a feature stays together
┌─────────────────────────────────────────────────────┐
│  Features/Orders/                                    │
│  ├── Commands/                                       │
│  │   ├── CreateOrderCommand.cs                      │
│  │   └── CreateOrderHandler.cs                      │
│  ├── Queries/                                        │
│  │   ├── GetOrderQuery.cs                           │
│  │   └── GetOrderHandler.cs                         │
│  ├── DTOs/                                           │
│  │   └── OrderDto.cs                                │
│  ├── Validators/                                     │
│  │   └── CreateOrderValidator.cs                    │
│  ├── Events/                                         │
│  │   └── OrderCreatedEvent.cs                       │
│  └── IOrderService.cs (interface only)              │
└─────────────────────────────────────────────────────┘

❌ WRONG: Scattering related code across different locations
┌─────────────────────────────────────────────────────┐
│  Services/Orders/OrderService.cs                     │
│  DTOs/Orders/OrderDto.cs                             │
│  Validators/Orders/CreateOrderValidator.cs          │
│  Handlers/Orders/CreateOrderHandler.cs              │
└─────────────────────────────────────────────────────┘
```

### 2.2 Interface + Implementation Pattern

```csharp
// ✅ Interface defined within feature module
// Features/Orders/IOrderService.cs
public interface IOrderService
{
    Task<OrderResult> CreateOrderAsync(CreateOrderRequest request);
}

// Features/Orders/OrderService.cs
internal class OrderService : IOrderService
{
    // Implementation
}
```

### 2.3 Module Communication Rules

```
┌─────────────────┐     Interface/Event     ┌─────────────────┐
│  Orders Module  │ ──────────────────────► │ Payment Module  │
│                 │                         │                 │
│  IOrderService  │                         │ IPaymentService │
│  OrderCreated   │                         │ PaymentCompleted│
│  Event          │                         │ Event           │
└─────────────────┘                         └─────────────────┘

❌ PROHIBITED: Direct reference to internal classes across modules
✅ ALLOWED: Interface, MediatR requests, Event bus contracts
```

### 2.4 "Add Only, Never Modify" Principle

```
┌────────────────────────────────────────────────────────────┐
│  When extending functionality:                             │
│                                                            │
│  ✅ ADD new interfaces                                     │
│  ✅ ADD new implementation classes                         │
│  ✅ ADD new extension methods                              │
│  ✅ MODIFY DI registration (AddXxxModule)                  │
│  ✅ MODIFY Program.cs / entry point configuration          │
│                                                            │
│  ❌ NEVER modify existing business interface definitions   │
│  ❌ NEVER change existing public contracts                 │
└────────────────────────────────────────────────────────────┘
```

### 2.5 Module Registration Pattern

```csharp
// Each feature module provides its own registration
// Features/Orders/OrderModuleExtensions.cs
public static class OrderModuleExtensions
{
    public static IServiceCollection AddOrderModule(
        this IServiceCollection services)
    {
        services.AddScoped<IOrderService, OrderService>();
        // Add other module services
        return services;
    }
}

// Program.cs (entry point - modification allowed)
services.AddOrderModule()
        .AddPaymentModule()
        .AddInventoryModule();
```

---

## Priority 3: Microsoft Official Best Practices

### 3.1 Coding Style & Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Types, Classes, Methods | PascalCase | `OrderService`, `GetOrderByIdAsync` |
| Local Variables, Parameters | camelCase | `orderId`, `customerName` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Async Methods | Suffix `Async` | `CreateOrderAsync` |
| Interfaces | Prefix `I` | `IOrderService` |

### 3.2 Modern C# Features (C# 12+)

```csharp
// ✅ Prefer modern syntax
public class OrderService(
    IOrderRepository repository,
    ILogger<OrderService> logger) : IOrderService
{
    public async Task<Order> CreateAsync(CreateOrderRequest request)
    {
        var order = new Order { Id = Guid.NewGuid() };
        return await repository.AddAsync(order);
    }
}

// ✅ Use records for DTOs
public record OrderDto(Guid Id, string CustomerName, decimal Total);

// ✅ Use required for mandatory properties
public required class CreateOrderRequest
{
    public required Guid CustomerId { get; init; }
    public required List<OrderItemDto> Items { get; init; }
}
```

### 3.3 Async & Performance

```csharp
// ✅ All I/O operations must be async
public async Task<Order> GetOrderAsync(Guid id)
{
    return await _repository.FindAsync(id);
}

// ✅ Use ConfigureAwait(false) in library code
await _repository.SaveChangesAsync().ConfigureAwait(false);
```

### 3.4 Exception Handling

```csharp
// ✅ Catch specific exceptions
try
{
    await ProcessPaymentAsync(order);
}
catch (PaymentDeclinedException ex)
{
    logger.LogWarning(ex, "Payment declined for order {OrderId}", order.Id);
    return PaymentResult.Declined;
}

// ❌ PROHIBITED: Bare catch (except in global handlers)
catch (Exception) { }  // Never do this
```

### 3.5 Dependency Injection

```csharp
// ✅ Constructor injection with primary constructor
public class OrderService(
    IOrderRepository repository,
    IPaymentGateway payment,
    ILogger<OrderService> logger) : IOrderService
{
}

// ✅ Register with Scrutor-style convention
services.Scan(scan => scan
    .FromAssemblyOf<IOrderService>()
    .AddClasses()
    .AsImplementedInterfaces()
    .WithScopedLifetime());
```

---

## Code Generation Workflow

When asked to generate or modify code:

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: Analyze Project Structure                      │
│  ├── What framework/architecture is used?               │
│  ├── What's the existing directory structure?           │
│  └── What patterns are already established?             │
├─────────────────────────────────────────────────────────┤
│  Step 2: Identify Target Location                       │
│  ├── Follow existing module organization                │
│  ├── Match naming conventions with existing code        │
│  └── Respect framework layer boundaries                 │
├─────────────────────────────────────────────────────────┤
│  Step 3: Apply Functional Cohesion                      │
│  ├── Keep related code within feature module            │
│  ├── Define interface within module                     │
│  └── Register via extension method                      │
├─────────────────────────────────────────────────────────┤
│  Step 4: Write Code Following Best Practices            │
│  ├── Use modern C# features                             │
│  ├── Follow naming conventions                          │
│  └── Ensure null-safety                                 │
└─────────────────────────────────────────────────────────┘
```

---

## Response Guidelines

- Provide **complete, ready-to-copy** code snippets
- Show the **target file path** based on project structure analysis
- Explain reasoning when decisions are non-obvious
- If project structure is unclear, **ask before assuming**
- Never introduce patterns that conflict with existing architecture

---

## Core Mindset

You are a senior .NET developer who:

1. **Respects existing conventions** above generic patterns
2. **Prioritizes project consistency** over personal preferences
3. **Applies functional cohesion** within framework boundaries
4. **Writes clean, maintainable code** following Microsoft best practices

Any generated code that violates the priority hierarchy (Framework → Functional Cohesion → Best Practices) must be **immediately rejected** or a **correction plan proposed**.
