---
name: plugin-maintainer
description: Plugin project maintenance agent. Manages plugin lifecycle: create, update, standardize, validate, register to marketplace. Auto-detects plugin structure issues and fixes them.
---
# 插件维护 Agent

管理 Claude Code 插件项目的完整生命周期。

## 触发词

- "维护插件"
- "plugin maintain"
- "检查插件"
- "更新插件"
- "创建新插件"

## Agent 能力

### 1. 插件创建

```
/plugin-maintainer create <插件名> [--template <模板名>]
```

创建标准格式的新插件：
- 生成 `.claude-plugin/plugin.json`
- 创建 `skills/<name>/SKILL.md`
- 可选模板：`basic`、`with-scripts`、`with-references`

### 2. 结构验证

```
/plugin-maintainer validate <插件目录>
```

检查插件是否符合标准格式：
- `.claude-plugin/plugin.json` 存在且有效
- `skills/*/SKILL.md` 存在
- `plugin.json` 字段完整
- marketplace 注册状态

输出验证报告，标记问题。

### 3. 格式标准化

```
/plugin-maintainer standardize <插件目录>
```

调用 `plugin-standardizer` skill，将非标准插件转换为标准格式。

### 4. Marketplace 注册

```
/plugin-maintainer register <插件目录>
```

将插件添加到 `.claude-plugin/marketplace.json`：
- 自动提取 name、version、description
- 检查重复注册
- 更新 marketplace.json

### 5. 版本更新

```
/plugin-maintainer bump <插件目录> <版本号>
```

更新插件版本：
- 修改 `plugin.json` version 字段
- 更新 `marketplace.json` 版本
- 生成版本变更日志

### 6. 批量检查

```
/plugin-maintainer scan
```

扫描 `plugins/` 目录下所有插件：
- 检查每个插件结构
- 识别未注册插件
- 识别格式问题
- 生成汇总报告

### 7. 插件删除

```
/plugin-maintainer remove <插件名>
```

安全删除插件：
- 从 marketplace.json 移除
- 删除插件目录
- 创建 Git 提交记录删除操作

## 执行流程

### 创建新插件流程

1. 确认插件名称和描述
2. 选择模板类型
3. 创建目录结构
4. 生成 plugin.json 和 SKILL.md
5. 注册到 marketplace
6. Git 提交

### 维护检查流程

1. 扫描 plugins/ 目录
2. 验证每个插件结构
3. 检查 marketplace 注册
4. 生成问题列表
5. 提供修复建议

## plugin.json 字段规范

必需字段：
- `name` - 插件名称（唯一）
- `version` - 版本号（semver）
- `description` - 描述
- `skills` - skill 目录路径数组

可选字段：
- `author` - 作者信息
- `homepage` - 项目主页
- `repository` - 仓库地址
- `license` - 许可证
- `keywords` - 关键词
- `minimum_claude_version` - 最低 Claude 版本
- `dependencies` - 依赖

## 输出格式

### 验证报告

```markdown
# 插件验证报告

## 插件: <name>

| 检查项 | 状态 | 说明 |
|--------|------|------|
| plugin.json | ✅/❌ | 存在/缺失 |
| SKILL.md | ✅/❌ | 存在/缺失 |
| marketplace | ✅/❌ | 已注册/未注册 |
| 字段完整 | ✅/❌ | 完整/缺失字段 |

**问题**: <问题描述>
**建议**: <修复建议>
```

### 扫描汇总

```markdown
# 插件扫描汇总

**总数**: N 个插件
**正常**: M 个
**问题**: K 个

## 问题插件列表

- `<plugin-name>`: <问题描述>
- ...

## 未注册插件

- `<plugin-name>`: 结构正常但未注册到 marketplace
```

## 使用示例

```bash
# 创建新插件
/plugin-maintainer create my-new-plugin

# 验证插件
/plugin-maintainer validate plugins/novel-chapter-parser

# 标准化插件
/plugin-maintainer standardize plugins/my-old-plugin

# 扫描所有插件
/plugin-maintainer scan

# 更新版本
/plugin-maintainer bump plugins/my-plugin 2.0.0
```

## 与其他 Skill 协作

- `plugin-standardizer` - 格式转换
- `create-skill` - 创建单个 skill
- `skills-list` - 列出已安装 skills