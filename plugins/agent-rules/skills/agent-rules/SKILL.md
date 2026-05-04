---
name: agent-rules
description: Use when creating, updating, merging, or replacing project-level AI instruction files (CLAUDE.md / AGENTS.md / Agents.md) for Claude Code, OpenCode, Copilot CLI, Hermes Agent, or Gemini CLI.
---

# Agent Rules

Manage project-level AI instruction files so the agent follows the repo's conventions.

## 规则库

Use the rules library in `References/Rules/`:

Core development rules now live under `Core/`; build and infrastructure rules
live under `Ops/`.

| 文件 | 适用场景 |
|------|----------|
| Core/DotNetRules.md | C# / .NET 项目（框架级架构与边界） |
| Core/DotNetLibrary.md | C# 类库设计（扩展点、Options、上下文对象、特性发现） |
| Languages/CSharp.md | C# 语言、命名、async、异常、现代语法 |
| Languages/Rust.md | Rust 语言与项目约束 |
| Languages/Go.md | Go 语言与项目约束 |
| Languages/Java.md | Java 语言与项目约束 |
| Languages/Python.md | Python 语言与项目约束 |
| Languages/JavaScript.md | JavaScript 语言与项目约束 |
| Languages/Vue.md | Vue 3 + Vite 前端 |
| Core/DotNetStyle.md | .NET 旧版风格补充（过渡兼容） |
| Core/DotNetLogging.md | .NET 日志、日志级别、结构化输出 |
| Targets/WebApi.md | ASP.NET Core Web API |
| Targets/WebForms.md | ASP.NET Web Forms |
| Targets/Mvc.md | ASP.NET MVC |
| Targets/Razor.md | Razor Pages / Server-side Razor |
| Targets/Console.md | Console / Worker / CLI |
| Targets/Wpf.md | WPF desktop apps |
| Targets/WinForms.md | WinForms desktop apps |
| Targets/Avalonia.md | Avalonia cross-platform desktop apps |
| Targets/Android.md | Android apps |
| Targets/BrowserExtension.md | Browser extensions / plugins |
| Targets/Aot.md | .NET trimming / NativeAOT |
| Targets/GitHubActions.md | GitHub Actions CI |
| Targets/Docker.md | Dockerfiles / image builds |
| Scripts/LinuxShell.md | Linux shell scripts |
| Scripts/PowerShell.md | PowerShell scripts |
| Scripts/Cmd.md | CMD / BAT scripts |
| Knowledge/Obsidian.md | Obsidian vaults / note organization |
| Knowledge/Markdown.md | Markdown notes / docs organization |
| Embedded/Embedded.md | Embedded firmware / hardware integration |
| Domains/ThreeDPrinting.md | 3D printing workflows |
| Domains/ThreeDModeling.md | 3D modeling workflows |
| Life/PersonalOps.md | Life admin / personal support folders |
| Responsibilities/Planning/Analysis.md | 需求分析 |
| Responsibilities/Planning/Todo.md | 任务 Todo 安排 |
| Responsibilities/Planning/UI.md | 界面设计 |
| Responsibilities/Planning/FeatureDesign.md | 功能设计 |
| Responsibilities/Delivery/Development.md | 业务开发 |
| Responsibilities/Delivery/UnitTest.md | 单元测试 |
| Responsibilities/Delivery/IntegrationTest.md | 集成测试 |
| Responsibilities/Delivery/RegressionTest.md | 回归测试 |
| Responsibilities/Delivery/Acceptance.md | 功能验收 |
| Core/BackendRules.md | API / 服务层（配合 DotNetRules 使用） |
| Ops/BuildRules.md | CI/CD / 容器化 / 基础设施 |
| Core/VueRules.md | Vue 3 + Vite 前端（历史兼容） |

For platform-specific target-file routing and precedence, read:

- `References/Platforms/ClaudeCode.md`
- `References/Platforms/OpenCode.md`
- `References/Platforms/CopilotCLI.md`
- `References/Platforms/HermesAgent.md`
- `References/Platforms/GeminiCLI.md`

For workflow-stage routing, use:

- `References/Rules/Responsibilities/Planning/` for analysis, todo planning, UI design, and feature design
- `References/Rules/Responsibilities/Delivery/` for development, tests, regression coverage, and acceptance

