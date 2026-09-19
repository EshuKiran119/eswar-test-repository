# AI-assisted and cloud-quality examples

Small, employer-independent companions to the runnable UI/API framework:

- `synthetic_data.py`: creates boundary-focused records using reserved `.invalid` email addresses. Reads no source data and requires no model.
- `local_llm_review.py`: sends only a built-in fictional specification and synthetic failure to loopback Ollama. Supports `--dry-run`; never reads workplace logs. Model responses require review.
- `n8n-local-review.json`: importable, inactive manual workflow calling the local model with the same fictional contract. No stored credentials, Jira site or automatic issue creation. In Docker, configure a reachable local Ollama origin before running; loopback otherwise means the n8n container itself.
- `lambda_mapping.py`: pure Lambda-style handler for offline contract/mapping validation. It does not provision or contact AWS.
- `observability_queries.md`: query patterns for synthetic CloudWatch/Splunk execution events; no real resource identifiers.

From this folder:

```bash
python synthetic_data.py
python local_llm_review.py --dry-run
python lambda_mapping.py
```

For optional live local inference, install Ollama, download the model you choose, and run `python local_llm_review.py --model qwen2.5:3b`. Live inference and n8n import/execution require those optional tools; they are not claimed as verified in this environment. Fixed synthetic inputs demonstrate privacy-conscious design, not a general PII-detection system.

References: [Ollama generate API](https://docs.ollama.com/api/generate), [n8n HTTP Request](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/).
