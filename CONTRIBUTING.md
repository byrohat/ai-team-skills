# Contributing to AI Team Skills

Thanks for your interest in improving **AI Team Skills**! This framework turns AI coding
assistants into a coordinated 17-agent engineering team, and contributions of all sizes are welcome —
new agents, better protocols, platform support, docs, and bug fixes.

## Ways to contribute

- 🐛 **Report a bug** — open an issue with steps to reproduce and which platform/IDE you used.
- 💡 **Suggest an improvement** — open an issue describing the problem and your proposed solution.
- 🤖 **Improve an agent skill** — sharpen the standards, templates, or quality gates in `.claude/skills/`.
- 🌍 **Add platform support** — wire the framework into another AI IDE via its native auto-load file.
- 📖 **Improve docs** — README, INSTALL, runbooks, examples.

## Project layout

| Path | What it is |
|------|------------|
| `.claude/skills/` | **Source of truth** — 17 agent skill files + `_core-protocols.md` |
| `.cursor/skills/`, `.windsurf/skills/` | Mirrors of `.claude/skills/` (must stay identical) |
| `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursor/rules/`, `.windsurf/rules/`, `.trae/rules/`, `.agents/rules/`, `.github/copilot-instructions.md`, `AI-TEAM.md`, `ANTIGRAVITY.md` | Per-platform auto-load activation files |
| `src/ai-team/brain/` | Brain templates the installer copies into projects |
| `install.sh`, `install.ps1` | Cross-platform installers |
| `skill.json` | Canonical manifest (version, agents, dependencies, protocols) |

## House rules (the CI enforces these)

These are the same rules the framework asks its own agents to follow — please keep them green:

1. **1000-line hard limit per file.** Warn at 700, split at 1000. (Checked in CI.)
2. **Keep the skill mirrors in sync.** Any change under `.claude/skills/` must be copied to
   `.cursor/skills/` and `.windsurf/skills/` so all three are byte-identical:
   ```bash
   cp .claude/skills/*.md .cursor/skills/ && cp .claude/skills/*.md .windsurf/skills/
   ```
3. **Valid JSON / TOML.** `skill.json`, brain templates, and `task-queue.toml` must parse. (Checked in CI.)
4. **Don't edit skills "silently" in spirit.** When proposing a behavioral change to a skill, explain
   *why* in the PR — the framework's own Self-Evolution protocol works the same way
   (propose via `proposed-improvements.md`, then apply on approval).
5. **No secrets, no personal data** in committed files. Use placeholder values (`@company.com`, etc.).

## Versioning

The framework uses semantic-ish versioning in `skill.json` and the activation file headers. If your
change is user-visible, bump the version consistently across `skill.json`, `CLAUDE.md`, and the other
activation files, and update `README.md`.

## Pull request checklist

- [ ] Changes under `.claude/skills/` are mirrored to `.cursor/skills/` and `.windsurf/skills/`.
- [ ] No file exceeds 1000 lines.
- [ ] All JSON/TOML still parse.
- [ ] Version bumped consistently (if user-visible).
- [ ] CI is green.

## Development quick checks

Run the same checks CI runs, locally:

```bash
# JSON validity
find . -name '*.json' -not -path '*/node_modules/*' -not -path './.git/*' \
  -exec sh -c 'python3 -c "import json,sys;json.load(open(sys.argv[1]))" "$1"' _ {} \;

# Line limit
find .claude/skills -name '*.md' -exec sh -c 'l=$(wc -l < "$1"); [ "$l" -le 1000 ] || echo "OVER: $1 ($l)"' _ {} \;

# Mirror sync
diff <(cd .claude/skills && md5sum *.md | sort) <(cd .cursor/skills && md5sum *.md | sort)
```

## Code of conduct

Be kind and constructive. We're here to build something useful together.

---

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
