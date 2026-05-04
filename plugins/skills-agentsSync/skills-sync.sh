#!/bin/bash

# Skills Sync - 自动同步 .agents 到 Git 仓库
# 功能：自动拉取 + 推送，冲突时询问用户
# 兼容：Linux, macOS, Windows (Git Bash / MSYS2 / Cygwin)

# Git 工作目录（.git 在 ~/.agents）
WORK_DIR="$HOME/.agents"
AGENTS_DIR="$HOME/.agents"
ENV_FILE="$HOME/.env"

REMOTE_NAME="origin"
DEFAULT_BRANCH="master"
GIT_REMOTE_URL=""
GIT_SSH_KEY=""
GIT_USER_NAME=""
GIT_USER_EMAIL=""
GIT_COMMIT_PREFIX="sync skills"

detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "linux";;
        Darwin*)    echo "macos";;
        CYGWIN*|MINGW*|MSYS*|MSYS2*)    echo "windows";;
        *)          echo "unknown";;
    esac
}

OS=$(detect_os)

# Windows 下检测 Git Bash 环境
is_git_bash() {
    if [ "$OS" = "windows" ] && [ -n "$MSYSTEM" ]; then
        return 0
    fi
    return 1
}

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Windows 下颜色可能不支持
if is_git_bash; then
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    CYAN=''
    NC=''
fi

