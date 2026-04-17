# MiniMax API 调用技能 (v1.1)

## 概述

本技能提供 MiniMax API (minimaxi.com) 的完整调用指南，包括 API 配置、调用方法、错误处理和模型选择。

---

## API 配置

### 端点 (重要: 使用 OpenAI 兼容端点)
```
API URL: https://api.minimaxi.com/v1/chat/completions
```

> ⚠️ 注意: 不要使用 `/v1/messages` (Anthropic 兼容端点)，那个会返回 invalid_request_error。

### 环境变量
```bash
# 在 ~/.hermes/.env 中配置
MINIMAX_CN_API_KEY=your_api_key_here
```

### 认证
```python
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
```

---

## 可用模型

| MiniMax-M2.5 | Sonnet 级别 | 默认选择，代码逻辑、数学计算、折扣计算 | ~240字/秒 |
| MiniMax-M2.5-HighSpeed | 高速版本 | 简单任务、批量处理、要求速度优先场景 | ~400字/秒 |
| MiniMax-M2.7 | Opus 级别 | 筛选任务、结构化输出、复杂推理 | ~130字/秒 |

### 模型选择决策树

```n
需要调用MiniMax API？
├── 速度优先、简单任务 → 使用 M2.5-HighSpeed
├── 折扣/百分比计算 → 使用 M2.5
├── 复合数学计算 → 使用 M2.5
├── 函数追踪/代码逻辑 → 使用 M2.5
├── 列表切片/数组操作 → 使用 M2.5
├── 筛选 / 过滤任务 → 使用 M2.7
├── 结构化 JSON 输出 → 使用 M2.7
├── 长文本 Recall → M2.5 或 M2.5-HighSpeed
└── 简单任务 → M2.5-HighSpeed 优先
```

---

## Python 调用示例

### 基本调用 (推荐使用 requests)

```python
import requests
import json

def call_minimax(model: str, messages: list, max_tokens: int = 500, timeout: int = 120) -> str:
    """调用MiniMax API"""
    
    # 读取 API Key (注意去除换行符)
    with open('/root/.hermes/.env', 'r') as f:
        for line in f:
            if line.startswith('MINIMAX_CN_API_KEY='):
                API_KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
                break
    
    URL = "https://api.minimaxi.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": model, "max_tokens": max_tokens, "messages": messages}
    
    r = requests.post(URL, headers=headers, json=payload, timeout=timeout)
    resp = r.json()
    
    # 提取响应
    choices = resp.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return ""

# 使用示例
messages = [{"role": "user", "content": "100元打8折是多少钱？"}]
result = call_minimax("MiniMax-M2.5", messages)
print(result)  # 输出: 80元
```

### 带重试的调用

```python
import time

def call_with_retry(model: str, messages: list, max_retries: int = 2, timeout: int = 120) -> str:
    """带重试的 API 调用"""
    for i in range(max_retries):
        result = call_minimax(model, messages, timeout=timeout)
        if result and len(result) > 10 and not result.startswith("ERROR:"):
            return result
        time.sleep(1)
    
    # 失败切换模型
    other = "MiniMax-M2.5" if model == "MiniMax-M2.7" else "MiniMax-M2.7"
    return call_minimax(other, messages, timeout=timeout)
```

---

## 错误处理

### 常见错误

| 错误码 | 原因 | 解决方案 |
|--------|------|----------|
| 400 invalid_request_error | 端点错误或模型名错误 | 检查 URL 是否为 `/v1/chat/completions` |
| 400 unknown model | 模型名称错误 | 使用 `MiniMax-M2.5` 或 `MiniMax-M2.7` |
| 401 | 认证失败 | 检查 API Key 是否正确，注意换行符 |
| 520 / 529 | 服务器错误 | 重试或切换模型 |

### 调试技巧

```python
# 调试: 打印完整响应
print(r.status_code)
print(r.text)
```

---

## 配置建议

### settings.json

```json
{
  "env": {
    "ANTHROPIC_MODEL": "MiniMax-M2.5",
    "ANTHROPIC_REASONING_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M2.5",
    "API_TIMEOUT_MS": "3000000"
  }
}
```

### 超时设置

- 长上下文任务建议超时: 3000000ms (5分钟)
- 简单任务建议超时: 60000ms (1分钟)

---

## 性能对比

| 任务类型 | M2.5 | M2.7 | 推荐 |
|----------|------|------|------|
| 基础任务 | 100% | 100% | 都可以 |
| 代码追踪 | ✅ 强 | ❌ 弱 | **M2.5** |
| 折扣计算 | ✅ 强 | ⚠️ 不稳定 | **M2.5** |
| 列表筛选 | ✅ | ✅ | 都可以 |
| 平均速度 | ~240字/秒 | ~130字/秒 | **M2.5 快 2x** |

---

## 使用场景示例

### 场景1: 折扣计算

```python
messages = [{"role": "user", "content": "100元打8折是多少钱？"}]
result = call_minimax("MiniMax-M2.5", messages)  # 使用 M2.5
```

### 场景2: 筛选任务

```python
messages = [{"role": "user", "content": "张三技术部，李四市场部，王五技术部。\n技术部有哪些人？"}]
result = call_minimax("MiniMax-M2.7", messages)  # 使用 M2.7
```

### 场景3: 代码追踪

```python
messages = [{"role": "user", "content": "def hello(): return 'hi'\n函数名有哪些？"}]
result = call_minimax("MiniMax-M2.5", messages)  # 使用 M2.5
```

---

## 更新记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.2 | 2026-04-17 | 新增 MiniMax-M2.5-HighSpeed 高速模型 |
| v1.1 | 2026-04-15 | 修复 API 端点，从 /v1/messages 改为 /v1/chat/completions |
| v1.0 | 2026-04-15 | 初始版本 |