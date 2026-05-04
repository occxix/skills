---
name: auto-fixer
description: Automatically detect and fix plugin project structure issues. Validates and corrects Skills, Agents, Commands, Hooks, Scripts, Templates, References against Claude Code plugin specifications.
---

# 自动修复器

自动检测并修复插件项目结构问题，确保符合 Claude Code 插件规范。

## 触发词

- "修复插件结构"
- "auto fix"
- "检查并修复"
- "结构异常"
- "auto-fixer"

## 检测与修复范围

### 1. Skills 结构

**检测项**：
| 问题 | 检测方法 | 修复动作 |
|------|----------|----------|
| SKILL.md 位置错误 | 检查根目录是否有 SKILL.md | 移动到 `skills/<name>/SKILL.md` |
| 缺少 frontmatter | 检查文件开头是否有 `---` | 添加 name, description |
| frontmatter 字段缺失 | 检查 name, description | 补充缺失字段 |
| skills/ 目录为空 | 检查目录是否存在且有内容 | 创建默认 SKILL.md |

### 2. Agents 结构

**检测项**：
| 问题 | 检测方法 | 修复动作 |
|------|----------|----------|
| 缺少 tools 字段 | 检查 frontmatter.tools | 添加默认工具集 |
| tools 格式错误 | 检查是否为逗号分隔字符串 | 转换为数组格式 |
| 缺少 description | 检查 frontmatter.description | 从文件内容提取或生成 |
| 文件位置错误 | 检查是否在 agents/ 目录 | 移动到正确位置 |

### 3. Commands 结构

**检测项**：
| 问题 | 检测方法 | 修复动作 |
|------|----------|----------|
| 缺少 description | 检查 frontmatter.description | 添加默认描述 |
| 缺少 allowed-tools | 检查 frontmatter.allowed-tools | 添加安全工具列表 |
| 动态上下文格式错误 | 检查 `!` 命令语法 | 修正格式 |

### 4. Hooks 结构

**检测项**：
| 问题 | 检测方法 | 修复动作 |
|------|----------|----------|
| hooks.json 格式错误 | JSON 解析检查 | 修复 JSON 格式 |
| 缺少事件类型 | 检查必需事件字段 | 添加缺失事件 |
| 脚本路径错误 | 检查脚本文件是否存在 | 创建默认脚本或修正路径 |
| 脚本缺少编码处理 | 检查 Python 脚本编码 | 添加 UTF-8 处理 |

### 5. Scripts 结构

**检测项**：
| 问题 | 检测方法 | 修复动作 |
|------|----------|----------|
| 缺少编码声明 | 检查 `# -*- coding: utf-8 -*-` | 添加编码声明 |
| Windows 编码问题 | 检查 console encoding 处理 | 添加 io.TextIOWrapper |
| 缺少 main 入口 | 检查 `if __name__` | 添加标准入口 |

### 6. Templates 结构

**检测项**：
| 问题 | 检测方法 | 修复动作 |
|------|----------|----------|
| 缺少 frontmatter | 检查文件开头 | 添加 name, type, usage |
| 变量标记格式错误 | 检查 `{{var}}` 格式 | 统一变量格式 |

### 7. References 结构

**检测项**：
| 问题 | 检测方法 | 修复动作 |
|------|----------|----------|
| 缺少 frontmatter | 检查文件开头 | 添加 name, type, tags |
| 缺少类型分类 | 检查 type 字段 | 添加默认类型 |

### 8. plugin.json 结构

**检测项**：
| 问题 | 检测方法 | 修复动作 |
|------|----------|----------|
| 缺少必需字段 | 检查 name, version, description, skills | 补充缺失字段 |
| skills 路径格式错误 | 检查路径格式 | 修正为 `./skills/` |
| version 格式错误 | 检查 semver 格式 | 修正为标准格式 |

### 9. marketplace.json 结构

**检测项**：
| 问题 | 检测方法 | 修复动作 |
|------|----------|----------|
| 插件未注册 | 对比 plugins/ 目录与注册列表 | 添加缺失注册 |
| 注册信息不完整 | 检查 name, source, description, version | 补充字段 |
| source 路径错误 | 检查路径格式 | 修正路径 |

