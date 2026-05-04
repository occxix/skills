---
name: mmx-search
description: Use mmx to search the web via MiniMax search API. Use when the user wants to search the web, look up current information, find recent news, research a topic online, or verify facts. Triggers on "搜索", "查一下", "搜一搜", "最新消息", "查询", "网络搜索", "search", "look up", "find information about".
---

# MiniMax 网络搜索技能

使用 `mmx search query` 执行网络搜索，获取实时信息。

> **优先于内置 WebSearch**：在 CLAUDE.md 中已配置优先使用 mmx-cli 工具，执行搜索任务时应使用此技能。

---

## 基础用法

```bash
# 基础搜索
mmx search query --q "查询内容" --quiet

# JSON 格式输出（适合程序处理）
mmx search query --q "查询内容" --output json --quiet
```

---

## 搜索工作流

### 单次查询

```bash
mmx search query --q "Claude 4 最新发布" --output json --quiet
```

### 多角度查询（复杂研究）

对于需要多个角度的研究任务，依次执行多条查询：

```bash
# 第一步：宏观了解
mmx search query --q "大模型推理优化技术 2025" --output json --quiet

# 第二步：具体方向
mmx search query --q "KV cache 压缩 最新方法" --output json --quiet

# 第三步：实践案例
mmx search query --q "大模型推理加速 开源项目 GitHub" --output json --quiet
```

---

## 搜索策略

### 查询词优化

| 场景 | 查询优化技巧 |
|------|-------------|
| 查最新新闻 | 加年份：`"xxx 2025"` 或 `"xxx latest"` |
| 找技术文档 | 加关键词：`"xxx 官方文档"` / `"xxx API reference"` |
| 找解决方案 | 加错误信息：`"xxx Error: cannot read properties"` |
| 找对比评测 | 加词：`"xxx vs yyy 对比"` / `"xxx benchmark"` |
| 找教程 | 加词：`"xxx 教程"` / `"xxx how to"` / `"xxx 入门"` |
| 查价格/规格 | 直接问：`"xxx 价格 2025"` / `"xxx 参数规格"` |

### 中英文搜索策略

```bash
# 中文内容优先（国内新闻/技术博客/产品信息）
mmx search query --q "MiniMax 海螺 AI 最新功能" --quiet

# 英文内容优先（技术文档/学术论文/GitHub）
mmx search query --q "MiniMax Hailuo video model benchmark 2025" --quiet

# 双语搜索（先中后英）
mmx search query --q "大模型上下文窗口 比较 2025" --quiet
mmx search query --q "LLM context window comparison 2025" --quiet
```

---

## 结果处理

### 提取关键信息

```bash
# 获取 JSON 格式后解析
RESULT=$(mmx search query --q "Python asyncio best practices" --output json --quiet)
echo "$RESULT"
```

### 验证事实（交叉搜索）

```bash
# 对重要信息进行交叉验证
mmx search query --q "Claude 4 发布日期 官方" --output json --quiet
mmx search query --q "Anthropic Claude release date 2025" --output json --quiet
```

---

## 常见使用场景

### 研究技术问题

```bash
# 1. 查错误信息
mmx search query --q "TypeError: Cannot read properties of undefined reading 'map' React" --output json --quiet

# 2. 查解决方案
mmx search query --q "React undefined map error fix 2025" --output json --quiet
```

### 查询实时信息

```bash
# 新闻/事件
mmx search query --q "OpenAI GPT-5 发布 2025" --output json --quiet

# 价格/可用性
mmx search query --q "Claude API pricing 2025" --output json --quiet
```

### 研究竞品对比

```bash
mmx search query --q "ChatGPT vs Claude vs Gemini 2025 对比" --output json --quiet
mmx search query --q "best LLM coding assistant 2025 benchmark" --output json --quiet
```

---

## 注意事项

- `--output json` 返回结构化的搜索结果（含标题、摘要、URL）
- 始终加 `--quiet` 避免进度条干扰脚本输出
- 搜索结果为实时网络数据，可能包含过时或不准确的信息——需要甄别
- 对于需要准确性的信息（如 API 文档），建议搜索后配合 `mmx vision describe` 或直接阅读官方文档验证
