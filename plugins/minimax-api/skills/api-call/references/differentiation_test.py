#!/usr/bin/env python3
"""
MiniMax 高难度区分测试套件 (v1.0)
用于区分 M2.5 和 M2.7 的能力差异
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../api'))
from call_minimax import call_minimax, call_with_retry
import time
from typing import Dict, List, Tuple

# ============================================================
# 测试用例 - 高难度区分测试
# ============================================================

TESTS = {
    # ---------- 多跳关联推理 ----------
    "multi_hop_1": {
        "context": "张三喜欢苹果，李四喜欢香蕉，王五喜欢橙子。李四和王五是同事。",
        "question": "谁喜欢的水果和李四不一样但是和王五一样？",
        "model": "M2.5",
        "expected": ["王五"]
    },
    
    # ---------- 否定约束推理 ----------
    "negation_1": {
        "context": "所有员工都准时上班，除了张三。",
        "question": "张三准时上班了吗？",
        "model": "auto",
        "expected": ["没有", "否", "没"]
    },
    
    # ---------- 数学逻辑陷阱 ----------
    "math_trap_1": {
        "context": "",
        "question": "一个数加上自身再乘以2等于30，这个数是多少？",
        "model": "M2.5",
        "expected": ["10"]
    },
    
    # ---------- 上下文干扰 ----------
    "distraction_1": {
        "context": "重要信息：A公司CEO是张三。干扰信息：B公司CEO是李四。C公司CEO是王五。",
        "question": "A公司CEO是谁？",
        "model": "auto",
        "expected": ["张三"]
    },
    
    # ---------- 代码逻辑组合 ----------
    "code_logic_1": {
        "context": "def calc(a, b):\n    return a * 2 + b\n\nx = calc(3, 1)",
        "question": "x等于多少？",
        "model": "M2.5",
        "expected": ["7"]
    },
    
    # ---------- 精确数字序列 ----------
    "number_seq_1": {
        "context": "序列：1, 3, 6, 10, 15",
        "question": "下一个数字是什么？",
        "model": "auto",
        "expected": ["21"]
    },
    
    # ---------- 时间顺序推理 ----------
    "time_order_1": {
        "context": "会议9:00开始，持续2小时。午休从11:00到11:30。",
        "question": "会议几点结束？",
        "model": "auto",
        "expected": ["11:00", "11点"]
    },
    
    # ---------- 多条件组合筛选 ----------
    "multi_filter_1": {
        "context": "张三男25岁，李四女30岁，王五男22岁，赵六女28岁。",
        "question": "年龄大于25岁的女生有哪些？",
        "model": "M2.7",
        "expected": ["李四", "赵六"]
    },
}

# ============================================================
# 测试执行
# ============================================================

def run_test(name: str, test: Dict, model: str = "MiniMax-M2.5", verbose: bool = True) -> Tuple[bool, str]:
    """运行单个测试"""
    ctx = test.get("context", "")
    q = test["question"]
    content = f"{ctx}\n\n{q}" if ctx else q
    
    messages = [{"role": "user", "content": content}]
    
    if verbose:
        print(f"\n【{name}】({model})")
        print(f"  问题: {q}")
    
    result = call_minimax(model, messages, timeout=60)
    
    # 检查结果
    expected = test.get("expected", "")
    if isinstance(expected, list):
        passed = any(e in result for e in expected)
    else:
        passed = expected in result
    
    if verbose:
        status = "✅" if passed else "❌"
        print(f"  结果: {result[:100] if result else '空'}")
        print(f"  状态: {status}")
    
    return passed, result


def run_differentiation_test():
    """运行高难度区分测试"""
    models = ["MiniMax-M2.5", "MiniMax-M2.7"]
    
    print("=" * 70)
    print("🔥 MiniMax 高难度区分测试")
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
            
            passed, result = run_test(name, test, test_model)
            
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


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="MiniMax高难度区分测试")
    parser.add_argument("--test", type=str, help="测试名称", default=None)
    parser.add_argument("--model", type=str, help="模型", default=None)
    parser.add_argument("--all", action="store_true", help="运行所有测试")
    
    args = parser.parse_args()
    
    if args.test:
        test = TESTS[args.test].copy()
        model = args.model or "MiniMax-M2.5"
        run_test(args.test, test, model)
    elif args.all:
        run_differentiation_test()
    else:
        print("使用 --all 运行所有测试，或 --test <名称> 运行单个测试")
