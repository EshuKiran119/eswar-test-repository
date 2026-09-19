# Synthetic execution observability

These query examples assume explicitly emitted fields `test_id`, `run_id`, `status`, `duration_ms` in a dedicated demo log source. No CloudWatch log group, Splunk index, AWS resource or employer schema is included or queried.

CloudWatch Logs Insights:

```sql
fields @timestamp, run_id, test_id, status, duration_ms
| filter test_id like /^SYN-/
| stats count(*) as executions, pct(duration_ms, 95) as p95_ms by status
```

Splunk, after selecting your own synthetic-only index in the UI:

```text
 test_id="SYN-*" | stats count as executions perc95(duration_ms) as p95_ms by status
```

For cloud validation, connect a correlation ID to request, Lambda log event and expected persisted mapping. Validate only the records the test owns. DynamoDB/S3 resource access and credentials deliberately remain environment configuration; these queries do not demonstrate a deployed AWS integration.
