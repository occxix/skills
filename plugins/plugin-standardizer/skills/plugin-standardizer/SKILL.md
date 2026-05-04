---
name: plugin-standardizer
description: Convert non-standard Claude Code plugin to standard format. Detects misplaced SKILL.md, skill.json, scripts and restructures to .claude-plugin/plugin.json + skills/name/SKILL.md format. Auto-registers to marketplace.json.
---
# 插件标准化工具

将非标准 Claude Code 插件目录转换为标准插件格式。

## 触发词

- "标准化插件"
- "转换插件格式"
- "plugin standardize"
- "修复插件结构"

## 标准格式

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json          ← 插件配置
└── skills/
    └── <skill-name>/
        ├── SKILL.md          ← Skill 定义
        ├── README.md         ← 文档（可选）
        ├── references/       ← 参考文档（可选）
        └── scripts/          ← 脚本（可选）
```

## 执行流程

### 1. 检测当前结构

扫描插件目录，识别：
- 根目录 `SKILL.md` 或 `skill.md`
- 根目录 `skill.json` 或 `plugin.json`
- 根目录 `scripts/` 目录
- 根目录 `README.md`
- 是否存在 `.claude-plugin/` 目录

### 2. 分析并规划

根据检测结果生成转换计划：

| 当前位置 | 目标位置 |
|---------|---------|
| `./SKILL.md` | `./skills/<name>/SKILL.md` |
| `./skill.json` | `./.claude-plugin/plugin.json` |
| `./scripts/` | `./skills/<name>/scripts/` |
| `./README.md` | `./skills/<name>/README.md` |

### 3. 执行转换

1. 创建 `.claude-plugin/` 目录
2. 创建 `skills/<name>/` 目录
3. 移动文件到目标位置
4. 转换 `skill.json` 为 `plugin.json` 格式（如需要）
5. 删除旧文件

### 4. 注册到 marketplace

更新 `.claude-plugin/marketplace.json`，添加插件条目：

```json
{
  "name": "<plugin-name>",
  "source": "./plugins/<plugin-name>",
  "description": "<从 plugin.json 提取>",
  "version": "<从 plugin.json 提取>"
}
```

### 5. Git 提交

自动创建两次提交：
1. `feat: add <plugin-name> plugin (wip)` - 原始状态
2. `refactor: restructure <plugin-name> to standard plugin format` - 转换后

## plugin.json 模板

```json
{
  "name": "<plugin-name>",
  "version": "1.0.0",
  "description": "<描述>",
  "author": {
    "name": "<作者>",
    "url": "<作者URL>"
  },
  "homepage": "<项目主页>",
  "repository": "<仓库地址>",
  "license": "MIT",
  "keywords": ["<关键词>"],
  "minimum_claude_version": "1.8.0",
  "skills": [
    "../skills/<skill-name>/"
  ]
}
```

## 使用方法

```
/plugin-standardizer <插件目录路径>
```

示例：
```
/plugin-standardizer plugins/novel-chapter-parser
```

## 注意事项

- 转换前自动 Git 暂存当前状态
- 已是标准格式的插件跳过转换
- 多个 skill 时，每个创建独立 `skills/<name>/` 目录
- 保留原有文件内容，仅移动位置
