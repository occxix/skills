#!/usr/bin/env python3
"""
MiniMax 综合测试套件 (v3.1)
包含：长文本测试 + 筛选 + 数学 + 代码 + 推理
支持上下文大小选择
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from api_call import call_minimax, call_with_retry
import time
import argparse
from typing import Dict, List, Tuple

# ============================================================
# 上下文大小配置
# ============================================================

CONTEXT_SIZES = {
    "tiny": {"repeat": 10, "desc": "~1K 字符"},
    "small": {"repeat": 50, "desc": "~5K 字符"},
    "medium": {"repeat": 500, "desc": "~50K 字符"},
    "large": {"repeat": 1000, "desc": "~100K 字符"},
    "128k": {"repeat": 2500, "desc": "~250K 字符 (128K tokens)"},
}

BASE_CONTEXT = "项目P001负责人张三，项目P002负责人李四，项目P003负责人王五，项目P004负责人赵六，项目P005负责人钱七。"

def generate_context(size_name: str) -> str:
    """根据大小生成上下文"""
    if size_name not in CONTEXT_SIZES:
        size_name = "medium"
    repeat = CONTEXT_SIZES[size_name]["repeat"]
    return BASE_CONTEXT * repeat

# ============================================================
# 测试用例
# ============================================================

TESTS = {
    # ---------- 长文本Recall ----------
    "recall_10k": {
        "context": "公司A的CEO是张三，总裁是李四，CTO是王五。" * 500,
        "question": "公司A的CEO是谁？",
        "model": "auto",
        "expected": "张三"
    },
    "recall_50k": {
        "context": "项目P001负责人张三，项目P002负责人李四，项目P003负责人王五。" * 2000,
        "question": "P002负责人是谁？",
        "model": "auto",
        "expected": "李四"
    },
    
    # ---------- 筛选任务 ----------
    "filter_simple": {
        "context": "张三技术部，李四市场部，王五技术部，赵六设计部。",
        "question": "技术部有哪些人？",
        "model": "auto",
        "expected": ["张三", "王五"]
    },
    "filter_condition": {
        "context": "张三3年，李四5年，王五2年，赵六4年。",
        "question": "工龄>=3年有哪些？",
        "model": "auto",
        "expected": ["张三", "李四", "赵六"]
    },
    
    # ---------- 数学计算 ----------
    "math_discount": {
        "context": "",
        "question": "100元打8折是多少钱？",
        "model": "M2.5",
        "expected": "80"
    },
    "math_compound": {
        "context": "",
        "question": "100元打8折 + 150元打7折 = ？",
        "model": "M2.5",
        "expected": "185"
    },
    "math_simple": {
        "context": "",
        "question": "100 + 200 = ？",
        "model": "auto",
        "expected": "300"
    },
    
    # ---------- 代码追踪 ----------
    "code_function": {
        "context": "def hello(): return 'hi'\ndef world(): return 'earth'",
        "question": "函数名有哪些？",
        "model": "M2.5",
        "expected": ["hello", "world"]
    },
    "code_list": {
        "context": "x = [1, 2, 3]\ny = x[1:]",
        "question": "y等于多少？",
        "model": "M2.5",
        "expected": ["[2, 3]", "2, 3"]
    },
    
    # ---------- 推理任务 ----------
    "reason_multihop": {
        "context": "张三和李四是同学，李四和王五是前同事。",
        "question": "张三和王五什么关系？",
        "model": "auto",
        "expected": "李四"
    },
    "reason_time": {
        "context": "会议9:00开始，13:00审查。如果9:00延迟30分钟，审查几点开始？",
        "question": "审查几点？",
        "model": "auto",
        "expected": "13:30"
    },
    "reason_causal": {
        "context": "倒闭导致失业。公司倒闭了。",
        "question": "员工会失业吗？",
        "model": "auto",
        "expected": "会"
    },
    
    # ---------- 超高难度任务 ----------
    "ultra_nested": {
        "context": "",
        "question": "如果A大于B，B大于C，那么A和C哪个大？A大于C吗？",
        "model": "auto",
        "expected": ["A", "大于"]
    },
    "ultra_causal": {
        "context": "因为下雨所以地湿了。现在地湿了，是因为下雨吗？",
        "question": "地湿了一定是因为下雨吗？",
        "model": "auto",
        "expected": ["不一定"]
    },
    "ultra_calc": {
        "context": "",
        "question": "小明有5个苹果，给了小红一半，又给了小张2个，还剩多少？",
        "model": "auto",
        "expected": ["0", "没有了"]
    },
    "ultra_extract": {
        "context": "订单号：ABC123，金额：500元，数量：10件。",
        "question": "订单号是多少？",
        "model": "auto",
        "expected": ["ABC123"]
    },
    "ultra_distraction": {
        "context": "重要：A公司CEO是张三。干扰：B公司CEO是李四，C公司是王五。",
        "question": "A公司CEO是谁？",
        "model": "auto",
        "expected": ["张三"]
    },
    "ultra_time": {
        "context": "",
        "question": "昨天今天明天，顺序是什么？",
        "model": "auto",
        "expected": ["昨天"]
    },
    "ultra_logic": {
        "context": "条件1：下雨。条件2：带伞。小明带伞了，所以下雨了。这个推理正确吗？",
        "question": "这个推理正确吗？",
        "model": "auto",
        "expected": ["不正确", "错误"]
    },
    "ultra_antonym": {
        "context": "",
        "question": "请给出\"不\"的反义词不少于3个",
        "model": "auto",
        "expected": ["有", "是", "在"]
    },
    
    # ---------- 128K 长上下文测试 ----------
    "ctx_recall_1": {
        "context": "auto",  # 使用生成的上下文
        "question": "P002负责人是谁？",
        "model": "auto",
        "expected": "李四"
    },
    "ctx_recall_2": {
        "context": "auto",
        "question": "P005负责人是谁？",
        "model": "auto",
        "expected": "钱七"
    },
    "ctx_filter_1": {
        "context": "auto",
        "question": "研发部负责人是谁？",
        "model": "auto",
        "expected": "赵六"
    },
    "ctx_filter_2": {
        "context": "auto",
        "question": "2022年入职的负责人是谁？",
        "model": "auto",
        "expected": "赵六"
    },
    "ctx_count": {
        "context": "auto",
        "question": "共多少个项目？",
        "model": "auto",
        "expected": "5"
    },
}

# ============================================================
# 测试执行
# ============================================================

def run_test(name: str, test: Dict, model: str = "MiniMax-M2.5", 
             context_size: str = "medium", verbose: bool = True) -> Tuple[bool, str]:
    """运行单个测试"""
    ctx = test.get("context", "")
    
    # 处理 auto 上下文 (128K 测试)
    if ctx == "auto":
        ctx = generate_context(context_size)
    
    q = test["question"]
    content = f"{ctx}\n\n{q}" if ctx else q
    
    if verbose and ctx:
        print(f"  [上下文: {len(ctx)} 字符]")
    
    messages = [{"role": "user", "content": content}]
    
    if verbose:
        print(f"\n【{name}】({model})")
        print(f"  问题: {q[:50]}...")
    
    result = call_minimax(model, messages, timeout=180)
    
    # 检查结果
    expected = test.get("expected", "")
    if isinstance(expected, list):
        passed = any(e in result for e in expected)
    else:
        passed = expected in result
    
    if verbose:
        status = "✅" if passed else "❌"
        print(f"  结果: {result[:80] if result else '空'}")
        print(f"  状态: {status}")
    
    return passed, result


def run_full_test(context_size: str = "medium"):
    """运行完整测试"""
    models = ["MiniMax-M2.5", "MiniMax-M2.7"]
    
    print("=" * 70)
    print(f"🔥 MiniMax 综合测试套件 v3.1 (上下文: {context_size})")
    print(f"   {CONTEXT_SIZES.get(context_size, {}).get('desc', '')}")
    print("=" * 70)
    
    results = {m: {"passed": 0, "total": 0, "tests": []} for m in models}
    
    for name, test in TESTS.items():
        model_spec = test.get("model", "auto")
        
        for model in models:
            if model_spec == "auto":
                test_model = model
            elif model_spec == "M2.5" and model != "MiniMax-M2.5":
                continue
            elif model_spec == "M2.7" and model != "MiniMax-M2.7":
                continue
            
            passed, result = run_test(name, test, test_model, context_size)
            
            results[model]["total"] += 1
            if passed:
                results[model]["passed"] += 1
            
            results[model]["tests"].append({"name": name, "passed": passed})
            time.sleep(0.5)
    
    # 汇总
    print("\n" + "=" * 70)
    print("📊 结果汇总")
    print("=" * 70)
    
    for model, data in results.items():
        pct = data["passed"] * 100 // data["total"] if data["total"] > 0 else 0
        print(f"\n【{model}】")
        print(f"  通过: {data['passed']}/{data['total']} ({pct}%)")
        for t in data["tests"]:
            status = "✅" if t["passed"] else "❌"
            print(f"  {status} {t['name']}")
    
    return results


def run_ctx_test(context_size: str = "128k"):
    """运行上下文测试"""
    models = ["MiniMax-M2.5", "MiniMax-M2.7"]
    
    print("=" * 70)
    print(f"🔥 128K 上下文测试 (上下文: {context_size})")
    print(f"   {CONTEXT_SIZES.get(context_size, {}).get('desc', '')}")
    print("=" * 70)
    
    # 选择上下文相关测试
    ctx_tests = [k for k in TESTS.keys() if k.startswith("ctx_")]
    
    results = {m: {"passed": 0, "total": 0, "tests": []} for m in models}
    
    for name in ctx_tests:
        test = TESTS[name]
        
        for model in models:
            passed, result = run_test(name, test, model, context_size)
            
            results[model]["total"] += 1
            if passed:
                results[model]["passed"] += 1
            
            results[model]["tests"].append({"name": name, "passed": passed})
            time.sleep(0.5)
    
    # 汇总
    print("\n" + "=" * 70)
    print("📊 上下文测试结果")
    print("=" * 70)
    
    for model, data in results.items():
        pct = data["passed"] * 100 // data["total"] if data["total"] > 0 else 0
        print(f"\n【{model}】")
        print(f"  通过: {data['passed']}/{data['total']} ({pct}%)")
        for t in data["tests"]:
            status = "✅" if t["passed"] else "❌"
            print(f"  {status} {t['name']}")
    
    return results


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MiniMax综合测试 v3.1")
    parser.add_argument("--test", type=str, help="测试名称", default=None)
    parser.add_argument("--model", type=str, help="模型", default=None)
    parser.add_argument("--all", action="store_true", help="运行所有测试")
    parser.add_argument("--ctx", action="store_true", help="运行上下文测试")
    parser.add_argument("--context-size", type=str, default="medium",
                       choices=list(CONTEXT_SIZES.keys()),
                       help="上下文大小")
    
    args = parser.parse_args()
    
    print("可用上下文大小:")
    for k, v in CONTEXT_SIZES.items():
        print(f"  {k}: {v['desc']}")
    print()
    
    if args.test:
        test = TESTS[args.test].copy()
        model = args.model or "MiniMax-M2.5"
        run_test(args.test, test, model, args.context_size)
    elif args.ctx:
        run_ctx_test(args.context_size)
    elif args.all:
        run_full_test(args.context_size)
    else:
        # 默认运行简短测试
        print("运行快速测试...")
        quick_tests = ["filter_simple", "math_discount", "code_function"]
        for name in quick_tests:
            test = TESTS[name].copy()
            run_test(name, test, "MiniMax-M2.5", args.context_size)
            time.sleep(0.5)
