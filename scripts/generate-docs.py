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
ROCKY9_VERSION = os.environ.get("ROCKY9_VERSION", "")
ROCKY8_VERSION = os.environ.get("ROCKY8_VERSION", "")


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


def main():
    """Main entry point."""
    print("=" * 50)
    print("Generating documentation from CDN metadata")
    print("=" * 50)
    print(f"BINTOOLS_VERSION: {BINTOOLS_VERSION or '(not set)'}")
    print(f"ROCKY9_VERSION: {ROCKY9_VERSION or '(not set)'}")
    print(f"ROCKY8_VERSION: {ROCKY8_VERSION or '(not set)'}")
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

    # rpmtools rocky9
    if ROCKY9_VERSION:
        url = f"{CDN_BASE}/rpmtools/rocky9/{ROCKY9_VERSION}/metadata.json"
        metadata = fetch_json(url)
        if metadata:
            update_section(
                DOCS_DIR / "rpmtools.md",
                "<!-- ROCKY9_PACKAGES_START -->",
                "<!-- ROCKY9_PACKAGES_END -->",
                generate_table(metadata)
            )
    else:
        print("Skipping rocky9 - ROCKY9_VERSION not set")

    # rpmtools rocky8
    if ROCKY8_VERSION:
        url = f"{CDN_BASE}/rpmtools/rocky8/{ROCKY8_VERSION}/metadata.json"
        metadata = fetch_json(url)
        if metadata:
            update_section(
                DOCS_DIR / "rpmtools.md",
                "<!-- ROCKY8_PACKAGES_START -->",
                "<!-- ROCKY8_PACKAGES_END -->",
                generate_table(metadata)
            )
    else:
        print("Skipping rocky8 - ROCKY8_VERSION not set")

    print("=" * 50)
    print("Done")


if __name__ == "__main__":
    main()
