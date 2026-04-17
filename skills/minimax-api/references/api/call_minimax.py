#!/usr/bin/env python3
"""
MiniMax API 调用核心模块
包含：API调用、重试机制、错误处理
"""

import json
import requests
import os
import time
from typing import Dict, List, Tuple, Optional

# ============================================================
# API 配置
# ============================================================

def load_api_key(env_path: str = '/root/.hermes/.env') -> str:
    """从环境变量文件读取 API Key"""
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('MINIMAX_CN_API_KEY='):
                key = line.split('=', 1)[1].strip().strip('"').strip("'")
                return key  # 确保没有换行符
    raise ValueError("MINIMAX_CN_API_KEY not found in .env")

API_URL = "https://api.minimaxi.com/v1/chat/completions"

# ============================================================
# 核心 API 调用
# ============================================================

def call_minimax(
    model: str,
    messages: List[Dict],
    max_tokens: int = 500,
    timeout: int = 120
) -> str:
    """
    调用 MiniMax API
    
    Args:
        model: 模型名称 (MiniMax-M2.5 或 MiniMax-M2.7)
        messages: 消息列表
        max_tokens: 最大生成 token 数
        timeout: 超时时间(秒)
    
    Returns:
        API 响应文本，错误时返回空字符串
    """
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
            return f"ERROR:{resp.get('error',{}).get('type','')}"
        
        # OpenAI 风格响应
        choices = resp.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "")
        return ""
    except Exception as e:
        return f"ERROR:{str(e)}"


def call_with_retry(
    model: str,
    messages: List[Dict],
    max_retries: int = 2,
    timeout: int = 120
) -> str:
    """
    带重试的 API 调用
    
    Args:
        model: 模型名称
        messages: 消息列表
        max_retries: 最大重试次数
        timeout: 超时时间
    
    Returns:
        API 响应文本
    """
    for i in range(max_retries):
        result = call_minimax(model, messages, timeout=timeout)
        if result and len(result) > 10 and not result.startswith("ERROR:"):
            return result
        time.sleep(1)
    
    # 失败时尝试切换模型
    other = "MiniMax-M2.5" if model == "MiniMax-M2.7" else "MiniMax-M2.7"
    return call_minimax(other, messages)


# ============================================================
# 便捷函数
# ============================================================

def call_simple(question: str, model: str = "MiniMax-M2.5") -> str:
    """简单问答调用"""
    messages = [{"role": "user", "content": question}]
    return call_minimax(model, messages)


def call_with_context(context: str, question: str, model: str = "MiniMax-M2.5") -> str:
    """带上下文的问答调用"""
    content = f"{context}\n\n{question}" if context else question
    messages = [{"role": "user", "content": content}]
    return call_minimax(model, messages)


# ============================================================
# 测试
# ============================================================

if __name__ == "__main__":
    import sys
    
    # 测试简单调用
    print("测试1: 简单问答")
    result = call_simple("100元打8折是多少钱？", "MiniMax-M2.5")
    print(f"  结果: {result}")
    
    # 测试带上下文
    print("\n测试2: 带上下文")
    result = call_with_context(
        "张三技术部，李四市场部，王五技术部。",
        "技术部有哪些人？",
        "MiniMax-M2.7"
    )
    print(f"  结果: {result}")
    
    # 测试重试
    print("\n测试3: 重试机制")
    result = call_with_retry("MiniMax-M2.5", [{"role": "user", "content": "你好"}])
    print(f"  结果: {result}")
