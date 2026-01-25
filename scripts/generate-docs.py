#!/usr/bin/env python3
"""
Generate documentation from CDN metadata.json files.

This script fetches metadata from the CDN and dynamically generates
markdown content. Versions are read from environment variables
set by the GitHub Actions workflow (S3 single source of truth).
"""

import json
import os
import re
import urllib.request
from pathlib import Path

CDN_BASE = "https://files.project-jelly.io/packages"
DOCS_DIR = Path(__file__).parent.parent / "docs"


def fetch_json(url):
    """Fetch JSON from URL."""
    try:
        print(f"Fetching: {url}")
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Warning: Failed to fetch {url}: {e}")
        return None


def generate_package_table(metadata):
    """Generate markdown table from package metadata."""
    if not metadata:
        return "_No metadata available_"

    packages = metadata.get("packages", [])
    if not packages:
        return "_No packages in metadata_"

    lines = ["| Package | Version | Description |", "|---------|---------|-------------|"]
    for pkg in packages:
        lines.append(f"| {pkg.get('name', '-')} | {pkg.get('version', '-')} | {pkg.get('description', '-')} |")
    return "\n".join(lines)


def update_section(filepath, start_marker, end_marker, content):
    """Update a section in a markdown file between markers."""
    if not filepath.exists():
        print(f"Warning: File not found: {filepath}")
        return False

    text = filepath.read_text()
    pattern = re.compile(rf"({re.escape(start_marker)})\n.*?\n({re.escape(end_marker)})", re.DOTALL)

    if not pattern.search(text):
        print(f"Warning: Markers not found in {filepath}: {start_marker}")
        return False

    new_text = pattern.sub(rf"\1\n{content}\n\2", text)
    filepath.write_text(new_text)
    print(f"Updated: {filepath}")
    return True


def generate_bintools_content(version):
    """Generate bintools download and package content."""
    if not version:
        return "_Version not available_"

    url = f"{CDN_BASE}/bintools/{version}/bintools"
    metadata_url = f"{CDN_BASE}/bintools/{version}/metadata.json"
    metadata = fetch_json(metadata_url)

    lines = [
        f"**Build:** `{version}`",
        "",
        "```bash",
        f'curl -LO "{url}"',
        "chmod +x bintools",
        "```",
        "",
        "---",
        "",
        "## 패키지 목록",
        "",
        generate_package_table(metadata),
    ]
    return "\n".join(lines)


def generate_snaptools_content(version):
    """Generate snaptools download and package content."""
    if not version:
        return "_Version not available_"

    url = f"{CDN_BASE}/snaptools/{version}/snaptools-bundle"
    metadata_url = f"{CDN_BASE}/snaptools/{version}/metadata.json"
    metadata = fetch_json(metadata_url)

    lines = [
        f"**Build:** `{version}`",
        "",
        "```bash",
        f'curl -LO "{url}"',
        "chmod +x snaptools-bundle",
        "```",
        "",
        "---",
        "",
        "## 패키지 목록",
        "",
        generate_package_table(metadata),
    ]
    return "\n".join(lines)


def generate_rpmtools_content(rpmtools_data):
    """Generate rpmtools content - 단일 섹션에 모든 OS 버전 나열."""
    if not rpmtools_data:
        return "_No packages available_"

    lines = []

    # 다운로드 테이블
    lines.append("| OS Version | Build | Download |")
    lines.append("|------------|-------|----------|")
    for os_ver in sorted(rpmtools_data.keys(), reverse=True):
        build_ver = rpmtools_data[os_ver]
        url = f"{CDN_BASE}/rpmtools/{os_ver}/{build_ver}/rpmtools-bundle"
        lines.append(f"| Rocky {os_ver} | `{build_ver}` | [Download]({url}) |")

    # 설치 예시
    lines.append("")
    lines.append("```bash")
    lines.append("# 예시: 다운로드 후 설치")
    first_os = sorted(rpmtools_data.keys(), reverse=True)[0]
    first_build = rpmtools_data[first_os]
    lines.append(f'curl -LO "{CDN_BASE}/rpmtools/{first_os}/{first_build}/rpmtools-bundle"')
    lines.append("chmod +x rpmtools-bundle")
    lines.append("```")

    # 패키지 목록 (OS별)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 패키지 목록")

    for os_ver in sorted(rpmtools_data.keys(), reverse=True):
        build_ver = rpmtools_data[os_ver]
        metadata_url = f"{CDN_BASE}/rpmtools/{os_ver}/{build_ver}/metadata.json"
        metadata = fetch_json(metadata_url)
        lines.append("")
        lines.append(f"### Rocky {os_ver}")
        lines.append("")
        lines.append(generate_package_table(metadata))

    return "\n".join(lines)


def main():
    """Main entry point."""
    # 환경변수에서 버전 정보 읽기
    bintools_version = os.environ.get("BINTOOLS_VERSION", "")
    snaptools_version = os.environ.get("SNAPTOOLS_VERSION", "")
    rpmtools_data_str = os.environ.get("RPMTOOLS_DATA", "{}")

    try:
        rpmtools_data = json.loads(rpmtools_data_str)
    except json.JSONDecodeError:
        print(f"Warning: Failed to parse RPMTOOLS_DATA: {rpmtools_data_str}")
        rpmtools_data = {}

    print("=" * 50)
    print("Generating documentation from S3 metadata")
    print("=" * 50)
    print(f"BINTOOLS_VERSION: {bintools_version or '(not set)'}")
    print(f"SNAPTOOLS_VERSION: {snaptools_version or '(not set)'}")
    print(f"RPMTOOLS_DATA: {rpmtools_data or '(not set)'}")
    print("=" * 50)

    # bintools
    if bintools_version:
        content = generate_bintools_content(bintools_version)
        update_section(
            DOCS_DIR / "bintools.md",
            "<!-- CONTENT_START -->",
            "<!-- CONTENT_END -->",
            content
        )
    else:
        print("Skipping bintools - BINTOOLS_VERSION not set")

    # snaptools
    if snaptools_version:
        content = generate_snaptools_content(snaptools_version)
        update_section(
            DOCS_DIR / "snaptools.md",
            "<!-- CONTENT_START -->",
            "<!-- CONTENT_END -->",
            content
        )
    else:
        print("Skipping snaptools - SNAPTOOLS_VERSION not set")

    # rpmtools
    if rpmtools_data:
        content = generate_rpmtools_content(rpmtools_data)
        update_section(
            DOCS_DIR / "rpmtools.md",
            "<!-- CONTENT_START -->",
            "<!-- CONTENT_END -->",
            content
        )
    else:
        print("Skipping rpmtools - RPMTOOLS_DATA not set")

    print("=" * 50)
    print("Done")


if __name__ == "__main__":
    main()
