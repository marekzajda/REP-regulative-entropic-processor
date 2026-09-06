#!/usr/bin/env python3
"""REP Connector v1.

Safe local runner for approved REP/RepNet jobs pulled from GitHub.

Security model:
- jobs cannot provide arbitrary shell commands;
- each job references a named suite from connector/config.json;
- suite maps to an allowlisted Python script;
- optional environment overrides are restricted to a configured allowlist;
- execution uses subprocess without shell=True;
- results are written as JSON + stdout/stderr logs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    tmp.replace(path)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
            timeout=15,
        )
        return result.stdout.strip()
    except Exception:
        return None


def safe_script_path(relative: str) -> Path:
    candidate = (ROOT / relative).resolve()
    scripts_root = (ROOT / "scripts").resolve()
    if scripts_root != candidate and scripts_root not in candidate.parents:
        raise ValueError(f"Script outside scripts/: {relative}")
    if candidate.suffix.lower() != ".py":
        raise ValueError(f"Only Python scripts are allowed: {relative}")
    if not candidate.is_file():
        raise FileNotFoundError(candidate)
    return candidate


def validate_job(job: dict[str, Any], config: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    run_id = job.get("run_id")
    suite = job.get("suite")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("job.run_id must be a non-empty string")
    if any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_." for c in run_id):
        raise ValueError("run_id contains unsupported characters")
    if not isinstance(suite, str) or suite not in config["allowed_jobs"]:
        raise ValueError(f"suite is not allowlisted: {suite!r}")
    suite_cfg = config["allowed_jobs"][suite]
    safe_script_path(suite_cfg["script"])
    args = job.get("args", [])
    if not isinstance(args, list) or not all(isinstance(x, str) for x in args):
        raise ValueError("job.args must be an array of strings")
    env = job.get("env", {})
    if not isinstance(env, dict):
        raise ValueError("job.env must be an object")
    allowed_env = set(config.get("environment_allowlist", []))
    unexpected = set(env) - allowed_env
    if unexpected:
        raise ValueError(f"environment keys not allowed: {sorted(unexpected)}")
    return run_id, suite_cfg


def execute_job(job_path: Path, config: dict[str, Any]) -> dict[str, Any]:
    job = load_json(job_path)
    run_id, suite_cfg = validate_job(job, config)

    result_root = ROOT / config.get("results_directory", "results") / run_id
    result_root.mkdir(parents=True, exist_ok=False)

    script = safe_script_path(suite_cfg["script"])
    python_exe = config.get("python_executable", sys.executable)
    working_dir = (ROOT / config.get("working_directory", ".")).resolve()
    timeout_s = int(suite_cfg.get("max_runtime_seconds", 3600))

    cmd = [python_exe, str(script), *job.get("args", [])]
    env = os.environ.copy()
    for key, value in job.get("env", {}).items():
        env[key] = str(value)

    metadata: dict[str, Any] = {
        "connector_version": "1.0",
        "run_id": run_id,
        "suite": job["suite"],
        "job_file": job_path.as_posix(),
        "job_sha256": sha256_file(job_path),
        "git_commit": git_commit(),
        "host": os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME") or "unknown",
        "python": sys.version,
        "command": cmd,
        "started_utc": utc_now(),
        "status": "RUNNING",
    }
    write_json(result_root / "metadata.json", metadata)

    start = time.monotonic()
    try:
        completed = subprocess.run(
            cmd,
            cwd=working_dir,
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout_s,
            shell=False,
        )
        elapsed = time.monotonic() - start
        (result_root / "stdout.log").write_text(completed.stdout, encoding="utf-8", errors="replace")
        (result_root / "stderr.log").write_text(completed.stderr, encoding="utf-8", errors="replace")
        metadata.update(
            {
                "finished_utc": utc_now(),
                "elapsed_seconds": elapsed,
                "return_code": completed.returncode,
                "status": "PASS" if completed.returncode == 0 else "FAIL",
            }
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.monotonic() - start
        (result_root / "stdout.log").write_text(exc.stdout or "", encoding="utf-8", errors="replace")
        (result_root / "stderr.log").write_text(exc.stderr or "", encoding="utf-8", errors="replace")
        metadata.update(
            {
                "finished_utc": utc_now(),
                "elapsed_seconds": elapsed,
                "return_code": None,
                "status": "TIMEOUT",
                "timeout_seconds": timeout_s,
            }
        )
    except Exception as exc:
        metadata.update(
            {
                "finished_utc": utc_now(),
                "elapsed_seconds": time.monotonic() - start,
                "return_code": None,
                "status": "ERROR",
                "error": repr(exc),
            }
        )

    write_json(result_root / "metadata.json", metadata)
    return metadata


def move_job(job_path: Path, destination_dir: Path) -> None:
    destination_dir.mkdir(parents=True, exist_ok=True)
    target = destination_dir / job_path.name
    if target.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        target = destination_dir / f"{job_path.stem}-{stamp}{job_path.suffix}"
    shutil.move(str(job_path), str(target))


def main() -> int:
    parser = argparse.ArgumentParser(description="Safe local REP job runner")
    parser.add_argument("--config", default="connector/config.json")
    parser.add_argument("--job", help="Run one specific job JSON path")
    parser.add_argument("--once", action="store_true", help="Process available inbox jobs once")
    args = parser.parse_args()

    config_path = (ROOT / args.config).resolve()
    if not config_path.is_file():
        print(f"Missing config: {config_path}\nCopy connector/config.example.json to connector/config.json and edit it locally.", file=sys.stderr)
        return 2

    config = load_json(config_path)
    inbox = (ROOT / config.get("jobs_directory", "jobs/inbox")).resolve()
    processed = (ROOT / config.get("processed_directory", "jobs/processed")).resolve()
    failed = (ROOT / config.get("failed_directory", "jobs/failed")).resolve()
    inbox.mkdir(parents=True, exist_ok=True)

    jobs = [Path(args.job).resolve()] if args.job else sorted(inbox.glob("*.json"))
    if not jobs:
        print("No REP jobs found.")
        return 0

    overall = 0
    for job_path in jobs:
        try:
            result = execute_job(job_path, config)
            print(json.dumps(result, ensure_ascii=False))
            if not args.job:
                move_job(job_path, processed if result["status"] == "PASS" else failed)
            if result["status"] != "PASS":
                overall = 1
        except Exception as exc:
            print(f"Job {job_path}: {exc!r}", file=sys.stderr)
            if not args.job and job_path.exists():
                move_job(job_path, failed)
            overall = 1

    return overall


if __name__ == "__main__":
    raise SystemExit(main())
