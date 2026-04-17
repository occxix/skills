# occxix/skills

[![Stars](https://img.shields.io/github/stars/occxix/skills?style=flat)](https://github.com/occxix/skills/stargazers)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Claude Code](https://img.shields.io/badge/-Claude%20Code-8A2BE2?logo=claude&logoColor=white)

**MiniMax 模型 API 与测试 Skills 集合，基于 Claude Code 插件架构。**

---

## Plugin 模块

| Plugin | 版本 | 说明 | 包含 Skills |
|--------|------|------|------------|
| [minimax-api](./plugins/minimax-api) | 1.0.0 | MiniMax M2.5/M2.7 API 调用指南 | api-call |
| [minimax-testing](./plugins/minimax-testing) | 1.0.0 | 上下文测试套件 | context-test |

---

## 快速开始

### 方式一：从 skills.sh 安装（推荐）

[![skills.sh](https://img.shields.io/badge/skills.sh-Open%20Skills%20Ecosystem-blue)](https://skills.sh)

```bash
# 安装所有 Plugin
npx skills add occxix/skills

# 安装特定 Plugin
npx skills add occxix/skills/plugins/minimax-api
npx skills add occxix/skills/plugins/minimax-testing
```

### 方式二：通过 Claude Code 插件市场安装

```bash
# 添加市场
/plugin marketplace add occxix/skills

# 安装单个 Plugin
/plugin install minimax-api@occxix
/plugin install minimax-testing@occxix

# 启用/禁用 Plugin
/plugin enable minimax-api@occxix
/plugin disable minimax-api@occxix
```

---

## Skills 详情

### minimax-api

> MiniMax M2.5/M2.7 API 调用指南，包含 Python 调用示例、模型选择建议与错误处理。

| Skill | 触发词 | 说明 |
|-------|--------|------|
| api-call | MiniMax API、调用 MiniMax、API key 配置 | 模型选择决策树、Python 调用示例、错误处理 |

### minimax-testing

> 上下文测试套件，支持 Recall、筛选、数学、代码、推理多维度测试。

| Skill | 触发词 | 说明 |
|-------|--------|------|
| context-test | 上下文测试、Recall 测试、模型测试 | 多维度测试框架：上下文大小配置、测试维度、运行命令 |

---

## 配置说明

### 配置文件位置

| 作用范围 | 文件路径 | 说明 |
|----------|----------|------|
| **全局** | `~/.claude/settings.json` | 所有项目生效 |
| **项目共享** | `.claude/settings.json` | 当前项目生效，提交到 git |
| **项目本地** | `.claude/settings.local.json` | 当前项目生效，不提交 git |

### 优先级

```
项目本地 > 项目共享 > 全局
```

### 手动配置示例

```json
// ~/.claude/settings.json 或 .claude/settings.json
{
  "enabledPlugins": {
    "minimax-api@occxix": true,
    "minimax-testing@occxix": true
  }
}
```

### 验证配置

```bash
# 查看当前生效的配置和 Plugin 状态
/status

# 查看已安装的 Plugin
/plugin list
```

---

## 目录结构

```
occxix/skills/
├── plugins/
│   ├── minimax-api/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── skills/
│   │       └── api-call/
│   │           └── SKILL.md
│   └── minimax-testing/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── context-test/
│               ├── SKILL.md
│               └── references/
├── CLAUDE.md
└── README.md
```

---

## 相关链接

- **GitHub**: https://github.com/occxix/skills
- **skills.sh**: https://skills.sh (Open Agent Skills Ecosystem)

---

## 贡献

欢迎提交 Issue 和 Pull Request！

---

## 许可证

[MIT](LICENSE) - 自由使用，按需修改。
