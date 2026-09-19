# Playwright + pytest-bdd quality framework

A personal reference implementation for a **fictional Sample Store**, built to demonstrate maintainable UI/API automation. Every account and record is synthetic. This is newly authored demonstration code, not a copy of an Experian or Capgemini framework.

## Architecture

| Layer | Location | Responsibility |
|---|---|---|
| Behavior specifications | `features/` | Authentication, negative scenarios, order mapping, UI journeys |
| Reusable step definitions | `steps/` | Business language and explicit assertions |
| UI abstraction | `framework/pages/` | Playwright page objects and locator ownership |
| API abstraction | `framework/clients/` | Requests sessions, timeouts, authentication and resource cleanup |
| Environment configuration | `framework/config.py`, `conftest.py` | LOCAL/QAT/UAT, per-worker synthetic identities, isolated local target |
| Test execution | `tests/api/`, `tests/ui/` | Tags, selective execution, contract edge cases |
| Fictional application | `demo_app/` | In-memory HTTP API and browser UI; no third-party target |
| Practical AI/workflow examples | `quality_workflows/` | Synthetic data, local LLM review and n8n orchestration |

Requirements: Python 3.11+, with Chromium installed for UI tests. Commands below run **inside this folder**.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m pytest tests/api -q
python -m pytest tests/ui --browser chromium --tracing retain-on-failure --screenshot only-on-failure
python -m pytest -n 2 --alluredir=reports/allure --junitxml=reports/junit.xml
```

LOCAL starts a fresh in-memory service automatically for each pytest worker. Twenty synthetic identities are available; workers do not share a service instance. No production server is contacted. Run `python -m demo_app.server --port 8765` separately when using the two performance frameworks.

## Environment selection

Copy `.env.example` to `.env`, set `QAT_BASE_URL`, `QAT_USER_01`, `QAT_PASSWORD_01` (and one pair per worker), then run:

```bash
python -m pytest --env QAT -m api
python -m pytest --env UAT -m smoke
```

Remote targets require `ALLOW_REMOTE_TARGET=true` and must implement the documented fictional contract. The demo ownership scenario assumes the sample01–sample20 identity pool. To adapt to another authorized application, replace its contracts and test identities first. Never paste workplace configuration or real customer records into this repository.

## Coverage and release gate

17 API tests cover session creation/invalidation, rejected credentials, authorization, order ownership, data mapping, quantity boundaries/types and deletion. Three BDD UI scenarios cover checkout, invalid login and sign-out. A new context isolates each UI test. A failed assertion produces a nonzero pytest exit code; CI retains JUnit and diagnostic artifacts even on failure. No retry hides flaky tests.

The API client deletes only IDs created by its test and invalidates its own session. The demo UI deletes its last order on sign-out. Stop/restart the in-memory server after an interrupted run; forced process termination can bypass teardown. Browser traces are intended for this synthetic target only because they can include page/network data.

## Specification-driven quality gate

Before adding a scenario, review expected behavior, acceptance criteria, dependencies, data, authorization, negative paths and testability. Map the accepted examples into `features/`, implement step/page/client changes, run the smallest relevant suite, then the regression gate. Review unexplained failures before release. This sample makes no quantified claim about defect reduction.

## CI and container execution

The repository's `sample-frameworks.yml` workflow runs API and UI jobs separately. `Dockerfile` uses a Playwright image matching the pinned Python Playwright version. `bitbucket-pipelines.yml` and `Jenkinsfile` provide equivalent API gates; adapt agent/tool installation to your own environment.

```bash
docker build -t sample-quality-framework .
docker run --rm sample-quality-framework
```

Reference: [pytest-bdd documentation](https://pytest-bdd.readthedocs.io/en/stable/). See the repository's `SAMPLE_VERIFICATION.md` for what has actually been executed.
