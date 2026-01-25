#!/usr/bin/env python3
"""
Generate documentation from CDN metadata.json files.

This script fetches metadata from the CDN and updates markdown files
with package tables. Versions are read from environment variables
set by the GitHub Actions workflow.
"""

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

CDN_BASE = "https://files.project-jelly.io/packages"
DOCS_DIR = Path(__file__).parent.parent / "docs"

# 환경변수에서 버전 읽기
BINTOOLS_VERSION = os.environ.get("BINTOOLS_VERSION", "")
SNAPTOOLS_VERSION = os.environ.get("SNAPTOOLS_VERSION", "")
RPMTOOLS_OS_VERSIONS = os.environ.get("RPMTOOLS_OS_VERSIONS", "")


def fetch_json(url):
    """Fetch JSON from URL."""
    try:
        print(f"Fetching: {url}")
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Warning: Failed to fetch {url}: {e}")
        return None


def generate_table(metadata):
    """Generate markdown table from package metadata."""
    packages = metadata.get("packages", [])
    if not packages:
        return "| Package | Version | Description |\n|---------|---------|-------------|\n"

    lines = ["| Package | Version | Description |", "|---------|---------|-------------|"]
    for pkg in packages:
        lines.append(f"| {pkg.get('name', '-')} | {pkg.get('version', '-')} | {pkg.get('description', '-')} |")
    return "\n".join(lines)


def update_section(filepath, start, end, content):
    """Update a section in a markdown file between markers."""
    if not filepath.exists():
        print(f"Warning: File not found: {filepath}")
        return False

    text = filepath.read_text()
    pattern = re.compile(rf"({re.escape(start)})\n.*?\n({re.escape(end)})", re.DOTALL)

    if not pattern.search(text):
        print(f"Warning: Markers not found in {filepath}")
        return False

    new_text = pattern.sub(rf"\1\n{content}\n\2", text)
    filepath.write_text(new_text)
    print(f"Updated: {filepath}")
    return True


def get_rpmtools_version(os_ver):
    """Get rpmtools version for a specific OS version from env var."""
    # 9.5 → RPMTOOLS_9_5_VERSION
    var_name = f"RPMTOOLS_{os_ver.replace('.', '_')}_VERSION"
    return os.environ.get(var_name, "")


def main():
    """Main entry point."""
    print("=" * 50)
    print("Generating documentation from CDN metadata")
    print("=" * 50)
    print(f"BINTOOLS_VERSION: {BINTOOLS_VERSION or '(not set)'}")
    print(f"SNAPTOOLS_VERSION: {SNAPTOOLS_VERSION or '(not set)'}")
    print(f"RPMTOOLS_OS_VERSIONS: {RPMTOOLS_OS_VERSIONS or '(not set)'}")
    print("=" * 50)

    # bintools
    if BINTOOLS_VERSION:
        url = f"{CDN_BASE}/bintools/{BINTOOLS_VERSION}/metadata.json"
        metadata = fetch_json(url)
        if metadata:
            update_section(
                DOCS_DIR / "bintools.md",
                "<!-- PACKAGES_TABLE_START -->",
                "<!-- PACKAGES_TABLE_END -->",
                generate_table(metadata)
            )
    else:
        print("Skipping bintools - BINTOOLS_VERSION not set")

    # snaptools
    if SNAPTOOLS_VERSION:
        url = f"{CDN_BASE}/snaptools/{SNAPTOOLS_VERSION}/metadata.json"
        metadata = fetch_json(url)
        if metadata:
            update_section(
                DOCS_DIR / "snaptools.md",
                "<!-- PACKAGES_TABLE_START -->",
                "<!-- PACKAGES_TABLE_END -->",
                generate_table(metadata)
            )
    else:
        print("Skipping snaptools - SNAPTOOLS_VERSION not set")

    # rpmtools - 동적 OS 버전 처리
    if RPMTOOLS_OS_VERSIONS:
        for os_ver in RPMTOOLS_OS_VERSIONS.split(","):
            os_ver = os_ver.strip()
            if not os_ver:
                continue

            build_ver = get_rpmtools_version(os_ver)
            if not build_ver:
                print(f"Skipping rpmtools {os_ver} - version not set")
                continue

            # 실제 S3 경로: rpmtools/9.5/{BUILD_DATE}/metadata.json
            url = f"{CDN_BASE}/rpmtools/{os_ver}/{build_ver}/metadata.json"
            metadata = fetch_json(url)
            if metadata:
                # OS 버전에 따른 마커 결정 (9.5 → ROCKY9, 8.10 → ROCKY8)
                major_ver = os_ver.split(".")[0]
                start_marker = f"<!-- ROCKY{major_ver}_PACKAGES_START -->"
                end_marker = f"<!-- ROCKY{major_ver}_PACKAGES_END -->"

                update_section(
                    DOCS_DIR / "rpmtools.md",
                    start_marker,
                    end_marker,
                    generate_table(metadata)
                )
    else:
        print("Skipping rpmtools - RPMTOOLS_OS_VERSIONS not set")

    print("=" * 50)
    print("Done")


if __name__ == "__main__":
    main()
