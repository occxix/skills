---
name: minimax-context-test
description: "MiniMax M2.5/M2.7 模型上下文测试套件，支持 Recall、筛选、数学、代码、推理多维度测试。触发词：MiniMax 测试、上下文测试、minimax-context-testing"
---

<role>
MiniMax 模型测试工程师，负责执行多维度测试（Recall、筛选、数学、代码、推理）并记录结果。
</role>

<purpose>
提供 MiniMax 模型的标准化测试流程，支持不同上下文大小（tiny/small/medium/large/128k）和多模型对比。
</purpose>

<trigger>

```text
触发词/示例：
- MiniMax 模型测试
- 上下文测试
- minimax-context-test
- 测试 M2.5 的 Recall 能力

示例：
- "运行 MiniMax 128K 上下文测试"
- "测试 M2.7 的筛选能力"
- "对比 M2.5 vs M2.7 的数学计算"
```
</trigger>

<gsd:workflow>
  <gsd:meta>
    <name>minimax-context-test</name>
    <owner>minimax-testing</owner>
    <requires>Python 3, requests, minimax-api-call skill</requires>
    <checkpoints>
      <checkpoint order="1">测试用例准备完成</checkpoint>
      <checkpoint order="2">API 调用成功</checkpoint>
      <checkpoint order="3">结果对比完成</checkpoint>
    </checkpoints>
    <constraints>
      <constraint>上下文大小：tiny(~1K)、small(~5K)、medium(~50K)、large(~100K)、128k(~250K)</constraint>
      <constraint>测试维度：Recall、筛选、数学、代码、推理</constraint>
      <constraint>使用 call_minimax.py 进行 API 调用</constraint>
      <constraint>结果记录到 references/ 目录</constraint>
    </constraints>
  </gsd:meta>

  <gsd:goal>输入测试维度 → 执行测试用例 → 输出通过率与速度</gsd:goal>

  <gsd:phase name="prepare" order="1">
    <gsd:step>确定测试维度（Recall/筛选/数学/代码/推理）</gsd:step>
    <gsd:step>选择上下文大小</gsd:step>
    <gsd:step>选择测试模型</gsd:step>
    <gsd:checkpoint>测试准备完成</gsd:checkpoint>
  </gsd:phase>

  <gsd:phase name="execute" order="2">
    <gsd:step>构建测试 prompt（context + question）</gsd:step>
    <gsd:step>调用 MiniMax API</gsd:step>
    <gsd:step>对比预期结果，计算是否通过</gsd:step>
    <gsd:step>记录响应时间</gsd:step>
    <gsd:checkpoint>测试执行完成</gsd:checkpoint>
  </gsd:phase>

  <gsd:phase name="report" order="3">
    <gsd:step>汇总通过率</gsd:step>
    <gsd:step>计算平均速度</gsd:step>
    <gsd:step>记录到结果文件</gsd:step>
    <gsd:checkpoint>测试报告完成</gsd:checkpoint>
  </gsd:phase>
</gsd:workflow>

# MiniMax 上下文测试套件

MiniMax M2.5 / M2.7 / M2.5-HighSpeed 模型测试手册。

## 上下文大小配置

| Size | Characters | Tokens (est.) |
|------|------------|---------------|
| tiny | ~1K | ~250 |
| small | ~5K | ~1.25K |
| medium | ~50K | ~12.5K |
| large | ~100K | ~25K |
| 128k | ~250K | ~128K |

## 测试维度

### 1. Recall（长文本记忆）
```python
context = "项目P001负责人张三，P002李四，P003王五。" * repeat
question = "P002负责人是谁？"
expected = "李四"
```

### 2. 筛选（条件过滤）
```python
context = "张三3年，李四5年，王五2年，赵六4年。"
question = "工龄>=3年有哪些？"
expected = ["张三", "李四", "赵六"]
```

### 3. 数学计算
```python
question = "100元打8折是多少钱？"
expected = "80"
```

### 4. 代码逻辑
```python
context = "def hello(): return 'hi'\ndef world(): return 'world'"
question = "有哪些函数？"
expected = ["hello", "world"]
```

### 5. 推理（多跳）
```python
context = "A在B前面，B在C前面。"
question = "谁在最后？"
expected = "C"
```

## 测试命令

```bash
# 运行快速测试 (默认 medium)
python3 references/full_test.py

# 运行所有测试 (指定上下文大小)
python3 references/full_test.py --all --context-size small

# 运行上下文测试
python3 references/full_test.py --ctx --context-size 128k

# 运行单个测试
python3 references/full_test.py --test filter_simple --model MiniMax-M2.5
```

## 测试结果

### Context Size: small (~5K)

| Model | Pass Rate | Speed |
|-------|-----------|-------|
| M2.5 | 80% | ~300字/秒 |
| M2.7 | 100% | ~180字/秒 |

### Context Size: 128k (~250K)

| Model | Pass Rate | Speed |
|-------|-----------|-------|
| M2.5 | 80% | ~33字/秒 |
| M2.7 | 100% | ~93字/秒 |
| Astron | 100% | ~6字/秒 |

## 结论

1. **通过率**: M2.7 在长上下文(128K)下更稳定
2. **速度**: M2.5 平均快 2x
3. **推荐**: 默认使用 M2.5，长上下文切换 M2.7

## 参考文件

- `references/TEST_RESULTS.md` - 详细测试结果
- `references/TEST_128K.md` - 128K 专项测试
- `references/full_test.py` - 测试脚本
