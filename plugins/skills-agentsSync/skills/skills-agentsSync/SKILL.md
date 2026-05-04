---
name: skills-agentsSync
description: |
  同步 `~/.agents` 目录到 Git 仓库。触发词：同步技能、sync agents、推送 skills、拉取已发布的技能更新。
  自动使用 settings.json 中的环境变量（GIT_SSH_KEY、GIT_BRANCH 等）。
  支持 --force 强制推送、--status 查看状态、--pull 仅拉取。
  **破坏性操作（提交/拉取/推送/冲突解决）前必须先预览变更，用户确认后才执行。**
---

# Skills Sync

自动将 `~/.agents` 目录同步到 Git 仓库。

**工作目录**: `$HOME/.agents`（整个 .agents 目录，包含 skills、.hermes/skills 等子目录）

## Scope

Use this skill for git synchronization only.

Do not use it to repair skill metadata, normalize `SKILL.md`, or decide which skill should exist. That is `skills-organizer`'s job.

## 环境变量（在 settings.json 中配置）

| 变量 | 必填 | 说明 |
|------|------|------|
| `GIT_SSH_KEY` | 是 | SSH 私钥路径 |
| `GIT_BRANCH` | 否 | 默认分支，默认 `master` |
| `GIT_REMOTE_NAME` | 否 | 远程名称，默认 `origin` |
| `GIT_COMMIT_PREFIX` | 否 | 提交信息前缀 |

**配置读取优先级**：
1. Claude Code 环境：直接读取 `$GIT_SSH_KEY` 环境变量
2. 其他环境：读取 `C:\Users\hlr\.claude\settings.json` 中 `env.GIT_SSH_KEY`

## 用法

```
/skills-sync          # 自动同步（提交 + 拉取 + 推送）
/skills-sync --force  # 强制推送
/skills-sync --status # 查看状态
/skills-sync --pull   # 仅拉取
```

## 执行流程

1. **配置 SSH 密钥** - 使用 `$GIT_SSH_KEY` 设置 `GIT_SSH_COMMAND`
2. **检查本地更改** - 扫描 untracked 和 modified 文件，过滤插件缓存子模块
3. **预览变更** - 执行任何破坏性操作前，先展示 diff/变更摘要
4. **确认后执行** - 用户确认后才执行提交/拉取/推送/冲突解决
5. **推送到远程** - 推送到 `$GIT_BRANCH` 分支

## 预览规则（强制）

**所有以下操作必须先预览，用户确认后才能执行：**

| 操作 | 预览内容 |
|------|----------|
| 自动提交 | `git diff --cached` + 提交信息 |
| 变基/合并拉取 | `git log --oneline HEAD..origin/master`（远程新提交）+ `git log --oneline origin/master..HEAD`（本地新提交）|
| 普通推送 | `git log --oneline origin/master..HEAD` |
| 强制推送 | diff + 明确警告 |
| 冲突解决 | 冲突文件列表 + 各方变更摘要 |

**预览格式示例：**
```
即将推送 2 个提交：
  abc1234 fix: add error handling
  def5678 feat: new skill xyz

Diff 摘要：
+ 10 files changed, +200 lines, -5 lines

[确认推送? y/n]
```

## 冲突处理

检测到冲突时，先展示冲突文件列表和各方变更，再提供交互选项：

| 选项 | 命令 | 说明 |
|------|------|------|
| 1 | git pull --no-rebase | 合并，保留双方历史 [推荐] |
| 2 | git pull --rebase | 变基，线性历史 |
| 3 | git push --force | 强制覆盖 [危险] |
| 4 | 查看差异 | 对比后再选择 |

**冲突前预览：** 展示远程与本地各自的提交，冲突文件 diff，用户确认后才执行合并/变基。

## 注意事项

- 环境变量从 `settings.json` 的 `env` 字段加载，无需 `.env` 文件
- SSH 密钥自动修复换行符问题和权限
- 强制推送需要额外确认（两次确认）
