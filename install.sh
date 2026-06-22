#!/bin/bash
#==============================================================================
# AI Team Skills - Cross-Platform Installer
# Installs AI Team Skills for Claude, Cursor, Windsurf, and VS Code
#==============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-$PWD}"

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         🤖 AI Team Skills - Cross-Platform Installer      ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Detect platform
detect_platform() {
    local platform=""

    if [ -n "$CLAUDE_DIR" ] || [ -d "$HOME/.claude" ]; then
        platform="claude"
    elif [ -n "$CURSOR_DIR" ] || [ -d "$HOME/.cursor" ]; then
        platform="cursor"
    elif [ -n "$WINDSURF_DIR" ] || [ -d "$HOME/.windsurf" ]; then
        platform="windsurf"
    elif [ -d "$HOME/.trae" ] || command -v trae &> /dev/null; then
        platform="trae"
    elif command -v codex &> /dev/null; then
        platform="codex"
    elif [ -d "$HOME/.gemini" ] || command -v gemini &> /dev/null; then
        platform="gemini"
    elif command -v code &> /dev/null; then
        platform="vscode"
    else
        platform="generic"
    fi

    echo "$platform"
}

# Install for Claude Code
install_claude() {
    echo -e "\n${GREEN}📦 Installing for Claude Code...${NC}"

    local claude_dir="$TARGET_DIR/.claude"
    local skills_dir="$claude_dir/skills"
    local brain_dir="$TARGET_DIR/.ai-team/brain"

    mkdir -p "$skills_dir"
    mkdir -p "$brain_dir"

    # Copy skill files
    cp "$SCRIPT_DIR/.claude/skills/"*.md "$skills_dir/"

    # Copy CLAUDE.md for auto-activation
    cp "$SCRIPT_DIR/CLAUDE.md" "$TARGET_DIR/CLAUDE.md"

    # Copy brain files
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.json "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.toml "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.md "$brain_dir/" 2>/dev/null || true

    echo -e "${GREEN}✅ Claude Code installed!${NC}"
}

# Install for Cursor
install_cursor() {
    echo -e "\n${GREEN}📦 Installing for Cursor...${NC}"

    local cursor_dir="$TARGET_DIR/.cursor"
    local skills_dir="$cursor_dir/skills"
    local brain_dir="$TARGET_DIR/.ai-team/brain"

    mkdir -p "$skills_dir"
    mkdir -p "$brain_dir"

    # Copy skill files
    cp "$SCRIPT_DIR/.claude/skills/"*.md "$skills_dir/"

    # Copy .cursorrules (legacy) + .cursor/rules/ai-team.mdc (modern, alwaysApply) for auto-activation
    cp "$SCRIPT_DIR/.cursorrules" "$TARGET_DIR/.cursorrules"
    mkdir -p "$cursor_dir/rules"
    cp "$SCRIPT_DIR/.cursor/rules/ai-team.mdc" "$cursor_dir/rules/ai-team.mdc"

    # Copy brain files
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.json "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.toml "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.md "$brain_dir/" 2>/dev/null || true

    echo -e "${GREEN}✅ Cursor installed!${NC}"
}

# Install for Windsurf
install_windsurf() {
    echo -e "\n${GREEN}📦 Installing for Windsurf...${NC}"

    local windsurf_dir="$TARGET_DIR/.windsurf"
    local skills_dir="$windsurf_dir/skills"
    local brain_dir="$TARGET_DIR/.ai-team/brain"

    mkdir -p "$skills_dir"
    mkdir -p "$brain_dir"

    # Copy skill files
    cp "$SCRIPT_DIR/.claude/skills/"*.md "$skills_dir/"

    # Copy .windsurfrules (legacy) + .windsurf/rules/ai-team.md (modern) for auto-activation
    cp "$SCRIPT_DIR/.windsurfrules" "$TARGET_DIR/.windsurfrules"
    mkdir -p "$windsurf_dir/rules"
    cp "$SCRIPT_DIR/.windsurf/rules/ai-team.md" "$windsurf_dir/rules/ai-team.md"

    # Copy brain files
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.json "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.toml "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.md "$brain_dir/" 2>/dev/null || true

    echo -e "${GREEN}✅ Windsurf installed!${NC}"
}

