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
| [auto-fixer](./plugins/auto-fixer) | 1.0.0 | 自动检测并修复插件结构问题 |

---

## 项目结构

```
csvkse/skills/
├── .claude-plugin/
│   └── marketplace.json          # 插件市场配置
├── agents/                       # Agent 定义
│   └── plugin-maintainer.md      # 插件维护 Agent
├── commands/                     # 斜杠命令（通用）
│   ├── install-all.md            # 一键安装所有插件
│   └── update-all.md             # 一键更新所有插件
├── hooks/                        # 事件钩子
│   ├── hooks.json                # 钩子配置
│   ├── validate_plugin_structure.py
│   └── session_start.py
├── scripts/                      # 工具脚本
│   ├── validate_plugin.py        # 插件验证
│   └── scan_plugins.py           # 扫描插件
├── templates/                    # 模板文件（通用）
│   ├── plugin-json.md            # plugin.json 模板
│   └── skill-md.md               # SKILL.md 模板
├── references/                   # 参考文档
│   └── plugin-structure-guide.md # 插件结构规范
├── docs/                         # 文档目录
│   └── plugin-types.md           # 插件类型说明
├── assets/                       # 资源文件
└── plugins/                      # 插件目录
    ├── minimax-api/
    ├── minimax-testing/
    ├── novel-chapter-parser/
    │   └── commands/
    │       └── init-novel.md     # 初始化小说知识库
    ├── plugin-standardizer/
    │   └── commands/
    │       └── standardize-plugin.md
    └── auto-fixer/
```

---

## 快速开始

### 方式一：一键安装全部插件

```bash
# 添加市场并安装所有插件
/plugin marketplace add csvkse/skills
/install-all
```

或使用 `/update-all` 更新所有已安装插件。

### 方式二：从 skills.sh 安装

```bash
# 安装所有插件
npx skills add csvkse/skills

# 安装特定插件
npx skills add csvkse/skills/plugins/novel-chapter-parser

# 更新插件
npx skills update csvkse/skills
```

### 方式三：通过 Claude Code 插件市场（按需选择）

```bash
# 添加市场
/plugin marketplace add csvkse/skills

# 按需安装单个插件
/plugin install novel-chapter-parser@csvkse
/plugin install plugin-standardizer@csvkse
/plugin install auto-fixer@csvkse

# 更新插件
/plugin update novel-chapter-parser@csvkse

# 更新所有插件
/plugin update --all

# 启用/禁用插件
/plugin enable novel-chapter-parser@csvkse
/plugin disable novel-chapter-parser@csvkse

# 查看已安装插件
/plugin list
```

> **已添加过旧版市场的用户**：需重新添加
> ```bash
> /plugin marketplace remove csvkse-skills
> /plugin marketplace add csvkse/skills
> ```

### 方式四：手动安装

```bash
git clone https://github.com/csvkse/skills.git
cp -r skills/plugins/* ~/.claude/plugins/

# 更新
cd skills && git pull
```

---

## 安装副作用

使用 `/plugin install` 方式安装任意插件后，以下共享组件自动加载：

| 组件 | 说明 |
|------|------|
| `plugin-maintainer` Agent | 插件生命周期管理 |
| `/install-all` 命令 | 一键安装所有插件 |
| `/update-all` 命令 | 一键更新所有插件 |

**原因**: 根目录 `agents/`、`commands/`、`hooks/` 为共享资源，通过 `/plugin` 安装时自动加载。

> **注意**: `npx skills add` 和手动安装方式无此副作用，仅复制文件，不加载共享组件。

---

## 插件专属命令

以下命令仅安装对应插件后可用：

| 命令 | 插件 | 说明 |
|------|------|------|
| `/init-novel` | novel-chapter-parser | 初始化小说知识库 |
| `/standardize-plugin` | plugin-standardizer | 标准化插件格式 |

---

## 安装路径

不同安装方式，插件存储位置不同：

| 安装方式 | 存储路径 |
|----------|----------|
| `/plugin install` | `~/.claude/plugins/marketplaces/csvkse-skills/plugins/<name>/` |
| `npx skills add` | `~/.agents/skills/<name>/` 或 `~/.claude/skills/<name>/` |
| 手动复制 | 用户指定位置 |

**示例**：

```bash
# /plugin install 方式
~/.claude/plugins/marketplaces/csvkse-skills/plugins/novel-chapter-parser/

# npx skills add 方式
~/.agents/skills/novel-chapter-parser/
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

### auto-fixer

自动检测并修复插件项目结构问题。

**功能**：
- 检测 Skills、Agents、Commands、Hooks 等结构问题
- 自动修复 frontmatter 缺失、格式错误
- 修复编码问题、路径错误
- 补充 plugin.json、marketplace.json 缺失字段

**命令**：
```bash
/auto-fixer scan              # 扫描问题
/auto-fixer fix               # 自动修复
/auto-fixer fix --type skills # 修复特定类型
```

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
