#!/usr/bin/env python3
"""
Generate packages.json from CDN metadata.json files.

This script fetches metadata from the CDN and generates a packages.json file
for the static HTML documentation site. Versions are read from environment
variables set by the GitHub Actions workflow (S3 single source of truth).
"""

import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CDN_BASE = "https://files.project-jelly.io/packages"
DOCS_DIR = Path(__file__).parent.parent / "docs"
OUTPUT_FILE = DOCS_DIR / "data" / "packages.json"


def fetch_json(url):
    """Fetch JSON from URL."""
    try:
        print(f"Fetching: {url}")
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Warning: Failed to fetch {url}: {e}")
        return None


def build_bintools_data(version):
    """Build bintools data structure."""
    if not version:
        return None

    download_url = f"{CDN_BASE}/bintools/{version}/bintools"
    metadata_url = f"{CDN_BASE}/bintools/{version}/metadata.json"
    metadata = fetch_json(metadata_url)

    packages = []
    if metadata and "packages" in metadata:
        packages = metadata["packages"]

    return {
        "name": "bintools",
        "description": "Go 바이너리 패키지 관리자",
        "version": version,
        "download_url": download_url,
        "packages": packages
    }


def build_rpmtools_data(rpmtools_data):
    """Build rpmtools data structure."""
    if not rpmtools_data:
        return None

    os_versions = {}
    for os_ver, build_ver in rpmtools_data.items():
        download_url = f"{CDN_BASE}/rpmtools/{os_ver}/{build_ver}/rpmtools-bundle"
        metadata_url = f"{CDN_BASE}/rpmtools/{os_ver}/{build_ver}/metadata.json"
        metadata = fetch_json(metadata_url)

        packages = []
        if metadata and "packages" in metadata:
            packages = metadata["packages"]

        os_versions[os_ver] = {
            "build": build_ver,
            "download_url": download_url,
            "packages": packages
        }

    return {
        "name": "rpmtools",
        "description": "RPM 패키지 번들러",
        "os_versions": os_versions
    }


def build_snaptools_data(version):
    """Build snaptools data structure."""
    if not version:
        return None

    download_url = f"{CDN_BASE}/snaptools/{version}/snaptools-bundle"
    metadata_url = f"{CDN_BASE}/snaptools/{version}/metadata.json"
    metadata = fetch_json(metadata_url)

    packages = []
    if metadata and "packages" in metadata:
        packages = metadata["packages"]

    return {
        "name": "snaptools",
        "description": "Snap 패키지 번들러",
        "version": version,
        "download_url": download_url,
        "packages": packages
    }


def main():
    """Main entry point."""
    # Read version info from environment variables
    bintools_version = os.environ.get("BINTOOLS_VERSION", "")
    snaptools_version = os.environ.get("SNAPTOOLS_VERSION", "")
    rpmtools_data_str = os.environ.get("RPMTOOLS_DATA", "{}")

    try:
        rpmtools_data = json.loads(rpmtools_data_str)
    except json.JSONDecodeError:
        print(f"Warning: Failed to parse RPMTOOLS_DATA: {rpmtools_data_str}")
        rpmtools_data = {}

    print("=" * 50)
    print("Generating packages.json from S3 metadata")
    print("=" * 50)
    print(f"BINTOOLS_VERSION: {bintools_version or '(not set)'}")
    print(f"SNAPTOOLS_VERSION: {snaptools_version or '(not set)'}")
    print(f"RPMTOOLS_DATA: {rpmtools_data or '(not set)'}")
    print("=" * 50)

    # Build output structure
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cdn_base": CDN_BASE,
        "tools": {}
    }

    # Add bintools
    bintools_data = build_bintools_data(bintools_version)
    if bintools_data:
        output["tools"]["bintools"] = bintools_data

    # Add rpmtools
    rpmtools_result = build_rpmtools_data(rpmtools_data)
    if rpmtools_result:
        output["tools"]["rpmtools"] = rpmtools_result

    # Add snaptools
    snaptools_data = build_snaptools_data(snaptools_version)
    if snaptools_data:
        output["tools"]["snaptools"] = snaptools_data

    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Write JSON file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Generated: {OUTPUT_FILE}")
    print("=" * 50)
    print("Done")


if __name__ == "__main__":
    main()
