# Sample framework verification

Verified on 9 September 2026 against the fictional local Sample Store.

| Area | Evidence |
|---|---|
| API automation | 17 pytest tests passed; all 20 API/UI tests collect successfully |
| JMeter backend | Two users × two checkout iterations; all response and 2000ms p95 gates passed; zero orders/sessions remained after cleanup |
| k6 backend | Two users × one checkout iteration; contract, success, error and 2000ms p95 thresholds passed; process exited 0 |
| Browser test source | Three BDD UI tests collect; JMeter UI XML parses and Selenium selectors match the supplied demo UI |
| Browser execution | Playwright test suite and Selenium/JMeter browser journey have not been executed here; manual CI workflows are supplied |
| Optional integrations | Local-LLM dry-run, synthetic generator and Lambda-style mapping run offline; live Ollama, n8n import, AWS and container/CI execution remain unverified |

These are smoke checks, not a capacity benchmark. Example budgets and synthetic results are not employer achievements or production SLAs. GitHub Actions workflows have not run remotely because repository write access is unavailable.
