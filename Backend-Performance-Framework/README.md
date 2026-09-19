# Backend performance and load framework

Two engines implement the same fictional-store behavior: **k6 / JavaScript** and **JMeter / Groovy assertions**. This sample demonstrates feature-level suites and a combined checkout journey. It contains no employer endpoint, dataset or performance result.

## Structure

| Location | Purpose |
|---|---|
| `specifications/performance.feature` | Human-readable behavior/workload contract; not an automatically executed Gherkin runner |
| `k6/config.js` | Workload profiles, user pool and pass/fail thresholds |
| `k6/journey.js` | Login, catalog, checkout, semantic checks, custom timing and cleanup |
| `jmeter/plans/sample-store.jmx` | HTTP samplers, transaction controller, conditional feature suites |
| `jmeter/scripts/` | Per-thread identity, contract assertions and correlation |
| `scripts/run.py` | Validated CLI configuration and unique report directories |
| `scripts/gate.py` | Fail-closed CSV gate; does not trust JMeter's process exit code alone |

## Start the target

From the repository root, in a separate terminal:

```bash
cd Playwright-Pytest-BDD-Framework
python -m demo_app.server --port 8765
```

Run the following commands **inside Backend-Performance-Framework**. Install Python 3.11+, Java 17 and Apache JMeter 5.6.3 for JMeter; install k6 0.57+ for k6. No additional JMeter plugin is needed.

```bash
python scripts/run.py jmeter --binary /path/to/apache-jmeter-5.6.3/bin/jmeter --suite checkout --users 2 --iterations 2
python scripts/run.py jmeter --suite login --profile baseline --users 3
python scripts/run.py k6 --suite catalog --profile smoke
python scripts/run.py k6 --suite checkout --profile load --users 5
```

Use a full path to `jmeter.bat` on Windows, or put the selected engine on PATH. `--url` defaults to loopback; a plain remote origin requires `--allow-remote-target` and an explicitly authorized synthetic environment. Twenty generated accounts are assigned by virtual-user/thread number.

## Workload model

| Profile | k6 | JMeter |
|---|---|---|
| smoke | One iteration per VU | One iteration per thread |
| baseline | Constant VUs, 30 seconds | Ten iterations per thread |
| load | 10s ramp, 30s steady, 10s ramp down | Twenty iterations per thread, one-second ramp |

These profiles intentionally have different duration semantics. Compare engines only after aligning workload, warm-up, target resources and measurement windows. This small closed-loop sample is not a capacity estimate. `--iterations` applies to JMeter; `--users` applies to both.

## Assertions, metrics and evidence

The checkout suite signs in, checks the catalog, creates two notebooks and reads the order back. It verifies ownership, SKU and a 2500-cent total. Dynamic token and order IDs are correlated per user. Each iteration removes its own order and invalidates its session.

`journey_ms` (k6) and `TXN | checkout` (JMeter) measure business work, excluding cleanup and pacing. Cleanup failures still fail the run. The JMeter gate reports nearest-rank p95, error rate, sample count and completed journeys per second; it selects a single transaction label rather than mixing API and transaction samples. k6 emits its native summary JSON and threshold status. The example budgets (p95 < 2000ms; errors ≤ 1%; JMeter also rejects every failed child/cleanup row) are **illustrative local budgets, not production SLAs**. Engine percentile calculations may differ.

Reports are written under `reports/<UTC timestamp>/`. JMeter generates HTML, CSV and a gate JSON; k6 writes summary JSON. Reports are ignored by Git. Never commit headers, credentials or captured real application data. Only synthetic identifiers appear in this demo.

Reference: [k6 thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) and [JMeter components](https://jmeter.apache.org/usermanual/component_reference.html). Execution evidence is recorded in `../SAMPLE_VERIFICATION.md`.