## 执行流程

### 步骤 1: 扫描项目

```bash
# 扫描所有插件目录
ls -la plugins/

# 扫描项目级目录
ls -la agents/ commands/ hooks/ scripts/ templates/ references/
```

### 步骤 2: 检测问题

对每个文件执行结构检测：
1. 读取文件内容
2. 解析 frontmatter（如有）
3. 检查必需字段
4. 检查格式规范
5. 记录问题列表

### 步骤 3: 生成修复计划

输出修复计划：
```markdown
# 自动修复计划

## Skills (2 问题)
- `plugins/xxx/SKILL.md`: 缺少 frontmatter → 添加 name, description
- `plugins/yyy/skills/`: 目录为空 → 创建默认 SKILL.md

## Agents (1 问题)
- `agents/zzz.md`: 缺少 tools → 添加默认工具集

## Hooks (1 问题)
- `hooks/hooks.json`: 格式错误 → 修复 JSON

**总计**: 4 个问题待修复
```

### 步骤 4: 执行修复

按优先级执行修复：
1. **高优先级**: 结构性错误（文件位置、目录缺失）
2. **中优先级**: 格式错误（frontmatter、JSON）
3. **低优先级**: 内容补充（缺少描述、标签）

每个修复：
- 读取原文件
- 应用修复
- 写入修正内容
- Git 暂存变更

### 步骤 5: 提交变更

```bash
git add -A
git commit -m "fix: auto-fix plugin structure issues"
```

### 步骤 6: 输出报告

```markdown
# 自动修复报告

**扫描**: X 个文件
**问题**: Y 个
**修复**: Z 个
**跳过**: W 个（需人工确认）

## 修复详情

| 文件 | 问题 | 修复动作 | 状态 |
|------|------|----------|------|
| xxx/SKILL.md | 缺少 frontmatter | 已添加 | ✅ |
| yyy/plugin.json | 缺少 version | 已添加 1.0.0 | ✅ |

## 待人工确认

- `agents/custom.md`: 内容复杂，建议人工检查
```

## 修复模板

### SKILL.md 默认模板

```markdown
---
name: {{skill-name}}
description: {{从文件第一行提取或默认描述}}
---

# {{skill-name}}

{{原有内容}}
```

### Agent 默认模板

```markdown
---
name: {{agent-name}}
description: {{从文件内容提取}}
tools: Read, Write, Edit, Bash, Glob, Grep
---

{{原有内容}}
```

### plugin.json 默认模板

```json
{
  "name": "{{plugin-name}}",
  "version": "1.0.0",
  "description": "{{从 README 或 SKILL.md 提取}}",
  "skills": "./skills/"
}
```

### hooks.json 默认模板

```json
{
  "description": "{{plugin-name}} hooks",
  "hooks": {
    "PreToolUse": [],
    "PostToolUse": [],
    "Stop": [],
    "SessionStart": []
  }
}
```

## 使用方法

```bash
# 扫描并显示问题（不修复）
/auto-fixer scan

# 自动修复所有问题
/auto-fixer fix

# 修复特定类型
/auto-fixer fix --type skills
/auto-fixer fix --type agents

# 修复特定文件
/auto-fixer fix plugins/xxx/SKILL.md

# 强制修复（跳过确认）
/auto-fixer fix --force
```

## 安全规则

- **不覆盖内容**: 修复只添加缺失部分，不删除现有内容
- **保留注释**: 保留文件中的注释和说明
- **备份原文件**: 修复前 Git 暂存，可回滚
- **跳过复杂文件**: 内容复杂的文件标记为需人工确认
- **不修改代码逻辑**: 只修复结构和格式，不改代码逻辑

## 跳过规则

以下情况跳过自动修复，标记需人工确认：
- 文件内容超过 500 行
- frontmatter 与内容高度耦合
- 自定义结构（非标准插件）
- 用户标记 `# auto-fixer: skip`