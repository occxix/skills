---
name: plugin-structure-guide
description: Claude Code 插件结构规范参考
type: guide
tags: [plugin, structure, claude-code]
---

# Claude Code 插件结构规范

## 标准目录结构

```
plugins/<name>/
├── .claude-plugin/
│   └── plugin.json              ← 插件配置（必需）
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md              ← Skill 定义（必需）
│       ├── agents/               ← 局部 Agents
│       ├── scripts/              ← 工具脚本
│       ├── references/           ← 参考文档
│       └── templates/            ← 模板
├── commands/                     ← 斜杠命令
├── hooks/                        ← 事件钩子
│   └── hooks.json
└── README.md
```

## plugin.json 必需字段

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 插件名称（唯一） |
| version | string | 版本号（semver） |
| description | string | 描述 |
| skills | array | skill 路径数组 |

## SKILL.md 格式

```markdown
---
name: skill-name
description: 技能描述
---

# 技能内容
...
```

## Hooks 配置

| 事件 | 触发时机 |
|------|----------|
| PreToolUse | 工具调用前 |
| PostToolUse | 工具调用后 |
| Stop | 会话结束 |
| UserPromptSubmit | 用户提交消息 |
| SessionStart | 会话开始 |

## 钩子退出码

- 0: 允许操作
- 2: 阻止操作