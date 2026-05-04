---
description: "安装 csvkse/skills 市场中的所有插件"
allowed-tools: ["Bash(plugin:*)"]
---

## Context

- 已添加的市场: !`plugin marketplace list`
- marketplace 插件列表: !`cat .claude-plugin/marketplace.json 2>/dev/null | grep -o '"name"[^,]*' || echo "无"`

## Your Task

安装 csvkse/skills 市场中的所有插件：

1. 检查市场是否已添加（csvkse-skills）
2. 读取 marketplace.json 获取插件列表
3. 逐个安装每个插件：
   - minimax-api@csvkse
   - minimax-testing@csvkse
   - novel-chapter-parser@csvkse
   - plugin-standardizer@csvkse
   - auto-fixer@csvkse
4. 启用所有已安装插件
5. 输出安装结果汇总

不要执行其他操作。