log_info() { printf '%b\n' "${BLUE}[INFO]${NC} $1"; }
log_success() { printf '%b\n' "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { printf '%b\n' "${YELLOW}[WARNING]${NC} $1"; }
log_error() { printf '%b\n' "${RED}[ERROR]${NC} $1"; }
log_step() { printf '%b\n' "${CYAN}[STEP]${NC} $1"; }

load_env() {
    # 优先从 settings.json 的 env 字段读取
    local settings_file="$HOME/.claude/settings.json"
    if [ -f "$settings_file" ]; then
        log_info "加载配置: $settings_file"
        # 解析 JSON 中的 env 字段
        if command -v python3 &>/dev/null; then
            eval "$(python3 -c '
import json
import os
import sys
settings_path = os.path.expanduser(sys.argv[1])
try:
    with open(settings_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    env = data.get("env", {})
    for k, v in env.items():
        if k.startswith("GIT_") or k in ["GIT_SSH_KEY", "GIT_BRANCH", "GIT_REMOTE_NAME", "GIT_COMMIT_PREFIX", "GIT_USER_NAME", "GIT_USER_EMAIL"]:
            escaped = v.replace("\"", "\\\"").replace("$", "\\$").replace("`", "\\`")
            print(f"export {k}=\"{escaped}\"")
except Exception as e:
    pass
' "$settings_file" 2>/dev/null)"
        elif command -v python &>/dev/null; then
            eval "$(python -c '
import json
import os
import sys
settings_path = os.path.expanduser(sys.argv[1])
try:
    with open(settings_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    env = data.get("env", {})
    for k, v in env.items():
        if k.startswith("GIT_") or k in ["GIT_SSH_KEY", "GIT_BRANCH", "GIT_REMOTE_NAME", "GIT_COMMIT_PREFIX", "GIT_USER_NAME", "GIT_USER_EMAIL"]:
            escaped = v.replace("\"", "\\\"").replace("$", "\\$").replace("`", "\\`")
            print(f"export {k}=\"{escaped}\"")
except Exception as e:
    pass
' "$settings_file" 2>/dev/null)"
        fi
    fi

    # 兼容旧的 .env 文件
    if [ -f "$ENV_FILE" ]; then
        log_info "加载配置: $ENV_FILE"
        # 去除 BOM 并读取配置
        while IFS='=' read -r key value || [ -n "$key" ]; do
            # 跳过注释和空行
            case "$key" in
                ''|\#*) continue ;;
            esac
            # 去除 Windows CR 和引号
            value="${value//$'\r'/}"
            value="${value%\"}"
            value="${value#\"}"
            value="${value%\'}"
            value="${value#\'}"
            # 导出变量（不覆盖已有的）
            [ -z "${!key}" ] && export "$key=$value"
        done < <(sed '1s/^\xEF\xBB\xBF//' "$ENV_FILE")
    fi

    # 应用配置
    [ -n "$GIT_REMOTE_URL" ] && REMOTE_URL="$GIT_REMOTE_URL"
    [ -n "$GIT_BRANCH" ] && DEFAULT_BRANCH="$GIT_BRANCH"
    [ -n "$GIT_REMOTE_NAME" ] && REMOTE_NAME="$GIT_REMOTE_NAME"
    [ -n "$GIT_SSH_KEY" ] && SSH_KEY="$GIT_SSH_KEY"
    [ -n "$GIT_USER_NAME" ] && USER_NAME="$GIT_USER_NAME"
    [ -n "$GIT_USER_EMAIL" ] && USER_EMAIL="$GIT_USER_EMAIL"
    [ -n "$GIT_COMMIT_PREFIX" ] && COMMIT_PREFIX="$GIT_COMMIT_PREFIX"
}

# 修复 SSH 密钥问题
fix_ssh_key() {
    if [ -n "$SSH_KEY" ]; then
        # 展开 ~ 路径
        SSH_KEY="${SSH_KEY/#\~/$HOME}"
        # Windows 下转换路径
        if is_git_bash; then
            SSH_KEY=$(cygpath -u "$SSH_KEY" 2>/dev/null || echo "$SSH_KEY")
        fi

        if [ -f "$SSH_KEY" ]; then
            # 检测并修复 CRLF 和非法换行符
            local key_lines=$(wc -l < "$SSH_KEY" 2>/dev/null || echo "1")
            local has_crlf=false

            # 检测 CRLF
            if grep -q $'\r' "$SSH_KEY" 2>/dev/null; then
                has_crlf=true
            fi

            # SSH 私钥应该是单行 base64，Windows 复制/编辑会导致断行
            if [ "$key_lines" -gt 2 ] || [ "$has_crlf" = true ]; then
                log_warn "SSH 密钥包含非法换行符，自动修复..."

                # 提取 base64 内容并去除所有换行和回车
                local key_content=$(cat "$SSH_KEY")
                local fixed_content=$(echo "$key_content" | grep -v "BEGIN\|END" | tr -d '\n\r')

                # 重新组装密钥
                {
                    echo "-----BEGIN OPENSSH PRIVATE KEY-----"
                    echo "$fixed_content"
                    echo "-----END OPENSSH PRIVATE KEY-----"
                } > "$SSH_KEY"

                log_info "已修复 SSH 密钥"
            fi

            # 设置权限（Windows Git Bash 需要）
            if is_git_bash; then
                chmod 600 "$SSH_KEY" 2>/dev/null
            else
                chmod 600 "$SSH_KEY"
            fi

            export GIT_SSH_COMMAND="ssh -i \"$SSH_KEY\" -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
            log_info "使用 SSH 密钥: $SSH_KEY"
        else
            log_warn "SSH 密钥不存在: $SSH_KEY"
        fi
    fi
}

setup_git_user() {
    if [ -n "$USER_NAME" ]; then
        git config user.name "$USER_NAME"
    fi
    if [ -n "$USER_EMAIL" ]; then
        git config user.email "$USER_EMAIL"
    fi
}

init_git_repo() {
    cd "$AGENTS_DIR" || exit 1

    if [ -d ".git" ]; then
        log_info "Git 仓库已存在"
        return 0
    fi

    log_info "初始化 Git 仓库..."
    git init
    git checkout -b "$DEFAULT_BRANCH" 2>/dev/null || git checkout "$DEFAULT_BRANCH"
    setup_git_user

    if [ -n "$REMOTE_URL" ]; then
        log_info "添加远程仓库: $REMOTE_URL"
        git remote add "$REMOTE_NAME" "$REMOTE_URL"
    fi

    log_success "Git 仓库初始化完成"
}

check_git_repo() {
    if [ ! -d "$WORK_DIR/.git" ]; then
        log_error "$WORK_DIR 不是 Git 仓库"
        echo "请先初始化: skills-sync --init"
        return 1
    fi
    return 0
}

get_current_branch() {
    cd "$AGENTS_DIR" || echo "$DEFAULT_BRANCH"
    git branch --show-current 2>/dev/null || echo "$DEFAULT_BRANCH"
}

# 询问用户冲突处理方式
ask_merge_strategy() {
    local branch=$(get_current_branch)

    echo ""
    log_warn "检测到冲突：远程和本地都有新提交"
    echo ""
    echo "请选择处理方案："
    echo ""
    echo "  1) 拉取并合并 (git pull) - 保留双方更改 [推荐]"
    echo "  2) 变基 (git pull --rebase) - 将本地提交放在远程之上"
    echo "  3) 强制推送 (git push --force) - 覆盖远程 [危险]"
    echo "  4) 查看差异 - 对比本地和远程后再选择"
    echo ""
    read -p "请输入选项 (1-4): " choice

    case $choice in
        1)
            log_info "执行 git pull --no-rebase --allow-unrelated-histories..."
            git pull --no-rebase --allow-unrelated-histories "$REMOTE_NAME" "$branch"
            ;;
        2)
            log_info "执行 git pull --rebase..."
            git pull --rebase "$REMOTE_NAME" "$branch"
            ;;
        3)
            log_warn "确认强制推送？输入 'yes' 确认: "
            read -p "> " confirm
            if [ "$confirm" = "yes" ]; then
                git push --force "$REMOTE_NAME" "$branch"
                return $?
            else
                log_info "已取消"
                return 1
            fi
            ;;
        4)
            echo ""
            log_info "=== 远程提交 ==="
            git log HEAD.."$REMOTE_NAME/$branch" --oneline 2>/dev/null || echo "无"
            echo ""
            log_info "=== 本地提交 ==="
            git log "$REMOTE_NAME/$branch"..HEAD --oneline 2>/dev/null || echo "无"
            echo ""
            return ask_merge_strategy
            ;;
        *)
            log_error "无效选项"
            return 1
            ;;
    esac
    return $?
}

