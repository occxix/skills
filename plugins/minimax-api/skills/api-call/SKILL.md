---
name: minimax-api-call
description: "MiniMax API 调用指南，包含 M2.5/M2.7 模型选择、Python 调用示例、错误处理与性能对比。触发词：MiniMax API、调用 MiniMax、minimax-api"
---

<role>
MiniMax API 技术顾问，负责调用 MiniMax M2.5/M2.7/M2.5-HighSpeed 模型并返回结果。

> **⚠️ 性能测试声明**：文字生成速度的测试方法和统计较为简陋，不够专业，仅供参考。实际速度受网络、服务器负载等因素影响较大。
</role>

<purpose>
封装 MiniMax API 的调用逻辑，提供模型选择建议、错误处理和性能对比，供上游 Agent 消费。
</purpose>

<trigger>

```text
触发词/示例：
- 调用 MiniMax API
- MiniMax M2.5 怎么用
- minimax-api
- 100元打8折是多少

示例：
- "用 MiniMax 计算 100*0.8"
- "调用 M2.7 筛选技术部人员"
- "MiniMax API 报错怎么办"
```
</trigger>

<gsd:workflow>
  <gsd:meta>
    <name>minimax-api-call</name>
    <owner>minimax-api</owner>
    <requires>Python 3, requests</requires>
    <checkpoints>
      <checkpoint order="1">API Key 已配置</checkpoint>
      <checkpoint order="2">模型选择正确</checkpoint>
      <checkpoint order="3">调用成功</checkpoint>
    </checkpoints>
    <constraints>
      <constraint>必须使用 /v1/chat/completions 端点（非 /v1/messages）</constraint>
      <constraint>API Key 从 ~/.hermes/.env 读取，格式 MINIMAX_CN_API_KEY=xxx</constraint>
      <constraint>失败时最多重试 2 次，仍失败则尝试切换模型</constraint>
      <constraint>长上下文任务超时设为 300 秒</constraint>
      <constraint>简单任务使用 M2.5-HighSpeed，长任务使用 M2.5，筛选任务使用 M2.7</constraint>
    </constraints>
  </gsd:meta>

  <gsd:goal>输入任务 → 选择最优模型 → 返回结果</gsd:goal>

  <gsd:phase name="prepare" order="1">
    <gsd:step>读取 API Key（MINIMAX_CN_API_KEY）</gsd:step>
    <gsd:step>分析任务类型，选择模型</gsd:step>
    <gsd:checkpoint>环境就绪</gsd:checkpoint>
  </gsd:phase>

  <gsd:phase name="call" order="2">
    <gsd:step>构建请求（model + messages + max_tokens）</gsd:step>
    <gsd:step>POST 到 https://api.minimaxi.com/v1/chat/completions</gsd:step>
    <gsd:step>解析响应，提取 content</gsd:step>
    <gsd:checkpoint>API 调用完成</gsd:checkpoint>
  </gsd:phase>

  <gsd:phase name="fallback" order="3">
    <gsd:step>失败？→ 重试 1 次</gsd:step>
    <gsd:step>仍失败？→ 切换模型重试</gsd:step>
    <gsd:step>全部失败 → 返回错误信息</gsd:step>
    <gsd:checkpoint>错误处理完成</gsd:checkpoint>
  </gsd:phase>
</gsd:workflow>

# MiniMax API 调用指南

MiniMax API 调用与模型选择参考手册。

## 模型选择决策树

```
需要调用 MiniMax？
│
├── 折扣/百分比计算 → M2.5
├── 复合数学计算 → M2.5
├── 函数追踪/代码逻辑 → M2.5
├── 列表切片/数组操作 → M2.5
├── 筛选/过滤任务 → M2.7
├── 结构化 JSON 输出 → M2.7
├── 速度优先、简单任务 → M2.5-HighSpeed
└── 长文本 Recall → M2.5 或 M2.5-HighSpeed
```

## 模型能力对比

| 任务 | M2.5 | M2.7 | M2.5-HighSpeed |
|------|------|------|----------------|
| 折扣计算 | ✅ 强 | ❌ 弱 | ✅ 强 |
| 复合计算 | ✅ 强 | ❌ 弱 | ✅ 强 |
| 函数追踪 | ✅ 强 | ❌ 弱 | ✅ 强 |
| 列表筛选 | ✅ 强 | ✅ 强 | ✅ 强 |
| 结构化输出 | ❌ 弱 | ✅ 强 | ❌ 弱 |
| 长文本 Recall | ✅ | ✅ | ✅ |
| 速度 | ~240字/秒 | ~130字/秒 | ~400字/秒 |

> **注**：速度数据仅供参考，实际速度因网络、服务器负载等因素可能有较大差异。

## Python 调用示例

### 基础调用

```python
import requests

def call_minimax(model: str, messages: list, max_tokens: int = 500) -> str:
    """调用 MiniMax API"""
    # 读取 API Key
    with open('/root/.hermes/.env') as f:
        for line in f:
            if line.startswith('MINIMAX_CN_API_KEY='):
                API_KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
                break

    URL = "https://api.minimaxi.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"model": model, "max_tokens": max_tokens, "messages": messages}

    r = requests.post(URL, headers=headers, json=payload, timeout=120)
    resp = r.json()
    return resp.get("choices", [{}])[0].get("message", {}).get("content", "")

# 使用示例
result = call_minimax("MiniMax-M2.5", [{"role": "user", "content": "100元打8折是多少钱？"}])
print(result)  # 输出: 80元
```

### 带重试的调用

```python
import time

def call_with_retry(model: str, messages: list, max_retries: int = 2) -> str:
    """带重试的 API 调用"""
    for i in range(max_retries):
        result = call_minimax(model, messages)
        if result and len(result) > 10 and not result.startswith("ERROR:"):
            return result
        time.sleep(1)

    # 失败时尝试切换模型
    other = "MiniMax-M2.5" if model == "MiniMax-M2.7" else "MiniMax-M2.7"
    return call_minimax(other, messages)
```

## API 配置

| 项目 | 值 |
|------|-----|
| 端点 | `https://api.minimaxi.com/v1/chat/completions` |
| 认证 | `Authorization: Bearer {API_KEY}` |
| Content-Type | `application/json` |

> ⚠️ 注意：不要使用 `/v1/messages`（Anthropic 兼容端点），那个会返回 `invalid_request_error`。

## 错误处理

| 错误码 | 原因 | 解决方案 |
|--------|------|---------|
| 400 invalid_request_error | 端点错误或模型名错误 | 检查 URL 是否为 `/v1/chat/completions` |
| 400 unknown model | 模型名称错误 | 使用 `MiniMax-M2.5` 或 `MiniMax-M2.7` |
| 401 | 认证失败 | 检查 API Key 是否正确，注意换行符 |
| 520 / 529 | 服务器错误 | 重试或切换模型 |

## 可执行脚本

```bash
# 测试 API 调用
python3 scripts/call_minimax.py

# 运行单个测试
python3 scripts/call_minimax.py --model MiniMax-M2.5 --prompt "100元打8折是多少钱？"
```
