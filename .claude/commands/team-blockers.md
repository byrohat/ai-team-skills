# Team Blockers

List all active blockers preventing project completion or deployment.

## Usage

```
/team-blockers
```

## What It Shows

1. **Critical Blockers**: Issues blocking deployment
2. **High Priority**: Important issues to fix
3. **Medium Priority**: Should be addressed soon
4. **Low Priority**: Nice to fix when possible

## Blocker Categories

- **Security**: Vulnerability or security issue
- **Quality**: Missing tests or coverage gaps
- **Documentation**: Incomplete docs
- **Logic**: Business logic issues
- **Integration**: Missing integrations

## Example Output

```
## Active Blockers

### Critical (Blocking Deployment)
1. **Security Vulnerability**: SQL injection in /api/users
   - Source: Security Agent
   - Status: OPEN
   - Assigned to: @backend

### High Priority
2. **Test Coverage**: Unit coverage below 80%
   - Source: QA Agent
   - Status: OPEN
   - Assigned to: @qa

### Medium Priority
3. **Documentation**: API docs incomplete
   - Source: Docs Agent
   - Status: OPEN
   - Assigned to: @docs
```

## Resolution

Each blocker should have:
- Clear description
- Source agent
- Assigned owner
- Resolution steps