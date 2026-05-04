# Claude Code 插件类型与结构

## 插件类型

### 单插件模式 (Single Plugin)

一个 `plugin.json` 入口，包含多个 skills。

**示例**: `superpowers@claude-plugins-official`

```
superpowers/
├── .claude-plugin/
│   └── plugin.json          # 单一入口
├── skills/                   # 14 个 skills 内置
│   ├── brainstorming/
│   ├── writing-plans/
│   ├── executing-plans/
│   ├── test-driven-development/
│   └── ...
├── agents/
│   └── code-reviewer.md
├── commands/
├── hooks/
└── ...
```

**安装方式**:
```bash
/plugin install superpowers@claude-plugins-official
```

**特点**:
- 一次性安装，获得所有 skills
- 适合功能完整的工作流套件

---

### Marketplace 模式

一个 `marketplace.json` 管理多个独立插件，用户按需选择。

**示例**: `csvkse/skills`

```
csvkse-skills/                  # marketplace 根
├── .claude-plugin/
│   └── marketplace.json        # 市场配置
├── agents/                     # 共享 agents
│   └── plugin-maintainer.md
├── commands/                   # 共享 commands
├── hooks/                      # 共享 hooks
└── plugins/                    # 独立插件目录
    ├── minimax-api/
    │   └── .claude-plugin/plugin.json
    ├── novel-chapter-parser/
    │   └── .claude-plugin/plugin.json
    └── ...
```

**安装方式**:
```bash
# 添加市场
/plugin marketplace add csvkse/skills

# 按需安装单个插件
/plugin install novel-chapter-parser@csvkse
/plugin install minimax-api@csvkse
```

**特点**:
- 用户按需选择插件
- 根目录 agents/commands/hooks 共享给所有插件

---

## 目录结构与加载规则

### 根目录组件 (共享)

| 目录 | 加载时机 | 说明 |
|------|----------|------|
| `agents/` | 安装任意插件即加载 | 共享 agents |
| `commands/` | 安装任意插件即加载 | 共享斜杠命令 |
| `hooks/` | 安装任意插件即加载 | 共享事件钩子 |
| `scripts/` | 安装任意插件即加载 | 共享脚本工具 |
| `templates/` | 安装任意插件即加载 | 共享模板 |
| `references/` | 安装任意插件即加载 | 共享参考文档 |

### 插件内组件 (独立)

| 目录 | 加载时机 | 说明 |
|------|----------|------|
| `plugins/<name>/skills/` | 仅安装该插件时加载 | 插件专属 skills |
| `plugins/<name>/agents/` | 仅安装该插件时加载 | 插件专属 agents |
| `plugins/<name>/commands/` | 仅安装该插件时加载 | 插件专属 commands |
| `plugins/<name>/hooks/` | 仅安装该插件时加载 | 插件专属 hooks |

---

## 安装路径

### 单插件模式

```
~/.claude/plugins/cache/{marketplace}/{plugin}/
```

示例:
```
~/.claude/plugins/cache/claude-plugins-official/superpowers/
```

### Marketplace 模式

```
~/.claude/plugins/marketplaces/{marketplace-name}/plugins/{plugin}/
```

示例:
```
~/.claude/plugins/marketplaces/csvkse-skills/plugins/novel-chapter-parser/
```

---

## 对比总结

| 特性 | 单插件模式 | Marketplace 模式 |
|------|-----------|-----------------|
| 入口文件 | `plugin.json` | `marketplace.json` + 多个 `plugin.json` |
| Skills | 内置多个 | 分散在各插件 |
| 安装粒度 | 整体安装 | 按需选择 |
| 共享组件 | 插件内共享 | 根目录共享 |
| 适用场景 | 完整工作流套件 | 工具集合/插件市场 |

---

## 配置文件格式

### plugin.json

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": {
    "name": "author",
    "url": "https://github.com/author"
  },
  "homepage": "https://github.com/author/repo",
  "repository": "https://github.com/author/repo",
  "license": "MIT",
  "keywords": ["claude-code", "skill"],
  "skills": "./skills/"
}
```

### marketplace.json

```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "owner"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "Plugin description",
      "version": "1.0.0"
    }
  ]
}
```
