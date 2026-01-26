#!/usr/bin/env python3
"""Aggregate S3 metadata into docs/data/packages.json.

Reads metadata.json files from S3 for each tool and produces a single
packages.json consumed by the GitHub Pages frontend.

Environment variables:
    S3_BUCKET   - S3 bucket name (e.g. jelly-prd-cdn-static)
    S3_PREFIX   - Key prefix (e.g. packages)
    CDN_BASE    - Public CDN URL base (e.g. https://files.project-jelly.io/packages)
    OUTPUT_FILE - Output path (e.g. docs/data/packages.json)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Tool registry
#   type: "simple"       → {tool}/{BUILD_DATE}/metadata.json
#   type: "os_versioned" → {tool}/{OS_VER}/{BUILD_DATE}/metadata.json
# ---------------------------------------------------------------------------
TOOLS: dict[str, dict] = {
    "bintools": {
        "type": "simple",
        "description": "Go 바이너리 패키지 관리자",
    },
    "snaptools": {
        "type": "simple",
        "description": "Snap 패키지 번들러",
    },
    "rpmtools": {
        "type": "os_versioned",
        "description": "RPM 패키지 번들러",
    },
}

# ---------------------------------------------------------------------------
# Configuration from environment
# ---------------------------------------------------------------------------
S3_BUCKET = os.environ.get("S3_BUCKET", "jelly-prd-cdn-static")
S3_PREFIX = os.environ.get("S3_PREFIX", "packages").strip("/")
CDN_BASE = os.environ.get("CDN_BASE", "https://files.project-jelly.io/packages").rstrip("/")
OUTPUT_FILE = os.environ.get("OUTPUT_FILE", "docs/data/packages.json")


def s3_base() -> str:
    return f"s3://{S3_BUCKET}/{S3_PREFIX}"


# ---------------------------------------------------------------------------
# S3 helpers
# ---------------------------------------------------------------------------
def s3_list_prefixes(path: str) -> list[str]:
    """Return subdirectory names under *path* using ``aws s3 ls``.

    Parses lines with the ``PRE`` marker emitted by ``aws s3 ls``.
    """
    result = subprocess.run(
        ["aws", "s3", "ls", f"{path}/"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"  [warn] s3 ls failed for {path}: {result.stderr.strip()}", file=sys.stderr)
        return []

    prefixes: list[str] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("PRE "):
            name = line[4:].strip().rstrip("/")
            if name:
                prefixes.append(name)
    return prefixes


def get_latest(prefixes: list[str]) -> str | None:
    """Pick the latest BUILD_DATE (YYYYMMDD-HHMM) by lexicographic sort."""
    if not prefixes:
        return None
    return sorted(prefixes)[-1]


def s3_fetch_json(path: str) -> dict | None:
    """Download a JSON file from S3 and return parsed content."""
    result = subprocess.run(
        ["aws", "s3", "cp", path, "-"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"  [warn] s3 cp failed for {path}: {result.stderr.strip()}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"  [warn] invalid JSON from {path}: {exc}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# download_url builders
# ---------------------------------------------------------------------------
def download_url_simple(tool: str, version: str) -> str:
    """simple: {cdn}/{tool}/{ver}/{tool}-{ver}"""
    return f"{CDN_BASE}/{tool}/{version}/{tool}-{version}"


def download_url_os_versioned(tool: str, os_ver: str, build: str) -> str:
    """os_versioned: {cdn}/{tool}/{os_ver}/{build}/{tool}-{os_ver}-{build}"""
    return f"{CDN_BASE}/{tool}/{os_ver}/{build}/{tool}-{os_ver}-{build}"


# ---------------------------------------------------------------------------
# Per-type processors
# ---------------------------------------------------------------------------
def process_simple(tool_name: str, description: str) -> dict | None:
    """Process a *simple* tool: one metadata.json at the latest BUILD_DATE."""
    base = f"{s3_base()}/{tool_name}"
    print(f"[{tool_name}] Listing builds at {base}")

    versions = s3_list_prefixes(base)
    latest = get_latest(versions)
    if latest is None:
        print(f"  [skip] no versions found for {tool_name}")
        return None

    print(f"  Latest build: {latest}")
    meta_path = f"{base}/{latest}/metadata.json"
    meta = s3_fetch_json(meta_path)
    if meta is None:
        return None

    return {
        "name": tool_name,
        "description": description,
        "version": latest,
        "download_url": download_url_simple(tool_name, latest),
        "packages": meta.get("packages", []),
    }


def process_os_versioned(tool_name: str, description: str) -> dict | None:
    """Process an *os_versioned* tool: iterate OS versions, pick latest each."""
    base = f"{s3_base()}/{tool_name}"
    print(f"[{tool_name}] Listing OS versions at {base}")

    os_versions = s3_list_prefixes(base)
    if not os_versions:
        print(f"  [skip] no OS versions found for {tool_name}")
        return None

    os_data: dict[str, dict] = {}
    for os_ver in sorted(os_versions):
        os_base = f"{base}/{os_ver}"
        print(f"  [{os_ver}] Listing builds at {os_base}")

        builds = s3_list_prefixes(os_base)
        latest = get_latest(builds)
        if latest is None:
            print(f"    [skip] no builds for {os_ver}")
            continue

        print(f"    Latest build: {latest}")
        meta_path = f"{os_base}/{latest}/metadata.json"
        meta = s3_fetch_json(meta_path)
        if meta is None:
            continue

        os_data[os_ver] = {
            "build": latest,
            "download_url": download_url_os_versioned(tool_name, os_ver, latest),
            "packages": meta.get("packages", []),
        }

    if not os_data:
        return None

    return {
        "name": tool_name,
        "description": description,
        "os_versions": os_data,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
PROCESSORS = {
    "simple": process_simple,
    "os_versioned": process_os_versioned,
}


def main() -> None:
    tools_output: dict[str, dict] = {}
    failures: list[str] = []

    for tool_name, cfg in TOOLS.items():
        tool_type = cfg["type"]
        description = cfg["description"]
        processor = PROCESSORS[tool_type]

        result = processor(tool_name, description)
        if result is None:
            failures.append(tool_name)
        else:
            tools_output[tool_name] = result

    if not tools_output:
        print("ERROR: No tools produced output. Aborting.", file=sys.stderr)
        sys.exit(1)

    if failures:
        print(f"\nWARNING: Skipped tools with no data: {', '.join(failures)}", file=sys.stderr)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cdn_base": CDN_BASE,
        "tools": tools_output,
    }

    out_path = Path(OUTPUT_FILE)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")

    print(f"\nWrote {out_path} with {len(tools_output)} tool(s)")


if __name__ == "__main__":
    main()
