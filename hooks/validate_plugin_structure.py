#!/usr/bin/env python3
"""PostToolUse hook - Validate plugin structure after Write operations."""

import json
import sys
import os
import re

def main():
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        file_path = tool_input.get('file_path', '')

        # Only check plugin-related files
        if not file_path or 'plugins/' not in file_path:
            sys.exit(0)

        # Check if writing to plugin.json or SKILL.md
        is_plugin_json = file_path.endswith('plugin.json')
        is_skill_md = file_path.endswith('SKILL.md')

        if is_plugin_json:
            content = tool_input.get('content', '')
            # Validate required fields
            required = ['name', 'version', 'description', 'skills']
            missing = []
            for field in required:
                if f'"name"' in content and field == 'name':
                    continue
                if f'"{field}"' not in content:
                    missing.append(field)

            if missing:
                result = {
                    "systemMessage": f"⚠️ plugin.json 缺少必需字段: {', '.join(missing)}。建议添加这些字段。"
                }
                print(json.dumps(result), file=sys.stdout)

        elif is_skill_md:
            content = tool_input.get('content', '')
            # Check frontmatter
            if not content.startswith('---'):
                result = {
                    "systemMessage": "⚠️ SKILL.md 缺少 frontmatter。建议添加 name 和 description 字段。"
                }
                print(json.dumps(result), file=sys.stdout)

        sys.exit(0)

    except Exception as e:
        # Allow operation on error
        sys.exit(0)

if __name__ == '__main__':
    main()