# Install for VS Code
install_vscode() {
    echo -e "\n${GREEN}📦 Installing for VS Code...${NC}"

    local vscode_dir="$TARGET_DIR/.vscode"
    local brain_dir="$TARGET_DIR/.ai-team/brain"

    mkdir -p "$vscode_dir"
    mkdir -p "$brain_dir"

    # Copy settings
    cp "$SCRIPT_DIR/.vscode/ai-team-settings.json" "$vscode_dir/"

    # Copy AI-TEAM.md + .github/copilot-instructions.md (auto-loaded by GitHub Copilot)
    cp "$SCRIPT_DIR/AI-TEAM.md" "$TARGET_DIR/AI-TEAM.md"
    mkdir -p "$TARGET_DIR/.github"
    cp "$SCRIPT_DIR/.github/copilot-instructions.md" "$TARGET_DIR/.github/copilot-instructions.md"

    # Copy brain files
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.json "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.toml "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.md "$brain_dir/" 2>/dev/null || true

    echo -e "${GREEN}✅ VS Code installed!${NC}"
}

# Install for Trae IDE (ByteDance)
install_trae() {
    echo -e "\n${GREEN}📦 Installing for Trae IDE...${NC}"

    local trae_dir="$TARGET_DIR/.trae/rules"
    local brain_dir="$TARGET_DIR/.ai-team/brain"

    mkdir -p "$trae_dir"
    mkdir -p "$brain_dir"

    # Copy Trae rules file
    cp "$SCRIPT_DIR/.trae/rules/ai-team.md" "$trae_dir/ai-team.md"

    # Copy brain files
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.json "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.toml "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.md "$brain_dir/" 2>/dev/null || true

    echo -e "${GREEN}✅ Trae IDE installed!${NC}"
}

# Install for OpenAI Codex CLI
install_codex() {
    echo -e "\n${GREEN}📦 Installing for OpenAI Codex CLI...${NC}"

    local brain_dir="$TARGET_DIR/.ai-team/brain"

    mkdir -p "$brain_dir"

    # Copy AGENTS.md (Codex CLI reads this file)
    cp "$SCRIPT_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"

    # Copy brain files
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.json "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.toml "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.md "$brain_dir/" 2>/dev/null || true

    echo -e "${GREEN}✅ OpenAI Codex CLI installed!${NC}"
}

# Install for Google Antigravity / Gemini CLI
install_gemini() {
    echo -e "\n${GREEN}📦 Installing for Antigravity / Gemini CLI...${NC}"

    local brain_dir="$TARGET_DIR/.ai-team/brain"
    local agents_rules_dir="$TARGET_DIR/.agents/rules"

    mkdir -p "$brain_dir"
    mkdir -p "$agents_rules_dir"

    # GEMINI.md (Gemini CLI + Antigravity), AGENTS.md (Antigravity), .agents/rules (Antigravity workspace)
    cp "$SCRIPT_DIR/GEMINI.md" "$TARGET_DIR/GEMINI.md"
    cp "$SCRIPT_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
    cp "$SCRIPT_DIR/.agents/rules/ai-team.md" "$agents_rules_dir/ai-team.md"
    cp "$SCRIPT_DIR/ANTIGRAVITY.md" "$TARGET_DIR/ANTIGRAVITY.md"

    # Copy brain files
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.json "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.toml "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.md "$brain_dir/" 2>/dev/null || true

    echo -e "${GREEN}✅ Antigravity / Gemini installed!${NC}"
}

# Generic install (works with any AI assistant)
install_generic() {
    echo -e "\n${GREEN}📦 Installing (Generic - works with all AI assistants)...${NC}"

    local brain_dir="$TARGET_DIR/.ai-team/brain"

    mkdir -p "$brain_dir"

    # Copy AI-TEAM.md (universal activation file)
    cp "$SCRIPT_DIR/AI-TEAM.md" "$TARGET_DIR/AI-TEAM.md"

    # Copy brain files
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.json "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.toml "$brain_dir/" 2>/dev/null || true
    cp "$SCRIPT_DIR/src/ai-team/brain/"*.md "$brain_dir/" 2>/dev/null || true

    echo -e "${GREEN}✅ Generic installation complete!${NC}"
}