# 自动拉取远程更改
auto_pull() {
    cd "$AGENTS_DIR" || return 1
    local branch=$(get_current_branch)
    local remote_branch="$REMOTE_NAME/$branch"

    # 检查远程分支是否存在
    if ! git rev-parse --verify "$remote_branch" >/dev/null 2>&1; then
        log_info "远程分支不存在，无需拉取"
        return 0
    fi

    # 检查是否有本地未提交的更改
    local has_local_changes=false
    if [ -n "$(git status --porcelain)" ]; then
        has_local_changes=true
        log_info "本地有未提交的更改，先暂存..."
        git add -A
        git stash push -m "skills-sync auto-stash before pull" 2>/dev/null
    fi

    # 检查远程是否有新提交
    git fetch "$REMOTE_NAME" 2>/dev/null
    local behind=$(git rev-list --count HEAD.."$remote_branch" 2>/dev/null || echo "0")

    if [ "$behind" -gt 0 ]; then
        log_info "远程有新提交 (${behind} 个)，自动拉取..."

        # 尝试变基拉取
        if git pull --rebase "$REMOTE_NAME" "$branch" 2>&1; then
            log_success "拉取变基成功"
        else
            # 变基失败，尝试合并
            log_warn "变基失败，尝试合并..."
            if git pull --no-rebase --allow-unrelated-histories "$REMOTE_NAME" "$branch" 2>&1; then
                log_success "合并成功"
            else
                # 合并失败，恢复 stash
                if [ "$has_local_changes" = true ]; then
                    git stash pop 2>/dev/null
                fi
                log_error "拉取失败，请手动解决冲突"
                return 1
            fi
        fi
    fi

    # 恢复 stash 的更改
    if [ "$has_local_changes" = true ]; then
        log_info "恢复本地更改..."
        git stash pop 2>/dev/null
    fi

    return 0
}

