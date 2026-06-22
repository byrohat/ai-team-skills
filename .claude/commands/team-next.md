# Team Next

Show recommended next actions based on current project state.

## Usage

```
/team-next
```

## What It Shows

1. **Immediate Actions**: Tasks to do right now
2. **Upcoming Tasks**: Next in queue
3. **Blocked Tasks**: Waiting on dependencies

## Decision Logic

The Team Lead agent analyzes:
1. Current project phase
2. Component completion status
3. Blocker dependencies
4. Task priorities

## Example Output

```
## Next Actions

### Do Now
1. **[HIGH]** Complete Dashboard component
   - Agent: @frontend
   - Estimated: 2 hours
   - Dependency: Backend API ready

2. **[HIGH]** Write E2E authentication tests
   - Agent: @qa
   - Estimated: 1 hour
   - Dependency: Login flow complete

### Do Next
3. **[MEDIUM]** Add privacy consent modal
   - Agent: @frontend
   - Estimated: 30 min

4. **[MEDIUM]** Run performance benchmarks
   - Agent: @qa
   - Estimated: 30 min

### Waiting On
- Frontend: API documentation from @backend
- QA: Test environment setup from @architecture
```