---
name: knowledge
description: 通用记忆库管理 — 结构性知识、任务计划、项目文档、问题解决方案
---

# Knowledge Base Management

管理本地知识库，支持多种内容类型：结构性知识、任务计划、项目文档、问题解决方案。

## 位置

```text
~/.agents/knowledge
```

## 目录结构

```
knowledge/
├── MEMORY.md              # 索引 + 统计
├── LOG.md                 # 变更日志
├── library-tips/          # 库/框架使用模式
├── problem-analysis/      # 问题分析 + 解决方案
├── projects/              # 项目文档
├── sessions/              # 任务会话记录
├── decisions/             # 决策记录 (ADR)
└── workarounds/           # 已知问题临时方案
```

## Frontmatter 规范

所有条目必须包含 YAML frontmatter：

```yaml
---
name: 条目名称
description: 一行描述
type: library-tips | problem-analysis | project | session | decision | workaround
date: YYYY-MM-DD
tags: [tag1, tag2]
related: [../other-entry.md]  # 可选：相关条目
status: resolved | open | wontfix  # problem-analysis 必填
confidence: high | medium | low    # 可选：结论可信度
---
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| name | ✅ | 条目唯一标识 |
| description | ✅ | 一行描述（用于索引） |
| type | ✅ | 内容类型 |
| date | ✅ | 创建日期 |
| tags | ✅ | 分类标签 |
| related | ❌ | 相关条目路径 |
| status | ⚠️ | problem-analysis 必填 |
| confidence | ❌ | 结论可信度 |

## 内容类型

### library-tips
库/框架使用模式、最佳实践。

```yaml
type: library-tips
library: 库名
version: 版本  # 可选
```

### problem-analysis
问题分析 + 解决方案。

```yaml
type: problem-analysis
status: resolved | open | wontfix
root_cause: 根因  # 可选
```

### project
项目文档、架构分析。

```yaml
type: project
path: 项目路径  # 可选
tech_stack: [技术栈]  # 可选
```

### session
任务会话记录。

```yaml
type: session
project: 项目名  # 可选
outcome: 结果摘要
```

### decision
决策记录 (ADR)。

```yaml
type: decision
context: 决策背景
decision: 决策内容
consequences: 影响
```

## 核心操作

### 添加条目

1. 选择正确分类目录
2. 使用 frontmatter 模板
3. 更新 MEMORY.md 索引
4. 追加 LOG.md 变更记录

### 更新条目

1. 修改内容
2. 更新 frontmatter 中的 date
3. 追加 LOG.md 变更记录

### 查询

```bash
# 搜索内容
grep -ri "关键词" ~/.agents/knowledge/

# 按类型搜索
grep -ri "关键词" ~/.agents/knowledge/library-tips/

# 按标签搜索
grep -ri "tags:.*dotnet" ~/.agents/knowledge/
```

## LOG.md 格式

```markdown
# Knowledge Log

## YYYY-MM-DD
### Added
- category/file.md — 简要描述

### Updated
- category/file.md — 变更说明

### Resolved
- problem-analysis/file.md — 解决方案摘要

### Archived
- category/file.md — 归档原因
```

## 交叉引用

使用 `related:` 字段链接相关条目：

```yaml
related:
  - ../library-tips/dotnet-di-tips.md
  - ../problem-analysis/onnx-runtime-gpu-cuda-setup.md
```

条目内使用相对路径引用：

```markdown
相关: [dotnet-di-tips](../library-tips/dotnet-di-tips.md)
```

## 质量标记

### status（problem-analysis 必填）

| 值 | 含义 |
|----|------|
| resolved | 已解决 |
| open | 待解决 |
| wontfix | 不修复/限制 |

### confidence（可选）

| 值 | 含义 |
|----|------|
| high | 多来源验证 |
| medium | 单来源/经验推断 |
| low | 猜测/待验证 |

## 迁移现有知识库

检查其他工具的知识目录：

```text
~/.codex/knowledge
~/.claude/knowledge
~/.cursor/knowledge
~/.qwen/knowledge
```

合并到 `~/.agents/knowledge`，然后用 junction 链接：

```powershell
New-Item -ItemType Junction -Path "$HOME\.codex\knowledge" -Target "$HOME\.agents\knowledge"
```

## 与 llm-wiki 联动

knowledge（过程记忆）与 llm-wiki（结构化知识）可双向联动。

### 定位差异

| 维度 | knowledge | llm-wiki |
|------|-----------|----------|
| 用途 | 过程记录 | 知识编译 |
| 类型 | tips/problems/sessions/decisions | entities/concepts/comparisons |
| 引用 | related 字段（可选） | [[wikilinks]]（强制） |
| 来源 | 开发过程 | 文献/文章 |

### 联动字段

在 frontmatter 中添加 `wiki_ref:` 链接 llm-wiki 条目：

```yaml
---
name: dotnet-di-tips
type: library-tips
wiki_ref: [[dependency-injection]]  # llm-wiki 概念页
---
```

### 联动操作

#### 1. knowledge → llm-wiki（提取概念）

从 knowledge 条目提取通用概念到 llm-wiki：

```bash
# 触发条件：library-tips 或 problem-analysis 包含通用模式
# 操作：在 llm-wiki 创建概念页，在 knowledge 添加 wiki_ref
```

示例：
- `library-tips/dotnet-di-tips.md` → `llm-wiki/concepts/dependency-injection.md`
- `problem-analysis/onnx-runtime-gpu-cuda-setup.md` → `llm-wiki/concepts/onnx-gpu-acceleration.md`

#### 2. llm-wiki → knowledge（辅助解决）

查询 llm-wiki 概念辅助问题解决：

```bash
# 触发条件：遇到新问题，llm-wiki 有相关概念
# 操作：在 problem-analysis 添加 wiki_ref 引用概念
```

#### 3. 双向同步

```markdown
<!-- knowledge 条目 -->
wiki_ref: [[dependency-injection]]

<!-- llm-wiki 概念页 -->
sources:
  - knowledge:library-tips/dotnet-di-tips.md
```

### 联动命令

```bash
# 从 knowledge 提取概念到 llm-wiki
/knowledge-extract <entry-path>

# 查询 llm-wiki 概念辅助问题
/knowledge-query <concept-name>

# 检查 knowledge 条目是否有 wiki_ref
/knowledge-lint
```

### 联动规则

1. **library-tips** → 提取为 llm-wiki `concepts/`
2. **problem-analysis** → 提取为 llm-wiki `entities/`（问题实体）
3. **decisions** → 提取为 llm-wiki `concepts/`（决策模式）
4. **sessions** → 不联动（过程记录）

### 判断是否提取

| 条件 | 提取 |
|------|------|
| 通用模式/概念 | ✅ |
| 项目特定细节 | ❌ |
| 可复用知识 | ✅ |
| 一次性问题 | ❌ |

## 验证

```powershell
# 检查索引完整性
Get-ChildItem "$HOME\.agents\knowledge" -Recurse -Filter "*.md"

# 验证 junction
Get-Item "$HOME\.codex\knowledge"

# 检查 wiki_ref 链接
grep -r "wiki_ref:" ~/.agents/knowledge/
```
