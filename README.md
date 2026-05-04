# csvkse/skills

[![Stars](https://img.shields.io/github/stars/csvkse/skills?style=flat)](https://github.com/csvkse/skills/stargazers)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Claude Code](https://img.shields.io/badge/-Claude%20Code-8A2BE2?logo=claude&logoColor=white)

**Claude Code 插件集合，包含 MiniMax API、小说解析器、插件维护工具等。**

---

## 插件列表

| Plugin | 版本 | 说明 |
|--------|------|------|
| [minimax-api](./plugins/minimax-api) | 1.0.0 | MiniMax M2.5/M2.7 API 调用指南 |
| [minimax-testing](./plugins/minimax-testing) | 1.0.0 | 上下文测试套件，多维度测试 |
| [novel-chapter-parser](./plugins/novel-chapter-parser) | 2.1.0 | 小说章节解析器，知识库自动构建 |
| [plugin-standardizer](./plugins/plugin-standardizer) | 1.0.0 | 插件格式标准化工具 |

---

## 项目结构

```
csvkse/skills/
├── .claude-plugin/
│   └── marketplace.json          # 插件市场配置
├── agents/                       # Agent 定义
│   └── plugin-maintainer.md      # 插件维护 Agent
├── commands/                     # 斜杠命令
│   ├── init-novel.md             # 初始化小说知识库
│   └── standardize-plugin.md     # 标准化插件
├── hooks/                        # 事件钩子
│   ├── hooks.json                # 钩子配置
│   ├── validate_plugin_structure.py
│   └── session_start.py
├── scripts/                      # 工具脚本
│   ├── validate_plugin.py        # 插件验证
│   └── scan_plugins.py           # 扫描插件
├── templates/                    # 模板文件
│   ├── chapter-summary.md        # 章节总结模板
│   ├── plugin-json.md            # plugin.json 模板
│   └── skill-md.md               # SKILL.md 模板
├── references/                   # 参考文档
│   └── plugin-structure-guide.md # 插件结构规范
└── plugins/                      # 插件目录
    ├── minimax-api/
    ├── minimax-testing/
    ├── novel-chapter-parser/
    └── plugin-standardizer/
```

---

## 快速开始

### 方式一：从 skills.sh 安装

```bash
# 安装所有插件
npx skills add csvkse/skills

# 安装特定插件
npx skills add csvkse/skills/plugins/novel-chapter-parser
```

### 方式二：通过 Claude Code 插件市场

```bash
# 添加市场
/plugin marketplace add csvkse/skills

# 安装插件
/plugin install novel-chapter-parser@csvkse
/plugin install plugin-standardizer@csvkse
```

### 方式三：手动安装

```bash
git clone https://github.com/csvkse/skills.git
cp -r skills/plugins/* ~/.claude/plugins/
```

---

## 插件详情

### minimax-api

MiniMax M2.5/M2.7 API 调用指南。

| Skill | 触发词 | 说明 |
|-------|--------|------|
| api-call | MiniMax API、调用 MiniMax | 模型选择、Python 示例、错误处理 |

### minimax-testing

上下文测试套件，支持 Recall、筛选、数学、代码、推理测试。

| Skill | 触发词 | 说明 |
|-------|--------|------|
| context-test | 上下文测试、模型测试 | 多维度测试框架 |

### novel-chapter-parser

小说章节解析器，三次操作流程构建知识库。

**功能**：
- 自动提取人物、组织、地域、事件
- 生成章节总结、变化日志、关键记忆点
- 支持批量处理、智能编码识别

**命令**：
```bash
/init-novel <小说名称>           # 初始化知识库
/parse-chapter <章节号> <文件>   # 处理单章
/parse-chapters 1 10 <文件>      # 批量处理
```

### plugin-standardizer

将非标准插件转换为标准格式。

**功能**：
- 检测并移动 SKILL.md、scripts 到正确位置
- 转换 skill.json 为 plugin.json
- 自动注册到 marketplace.json

---

## 工具脚本

```bash
# 验证插件结构
python scripts/validate_plugin.py plugins/novel-chapter-parser

# 扫描所有插件
python scripts/scan_plugins.py plugins
```

---

## Agent

### plugin-maintainer

插件维护 Agent，管理插件生命周期。

**能力**：
- `create` - 创建新插件
- `validate` - 验证插件结构
- `standardize` - 标准化格式
- `register` - 注册到 marketplace
- `bump` - 更新版本
- `scan` - 扫描所有插件
- `remove` - 删除插件

**调用方式**：
```
Agent(subagent_type="plugin-maintainer", prompt="scan")
```

---

## 配置

### 启用插件

```json
// ~/.claude/settings.json
{
  "enabledPlugins": {
    "novel-chapter-parser@csvkse": true,
    "plugin-standardizer@csvkse": true
  }
}
```

### 验证安装

```bash
/status
/plugin list
```

---

## 相关链接

- **GitHub**: https://github.com/csvkse/skills
- **skills.sh**: https://skills.sh

---

## 许可证

[MIT](LICENSE) - 自由使用，按需修改。
