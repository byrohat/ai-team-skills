# Runbook: {Service Name} — {Task or Incident Type}

**ID**: RB-{NNN} | **Target System**: {Component Name} | **Severity**: P1 (Critical) | P2 (High) | P3 (Medium) | P4 (Low)
**Last Updated**: YYYY-MM-DD
**Owner**: DevOps Agent / SRE Team

---

## 1. Overview
[Provide a brief description of the task, when to run it, what systems it modifies, and its intended outcome.]

## 2. Prerequisites & Permissions
* **Tools Required**: `kubectl` / `aws-cli` / `terraform` / `pg_dump`
* **Access Credentials**: `kube-prod-admin` / `aws-readonly`
* **Impact Level**: Low / High (Could cause temporary packet loss or API latency spikes)

## 3. Step-by-Step Instructions

### Step 3.1: Pre-Execution Verification
Check system health before starting:
```bash
# Verify pod statuses
kubectl get pods -n production -l app=my-service

# Check error rate metric
curl -s "http://prometheus-server/api/v1/query?query=sum(rate(http_requests_total{status_code=~'5..'}[5m]))"
```

### Step 3.2: Execution Sequence
Follow these commands in exact order:
```bash
# 1. Take database snapshot (if database modification is involved)
pg_dump -h db-prod.internal -U dbuser -d prod_db -F c -b -v -f /tmp/backup_pre_deploy.dump

# 2. Run deployment or migration script
./scripts/deploy.sh --version=v2.0.0 --env=production
```

### Step 3.3: Post-Execution Verification
Confirm successful completion and healthy metrics:
```bash
# Verify API response
curl -I https://api.production.internal/healthz
```

## 4. Rollback Procedure
If the execution fails, triggers alarms, or metrics degrade:
1. Roll back deployment:
   ```bash
   kubectl rollout undo deployment/my-service -n production
   ```
2. Restore database from pre-execution snapshot (if corrupted):
   ```bash
   pg_restore -h db-prod.internal -U dbuser -d prod_db -v /tmp/backup_pre_deploy.dump
   ```
3. Notify the incident channel: Slack `#incidents` / PagerDuty escalation.
