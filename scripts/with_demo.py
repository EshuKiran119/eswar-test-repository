"""Run a command against the local fictional target; no background-process leaks."""

from pathlib import Path
import subprocess
import sys

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "Playwright-Pytest-BDD-Framework")
)
from demo_app.server import start_server

if len(sys.argv) < 2:
    raise SystemExit("Usage: python scripts/with_demo.py COMMAND [ARGS ...]")
server = start_server(8765)
try:
    result = subprocess.run(sys.argv[1:])
    raise SystemExit(result.returncode)
finally:
    server.shutdown()
    server.server_close()
