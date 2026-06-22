# Team Status

Display the current status of all AI team agents and project progress.

## Usage

```
/team-status
```

## What It Shows

1. **Overall Progress**: Project phase and completion percentage
2. **Component Status**: Status of each agent (pending, in_progress, complete)
3. **Blockers**: Active deployment blockers
4. **Next Actions**: Recommended next steps

## Example Output

```
## Team Status Report

**Project**: My App
**Phase**: Development
**Completion**: 65%

### Component Status
- [x] Architecture: COMPLETE (100%)
- [x] Backend: COMPLETE (100%)
- [ ] Frontend: IN PROGRESS (50%)
- [x] Security: COMPLETE (100%)
- [x] Privacy: COMPLETE (100%)
- [ ] QA: IN PROGRESS (30%)
- [x] Docs: COMPLETE (100%)

### Blockers
1. Frontend: Dashboard component missing - @frontend
2. QA: E2E tests not written - @qa

### Next Steps
1. Complete Dashboard component
2. Write E2E tests
3. Run final security audit
```

## Brain Files Used

- `.ai-team/brain/project-state.json`
- `.ai-team/brain/team-lead-brain.json`
- `.ai-team/brain/*-brain.json`