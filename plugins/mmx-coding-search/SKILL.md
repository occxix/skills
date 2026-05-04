---
name: mmx-coding-search
description: Use mmx search to research coding solutions, find library docs, look up API references, investigate errors, or gather technical context before writing code. Triggers on "搜索解决方案", "查文档", "找库", "查 API", "搜错误", "research before coding", "look up how to", "find examples", "查怎么实现".
---

# MiniMax 搜索辅助编程技能

使用 `mmx search query` 在编码前研究技术方案、查找文档、排查错误，提高代码质量。

> **核心原则**：先搜索后编码。不要凭记忆猜 API，先查再写。

---

## 工作流

```
遇到技术问题或需要实现新功能
  ↓
【第一步】分解搜索问题
  ↓
【第二步】执行多角度搜索
  ↓
【第三步】整合搜索结果
  ↓
【第四步】基于真实信息编写代码
```

---

## 第一步：分解搜索问题

| 任务类型 | 需要搜索的方向 |
|----------|--------------|
| 实现新功能 | 最佳实践、推荐库、官方文档 |
| 修复 Bug | 错误信息、GitHub Issues、Stack Overflow |
| 选型决策 | 库对比、性能评测、社区活跃度 |
| 升级依赖 | Breaking changes、迁移指南 |
| 安全问题 | CVE 漏洞、修复方案 |

---

## 第二步：执行搜索

### 标准搜索模式

```bash
# 基础搜索
mmx search query --q "React hooks useEffect cleanup 2025" --output json --quiet

# 查错误
mmx search query --q "TypeError: Cannot read properties of null reading addEventListener" --output json --quiet

# 查最新文档
mmx search query --q "Next.js 15 app router data fetching official docs" --output json --quiet

# 查对比选型
mmx search query --q "Zustand vs Redux Toolkit 2025 performance comparison" --output json --quiet
```

### 多角度研究（推荐用于重要决策）

```bash
# 角度1：官方文档/最佳实践
mmx search query --q "Prisma ORM best practices production 2025" --output json --quiet

# 角度2：常见问题
mmx search query --q "Prisma ORM common issues N+1 query optimization" --output json --quiet

# 角度3：实际案例
mmx search query --q "Prisma ORM real world example GitHub" --output json --quiet
```

---

## 第三步：整合搜索结果生成方案

将搜索结果传给 text chat 生成可执行代码：

```bash
# 搜索 + 生成代码（一体化流程）
SEARCH_RESULT=$(mmx search query \
  --q "Node.js file upload with progress tracking multer 2025" \
  --output json --quiet)

mmx text chat \
  --system "你是 Node.js 专家。基于搜索到的最新信息给出代码。" \
  --message "user:根据以下搜索结果，实现一个支持进度追踪的文件上传功能（Express + Multer）：

$SEARCH_RESULT

要求：
- 使用 TypeScript
- 支持进度回调
- 文件大小和类型验证
- 错误处理" \
  --quiet
```

---

## 常用编程搜索模板

### 错误排查

```bash
# 精确错误信息搜索（用引号）
mmx search query \
  --q '"EADDRINUSE address already in use" Node.js fix' \
  --output json --quiet

# 框架+错误组合
mmx search query \
  --q "React 18 hydration error fix server client mismatch" \
  --output json --quiet
```

### 库/框架文档

```bash
# 查特定版本文档
mmx search query \
  --q "Tailwind CSS v4 migration guide breaking changes" \
  --output json --quiet

# 查特定功能
mmx search query \
  --q "Pinia store persist localStorage Vue 3 example" \
  --output json --quiet
```

### 技术选型

```bash
# 库对比
mmx search query \
  --q "SWR vs React Query vs Tanstack Query 2025 comparison" \
  --output json --quiet

# 性能评测
mmx search query \
  --q "PostgreSQL vs MongoDB performance benchmark 2025 use case" \
  --output json --quiet
```

### 安全漏洞

```bash
# CVE 查询
mmx search query \
  --q "lodash CVE security vulnerability 2025 fix" \
  --output json --quiet

# 依赖安全
mmx search query \
  --q "npm package xxx security advisory" \
  --output json --quiet
```

---

## 搜索→分析→编码完整流程

```bash
#!/bin/bash
# 完整的"研究后编码"流程示例

TASK="实现 JWT 刷新 Token 机制"
STACK="Node.js + Express + TypeScript"

echo "=== 第1步：搜索最佳实践 ==="
BEST_PRACTICE=$(mmx search query \
  --q "JWT refresh token best practices Node.js 2025" \
  --output json --quiet)

echo "=== 第2步：搜索安全注意事项 ==="
SECURITY=$(mmx search query \
  --q "JWT refresh token security vulnerabilities XSS CSRF" \
  --output json --quiet)

echo "=== 第3步：生成代码方案 ==="
mmx text chat \
  --system "你是安全意识强的 Node.js 后端工程师。" \
  --message "user:任务：$TASK
技术栈：$STACK

最佳实践参考：
$BEST_PRACTICE

安全注意事项：
$SECURITY

请生成完整的 JWT 刷新 Token 实现代码，包含安全处理。" \
  --quiet
```

---

## 搜索质量提升技巧

| 技巧 | 示例 |
|------|------|
| 加年份限定 | `"xxx 2025"` 避免过时答案 |
| 加 `official docs` | 避免博客文章，找官方文档 |
| 用引号精确匹配 | `'"error message exact text"'` |
| 加框架版本号 | `"Next.js 15"` 而非 `"Next.js"` |
| 加 `GitHub` | 找开源实现示例 |
| 加 `fix` / `solution` | 找解决方案而非问题描述 |

---

## 注意事项

- `--output json` 返回结构化结果，适合传给 text chat 处理
- 搜索结果可能包含过时信息，注意检查发布日期
- 重要安全决策（加密、认证）建议搜索后额外用 context7 查官方文档
- 始终加 `--quiet` 避免进度条干扰脚本
