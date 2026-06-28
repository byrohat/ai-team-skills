# Team Stack — Technology Decision

Run the **Technology Decision Protocol** for a project, module, or feature. The **Technology Strategist** agent selects the healthiest language, framework, architecture and stack based on real technical needs — never popularity — compares alternatives, scores a decision matrix, names risks, drafts an ADR, and records the decision to the brain.

## Usage

```
/team-stack [describe the system / module / feature]
```

Examples:
```
/team-stack a multi-tenant SaaS with a realtime dashboard and an LLM assistant
/team-stack a high-throughput webhook ingestion + worker pipeline
/team-stack the new mobile app, offline-first, iOS + Android
```

## What It Does

1. **Elicits decision drivers** — functional + non-functional needs, team reality, budget, compliance, and 6-month / 1-year / 3-year growth.
2. **Generates ≥3 candidate stacks** across the Fast MVP / Balanced production / High-scale enterprise spectrum.
3. **Collects multi-role input** — Architecture, AI/Data, Backend/Frontend/Mobile, DevOps/SRE, Security, Privacy.
4. **Applies the gates** — Security may **VETO** risky tech/dependency choices; SRE/DevOps weigh operability, scaling and runtime cost.
5. **Scores a decision matrix** with stated, project-specific weights.
6. **Produces the decision** — recommended stack, justification, risks, mitigations, and a **draft ADR** handed to Architecture to ratify.
7. **Records to memory** — appends to `tech-strategist-brain.json` (`tech_decisions[]`) and updates the `project-profile.json` stack.

## When It Auto-Triggers

The Team Lead / orchestration layer triggers this **before implementation** when:
- A new project has no ratified stack in `project-profile.json`.
- A new large module/service has different needs than the existing stack (AI service, realtime layer, data pipeline, worker tier).
- A significant choice is on the table (core language, framework, datastore, queue, realtime transport, deployment topology, heavyweight dependency).
- The stack is uncertain or contested.

If a still-valid decision already exists and the new work fits it, this references the existing ADR instead of re-running.

## Output

The structured 10-section decision: Short Decision · Context · Recommended Stack · Why This Stack · Alternatives Considered · Decision Matrix · Risks · Mitigations · ADR (draft) · Memory / Brain Update. See `.claude/skills/tech-strategist.md` for the full format.

## Core Rule

No language is chosen because it is popular, modern, fast, easy, or old. Every choice is justified by technical fit, team reality, growth scenario and operating cost. PHP is not disparaged — it is simply not auto-selected where it does not fit; Python, TypeScript, Go and every other language are held to the same rule.

## Brain Files Used

- `.ai-team/brain/tech-strategist-brain.json`
- `.ai-team/brain/project-profile.json`
- `docs/adr/` (draft ADR for Architecture to ratify)
