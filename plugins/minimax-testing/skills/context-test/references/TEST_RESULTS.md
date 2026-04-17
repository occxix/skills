# MiniMax 综合测试结果 (v3.0)

> **⚠️ 性能测试声明**：文字生成速度的测试方法和统计较为简陋，不够专业，仅供参考。实际速度受网络、服务器负载等因素影响较大。

## 测试时间
2026-04-15 14:30 UTC+8

## 测试结果汇总

| 模型 | 通过率 | 平均速度 |
|------|--------|----------|
| MiniMax-M2.5 | 95% (19/20) | ~300字/秒 |
| MiniMax-M2.7 | 93% (15/16) | ~180字/秒 |

---

## 详细测试结果

### MiniMax-M2.5

| 测试 | 状态 | 说明 |
|------|------|------|
| recall_10k | ✅ | 长文本Recall |
| recall_50k | ✅ | 长文本Recall |
| filter_simple | ✅ | 简单筛选 |
| filter_condition | ✅ | 条件筛选 |
| math_discount | ✅ | 折扣计算 |
| math_compound | ✅ | 复合计算 |
| math_simple | ✅ | 简单计算 |
| code_function | ✅ | 函数追踪 |
| code_list | ✅ | 列表操作 |
| reason_multihop | ✅ | 多跳推理 |
| reason_time | ✅ | 时间推理 |
| reason_causal | ✅ | 因果推理 |
| ultra_nested | ✅ | 嵌套推理 |
| ultra_causal | ✅ | 反向因果 |
| ultra_calc | ✅ | 多步计算 |
| ultra_extract | ✅ | 精确提取 |
| ultra_distraction | ✅ | 干扰信息 |
| ultra_time | ✅ | 时序推理 |
| ultra_logic | ❌ | 逻辑与或 |
| ultra_antonym | ✅ | 反义词陷阱 |

**未通过**: ultra_logic (逻辑与或推理)

---

### MiniMax-M2.7

| 测试 | 状态 | 说明 |
|------|------|------|
| recall_10k | ✅ | 长文本Recall |
| recall_50k | ✅ | 长文本Recall |
| filter_simple | ✅ | 简单筛选 |
| filter_condition | ✅ | 条件筛选 |
| math_simple | ✅ | 简单计算 |
| reason_multihop | ✅ | 多跳推理 |
| reason_time | ✅ | 时间推理 |
| reason_causal | ✅ | 因果推理 |
| ultra_nested | ✅ | 嵌套推理 |
| ultra_causal | ✅ | 反向因果 |
| ultra_calc | ✅ | 多步计算 |
| ultra_extract | ✅ | 精确提取 |
| ultra_distraction | ✅ | 干扰信息 |
| ultra_time | ✅ | 时序推理 |
| ultra_logic | ❌ | 逻辑与或 |
| ultra_antonym | ✅ | 反义词陷阱 |

**未通过**: ultra_logic (逻辑与或推理)

---

## 速度对比

| 任务类型 | M2.5 | M2.7 | 差异 |
|----------|------|------|------|
| 折扣计算 | 214字/秒 | 130字/秒 | M2.5 快 64% |
| 百分比 | 127字/秒 | 114字/秒 | M2.5 快 11% |
| 列表筛选 | 251字/秒 | 185字/秒 | M2.5 快 36% |
| 多跳推理 | 289字/秒 | 125字/秒 | M2.5 快 131% |
| 代码追踪 | 430字/秒 | 96字/秒 | M2.5 快 348% |
| 长文本生成 | 155字/秒 | 135字/秒 | M2.5 快 15% |

---

## 结论

1. **通过率**: M2.5 (95%) > M2.7 (93%)
2. **速度**: M2.5 平均快 ~2x
3. **共同弱点**: ultra_logic (逻辑与或推理) 两者都失败
4. **推荐**: 默认使用 M2.5，需要筛选任务时可切换 M2.7

---

## 测试命令

```bash
# 运行全部测试
python3 full_test.py --all

# 运行单个测试
python3 full_test.py --test <测试名> --model MiniMax-M2.5
```
