# AI Team Skills - Windows PowerShell Installer
# Installs AI Team Skills for Claude, Cursor, Windsurf, Trae, Codex CLI, and VS Code on Windows

$ErrorActionPreference = "Stop"

Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "         🤖 AI Team Skills - Windows Installer              " -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$TargetDir = $PWD.Path

# Copy all brain templates (json, toml, md) into the target brain dir
function Copy-Brain {
    param([string]$DestBrain)
    New-Item -ItemType Directory -Force -Path $DestBrain | Out-Null
    if (Test-Path (Join-Path $ScriptDir "src\ai-team\brain")) {
        Copy-Item -Path (Join-Path $ScriptDir "src\ai-team\brain\*.*") -Destination $DestBrain -Force -ErrorAction SilentlyContinue
    }
}

# Detect Platform
function Detect-Platform {
    if (Test-Path "$env:USERPROFILE\.claude") { return "claude" }
    if (Test-Path "$env:USERPROFILE\.cursor") { return "cursor" }
    if (Test-Path "$env:USERPROFILE\.windsurf") { return "windsurf" }
    if (Test-Path "$env:USERPROFILE\.trae") { return "trae" }
    if (Get-Command codex -ErrorAction SilentlyContinue) { return "codex" }
    if ((Test-Path "$env:USERPROFILE\.gemini") -or (Get-Command gemini -ErrorAction SilentlyContinue)) { return "gemini" }
    if (Get-Command code -ErrorAction SilentlyContinue) { return "vscode" }
    return "generic"
}

# Install Claude Code
function Install-Claude {
    Write-Host "📦 Installing for Claude Code..." -ForegroundColor Green
    $destSkills = Join-Path $TargetDir ".claude\skills"
    New-Item -ItemType Directory -Force -Path $destSkills | Out-Null

    Copy-Item -Path (Join-Path $ScriptDir ".claude\skills\*.md") -Destination $destSkills -Force
    Copy-Item -Path (Join-Path $ScriptDir "CLAUDE.md") -Destination $TargetDir -Force

    Copy-Brain (Join-Path $TargetDir ".ai-team\brain")
    Write-Host "✅ Claude Code installed!" -ForegroundColor Green
}

# Install Cursor
function Install-Cursor {
    Write-Host "📦 Installing for Cursor..." -ForegroundColor Green
    $destSkills = Join-Path $TargetDir ".cursor\skills"
    New-Item -ItemType Directory -Force -Path $destSkills | Out-Null

    Copy-Item -Path (Join-Path $ScriptDir ".claude\skills\*.md") -Destination $destSkills -Force
    Copy-Item -Path (Join-Path $ScriptDir ".cursorrules") -Destination $TargetDir -Force
    $cursorRules = Join-Path $TargetDir ".cursor\rules"
    New-Item -ItemType Directory -Force -Path $cursorRules | Out-Null
    Copy-Item -Path (Join-Path $ScriptDir ".cursor\rules\ai-team.mdc") -Destination $cursorRules -Force

    Copy-Brain (Join-Path $TargetDir ".ai-team\brain")
    Write-Host "✅ Cursor installed!" -ForegroundColor Green
}

# Install Windsurf
function Install-Windsurf {
    Write-Host "📦 Installing for Windsurf..." -ForegroundColor Green
    $destSkills = Join-Path $TargetDir ".windsurf\skills"
    New-Item -ItemType Directory -Force -Path $destSkills | Out-Null

    Copy-Item -Path (Join-Path $ScriptDir ".claude\skills\*.md") -Destination $destSkills -Force
    Copy-Item -Path (Join-Path $ScriptDir ".windsurfrules") -Destination $TargetDir -Force
    $windsurfRules = Join-Path $TargetDir ".windsurf\rules"
    New-Item -ItemType Directory -Force -Path $windsurfRules | Out-Null
    Copy-Item -Path (Join-Path $ScriptDir ".windsurf\rules\ai-team.md") -Destination $windsurfRules -Force

    Copy-Brain (Join-Path $TargetDir ".ai-team\brain")
    Write-Host "✅ Windsurf installed!" -ForegroundColor Green
}

# Install Trae IDE
function Install-Trae {
    Write-Host "📦 Installing for Trae IDE..." -ForegroundColor Green
    $destRules = Join-Path $TargetDir ".trae\rules"
    New-Item -ItemType Directory -Force -Path $destRules | Out-Null

    Copy-Item -Path (Join-Path $ScriptDir ".trae\rules\ai-team.md") -Destination $destRules -Force

    Copy-Brain (Join-Path $TargetDir ".ai-team\brain")
    Write-Host "✅ Trae IDE installed!" -ForegroundColor Green
}

# Install OpenAI Codex CLI
function Install-Codex {
    Write-Host "📦 Installing for OpenAI Codex CLI..." -ForegroundColor Green
    Copy-Item -Path (Join-Path $ScriptDir "AGENTS.md") -Destination $TargetDir -Force

    Copy-Brain (Join-Path $TargetDir ".ai-team\brain")
    Write-Host "✅ OpenAI Codex CLI installed!" -ForegroundColor Green
}

