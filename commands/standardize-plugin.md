---
description: "标准化插件目录结构"
allowed-tools: ["Bash(mv:*)", "Bash(mkdir:*)", "Read", "Write", "Edit"]
argument-hint: "<插件目录路径>"
---

## Context

- 插件目录: !`ls -d plugins/*/ 2>/dev/null | head -5`
- marketplace 注册: !`cat .claude-plugin/marketplace.json 2>/dev/null | grep -o '"name"[^,]*' | head -5`

## Your Task

将非标准插件转换为标准格式：

1. 检测当前结构：
   - 根目录 SKILL.md → 应移至 `skills/<name>/`
   - 根目录 skill.json → 应转为 `.claude-plugin/plugin.json`
   - 根目录 scripts/ → 应移至 `skills/<name>/scripts/`

2. 创建标准目录：
   - `.claude-plugin/`
   - `skills/<name>/`

3. 移动文件到正确位置

4. 更新 marketplace.json（如需要）

5. Git 提交变更

不要执行其他操作。
