#!/usr/bin/env python3
"""SessionStart hook - Initialize plugin project context."""

import json
import sys
import os

def main():
    try:
        # Output welcome message
        result = {
            "systemMessage": "📚 Skills 插件项目已加载。可用命令: /init-novel, /standardize-plugin。使用 /plugin-maintainer scan 检查所有插件。"
        }
        print(json.dumps(result), file=sys.stdout)
        sys.exit(0)
    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()