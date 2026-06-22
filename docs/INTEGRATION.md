# AI Team Skills — Integration Guide (v2.1.0)

## Installation & Setup

### For Claude Code
```bash
# Initialize inside your project
aiteam init --ai claude
```

### For Cursor / Windsurf / Antigravity (Gemini)
```bash
aiteam init --ai cursor
aiteam init --ai windsurf
aiteam init --ai generic
```

### Windows (PowerShell Installer)
```powershell
.\install.ps1 auto
```

---

## How It Works

### 1. The 13-Agent Structure
Each AI agent specializes in a specific area:

| Agent | Role | Focus Areas |
|-------|------|-------------|
| **Product Owner** | Requirement Analyst | Backlog management, INVEST user stories, Gherkin acceptance criteria, sprint planning |
| **Team Lead** | Coordinator | Assigns tasks, tracks sprint velocity (using standard deviation) & risk matrix, owns ADR process |
| **Architecture** | Designer | High-level system design, tactical DDD, microservices boundaries, C4 Level 3/4 diagrams, ADR registry |
| **AI Engineer** | Specialist | LLM API integrations, prompt engineering, semantic cache, hybrid search, RAG evaluation |
| **Backend** | Developer | API contracts, database locking patterns, DB connection pool math, Transactional Outbox, business logic |
| **Frontend** | Developer | Accessible UI (WCAG 2.2), Core Web Vitals performance (INP), micro-frontends, i18n, Zustand |
| **DevOps** | Platform | CI/CD automation pipelines, multi-stage Docker builds, Kubernetes manifests, secrets (SOPS), Infracost |
| **Performance** | Optimizer | Latency profiling, slow query index optimization, k6 load testing, DB sharding, Wasm, N+1 detection |
| **Observability** | Engineer | OpenTelemetry semantic conventions, multi-burn-rate SLO alerting rules, Prometheus, Grafana |
| **Security** | Auditor | OWASP 2024 compliance audits, vulnerability scan checks, custom Semgrep rules (VETO POWER) |
| **Privacy** | Specialist | GDPR/CCPA/KVKK compliance audits, PII protection masking pipelines, consent schemas, DPIA |
| **QA** | Tester | Automated test suites (unit, integration, E2E), contract tests (Pact Broker), mutation, visual regression |
| **Docs** | Writer | Runbooks, OpenAPI 3.1 specifications, Post-mortems, Vale doc-as-code linting, MkDocs/Docusaurus templates |

### 2. Brain System
Agents save their state to brain files in the `.ai-team/brain/` directory:

```
.ai-team/brain/
├── project-state.json         # Overall project status (v2.1.0 schema)
├── task-queue.toml            # Backlog of sprint tasks (TOML)
├── audit-log.jsonl            # JSONL logs of all status edits (Audit Trail)
├── product-owner-brain.json   # Backlog stories and sprint metrics
├── team-lead-brain.json       # Sprint targets, velocity & risk matrix
├── architecture-brain.json    # Architecture records index
├── ai-engineer-brain.json     # Models, vector DB & RAG evaluations state
├── backend-brain.json         # API routes inventory
├── devops-brain.json          # Deployment environments state
├── performance-brain.json     # Performance scores & budgets
├── observability-brain.json   # Traces & metrics endpoints state
└── ...
```

### 3. Quality Gates
Deployment is blocked until:
- [ ] **Security Gate**: Security audit passes (0 Critical/High issues) — VETO POWER active.
- [ ] **Quality Gate**: Unit coverage ≥ 80% | Integration coverage ≥ 70%.
- [ ] **Performance Gate**: Lighthouse ≥ 90 | Core Web Vitals targets met | API latency p95 < 200ms.
- [ ] **Observability Gate**: OpenTelemetry traces and structured JSON logging configured.
- [ ] **Docs Gate**: OpenAPI 3.1 specifications, Runbooks, and system README files complete.
- [ ] **File Size Gate**: No source code file exceeds 700 lines.

---

## Usage Guide

### Start a New Project
```bash
aiteam init --name "My Enterprise App" --ai claude
```

### Check Team Status
In your AI assistant's chat window, type:
```
/team-status
```
Or run via terminal:
```bash
aiteam status
```

### Request a Feature
Simply describe what you need in natural language:
```
Build a user registration endpoint with bcrypt password hashing
```
The Team Lead will automatically:
1. Decompose the request into dependencies.
2. Delegate system design tasks to **Architecture**.
3. Sequentially task **Backend**, **Frontend**, and **DevOps**.
4. Trigger verification gates through **QA**, **Performance**, **Security**, and **Privacy**.
5. Track completion metrics.

### Check Deployment Readiness
Type `/deploy-check` or run:
```bash
aiteam deploy-check
```

---

## Best Practices

1. **Let the Team Lead Orchestrate**: Do not skip the sequence. Let the Team Lead assign tasks and block merges when quality gates fail.
2. **Security Veto is Absolute**: Resolve all security concerns before attempting deployment checks.
3. **Respect File Limits (700 Lines)**: Keep modules small and highly focused. This reduces context token consumption and prevents complex spaghetti code.
4. **Use ADRs for Architecture**: Create a new ADR for every design decision using `/team-adr` or `aiteam adr`.
5. **Write Runbooks for DevOps**: Any infrastructure deployment requires a runbook under `docs/runbooks/` using the standard docs agent format.