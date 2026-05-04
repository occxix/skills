<#
.SYNOPSIS
    Skills Sync - 同步 .agents 到 Git 仓库

.DESCRIPTION
    自动将 .agents 目录推送到 Git 仓库，支持 .env 配置、冲突检测和交互式解决。

.PARAMETER Force
    强制推送，跳过冲突检查

.PARAMETER Status
    仅检查状态，不推送

.PARAMETER Init
    初始化 Git 仓库

.PARAMETER Message
    指定提交信息

.EXAMPLE
    skills-sync.ps1
    skills-sync.ps1 -Force
    skills-sync.ps1 -Status
#>

param(
    [switch]$Force,
    [switch]$Status,
    [switch]$Init,
    [string]$Message
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$WORK_DIR = Join-Path $HOME ".agents"
$AGENTS_DIR = Join-Path $HOME ".agents"
$ENV_FILE = Join-Path $AGENTS_DIR ".env"

$REMOTE_NAME = "origin"
$DEFAULT_BRANCH = "main"
$REMOTE_URL = ""
$SSH_KEY = ""
$USER_NAME = ""
$USER_EMAIL = ""
$COMMIT_PREFIX = "sync skills"
$ForcePush = $Force

function Write-Info { param($msg) Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Success { param($msg) Write-Host "[SUCCESS] $msg" -ForegroundColor Green }
function Write-Warning { param($msg) Write-Host "[WARNING] $msg" -ForegroundColor Yellow }
function Write-Error { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }

function Load-Env {
    if (Test-Path $ENV_FILE) {
        Write-Info "Load config: $ENV_FILE"
        Get-Content $ENV_FILE | ForEach-Object {
            if ($_ -match '^([^#][^=]+)=(.*)$') {
                $key = $Matches[1].Trim()
                $value = $Matches[2].Trim().Trim('"').Trim("'")
                switch ($key) {
                    "GIT_REMOTE_URL" { $script:REMOTE_URL = $value }
                    "GIT_BRANCH" { $script:DEFAULT_BRANCH = $value }
                    "GIT_REMOTE_NAME" { $script:REMOTE_NAME = $value }
                    "GIT_SSH_KEY" { $script:SSH_KEY = $value }
                    "GIT_USER_NAME" { $script:USER_NAME = $value }
                    "GIT_USER_EMAIL" { $script:USER_EMAIL = $value }
                    "GIT_COMMIT_PREFIX" { $script:COMMIT_PREFIX = $value }
                }
            }
        }
    }
}

function Setup-SSH {
    if ($SSH_KEY) {
        $script:SSH_KEY = $SSH_KEY -replace '^~', $HOME
        if (Test-Path $script:SSH_KEY) {
            $content = [System.IO.File]::ReadAllBytes($script:SSH_KEY)
            $hasCRLF = $false
            for ($i = 0; $i -lt $content.Length - 1; $i++) {
                if ($content[$i] -eq 0x0D -and $content[$i + 1] -eq 0x0A) {
                    $hasCRLF = $true
                    break
                }
            }
            if ($hasCRLF) {
                Write-Warning "Converting CRLF to LF..."
                $text = [System.IO.File]::ReadAllText($script:SSH_KEY)
                $text = $text -replace "`r`n", "`n"
                [System.IO.File]::WriteAllText($script:SSH_KEY, $text)
                Write-Info "Fixed line endings: $script:SSH_KEY"
            }
            $env:GIT_SSH_COMMAND = "ssh -i `"$script:SSH_KEY`" -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
            Write-Info "Using SSH key: $script:SSH_KEY"
        } else {
            Write-Warning "SSH key not found: $script:SSH_KEY"
        }
    }
}

function Setup-GitUser {
    Push-Location $AGENTS_DIR
    if ($USER_NAME) { git config user.name $USER_NAME }
    if ($USER_EMAIL) { git config user.email $USER_EMAIL }
    Pop-Location
}

function Initialize-GitRepo {
    Push-Location $AGENTS_DIR
    if (Test-Path ".git") {
        Write-Info "Git repo already exists"
        Pop-Location
        return
    }
    Write-Info "Initializing Git repo..."
    git init
    git checkout -b $DEFAULT_BRANCH 2>$null
    Setup-GitUser
    if ($REMOTE_URL) {
        Write-Info "Adding remote: $REMOTE_URL"
        git remote add $REMOTE_NAME $REMOTE_URL
    } else {
        Write-Warning "Remote URL not configured (GIT_REMOTE_URL)"
    }
    $gitignore = @"
# Only sync .agents directory
/*
!.gitignore
!/.agents/
.agents/.env
.agents/.env.example
.DS_Store
Thumbs.db
*.tmp
*.log
*.bak
"@
    $gitignorePath = Join-Path $WORK_DIR ".gitignore"
    $gitignore | Out-File -FilePath $gitignorePath -Encoding utf8
    Write-Success "Git repo initialized"
    Pop-Location
}

function Test-GitRepo {
    $gitPath = Join-Path $AGENTS_DIR ".git"
    if (-not (Test-Path $gitPath)) {
        Write-Error "$AGENTS_DIR is not a Git repo"
        Write-Host "Run: skills-sync.ps1 -Init"
        return $false
    }
    return $true
}

function Get-CurrentBranch {
    Push-Location $AGENTS_DIR
    $branch = git branch --show-current 2>$null
    if (-not $branch) { $branch = $DEFAULT_BRANCH }
    Pop-Location
    return $branch
}

function Test-Conflicts {
    Push-Location $AGENTS_DIR
    $branch = Get-CurrentBranch
    git fetch $REMOTE_NAME 2>$null
    $remoteBranch = "$REMOTE_NAME/$branch"
    $remoteExists = git rev-parse --verify $remoteBranch 2>$null
    if (-not $remoteExists) {
        Pop-Location
        return $false
    }
    $ahead = git rev-list --count "$remoteBranch..HEAD" 2>$null
    $behind = git rev-list --count "HEAD..$remoteBranch" 2>$null
    Pop-Location
    if ([int]$behind -gt 0 -and [int]$ahead -gt 0) { return $true }
    return $false
}

function Show-ConflictOptions {
    $branch = Get-CurrentBranch
    $remoteBranch = "$REMOTE_NAME/$branch"
    Write-Host ""
    Write-Warning "Conflicts detected: both local and remote have new commits"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  1) Pull and merge (git pull)"
    Write-Host "  2) Rebase (git pull --rebase)"
    Write-Host "  3) Force push (git push --force) [DANGEROUS]"
    Write-Host "  4) Cancel - resolve manually"
    Write-Host "  5) View diff"
    Write-Host ""
    $choice = Read-Host "Select (1-5)"
    Push-Location $AGENTS_DIR
    switch ($choice) {
        "1" {
            Write-Info "Running git pull..."
            git pull $REMOTE_NAME $branch
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Merge successful"
                Pop-Location
                return $true
            }
            Write-Error "Merge failed, resolve conflicts manually"
            Pop-Location
            return $false
        }
        "2" {
            Write-Info "Running git pull --rebase..."
            git pull --rebase $REMOTE_NAME $branch
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Rebase successful"
                Pop-Location
                return $true
            }
            Write-Error "Rebase failed, resolve conflicts manually"
            Pop-Location
            return $false
        }
        "3" {
            Write-Warning "Confirm force push? This will overwrite remote changes!"
            $confirm = Read-Host "Type 'yes' to confirm"
            if ($confirm -eq "yes") {
                $script:ForcePush = $true
                Pop-Location
                return $true
            }
            Write-Info "Cancelled"
            Pop-Location
            return $false
        }
        "4" {
            Write-Info "Cancelled, resolve manually"
            Pop-Location
            return $false
        }
        "5" {
            Write-Host ""
            Write-Info "Local vs Remote diff:"
            Write-Host "=== Remote new commits ==="
            git log "HEAD..$remoteBranch" --oneline 2>$null
            Write-Host ""
            Write-Host "=== Local new commits ==="
            git log "$remoteBranch..HEAD" --oneline 2>$null
            Pop-Location
            return $false
        }
        default {
            Write-Error "Invalid option"
            Pop-Location
            return $false
        }
    }
}

function Show-Status {
    Push-Location $AGENTS_DIR
    Write-Host ""
    Write-Host "=== Git Status ==="
    Write-Host ""
    if (Test-Path $ENV_FILE) {
        Write-Host "Config: $ENV_FILE OK"
    } else {
        Write-Host "Config: ~/.agents/.env not found"
    }
    if ($SSH_KEY) {
        Write-Host "SSH Key: $SSH_KEY"
    }
    Write-Host ""
    $branch = Get-CurrentBranch
    Write-Host "Branch: $branch"
    $remoteUrl = git remote get-url $REMOTE_NAME 2>$null
    Write-Host "Remote: $(if ($remoteUrl) { $remoteUrl } else { 'not configured' })"
    Write-Host ""
    $staged = git diff --cached --stat 2>$null
    $modified = git diff --stat 2>$null
    $untracked = git ls-files --others --exclude-standard 2>$null | Select-Object -First 10
    if ($staged) { Write-Host "Staged:`n$staged`n" }
    if ($modified) { Write-Host "Modified:`n$modified`n" }
    if ($untracked) { Write-Host "Untracked:`n$untracked`n" }
    git fetch $REMOTE_NAME 2>$null
    $remoteBranch = "$REMOTE_NAME/$branch"
    $remoteExists = git rev-parse --verify $remoteBranch 2>$null
    if ($remoteExists) {
        $ahead = git rev-list --count "$remoteBranch..HEAD" 2>$null
        $behind = git rev-list --count "HEAD..$remoteBranch" 2>$null
        Write-Host "Ahead: $ahead commits"
        Write-Host "Behind: $behind commits"
        if ([int]$behind -gt 0 -and [int]$ahead -gt 0) {
            Write-Warning "Status: CONFLICT (both local and remote have new commits)"
        } elseif ([int]$ahead -gt 0) {
            Write-Success "Status: Ready to push"
        } elseif ([int]$behind -gt 0) {
            Write-Info "Status: Need to pull first"
        } else {
            Write-Success "Status: Synced"
        }
    } else {
        Write-Info "Status: Remote branch not found, first push"
    }
    Pop-Location
}

function Sync-ToRemote {
    Push-Location $AGENTS_DIR
    $branch = Get-CurrentBranch
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $commitMsg = if ($Message) { $Message } else { "$COMMIT_PREFIX - $timestamp" }
    $status = git status --porcelain 2>$null
    if (-not $status) {
        Write-Info "No changes to commit"
    } else {
        Write-Info "Staging changes..."
        git add -A
        Write-Info "Committing..."
        git commit -m $commitMsg
    }
    if (-not $ForcePush) {
        if (Test-Conflicts) {
            if (-not (Show-ConflictOptions)) {
                Pop-Location
                return
            }
        }
    }
    Write-Info "Pushing to $REMOTE_NAME/$branch ..."
    if ($ForcePush) {
        git push --force $REMOTE_NAME $branch 2>&1
    } else {
        git push $REMOTE_NAME $branch 2>&1
    }
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Push successful"
    } else {
        Write-Error "Push failed"
    }
    Pop-Location
}

# Main
Load-Env
Setup-SSH

if ($Init) {
    Initialize-GitRepo
    exit 0
}

if (-not (Test-GitRepo)) {
    exit 1
}

Setup-GitUser

if ($Status) {
    Show-Status
} else {
    Sync-ToRemote
}
