# API and security testing starters

This folder contains a Karate-style user API scenario and a Python helper intended to invoke an OWASP ZAP active scan.

## Current scope

- `features/users.feature`: user-list request and response assertion.
- `utils/zap_integration.py`: ZAP client helper with a placeholder API key and local proxy configuration.
- `features/security.feature`: empty placeholder.

## Remaining setup

This is a starter, not a ready-to-run security suite. A Karate Java/Maven runner and `pom.xml` are not included; the previous `mvn test` instruction could not work from this folder alone. Installing a Python package named `karate` is not a substitute for that runner.

Before executing the API scenario, verify the current test service access requirements and expected response schema. Its existing assertion may not match the actual user-list response.

Before using the ZAP helper, configure a running ZAP service, provide its API key securely and verify the alert retrieval API against the installed client. Active scans must target an environment you own or have explicit permission to test. No scans were run during this portfolio work.

Source code remains unchanged. [Repository overview](../README.md)
