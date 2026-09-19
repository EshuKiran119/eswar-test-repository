# Browser journey performance with JMeter, Selenium and Groovy

A small real-browser performance sample for the fictional Sample Store. **JMeter orchestrates users, Selenium drives Chrome, and Groovy owns the workflow and assertions.** No third-party WebDriver Sampler plugin is required.

This is separate from high-volume HTTP load testing. Each browser consumes substantial resources, so the runner permits one to three users. Timings describe complete scripted journeys; they are neither server request throughput nor Core Web Vitals.

## Setup

Install Python 3.11+, Java 17, Maven 3.9+, Apache JMeter 5.6.3 and Chrome. Selenium Manager needs network access on its first run to obtain a compatible driver. Run the following **inside this folder**:

```bash
mvn dependency:copy-dependencies -DoutputDirectory=deps
python scripts/run.py --jmeter /path/to/apache-jmeter-5.6.3/bin/jmeter --users 1 --iterations 2
```

Start the sibling target in another terminal first:

```bash
cd ../Playwright-Pytest-BDD-Framework
python -m demo_app.server --port 8765
```

Use `--headed` for debugging, `--p95-ms 15000` for the illustrative default budget, and `--url` for an owned origin. Remote use requires `--allow-remote-target`. On Windows, pass the full `jmeter.bat` path. Browser dependencies are resolved through the pinned Maven POM and loaded using `user.classpath`.

## Framework responsibilities

| File | Responsibility |
|---|---|
| `jmeter/plans/browser-checkout.jmx` | Thread ownership, business loops and teardown order |
| `jmeter/scripts/setup.groovy` | One ChromeDriver per thread; browser startup outside timing |
| `jmeter/scripts/journey.groovy` | Explicit waits, login, checkout and visible $25.00 confirmation |
| `jmeter/scripts/cleanup.groovy` | Sign-out and owned-resource cleanup outside timing |
| `jmeter/scripts/quit.groovy` | Driver shutdown after the loop |
| `scripts/run.py` | Bounded users, dependency checks, execution and reports |
| `scripts/gate.py` | Business-label p95 and failure gate from JTL evidence |

No implicit waits or hard sleeps are used to synchronize UI behavior. Pacing is a separate JMeter pause. Thread errors continue through cleanup and driver teardown; failures remain visible in the JTL gate. Forced JVM termination cannot guarantee cleanup, so restart the in-memory service after an interrupted run.

The measured `UI | checkout` sampler covers navigation, sign-in, order submission and visible confirmation. Its 15-second p95 budget is a sample value only. Driver launch, cleanup and pacing are excluded. The gate rejects missing evidence, any failed sample and a breached timing budget. Generated JMeter HTML/CSV/gate JSON remain in ignored `reports/`.

The manual `sample-ui-performance.yml` CI workflow installs the engines, browser and dependencies and runs this synthetic target. See `../SAMPLE_VERIFICATION.md` for the distinction between source validation and executed browser tests.

Reference: [Selenium explicit waits](https://www.selenium.dev/documentation/webdriver/waits/) and [JMeter JSR223 components](https://jmeter.apache.org/usermanual/component_reference.html).
