"""Local-first engine runner with explicit suite selection and evidence gates."""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("engine", choices=["k6", "jmeter"])
    p.add_argument("--binary", help="Absolute path to the selected engine")
    p.add_argument("--url", default="http://127.0.0.1:8765")
    p.add_argument(
        "--suite", choices=["login", "catalog", "checkout"], default="checkout"
    )
    p.add_argument("--profile", choices=["smoke", "baseline", "load"], default="smoke")
    p.add_argument("--users", type=int, default=1)
    p.add_argument("--iterations", type=int, help="JMeter iterations per user")
    p.add_argument("--p95-ms", type=float, default=2000)
    p.add_argument("--allow-remote-target", action="store_true")
    a = p.parse_args()
    u = urlsplit(a.url)
    if (
        u.scheme not in ["http", "https"]
        or not u.hostname
        or u.username
        or u.password
        or u.query
        or u.fragment
        or u.path not in ["", "/"]
    ):
        p.error(
            "Use a plain HTTP(S) origin without credentials, path, query or fragment"
        )
    if u.hostname not in ["localhost", "127.0.0.1"] and not a.allow_remote_target:
        p.error("An owned remote target requires --allow-remote-target")
    if (
        not 1 <= a.users <= 20
        or a.p95_ms <= 0
        or (a.iterations is not None and a.iterations < 1)
    ):
        p.error("Use 1-20 synthetic users and positive iterations/budget")
    binary = a.binary or shutil.which(a.engine)
    if not binary:
        p.error(f"Install {a.engine} or pass --binary")
    out = ROOT / "reports" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    out.mkdir(parents=True)
    if a.engine == "k6":
        env = {
            **os.environ,
            "BASE_URL": a.url.rstrip("/"),
            "K6_NO_USAGE_REPORT": "true",
            "SUITE": a.suite,
            "PROFILE": a.profile,
            "VUS": str(a.users),
            "P95_MS": str(a.p95_ms),
            "SUMMARY_PATH": str(out / "summary.json"),
            "ALLOW_REMOTE_TARGET": str(a.allow_remote_target).lower(),
        }
        result = subprocess.run([binary, "run", str(ROOT / "k6/journey.js")], env=env)
        return result.returncode
    iterations = a.iterations or {"smoke": 1, "baseline": 10, "load": 20}[a.profile]
    result = subprocess.run(
        [
            binary,
            "-n",
            "-t",
            str(ROOT / "jmeter/plans/sample-store.jmx"),
            "-l",
            str(out / "results.jtl"),
            "-j",
            str(out / "jmeter.log"),
            "-e",
            "-o",
            str(out / "html"),
            f"-Jhost={u.hostname}",
            f'-Jport={u.port or (443 if u.scheme == "https" else 80)}',
            f"-Jprotocol={u.scheme}",
            f"-Jusers={a.users}",
            f"-Jiterations={iterations}",
            f"-Jsuite={a.suite}",
            f'-Jscript_dir={ROOT / "jmeter/scripts"}',
            "-Jjmeter.save.saveservice.output_format=csv",
            "-Jjmeter.save.saveservice.print_field_names=true",
            "-Jjmeter.save.saveservice.assertion_results_failure_message=true",
        ]
    )
    if result.returncode:
        return result.returncode
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/gate.py"),
            str(out / "results.jtl"),
            "--label",
            f"TXN | {a.suite}",
            "--p95-ms",
            str(a.p95_ms),
        ]
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
