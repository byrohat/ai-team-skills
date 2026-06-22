# Incident Post-Mortem: {Incident Title}

**Date**: YYYY-MM-DD | **Incident Commander**: {Name} | **Severity**: SEV-1 (Critical) | SEV-2 (High)
**Service Impacted**: {e.g. api-service, payment-gateway}
**Downtime Duration**: {e.g. 22 minutes}

---

## 1. Executive Summary
[Provide a 3-4 sentence summary of what happened, the customer impact, duration, and the root cause. This section is for high-level business stakeholder review.]

## 2. Customer Impact
* **Total Users Affected**: [e.g. Approximately 12,000 active users]
* **Impact Description**: [e.g. Users received HTTP 500 errors when attempting to check out.]
* **Downtime Details**: Start time (UTC) to End time (UTC).

## 3. Incident Timeline
All times in UTC.
* **14:05** — Automated alert triggers for HTTP 5xx spikes on `api-service` (Datadog/PagerDuty).
* **14:10** — Incident team assembled on Slack bridge.
* **14:15** — SRE identifies the source of the issue: database connection pool exhaustion.
* **14:18** — Temporary mitigation applied: scaled up database connections limit.
* **14:22** — API success rates return to 100%. Incident resolved.

## 4. Root Cause Analysis (The 5 Whys)
1. **Why did the service return 500 errors?**
   Because it could not establish a connection to the database.
2. **Why could it not connect to the database?**
   Because the connection pool limit (100) was fully saturated.
3. **Why was the connection pool saturated?**
   Because database queries were taking > 5 seconds to execute, keeping connections open.
4. **Why were the database queries taking > 5 seconds?**
   Because a new feature ran a search query without utilizing an index.
5. **Why was the index missing?**
   Because the migration script adding the index was not included in the deploy package due to a merge conflict.

## 5. Resolution & Recovery
[Detail the exact actions taken to resolve the incident, both immediate short-term fixes and long-term mitigations.]

## 6. Action Items
Action items are tracked in Jira/GitHub Issues and must follow the format below:

| ID | Action Item | Owner | Target Date | Status |
|---|---|---|---|---|
| Action-1 | Add composite index on `orders(user_id, status)` | Backend Lead | YYYY-MM-DD | Todo |
| Action-2 | Implement query timeout limits of 2000ms | SRE Team | YYYY-MM-DD | Todo |
| Action-3 | Setup Prometheus alerts for connection pool utilization > 80% | DevOps Agent | YYYY-MM-DD | Done |
