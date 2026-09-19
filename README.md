# Eswar Sai Kiran Singamsetty

**Senior QA Engineer | SDET | Automation & Quality Engineering**

Senior QA Engineer at Experian, focused on Playwright/Python framework architecture, UI and API automation, performance engineering, CI/CD release validation and AWS observability. I apply specification-driven quality review and practical AI-assisted testing, including local LLM integration and n8n workflows.

[Public portfolio](https://eshukiran119.github.io/eswar-test-repository/) · [LinkedIn](https://www.linkedin.com/in/eswar-sai-kiran-singamsetty-429840198) · [Email](mailto:eshukiran57@gmail.com) · [Resume PDF](docs/assets/Eswar_Sai_Kiran_Singamsetty_ATS_Resume.pdf) · [Resume Word](docs/assets/Eswar_Sai_Kiran_Singamsetty_ATS_Resume.docx)

## Framework showcase

New personal reference implementations use a fictional store and synthetic data. They demonstrate framework structure and selected techniques; they are not copies of employer systems.

| Framework | What to inspect |
|---|---|
| [Playwright + pytest-bdd](Playwright-Pytest-BDD-Framework/) | UI/API layers, environments, BDD, cleanup, CI and local AI/workflow examples |
| [Backend performance](Backend-Performance-Framework/) | k6/JMeter suites, correlation, assertions, workload profiles and result gates |
| [UI performance](UI-Performance-Framework/) | JMeter/Selenium/Groovy, browser ownership, explicit waits and journey measurement |

[Execution evidence](SAMPLE_VERIFICATION.md) records what has actually been run. Browser and optional integration execution still need their declared dependencies.

## Public code samples

These personal examples illustrate selected techniques. They are not the employer-owned automation frameworks described in my professional experience.

| Project | Code currently present | Technologies |
|---|---|---|
| [Playwright login automation](Playwright-Ecommerce-Tests/) | Parameterized SauceDemo login test, Chromium fixture and Allure configuration | Python, Playwright, pytest |
| [API/security starters](API-Security-Tests/) | Karate user-list scenario and a Python ZAP integration helper | Karate, REST, Python, OWASP ZAP |
| [Selenium/Robot login examples](Telecom-Automation/) | Selenium page object, unittest login example and Robot login scenario | Python, Selenium, Robot Framework |

Each folder README documents its actual scope and remaining execution prerequisites. Existing project source files have been preserved.

## Engineering approach

- Design maintainable framework layers and reusable BDD scenarios.
- Review acceptance criteria, integration behavior, test data and negative scenarios before implementation.
- Connect UI/API regression evidence with CI/CD quality gates and release validation.
- Investigate failures using cloud logs, service evidence and test-data checks.
- Apply AI-assisted test design and privacy-safe synthetic data with engineering review.

## Portfolio and GitHub Pages

Website source lives in `docs/`. GitHub Pages is configured through `.github/workflows/deploy-portfolio-pages.yml`, which validates the site and publishes only that directory. Changes pushed to `main` under `docs/` redeploy the portfolio.

See [editing and maintenance guide](MAINTAINING_PORTFOLIO.md) and [deployment notes](docs/README_DEPLOY.md). Existing project source has been preserved. All new frameworks are personal demonstrations using fictional data.
