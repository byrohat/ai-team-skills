# Deploy Check

Verify if the project is ready for deployment.

## Usage

```
/deploy-check
```

## Quality Gates

Deployment is blocked until ALL gates pass:

### 1. Security Gate
- [ ] No critical vulnerabilities
- [ ] No high vulnerabilities
- [ ] Security audit passed
- [ ] Dependencies scanned

### 2. Quality Gate
- [ ] Unit test coverage > 80%
- [ ] Integration test coverage > 70%
- [ ] All tests passing
- [ ] No flaky tests

### 3. Documentation Gate
- [ ] README complete
- [ ] API documentation complete
- [ ] Architecture documented
- [ ] Changelog updated

### 4. Privacy Gate
- [ ] GDPR compliance verified
- [ ] Data protection implemented
- [ ] Privacy policy published

### 5. File Quality Gate
- [ ] No file exceeds 700 lines
- [ ] No TODO comments without context
- [ ] All public APIs documented

## Example Output

```
## Deployment Readiness Check

### Security Gate: FAIL ❌
- [x] No critical vulnerabilities
- [x] No high vulnerabilities
- [x] Security audit passed
- [x] Dependencies scanned
Result: PASS

### Quality Gate: FAIL ❌
- [x] Unit test coverage > 80% (85%)
- [x] Integration test coverage > 70% (72%)
- [x] All tests passing
- [x] No flaky tests
Result: PASS

### Documentation Gate: FAIL ❌
- [ ] README complete (missing: deployment section)
- [x] API documentation complete
- [x] Architecture documented
- [x] Changelog updated
Result: FAIL

### Privacy Gate: PASS ✅
- [x] GDPR compliance verified
- [x] Data protection implemented
- [x] Privacy policy published
Result: PASS

### File Quality Gate: PASS ✅
- [x] No file exceeds 700 lines
- [x] All public APIs documented
Result: PASS

---

## Result: NOT READY FOR DEPLOYMENT

### Blockers:
1. Documentation: README missing deployment section

### Next Steps:
1. Add deployment section to README
2. Re-run deploy-check
```