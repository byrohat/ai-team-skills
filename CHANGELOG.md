# Changelog

All notable changes to **AI Team Skills** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.4.0] — 2026-06-29

### Added
- **Technology Strategist** — the 18th agent (`.claude/skills/tech-strategist.md`),
  owner of the **Technology Decision Protocol**. Selects language, framework,
  architecture and stack on real technical needs, growth scenario and operating
  cost — **never popularity**. Produces a decision matrix, ≥3 alternatives
  (Fast MVP / Balanced production / High-scale enterprise), risks, mitigations
  and a draft ADR. Includes engineering heuristics for 30+ languages, a 10-section
  decision output format, and an explicit anti-pattern guard.
- **`/team-stack`** command (`.claude/commands/team-stack.md`) to run the protocol.
- **Core Protocol 5 — Technology Decision**: a trigger in `_core-protocols.md`
  that fires the decision flow before implementation when a project or large
  module has an unratified or contested stack.
- `tech-strategist-brain.json` brain (shipped template + active brain) with a
  `tech_decisions[]` ledger.

### Changed
- **Ownership boundary**: the Technology Strategist *proposes*; **Architecture**
  *ratifies* the decision into a formal ADR and owns it afterward
  (`architecture.md`).
- **Orchestration**: Team Lead triggers the decision before design and tracks the
  new agent in the roster (`team-lead.md`).
- **Security VETO** now explicitly covers risky technology/dependency choices made
  during the decision protocol (`security.md`).
- Registered the agent, `/team-stack` command, brain file and dependencies in
  `skill.json`; bumped the framework version **2.3.0 → 2.4.0**.
- Propagated the agent table, command list, agent count (17 → 18) and version
  across every activation and rule file: CLAUDE, AGENTS, ANTIGRAVITY, AI-TEAM,
  GEMINI, README, `.cursorrules`, `.windsurfrules`, `.trae`, `.agents`,
  `.cursor/rules`, `.windsurf/rules`, `.github/copilot-instructions.md`,
  `.vscode`, CONTRIBUTING and `docs/INTEGRATION.md`.
- `cli/src/index.ts`: completed the `SKILL_FILES` list and the new-project state.

### Fixed
- **Autonomous activation chain**: `auto-activator.py` and `brain_manager.py`
  hardcoded a stale agent subset, so a fresh install would not seed, restore or
  validate several agents (including the new one). The full 18-agent roster is now
  authoritative across seeding, session restore (`get_full_context`) and
  `validate_project_state`, and the shipped/active `project-state.json` templates
  include `tech-strategist`.

## [2.3.0] — 2026-06-22

### Added
- Four **Core Protocols** — Continuity, Adaptation, Self-Evolution, Clarification.
- **Project DNA** brain file (`project-profile.json`) and a propose-don't-edit
  channel (`proposed-improvements.md`).
- Four additional agents: UX/UI Designer, Data Engineer, SRE, Mobile Engineer.

### Changed
- Every skill gained an Operating Protocols block; all activation files and brain
  templates were brought to parity (including `install.ps1`).

[2.4.0]: https://github.com/byrohat/ai-team-skills/releases/tag/v2.4.0
[2.3.0]: https://github.com/byrohat/ai-team-skills/releases/tag/v2.3.0
