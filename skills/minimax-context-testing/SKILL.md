# MiniMax Context Testing Skill (v3.1)

## Core Features

- **Multi-model testing**: M2.5 vs M2.7 vs Astron
- **Configurable context size**: tiny, small, medium, large, 128k
- **Comprehensive test suite**: Recall, Filter, Math, Code, Reasoning

---

## Context Size Options

| Size | Characters | Tokens (est.) |
|------|------------|---------------|
| tiny | ~1K | ~250 |
| small | ~5K | ~1.25K |
| medium | ~50K | ~12.5K |
| large | ~100K | ~25K |
| 128k | ~250K | ~128K |

---

## Test Commands

```bash
# 运行快速测试 (默认 medium)
python3 full_test.py

# 运行所有测试 (指定上下文大小)
python3 full_test.py --all --context-size small

# 运行上下文测试
python3 full_test.py --ctx --context-size 128k

# 运行单个测试
python3 full_test.py --test filter_simple --model MiniMax-M2.5 --context-size medium
```

---

## Test Results (v3.1)

### Context Size: small (~5K)

| Model | Pass Rate | Speed |
|-------|-----------|-------|
| M2.5 | 80% | - |
| M2.7 | 100% | - |

### Context Size: 128k (~250K)

| Model | Pass Rate | Speed |
|-------|-----------|-------|
| M2.5 | 60% | - |
| M2.7 | 80% | - |

---

## Model Comparison

| Model | Speed | 128K Support | Best For |
|-------|-------|--------------|----------|
| M2.5 | 300字/秒 | ⚠️ 60% | Fast generation |
| M2.7 | 180字/秒 | ✅ 80% | Long context |
| Astron | 16字/秒 | ✅ 100% | Code understanding |

---

## Related Files

- `references/high-difficulty/full_test.py` - Test suite
- `references/TEST_RESULTS.md` - Detailed results
- `references/TEST_128K.md` - 128K test results
- `../minimax-api/SKILL.md` - API calling guide

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v3.1 | 2026-04-15 | Added context size selection |
| v3.0 | 2026-04-15 | Split into API + Testing skills |