# Install VS Code
function Install-VSCode {
    Write-Host "📦 Installing for VS Code..." -ForegroundColor Green
    $destVscode = Join-Path $TargetDir ".vscode"
    New-Item -ItemType Directory -Force -Path $destVscode | Out-Null

    Copy-Item -Path (Join-Path $ScriptDir ".vscode\ai-team-settings.json") -Destination $destVscode -Force
    Copy-Item -Path (Join-Path $ScriptDir "AI-TEAM.md") -Destination $TargetDir -Force
    $githubDir = Join-Path $TargetDir ".github"
    New-Item -ItemType Directory -Force -Path $githubDir | Out-Null
    Copy-Item -Path (Join-Path $ScriptDir ".github\copilot-instructions.md") -Destination $githubDir -Force

    Copy-Brain (Join-Path $TargetDir ".ai-team\brain")
    Write-Host "✅ VS Code installed!" -ForegroundColor Green
}

# Install Google Antigravity / Gemini CLI
function Install-Gemini {
    Write-Host "📦 Installing for Antigravity / Gemini CLI..." -ForegroundColor Green
    Copy-Item -Path (Join-Path $ScriptDir "GEMINI.md") -Destination $TargetDir -Force
    Copy-Item -Path (Join-Path $ScriptDir "AGENTS.md") -Destination $TargetDir -Force
    Copy-Item -Path (Join-Path $ScriptDir "ANTIGRAVITY.md") -Destination $TargetDir -Force
    $agentsRules = Join-Path $TargetDir ".agents\rules"
    New-Item -ItemType Directory -Force -Path $agentsRules | Out-Null
    Copy-Item -Path (Join-Path $ScriptDir ".agents\rules\ai-team.md") -Destination $agentsRules -Force
    Copy-Brain (Join-Path $TargetDir ".ai-team\brain")
    Write-Host "✅ Antigravity / Gemini installed!" -ForegroundColor Green
}

# Generic install (works with any AI assistant)
function Install-Generic {
    Write-Host "📦 Installing Universal Configuration..." -ForegroundColor Green
    Copy-Item -Path (Join-Path $ScriptDir "AI-TEAM.md") -Destination $TargetDir -Force
    Copy-Item -Path (Join-Path $ScriptDir "ANTIGRAVITY.md") -Destination $TargetDir -Force

    Copy-Brain (Join-Path $TargetDir ".ai-team\brain")
    Write-Host "✅ Universal configuration installed!" -ForegroundColor Green
}

# Initialize Project State
function Initialize-Project {
    Write-Host ""
    Write-Host "🔍 Analyzing project structure..." -ForegroundColor Yellow

    if (Test-Path (Join-Path $TargetDir "package.json")) { Write-Host "  • Detected: Node.js/TypeScript project" }
    if (Test-Path (Join-Path $TargetDir "requirements.txt")) { Write-Host "  • Detected: Python project" }
    if (Test-Path (Join-Path $TargetDir "go.mod")) { Write-Host "  • Detected: Go project" }

    $stateFile = Join-Path $TargetDir ".ai-team\brain\project-state.json"
    if (Test-Path $stateFile) {
        $state = Get-Content $stateFile -Raw | ConvertFrom-Json
        $state.project_name = Split-Path $TargetDir -Leaf
        $state.project_id = [string]([DateTimeOffset]::UtcNow.ToUnixTimeSeconds())
        $state | ConvertTo-Json -Depth 100 | Set-Content $stateFile
    }
    Write-Host "✅ Project initialized!" -ForegroundColor Green
}

# Main
$Platform = "auto"
if ($args.Count -gt 0) { $Platform = $args[0] }

if ($Platform -eq "auto") {
    $Platform = Detect-Platform
}

Write-Host "Target directory: $TargetDir" -ForegroundColor Yellow
Write-Host "Platform:         $Platform" -ForegroundColor Yellow
Write-Host ""

switch ($Platform) {
    "claude" { Install-Claude }
    "cursor" { Install-Cursor }
    "windsurf" { Install-Windsurf }
    "trae" { Install-Trae }
    "codex" { Install-Codex }
    "gemini" { Install-Gemini }
    "antigravity" { Install-Gemini }
    "vscode" { Install-VSCode }
    "all" {
        Install-Claude
        Install-Cursor
        Install-Windsurf
        Install-Trae
        Install-Codex
        Install-Gemini
        Install-VSCode
        Install-Generic
    }
    "generic" { Install-Generic }
    default { Install-Generic }
}

Initialize-Project

Write-Host ""
Write-Host "===========================================================" -ForegroundColor Green
Write-Host "            🎉 INSTALLATION COMPLETED SUCCESSFULLY!         " -ForegroundColor Green
Write-Host "===========================================================" -ForegroundColor Green
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Restart your AI assistant / reload session"
Write-Host "  2. AI Team Skills will auto-activate"
Write-Host "  3. Use /team-status or type commands in terminal"
Write-Host ""
Write-Host "Platforms: claude, cursor, windsurf, trae, codex, gemini, vscode, all, generic" -ForegroundColor Cyan
Write-Host ""
