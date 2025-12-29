#!/usr/bin/env python3
"""
Update Allure versions in the GitHub workflow.

Fetches the latest Allure 2.x and 3.x versions from GitHub releases
and updates .github/workflows/dockerhub.yml with the latest versions.

Usage:
    python update_allure_versions.py [--dry-run]
    or
    uv run update_allure_versions.py [--dry-run]

Options:
    --dry-run    Show what would be updated without making changes
"""

import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError


def fetch_latest_versions():
    """Fetch latest Allure versions from GitHub API."""
    url = "https://api.github.com/repos/allure-framework/allure2/releases"

    try:
        request = Request(url)
        request.add_header("Accept", "application/vnd.github+json")
        request.add_header("User-Agent", "docker-allure-version-updater")

        with urlopen(request, timeout=10) as response:
            releases = json.loads(response.read().decode())
    except URLError as e:
        print(f"Error fetching releases: {e}", file=sys.stderr)
        print("\nTip: You can also manually check versions at:", file=sys.stderr)
        print("https://github.com/allure-framework/allure2/releases", file=sys.stderr)
        sys.exit(1)

    # Find latest versions for each major version
    latest_2x = None
    latest_3x = None

    for release in releases:
        if release.get("draft") or release.get("prerelease"):
            continue

        tag = release["tag_name"]
        # Remove 'v' prefix if present
        version = tag.lstrip("v")

        # Check if it's a valid version number
        if not re.match(r"^\d+\.\d+\.\d+$", version):
            continue

        major = version.split(".")[0]

        if major == "2" and not latest_2x:
            latest_2x = version
        elif major == "3" and not latest_3x:
            latest_3x = version

        # Stop once we have both
        if latest_2x and latest_3x:
            break

    return latest_2x, latest_3x


def get_current_versions():
    """Get current versions from workflow file."""
    workflow_path = Path(".github/workflows/dockerhub.yml")

    if not workflow_path.exists():
        print(f"Error: Workflow file not found: {workflow_path}", file=sys.stderr)
        sys.exit(1)

    content = workflow_path.read_text()

    current_2x = None
    current_3x = None

    # Extract current 2.x version
    match_2x = re.search(r'- version: "([^"]+)"\s+major: "2"', content)
    if match_2x:
        current_2x = match_2x.group(1)

    # Extract current 3.x version
    match_3x = re.search(r'- version: "([^"]+)"\s+major: "3"', content)
    if match_3x:
        current_3x = match_3x.group(1)

    return current_2x, current_3x


def update_workflow(latest_2x, latest_3x, dry_run=False):
    """Update workflow file with new versions."""
    workflow_path = Path(".github/workflows/dockerhub.yml")

    if not workflow_path.exists():
        print(f"Error: Workflow file not found: {workflow_path}", file=sys.stderr)
        sys.exit(1)

    content = workflow_path.read_text()

    # Pattern to match the matrix section
    # We need to update the version values in the matrix
    if latest_2x:
        content = re.sub(
            r'(- version: ")[^"]+(" *\n\s+major: "2")',
            rf'\g<1>{latest_2x}\g<2>',
            content
        )

    if latest_3x:
        content = re.sub(
            r'(- version: ")[^"]+(" *\n\s+major: "3")',
            rf'\g<1>{latest_3x}\g<2>',
            content
        )

    if not dry_run:
        workflow_path.write_text(content)


def main():
    """Main function."""
    dry_run = "--dry-run" in sys.argv

    # Get current versions
    print("Current versions in workflow:")
    current_2x, current_3x = get_current_versions()
    print(f"  Allure 2.x: {current_2x or 'not set'}")
    print(f"  Allure 3.x: {current_3x or 'not set'}")

    # Fetch latest versions
    print("\nFetching latest Allure versions from GitHub...")
    latest_2x, latest_3x = fetch_latest_versions()

    if not latest_2x:
        print("Warning: Could not find latest Allure 2.x version", file=sys.stderr)
    else:
        print(f"  Latest Allure 2.x: {latest_2x}")

    if not latest_3x:
        print("  Info: Allure 3.x not yet released (this is expected)")
    else:
        print(f"  Latest Allure 3.x: {latest_3x}")

    if not latest_2x and not latest_3x:
        print("Error: No versions found", file=sys.stderr)
        sys.exit(1)

    # Check if update is needed
    needs_update = False
    if latest_2x and latest_2x != current_2x:
        print(f"\n→ Allure 2.x update available: {current_2x} → {latest_2x}")
        needs_update = True
    if latest_3x and latest_3x != current_3x:
        print(f"\n→ Allure 3.x update available: {current_3x or 'none'} → {latest_3x}")
        needs_update = True

    if not needs_update:
        print("\n✓ Already at latest versions!")
        return

    # Update workflow
    if dry_run:
        print("\n[DRY RUN] Would update .github/workflows/dockerhub.yml")
        print("Run without --dry-run to apply changes")
    else:
        print("\nUpdating .github/workflows/dockerhub.yml...")
        update_workflow(latest_2x, latest_3x, dry_run=False)
        print("✓ Workflow updated successfully!")

        print("\nNext steps:")
        print("1. Review changes: git diff .github/workflows/dockerhub.yml")
        print("2. Commit and push: git commit -am 'Update Allure versions' && git push")


if __name__ == "__main__":
    main()
