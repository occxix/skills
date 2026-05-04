#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
插件扫描脚本 - 扫描所有插件并生成报告

用法: python scan_plugins.py [plugins目录]
"""

import json
import sys
import os
import io
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def scan_plugins(plugins_dir: str) -> dict:
    """扫描所有插件"""
    results = {
        "total": 0,
        "valid": 0,
        "invalid": 0,
        "plugins": []
    }

    plugins_path = Path(plugins_dir)
    if not plugins_path.exists():
        return results

    for plugin_dir in plugins_path.iterdir():
        if not plugin_dir.is_dir():
            continue

        results["total"] += 1
        plugin_info = {
            "name": plugin_dir.name,
            "valid": True,
            "issues": []
        }

        # 检查 plugin.json
        plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
        if not plugin_json.exists():
            plugin_info["valid"] = False
            plugin_info["issues"].append("缺少 plugin.json")

        # 检查 skills/
        skills_dir = plugin_dir / "skills"
        if not skills_dir.exists():
            plugin_info["valid"] = False
            plugin_info["issues"].append("缺少 skills/ 目录")
        else:
            skill_count = len(list(skills_dir.iterdir()))
            plugin_info["skills"] = skill_count
            if skill_count == 0:
                plugin_info["valid"] = False
                plugin_info["issues"].append("skills/ 目录为空")

        if plugin_info["valid"]:
            results["valid"] += 1
        else:
            results["invalid"] += 1

        results["plugins"].append(plugin_info)

    return results

def main():
    plugins_dir = sys.argv[1] if len(sys.argv) > 1 else "plugins"

    results = scan_plugins(plugins_dir)

    print(f"\n插件扫描报告")
    print(f"{'=' * 40}")
    print(f"总计: {results['total']} 个插件")
    print(f"有效: {results['valid']} 个")
    print(f"问题: {results['invalid']} 个")

    if results["invalid"] > 0:
        print(f"\n问题插件:")
        for plugin in results["plugins"]:
            if not plugin["valid"]:
                print(f"  - {plugin['name']}: {', '.join(plugin['issues'])}")

    print(f"\n所有插件:")
    for plugin in results["plugins"]:
        symbol = "✅" if plugin["valid"] else "❌"
        skills = plugin.get("skills", 0)
        print(f"  {symbol} {plugin['name']} ({skills} skills)")

if __name__ == "__main__":
    main()