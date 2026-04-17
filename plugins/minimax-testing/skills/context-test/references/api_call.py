#!/usr/bin/env python3
"""
MiniMax API 调用脚本
用法: python3 call_minimax.py --model MiniMax-M2.5 --prompt "你的问题"
"""

import argparse
import requests
import sys
import time

API_URL = "https://api.minimaxi.com/v1/chat/completions"


def load_api_key(env_path: str = '/root/.hermes/.env') -> str:
    """从环境变量文件读取 API Key"""
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('MINIMAX_CN_API_KEY='):
                key = line.split('=', 1)[1].strip().strip('"').strip("'")
                return key
    raise ValueError("MINIMAX_CN_API_KEY not found in .env")


def call_minimax(
    model: str,
    messages: list,
    max_tokens: int = 500,
    timeout: int = 120
) -> str:
    """调用 MiniMax API"""
    API_KEY = load_api_key()
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages
    }

    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=timeout)
        resp = r.json()

        if resp.get("type") == "error":
            return f"ERROR:{resp.get('error', {}).get('type', '')}"

        choices = resp.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "")
        return ""
    except Exception as e:
        return f"ERROR:{str(e)}"


def call_with_retry(
    model: str,
    messages: list,
    max_retries: int = 2,
    timeout: int = 120
) -> str:
    """带重试的 API 调用"""
    for i in range(max_retries):
        result = call_minimax(model, messages, timeout=timeout)
        if result and len(result) > 10 and not result.startswith("ERROR:"):
            return result
        time.sleep(1)

    # 失败时尝试切换模型
    other = "MiniMax-M2.5" if model == "MiniMax-M2.7" else "MiniMax-M2.7"
    return call_minimax(other, messages)


def call_simple(question: str, model: str = "MiniMax-M2.5") -> str:
    """简单问答调用"""
    messages = [{"role": "user", "content": question}]
    return call_minimax(model, messages)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MiniMax API 调用')
    parser.add_argument('--model', default='MiniMax-M2.5', help='模型名称')
    parser.add_argument('--prompt', required=True, help='输入问题')
    parser.add_argument('--max-tokens', type=int, default=500, help='最大 token 数')
    parser.add_argument('--timeout', type=int, default=120, help='超时时间(秒)')
    args = parser.parse_args()

    print(f"模型: {args.model}")
    print(f"问题: {args.prompt}")
    print("-" * 50)

    result = call_minimax(args.model, [{"role": "user", "content": args.prompt}], args.max_tokens, args.timeout)
    print(f"结果: {result}")
