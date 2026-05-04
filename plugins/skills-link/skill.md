---
name: skills-link
description: "自动发现并整理本地 skill 目录为符号链接。先预览计划，用户确认后再执行。"
metadata:
  short-description: 统一管理本地 skill 目录，链接到 .agents/skills
---

# Skills Link

自动发现并整理用户目录下所有工具的 skills 目录，先预览计划，用户确认后再执行。

## 用法

```bash
# 预览模式（默认）：显示操作计划，不执行
skills-link

# 执行模式：用户确认后执行
skills-link --execute
```

## 工作流

### 预览阶段（默认）

1. 扫描 `~/` 下 maxdepth=3 的所有 `skills` 目录
2. 分类每个目录的处理方式
3. 输出结构化操作计划（含操作类型、源、目标）
4. **等待用户确认**
5. 按计划执行（失败时停止并报告）

### 排除规则

- `*/.agents/*` 下的 skills → 跳过
- `~/.hermes/hermes-agent/skills` → 跳过
- 已是符号链接的目录 → 跳过
- 不存在的目录 → 跳过

### 链接规则

| 目录 | 目标 |
|------|------|
| `~/.hermes/skills` | `~/.agents/.hermes/skills`（独立存储） |
| `~/.hermes/skills/agentsSkills` | `~/.agents/skills`（统一存储） |
| 其他 skills | `~/.agents/skills`（统一存储） |

### 操作类型

- **COPY**: 复制目录内容到目标
- **DELETE**: 删除空目录
- **LINK**: 创建符号链接

## 执行脚本