For special-domain routing, use:

- `References/Rules/Scripts/` for Linux shell, PowerShell, and CMD scripts
- `References/Rules/Knowledge/` for Obsidian vaults and Markdown note organization
- `References/Rules/Embedded/` for embedded firmware and hardware integration
- `References/Rules/Domains/` for 3D printing and 3D modeling
- `References/Rules/Life/` for life admin and personal support folders

## 工作流程

### 1. Detect the target

**Agent 类型 → 目标文件：**
- Claude Code → `.claude/CLAUDE.md`（优先）或 `CLAUDE.md`
- OpenCode → `AGENTS.md` 或 `Agents.md`
- Copilot CLI → `.github/copilot-instructions.md` 优先，其次 `AGENTS.md`
- Hermes Agent → `.hermes.md` / `HERMES.md` 优先，其次 `AGENTS.md`
- Gemini CLI → `GEMINI.md`
- 无法判断 → 询问用户

**File state → choose the mode:**
- Missing or empty → **direct mode**
- Existing content → **edit mode**

---

### 2A. Direct mode

Scan the project, infer the stack, and write the minimum useful rules without extra confirmation.

| 检测条件 | 自动选用规则 |
|----------|-------------|
| 存在 `*.csproj`，且 `OutputType` 为 `Library` 或无 `Startup`/`Program` 入口 | DotNetRules + DotNetLibrary |
| 存在 `*.csproj`（其他） | DotNetRules + BackendRules |
| 存在 `package.json` 且含 `vue` | VueRules |
| 存在 `Dockerfile` | BuildRules |
| 存在 `AndroidManifest.xml` / Android 工程结构 | Targets/Android.md |
| 存在 `manifest.json` 且是浏览器扩展 | Targets/BrowserExtension.md |
| 存在 `*.sh` / `*.ps1` / `*.cmd` / `*.bat` | Scripts rules |
| 存在 `.obsidian/` 或笔记库结构 | Knowledge rules |
| 存在 `*.stl` / `*.obj` / `*.3mf` / `*.blend` | Domains rules |
| 以上均符合 | 全部合并写入 |
| 无法识别 | 展示规则列表，用户勾选后直接写入 |

**Default behavior:**
- Merge multiple matches by section.
- Remove obvious duplicates.
- Keep only rules that match the actual project stack.
- Prefer writing into the platform's highest-priority project file when multiple targets are available.
- For Claude Code, prefer `.claude/CLAUDE.md` first when the project can use it; fall back to root `CLAUDE.md` only when that is the project's established convention.

**Example:**
```
检测到 .NET 项目 → 合并 Core/DotNetRules.md + Core/BackendRules.md → 写入 .claude/CLAUDE.md ✓
```

---

### 2B. Edit mode

Show a short summary of the existing file and ask for the edit strategy.

```
检测到已有约束文件（约 XXX 行），请选择：

A) 附加 - 末尾追加新规则，原内容不变
B) 替换 - 覆盖整个文件，先二次确认
C) 融合 - 智能合并并去重
D) 仅查看 - 显示当前内容，不做任何修改
```

**Merge policy:**
- 相同章节标题 → 合并内容，去除重复条目
- 轻微冲突 → 优先保留更贴近当前项目的规则
- 明显冲突 → 先提示用户确认，再改写
- 独有内容 → 原样保留
- 涉及替换整份文件时 → 先确认目标平台的优先路径，再确认是否覆盖

---

## Output template

```markdown
# [项目名] AI 指令

## 技术栈
- [检测到的技术栈]

## 编码规范
[选中规则内容]

## 项目特定约束
[用户自定义内容 - 如有]
```

## Shortcuts

| 命令 | 说明 |
|------|------|
| `/agent-rules` | 启动向导（自动检测环境和技术栈） |
| `/agent-rules list` | 列出所有可用规则模板 |
| `/agent-rules add <规则名>` | 直接添加指定规则（跳过检测） |
| `/agent-rules show` | 显示当前项目约束内容 |

## Guardrails

- 替换模式执行前必须明确二次确认
- `.claude/CLAUDE.md` 优先级高于根目录 `CLAUDE.md`
- 有硬性冲突时，先保守合并，再请求确认是否覆盖
- If the target file is not obvious, ask before writing
