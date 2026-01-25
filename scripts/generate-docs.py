#!/usr/bin/env python3
"""
Generate documentation from CDN metadata.json files.

This script fetches metadata from the CDN and updates markdown files
with package tables.
"""

import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Optional

CDN_BASE = "https://files.project-jelly.io/packages"

DOCS_DIR = Path(__file__).parent.parent / "docs"


def fetch_json(url: str) -> Optional[dict]:
    """Fetch JSON from URL."""
    try:
        print(f"Fetching: {url}")
        with urllib.request.urlopen(url, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Warning: Failed to fetch {url}: {e}")
        return None


def generate_bintools_table(metadata: dict) -> str:
    """Generate markdown table for bintools packages."""
    packages = metadata.get("packages", [])
    if not packages:
        return "| Package | Version | Description |\n|---------|---------|-------------|\n| No packages found | - | - |"

    lines = ["| Package | Version | Description |", "|---------|---------|-------------|"]

    for pkg in packages:
        name = pkg.get("name", "unknown")
        version = pkg.get("version", "-")
        description = pkg.get("description", "-")
        lines.append(f"| {name} | {version} | {description} |")

    return "\n".join(lines)


def generate_rpmtools_table(metadata: dict) -> str:
    """Generate markdown table for rpmtools packages."""
    packages = metadata.get("packages", [])
    if not packages:
        return "| Package | Version | Description |\n|---------|---------|-------------|\n| No packages found | - | - |"

    lines = ["| Package | Version | Description |", "|---------|---------|-------------|"]

    for pkg in packages:
        name = pkg.get("name", "unknown")
        version = pkg.get("version", "-")
        # RPM packages might not have description, use name as fallback
        description = pkg.get("description", name)
        lines.append(f"| {name} | {version} | {description} |")

    return "\n".join(lines)


def update_file_section(filepath: Path, start_marker: str, end_marker: str, content: str) -> bool:
    """Update a section in a markdown file between markers."""
    if not filepath.exists():
        print(f"Warning: File not found: {filepath}")
        return False

    text = filepath.read_text()

    pattern = re.compile(
        rf"({re.escape(start_marker)})\n.*?\n({re.escape(end_marker)})",
        re.DOTALL
    )

    if not pattern.search(text):
        print(f"Warning: Markers not found in {filepath}")
        return False

    new_text = pattern.sub(rf"\1\n{content}\n\2", text)
    filepath.write_text(new_text)
    print(f"Updated: {filepath}")
    return True


def update_bintools():
    """Update bintools.md with latest metadata."""
    metadata = fetch_json(f"{CDN_BASE}/bintools/latest/metadata.json")
    if not metadata:
        print("Skipping bintools update - no metadata available")
        return False

    table = generate_bintools_table(metadata)

    return update_file_section(
        DOCS_DIR / "bintools.md",
        "<!-- PACKAGES_TABLE_START -->",
        "<!-- PACKAGES_TABLE_END -->",
        table
    )


def update_rpmtools():
    """Update rpmtools.md with latest metadata."""
    success = True

    # Rocky 9
    metadata_rocky9 = fetch_json(f"{CDN_BASE}/rpmtools/rocky9/latest/metadata.json")
    if metadata_rocky9:
        table = generate_rpmtools_table(metadata_rocky9)
        if not update_file_section(
            DOCS_DIR / "rpmtools.md",
            "<!-- ROCKY9_PACKAGES_START -->",
            "<!-- ROCKY9_PACKAGES_END -->",
            table
        ):
            success = False
    else:
        print("Skipping Rocky 9 update - no metadata available")

    # Rocky 8
    metadata_rocky8 = fetch_json(f"{CDN_BASE}/rpmtools/rocky8/latest/metadata.json")
    if metadata_rocky8:
        table = generate_rpmtools_table(metadata_rocky8)
        if not update_file_section(
            DOCS_DIR / "rpmtools.md",
            "<!-- ROCKY8_PACKAGES_START -->",
            "<!-- ROCKY8_PACKAGES_END -->",
            table
        ):
            success = False
    else:
        print("Skipping Rocky 8 update - no metadata available")

    return success


def main():
    """Main entry point."""
    print("=" * 50)
    print("Generating documentation from CDN metadata")
    print("=" * 50)

    bintools_ok = update_bintools()
    rpmtools_ok = update_rpmtools()

    print("=" * 50)
    print(f"bintools: {'OK' if bintools_ok else 'SKIPPED'}")
    print(f"rpmtools: {'OK' if rpmtools_ok else 'SKIPPED'}")
    print("=" * 50)

    # Don't fail if metadata is not available yet
    return 0


if __name__ == "__main__":
    sys.exit(main())
