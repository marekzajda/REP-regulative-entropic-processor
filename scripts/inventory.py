#!/usr/bin/env python3
"""Read-only inventory of the historical REP/RepNet source tree.

The source directory is supplied locally through REP_SOURCE_ROOT so that an
absolute workstation path never has to be committed to the public repository.
No source files are modified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from pathlib import Path

SKIP_DIRS = {
    ".git", ".venv", "venv", "env", "__pycache__", "node_modules",
    ".idea", ".vscode", "dist", "build", ".pytest_cache", ".mypy_cache"
}

DEFAULT_EXTENSIONS = {
    ".py", ".js", ".ts", ".html", ".css", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".md", ".txt", ".csv"
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="Override REP_SOURCE_ROOT for this local run")
    parser.add_argument("--hash", action="store_true", help="SHA-256 each included file")
    parser.add_argument("--max-files", type=int, default=20000)
    args = parser.parse_args()

    source_text = args.source or os.environ.get("REP_SOURCE_ROOT")
    if not source_text:
        raise SystemExit("Set REP_SOURCE_ROOT locally or pass --source.")

    root = Path(source_text).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Source directory does not exist: {root}")

    files = []
    ext_counts: Counter[str] = Counter()
    total_bytes = 0

    for current, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        current_path = Path(current)
        for name in names:
            path = current_path / name
            suffix = path.suffix.lower()
            if suffix not in DEFAULT_EXTENSIONS:
                continue
            try:
                stat = path.stat()
            except OSError:
                continue
            rel = path.relative_to(root).as_posix()
            item = {
                "path": rel,
                "extension": suffix,
                "bytes": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
            }
            if args.hash:
                try:
                    item["sha256"] = sha256(path)
                except OSError:
                    item["sha256"] = None
            files.append(item)
            ext_counts[suffix] += 1
            total_bytes += stat.st_size
            if len(files) >= args.max_files:
                break
        if len(files) >= args.max_files:
            break

    report = {
        "schema": "rep.inventory.v1",
        "source_name": root.name,
        "file_count": len(files),
        "total_bytes": total_bytes,
        "extension_counts": dict(sorted(ext_counts.items())),
        "truncated": len(files) >= args.max_files,
        "files": files,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