# Initialize project
init_project() {
    echo -e "\n${BLUE}🔍 Analyzing project structure...${NC}"

    # Detect project type
    if [ -f "$TARGET_DIR/package.json" ]; then
        echo -e "  • Detected: Node.js/TypeScript project"
    elif [ -f "$TARGET_DIR/requirements.txt" ]; then
        echo -e "  • Detected: Python project"
    elif [ -f "$TARGET_DIR/go.mod" ]; then
        echo -e "  • Detected: Go project"
    elif [ -f "$TARGET_DIR/Cargo.toml" ]; then
        echo -e "  • Detected: Rust project"
    else
        echo -e "  • Detected: Unknown project type"
    fi

    # Update project state
    local state_file="$TARGET_DIR/.ai-team/brain/project-state.json"
    if [ -f "$state_file" ]; then
        # Update with project name
        local project_name=$(basename "$TARGET_DIR")
        sed -i.bak "s/\"project_name\": \"\"/\"project_name\": \"$project_name\"/" "$state_file"
        sed -i.bak "s/\"project_id\": \"\"/\"project_id\": \"$(date +%s)\"/" "$state_file"
        rm -f "$state_file.bak"
    fi

    echo -e "\n${GREEN}✅ Project initialized!${NC}"
}

# Show completion
show_completion() {
    echo -e "\n${GREEN}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                    ✅ INSTALLATION COMPLETE               ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    echo -e "${YELLOW}Next Steps:${NC}"
    echo "  1. Restart your AI assistant"
    echo "  2. AI Team Skills will auto-activate"
    echo "  3. Type /team-status to see team report"
    echo ""
    echo -e "${YELLOW}Slash Commands:${NC}"
    echo "  /team-status     - Full team report"
    echo "  /team-blockers   - List active blockers"
    echo "  /team-next       - Next actions"
    echo "  /deploy-check    - Deployment readiness"
    echo ""
    echo -e "${BLUE}Documentation:${NC}"
    echo "  • AI-TEAM.md      - Universal activation file"
    echo "  • README.md       - Project documentation"
    echo "  • docs/           - Detailed guides"
    echo ""
}

# Main
main() {
    local platform="${2:-auto}"

    if [ "$platform" = "auto" ]; then
        platform=$(detect_platform)
    fi

    echo -e "\n${YELLOW}Target directory:${NC} $TARGET_DIR"
    echo -e "${YELLOW}Detected platform:${NC} $platform"

    case "$platform" in
        claude)
            install_claude
            ;;
        cursor)
            install_cursor
            ;;
        windsurf)
            install_windsurf
            ;;
        trae)
            install_trae
            ;;
        codex)
            install_codex
            ;;
        gemini|antigravity)
            install_gemini
            ;;
        vscode)
            install_vscode
            ;;
        all)
            install_claude
            install_cursor
            install_windsurf
            install_trae
            install_codex
            install_gemini
            install_vscode
            install_generic
            ;;
        generic)
            install_generic
            ;;
        *)
            echo -e "${RED}Unknown platform: $platform${NC}"
            echo "Usage: $0 [target-dir] [platform]"
            echo "Platforms: claude, cursor, windsurf, trae, codex, gemini, vscode, all, generic"
            exit 1
            ;;
    esac

    init_project
    show_completion
}

# Help
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "AI Team Skills - Cross-Platform Installer"
    echo ""
    echo "Usage: $0 [target-dir] [platform]"
    echo ""
    echo "Options:"
    echo "  target-dir  Target directory (default: current directory)"
    echo "  platform    claude, cursor, windsurf, trae, codex, gemini, vscode, all, generic"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Auto-detect, current dir"
    echo "  $0 /path/to/project                   # Auto-detect platform"
    echo "  $0 /path/to/project claude            # Claude Code only"
    echo "  $0 /path/to/project all               # All platforms"
    echo ""
    exit 0
fi

main "$@"