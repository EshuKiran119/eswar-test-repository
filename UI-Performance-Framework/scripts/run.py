"""Launch a small real-browser workload, then enforce its own timing budget."""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jmeter", default=shutil.which("jmeter"))
    p.add_argument("--url", default="http://127.0.0.1:8765")
    p.add_argument("--users", type=int, default=1)
    p.add_argument("--iterations", type=int, default=2)
    p.add_argument("--p95-ms", type=float, default=15000)
    p.add_argument("--headed", action="store_true")
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
    if not a.jmeter or not 1 <= a.users <= 3 or a.iterations < 1 or a.p95_ms <= 0:
        p.error("Install JMeter and use 1-3 users with positive iterations/budget")
    jars = sorted((ROOT / "deps").glob("*.jar"))
    if not jars:
        p.error("Run mvn dependency:copy-dependencies -DoutputDirectory=deps first")
    out = ROOT / "reports" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    out.mkdir(parents=True)
    # JMeter user.classpath supports a directory of jars. This avoids copying into JMeter/lib.
    result = subprocess.run(
        [
            a.jmeter,
            "-n",
            "-t",
            str(ROOT / "jmeter/plans/browser-checkout.jmx"),
            "-l",
            str(out / "results.jtl"),
            "-j",
            str(out / "jmeter.log"),
            "-e",
            "-o",
            str(out / "html"),
            f'-Juser.classpath={ROOT / "deps"}',
            f'-Jscript_dir={ROOT / "jmeter/scripts"}',
            f'-Jbase_url={a.url.rstrip("/")}',
            f"-Jusers={a.users}",
            f"-Jiterations={a.iterations}",
            f"-Jheadless={str(not a.headed).lower()}",
            "-Jjmeter.save.saveservice.output_format=csv",
            "-Jjmeter.save.saveservice.print_field_names=true",
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
            "UI | checkout",
            "--p95-ms",
            str(a.p95_ms),
        ]
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
