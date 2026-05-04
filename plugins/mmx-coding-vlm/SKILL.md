---
name: mmx-coding-vlm
description: Use mmx vision to analyze code-related images — screenshots, architecture diagrams, UI mockups, error screenshots, database schemas, flowcharts — and generate coding plans or solutions. Triggers on "看这张截图", "分析这张图", "根据图片写代码", "看这个UI", "截图里的错误", "架构图", "看图写代码", "analyze screenshot", "code from image".
---

# MiniMax VLM 代码视觉分析技能

使用 `mmx vision describe` 分析与编程相关的图片（截图、UI 设计图、架构图、错误截图），提取信息并生成可执行的编码建议。

> **核心价值**：把视觉内容转成代码计划。不只是描述图片，而是输出可执行的实现方案。

---

## 适用场景

| 场景 | 输入图片类型 | 输出 |
|------|------------|------|
| UI 实现 | 设计稿/Figma 截图/原型图 | 组件结构 + 代码骨架 |
| 错误排查 | 错误截图/报错信息图 | 错误分析 + 修复方案 |
| 架构理解 | 系统架构图/流程图 | 架构说明 + 实现建议 |
| 数据库设计 | ER 图/表结构图 | SQL 建表语句 |
| 代码审查 | 代码截图 | 代码问题识别 + 优化建议 |
| 逆向还原 | 已有应用截图 | 功能分析 + 实现路径 |

---

## 工作流

```
用户提供图片
  ↓
【第一步】分析图片（vision describe）
  ↓
【第二步】提取结构化信息
  ↓
【第三步】生成编码计划
```

---

## 第一步：分析图片

根据图片类型使用不同的 `--prompt`：

### 分析模板

```bash
# UI/设计稿 → 组件分析
mmx vision describe \
  --image design.png \
  --prompt "分析这个 UI 设计图，列出：1) 所有 UI 组件及其层次结构 2) 交互行为 3) 数据需求 4) 用 React/Vue 实现的组件划分建议" \
  --quiet

# 错误截图 → 问题诊断
mmx vision describe \
  --image error.png \
  --prompt "分析这个错误截图，说明：1) 错误类型和原因 2) 可能的触发条件 3) 具体修复方案和代码示例" \
  --quiet

# 架构图 → 实现路径
mmx vision describe \
  --image architecture.png \
  --prompt "解析这个系统架构图，说明：1) 各模块功能 2) 模块间通信方式 3) 技术栈建议 4) 实现优先级" \
  --quiet

# ER 图 → SQL 语句
mmx vision describe \
  --image er_diagram.png \
  --prompt "根据这个 ER 图生成 SQL 建表语句，包含：主键、外键、索引、约束。使用 MySQL 语法。" \
  --quiet

# 代码截图 → 代码审查
mmx vision describe \
  --image code_screenshot.png \
  --prompt "审查这段代码，指出：1) 潜在的 Bug 2) 性能问题 3) 安全漏洞 4) 可读性建议，给出改进后的代码" \
  --quiet

# 流程图 → 代码逻辑
mmx vision describe \
  --image flowchart.png \
  --prompt "将这个流程图转换为伪代码或实际代码，说明每个判断分支的处理逻辑" \
  --quiet
```

---

## 第二步：结合文本上下文深度分析

当图片分析需要结合代码文件或上下文时，用管道组合：

```bash
# 分析错误截图并结合代码文件
VISION_RESULT=$(mmx vision describe \
  --image error_screenshot.png \
  --prompt "这个错误发生在什么场景？涉及哪些关键变量/函数？" \
  --quiet)

# 将 vision 结果传给 text chat 深度分析
echo "$VISION_RESULT" | mmx text chat \
  --system "你是一个资深工程师，专注于 Bug 分析和修复。" \
  --message "user:根据以下错误截图分析，结合常见的代码错误模式，给出完整的修复方案：$VISION_RESULT" \
  --quiet
```

```bash
# 根据 UI 截图生成 React 代码
UI_ANALYSIS=$(mmx vision describe \
  --image mockup.png \
  --prompt "详细描述这个 UI 的组件结构、布局、颜色和交互" \
  --quiet)

mmx text chat \
  --system "你是一个 React 专家，使用 TypeScript + Tailwind CSS。" \
  --message "user:根据以下 UI 分析，生成完整的 React 组件代码：

$UI_ANALYSIS

要求：
- 使用 TypeScript 类型
- Tailwind CSS 样式
- 包含交互逻辑
- 组件化拆分" \
  --quiet
```

---

## 第三步：生成编码计划

复杂任务（多图/多步骤）时生成结构化计划：

```bash
# 多图分析（多个视角）
ARCH=$(mmx vision describe --image arch.png --prompt "描述架构" --quiet)
DB=$(mmx vision describe --image db_schema.png --prompt "列出所有表和字段" --quiet)

mmx text chat \
  --system "你是技术架构师，负责制定开发计划。" \
  --message "user:根据架构图分析和数据库设计，生成详细的开发计划：

## 架构分析
$ARCH

## 数据库设计
$DB

请输出：
1. 技术选型建议
2. 分阶段实现计划（每阶段目标、工作量）
3. 关键模块代码骨架
4. 潜在风险点" \
  --quiet
```

---

## 快速场景模板

```bash
# 场景1：还原竞品功能
mmx vision describe \
  --image competitor_app.jpg \
  --prompt "分析这个应用的核心功能和交互，如何用现代 Web 技术实现一个类似的功能？给出技术方案" \
  --quiet

# 场景2：分析 API 文档截图
mmx vision describe \
  --image api_docs.png \
  --prompt "从这个 API 文档截图中提取：接口地址、请求方法、参数、返回格式，生成对应的 TypeScript 类型定义和调用代码" \
  --quiet

# 场景3：识别性能瓶颈截图（如 Chrome DevTools）
mmx vision describe \
  --image performance_screenshot.png \
  --prompt "分析这个性能报告，找出主要性能瓶颈，给出具体的优化代码方案" \
  --quiet
```

---

## 注意事项

- 本地图片自动 base64 编码传输
- 提供具体的 `--prompt` 比默认描述效果好得多
- 代码截图分析时，提前说明编程语言/框架可以提高准确性
- 复杂分析建议分步：先 vision 提取信息，再 text chat 生成代码
- 始终加 `--quiet` 避免进度条干扰