```bash
#!/bin/bash

# Skills Link - 自动发现并整理 skills 目录到统一存储
# 用法: skills-link [--execute]
# 支持: Linux, macOS, Windows (Git Bash)

TARGET_DIR="$HOME/.agents/skills"
EXECUTE=false

# 解析参数
if [[ "$1" == "--execute" ]]; then
    EXECUTE=true
fi

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "linux" ;;
        Darwin*)    echo "macos" ;;
        CYGWIN*|MINGW*|MSYS*) echo "windows" ;;
        *)          echo "unknown" ;;
    esac
}

OS=$(detect_os)

mkdir -p "$TARGET_DIR"

# 创建符号链接
create_link() {
    local source="$1"
    local target="$2"
    case "$OS" in
        windows)
            local source_win=$(cygpath -w "$source" 2>/dev/null || echo "$source")
            local target_win=$(cygpath -w "$target" 2>/dev/null || echo "$target")
            powershell -Command "New-Item -ItemType Junction -Path '$source_win' -Target '$target_win' -Force" > /dev/null 2>&1 ;;
        linux|macos)
            ln -sfn "$target" "$source" ;;
        *)
            echo "  [错误] 不支持的系统: $OS" && return 1 ;;
    esac
}

# 转换为绝对路径
to_abs() {
    local path="$1"
    if [[ "$path" == /* ]]; then echo "$path"
    else echo "$(cd "$(dirname "$path")" 2>/dev/null && pwd)/$(basename "$path")"; fi
}

# 获取非链接真实目录的技能数量
count_skills() {
    if [ -d "$1" ] && [ ! -L "$1" ]; then
        ls "$1" 2>/dev/null | wc -l | tr -d ' '
    else
        echo "0"
    fi
}

# 预览单个目录，返回计划项
plan_one() {
    local dir="$1"
    local source_abs
    source_abs=$(to_abs "$dir")

    # 已是链接
    if [ -L "$dir" ]; then
        return
    fi

    # 不存在
    if [ ! -d "$dir" ]; then
        return
    fi

    # 排除：.agents 下
    if [[ "$dir" == *"/.agents/"* ]]; then
        return
    fi

    # 排除：hermes-agent
    if [[ "$dir" == "$HOME/.hermes/hermes-agent/skills" ]]; then
        return
    fi

    # hermes/skills/agentsSkills 特殊处理：链接到统一存储
    if [[ "$dir" == "$HOME/.hermes/skills/agentsSkills" ]]; then
        local target="$HOME/.agents/skills"
        if [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
            echo "DELETE|$dir|空目录"
            echo "LINK|$dir|$target"
        else
            local cnt
            cnt=$(count_skills "$dir")
            echo "COPY|$dir|$target|$cnt|迁移到统一存储"
            echo "DELETE|$dir|迁移后删除"
            echo "LINK|$dir|$target|创建链接"
        fi
        return
    fi

    # hermes/skills 特殊处理：链接到独立存储
    if [[ "$dir" == "$HOME/.hermes/skills" ]]; then
        local target="$HOME/.agents/.hermes/skills"
        mkdir -p "$target"
        if [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
            echo "DELETE|$dir|空目录"
            echo "LINK|$dir|$target"
        else
            local cnt
            cnt=$(count_skills "$dir")
            echo "COPY|$dir|$target|$cnt|迁移到独立存储"
            echo "DELETE|$dir|迁移后删除"
            echo "LINK|$dir|$target|创建链接"
        fi
        return
    fi

    # 其他目录：统一迁移
    if [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
        echo "DELETE|$dir|空目录"
        echo "LINK|$dir|$TARGET_DIR"
    else
        local cnt
        cnt=$(count_skills "$dir")
        echo "COPY|$dir|$TARGET_DIR|$cnt|迁移到统一存储"
        echo "DELETE|$dir|迁移后删除"
        echo "LINK|$dir|$TARGET_DIR|创建链接"
    fi
}

# 执行单个操作
do_op() {
    local op="$1"
    local src="$2"
    local tgt="$3"
    local msg="$4"

    case "$op" in
        COPY)
            mkdir -p "$tgt"
            if cp -r "$src"/* "$tgt/" 2>/dev/null; then
                echo "  ✓ COPY $src -> $tgt"
            else
                echo "  ✗ COPY 失败: $src"
                return 1
            fi ;;
        DELETE)
            if [ -d "$src" ]; then
                rm -rf "$src" && echo "  ✓ DELETE $src" || echo "  ✗ DELETE 失败: $src"
            fi ;;
        LINK)
            if create_link "$src" "$tgt"; then
                echo "  ✓ LINK $src -> $tgt"
            else
                echo "  ✗ LINK 失败: $src"
                return 1
            fi ;;
    esac
}

# 主流程
main() {
    echo "=== Skills Link - 操作计划预览 ==="
    echo "目标: $TARGET_DIR"
    echo "系统: $OS"
    echo ""

    if ! $EXECUTE; then
        echo "【预览模式】添加 --execute 参数开始执行"
        echo ""
    else
        echo "【执行模式】"
        echo ""
    fi

    local total_ops=0
    local plans=()

    # 扫描并生成计划
    while IFS= read -r dir; do
        while IFS= read -r line; do
            if [ -n "$line" ]; then
                plans+=("$line")
                ((total_ops++)) || true
            fi
        done < <(plan_one "$dir")
    done < <(find "$HOME" -maxdepth 3 -type d -name "skills" 2>/dev/null)

    if [ $total_ops -eq 0 ]; then
        echo "未发现需要处理的 skills 目录。"
        exit 0
    fi

    # 输出计划
    echo "┌─────────────────────────────────────────────────────────────┐"
    echo "│ 操作计划 ($total_ops 项)                                       │"
    echo "├─────────────────────────────────────────────────────────────┤"
    while IFS='|' read -r op src tgt msg; do
        printf "│ %-6s │ %-30s │ %s\n" "$op" "$(basename "$src")" "$msg"
    done <<< "$(printf '%s\n' "${plans[@]}")"
    echo "└─────────────────────────────────────────────────────────────┘"
    echo ""

    if ! $EXECUTE; then
        echo "输入 skills-link --execute 确认执行。"
        exit 0
    fi

    # 确认
    echo -n "确认执行以上 $total_ops 项操作？(y/N): "
    read -r confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        echo "已取消。"
        exit 0
    fi

    # 执行
    echo ""
    echo "=== 执行中 ==="
    local failed=0
    for plan in "${plans[@]}"; do
        IFS='|' read -r op src tgt msg <<< "$plan"
        if ! do_op "$op" "$src" "$tgt" "$msg"; then
            ((failed++)) || true
            echo "  停止于: $op $src"
            break
        fi
    done

    echo ""
    if [ $failed -eq 0 ]; then
        echo "=== 完成 ==="
        local cnt
        cnt=$(ls "$TARGET_DIR" 2>/dev/null | wc -l | tr -d ' ')
        echo "统一存储: $TARGET_DIR ($cnt 个 skills)"
    else
        echo "执行失败: $failed 项"
        exit 1
    fi
}

main
```

## 示例输出（预览模式）

```
=== Skills Link - 操作计划预览 ===
目标: /home/user/.agents/skills
系统: linux

【预览模式】添加 --execute 参数开始执行

┌─────────────────────────────────────────────────────────────┐
│ 操作计划 (9 项)                                             │
├─────────────────────────────────────────────────────────────┤
│ COPY   │ .claude/skills             │ 迁移到统一存储         │
│ DELETE │ .claude/skills             │ 迁移后删除             │
│ LINK   │ .claude/skills             │ 创建链接              │
│ COPY   │ .hermes/skills             │ 迁移到独立存储         │
│ DELETE │ .hermes/skills             │ 迁移后删除             │
│ LINK   │ .hermes/skills             │ 创建链接              │
│ DELETE │ .hermes/hermes-agent/skills│ 空目录                │
│ DELETE │ .codex/skills              │ 空目录                │
│ LINK   │ .codex/skills              │ 创建链接              │
└─────────────────────────────────────────────────────────────┘

输入 skills-link --execute 确认执行。
```
