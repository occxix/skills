"""
初始化小说知识库

用法: /init-novel <小说名称>
"""

import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 添加脚本路径
SCRIPTS_PATH = Path(__file__).parent
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))

from kb_tools import init_knowledge_base, KB_STRUCTURE


def create_knowledge_base(novel_name: str, base_path: str = None):
    """
    创建小说知识库
    
    Args:
        novel_name: 小说名称
        base_path: 基础路径（默认为当前工作目录）
    """
    if base_path is None:
        base_path = os.getcwd()
    
    result = init_knowledge_base(base_path, novel_name)
    
    if result["success"]:
        print(f"[OK] {result['message']}")
        print(f"Path: {result['path']}")
        print(f"\nCreated directories:")
        for d in result["created_dirs"]:
            print(f"  |-- {d}")
        print(f"\nCreated files:")
        for f in result["created_files"]:
            print(f"  |-- {f}")
        print(f"\nKnowledge base structure:")
        print_structure(KB_STRUCTURE, "  ")
    else:
        print(f"[WARN] {result['message']}")
        print(f"Path: {result['path']}")
    
    return result


def print_structure(structure: dict, prefix: str = ""):
    """Print directory structure"""
    items = list(structure.items())
    for i, (name, content) in enumerate(items):
        is_last = i == len(items) - 1
        connector = "`-- " if is_last else "|-- "
        print(f"{prefix}{connector}{name}")
        
        if isinstance(content, dict) and content:
            new_prefix = prefix + ("    " if is_last else "|   ")
            print_structure(content, new_prefix)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python init_novel.py <小说名称>")
        print("示例: python init_novel.py 诡秘之主")
        sys.exit(1)
    
    novel_name = sys.argv[1]
    create_knowledge_base(novel_name)


if __name__ == "__main__":
    main()
