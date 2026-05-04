#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
插件验证脚本 - 检查插件结构是否符合规范

用法: python validate_plugin.py <插件目录>
"""

import json
import sys
import os
import io
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def validate_plugin(plugin_dir: str) -> dict:
    """验证插件结构"""
    results = {
        "valid": True,
        "checks": [],
        "errors": []
    }

    plugin_path = Path(plugin_dir)

    # 检查 plugin.json
    plugin_json = plugin_path / ".claude-plugin" / "plugin.json"
    if plugin_json.exists():
        try:
            with open(plugin_json, 'r', encoding='utf-8') as f:
                config = json.load(f)
            required = ['name', 'version', 'description', 'skills']
            for field in required:
                if field not in config:
                    results["errors"].append(f"plugin.json 缺少字段: {field}")
                    results["valid"] = False
            results["checks"].append(("plugin.json", True, "有效"))
        except json.JSONDecodeError:
            results["errors"].append("plugin.json 格式无效")
            results["valid"] = False
            results["checks"].append(("plugin.json", False, "JSON 格式错误"))
    else:
        results["errors"].append("缺少 .claude-plugin/plugin.json")
        results["valid"] = False
        results["checks"].append(("plugin.json", False, "不存在"))

    # 检查 SKILL.md
    skills_dir = plugin_path / "skills"
    if skills_dir.exists():
        skill_dirs = list(skills_dir.iterdir())
        if skill_dirs:
            for skill_dir in skill_dirs:
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    results["checks"].append((f"skills/{skill_dir.name}/SKILL.md", True, "存在"))
                else:
                    results["errors"].append(f"缺少 skills/{skill_dir.name}/SKILL.md")
                    results["valid"] = False
                    results["checks"].append((f"skills/{skill_dir.name}/SKILL.md", False, "不存在"))
        else:
            results["errors"].append("skills/ 目录为空")
            results["valid"] = False
    else:
        results["errors"].append("缺少 skills/ 目录")
        results["valid"] = False
        results["checks"].append(("skills/", False, "不存在"))

    return results

def main():
    if len(sys.argv) < 2:
        print("用法: python validate_plugin.py <插件目录>")
        sys.exit(1)

    plugin_dir = sys.argv[1]
    if not os.path.isdir(plugin_dir):
        print(f"错误: 目录不存在: {plugin_dir}")
        sys.exit(1)

    results = validate_plugin(plugin_dir)

    print(f"\n验证结果: {'✅ 通过' if results['valid'] else '❌ 失败'}")
    print("\n检查项:")
    for check, status, msg in results["checks"]:
        symbol = "✅" if status else "❌"
        print(f"  {symbol} {check}: {msg}")

    if results["errors"]:
        print("\n错误:")
        for error in results["errors"]:
            print(f"  - {error}")

    sys.exit(0 if results["valid"] else 1)

if __name__ == "__main__":
    main()