show_status() {
    cd "$AGENTS_DIR" || exit 1

    echo ""
    echo "=== Git 状态 ==="
    echo ""

    local settings_file="$HOME/.claude/settings.json"
    local has_settings=false
    if [ -f "$settings_file" ]; then
        has_settings=true
    fi

    if [ -f "$ENV_FILE" ]; then
        echo "配置文件: $ENV_FILE ✓"
    elif [ "$has_settings" = true ]; then
        echo "配置文件: $settings_file ✓"
    else
        echo "配置文件: 未找到"
    fi

    echo "平台: $OS"
    if is_git_bash; then
        echo "环境: Git Bash (Windows)"
    fi
    echo ""

    local branch=$(get_current_branch)
    echo "当前分支: $branch"
    echo "远程仓库: $(git remote get-url "$REMOTE_NAME" 2>/dev/null || echo '未配置')"
    echo ""

    git fetch "$REMOTE_NAME" 2>/dev/null
    local remote_branch="$REMOTE_NAME/$branch"

    if git rev-parse --verify "$remote_branch" >/dev/null 2>&1; then
        local ahead=$(git rev-list --count "$remote_branch"..HEAD 2>/dev/null || echo "0")
        local behind=$(git rev-list --count HEAD.."$remote_branch" 2>/dev/null || echo "0")

        echo "与远程的关系:"
        echo "  本地领先: $ahead 个提交"
        echo "  本地落后: $behind 个提交"

        if [ "$behind" -gt 0 ] && [ "$ahead" -gt 0 ]; then
            echo ""
            log_warn "状态: 存在冲突，需要合并"
        elif [ "$ahead" -gt 0 ]; then
            echo ""
            log_success "状态: 可以推送"
        elif [ "$behind" -gt 0 ]; then
            echo ""
            log_info "状态: 需要拉取"
        else
            echo ""
            log_success "状态: 已同步"
        fi
    else
        echo ""
        log_info "状态: 远程分支不存在"
    fi
}

# 主同步函数
sync_to_remote() {
    cd "$AGENTS_DIR" || exit 1

    local branch=$(get_current_branch)
    local commit_msg="${COMMIT_MSG:-$COMMIT_PREFIX - $(date '+%Y-%m-%d %H:%M')}"

    log_step "1/3 检查本地更改..."
    if [ -z "$(git status --porcelain)" ]; then
        log_info "没有需要提交的更改"
    else
        log_info "提交本地更改..."
        git add -A
        git commit -m "$commit_msg"
        log_success "已提交"
    fi

    log_step "2/3 自动拉取远程更改..."
    if ! auto_pull; then
        log_error "拉取失败，尝试解决冲突..."
        if ! ask_merge_strategy; then
            return 1
        fi
    fi

    log_step "3/3 推送到远程..."
    if git push "$REMOTE_NAME" "$branch" 2>&1; then
        log_success "推送成功"
    else
        log_warn "推送被拒绝，可能有冲突"
        if ask_merge_strategy; then
            log_info "重新推送..."
            git push "$REMOTE_NAME" "$branch"
        else
            return 1
        fi
    fi

    return 0
}

# 参数解析
PULL_ONLY=false
STATUS_ONLY=false
INIT_REPO=false
COMMIT_MSG=""

while [ $# -gt 0 ]; do
    case "$1" in
        --pull)
            PULL_ONLY=true
            ;;
        --force)
            cd "$AGENTS_DIR" && git push --force "$REMOTE_NAME" "$(get_current_branch)"
            exit $?
            ;;
        --status)
            STATUS_ONLY=true
            ;;
        --init)
            INIT_REPO=true
            ;;
        -m|--message)
            shift
            COMMIT_MSG="$1"
            ;;
        -h|--help)
            echo "用法: skills-sync [选项]"
            echo ""
            echo "选项:"
            echo "  --pull        仅拉取"
            echo "  --force       强制推送"
            echo "  --status      仅显示状态"
            echo "  --init        初始化仓库"
            echo "  -m <消息>     指定提交信息"
            echo "  -h            显示帮助"
            echo ""
            echo "配置文件: ~/.env"
            echo ""
            echo "支持平台: Linux, macOS, Windows (Git Bash / MSYS2 / Cygwin)"
            exit 0
            ;;
    esac
    shift
done

# 主流程
load_env
fix_ssh_key

if [ "$INIT_REPO" = "true" ]; then
    init_git_repo
    exit 0
fi

if ! check_git_repo; then
    exit 1
fi

setup_git_user

if [ "$STATUS_ONLY" = "true" ]; then
    show_status
elif [ "$PULL_ONLY" = "true" ]; then
    auto_pull
else
    sync_to_remote
fi
