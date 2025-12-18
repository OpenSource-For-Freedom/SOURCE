#!/usr/bin/env python3
"""Update README `## Database Statistics` block from data/stats.json."""
import json
import re
from pathlib import Path
from datetime import datetime


def load_stats(path="data/stats.json"):
    """Load statistics JSON from `path` and return parsed dict or None."""
    p = Path(path)
    if not p.exists():
        return None
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def format_time(iso_str):
    """Convert ISO timestamp to human-readable UTC string when possible."""
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except (ValueError, TypeError):
        return iso_str


def build_block(stats):
    """Build the markdown stats block from a `stats` dict."""
    update_time = format_time(
        stats.get("update_time") or stats.get("update_time_iso") or ""
    )
    total = stats.get("total_ips", 0)
    countries = stats.get("countries_affected") or stats.get("countries") or 0
    severity = stats.get("severity_avg") or stats.get("average_severity") or 0.0

    block = (
        "## Database Statistics\n\n"
        f"- **Total Malicious IPs**: {int(total):,}\n"
        f"- **Countries Affected**: {int(countries)}\n"
        f"- **Average Threat Severity**: {float(severity):.2f}/5\n"
        f"- **Last Updated**: {update_time}\n\n"
    )
    return block


def replace_block(readme_path="README.md", stats_path="data/stats.json"):
    """Replace the `## Database Statistics` block and update Last Generated timestamp in `README.md`."""
    stats = load_stats(stats_path)
    if not stats:
        print("No stats available; skipping README update")
        return 1

    readme = Path(readme_path)
    content = readme.read_text(encoding="utf-8")
    pattern = re.compile(r"## Database Statistics.*?\n---", re.S)
    new_block = build_block(stats) + "---"

    if not pattern.search(content):
        content = new_block + "\n\n" + content
    else:
        content = pattern.sub(new_block, content, count=1)

    # Also update the "Last Generated" timestamp at the bottom
    update_time = format_time(stats.get("update_time") or "")
    timestamp_pattern = re.compile(r"(\*\*Last Generated\*\*:) [^\n]+")
    if timestamp_pattern.search(content):
        content = timestamp_pattern.sub(rf"\1 {update_time}", content)
    else:
        # If pattern doesn't exist, add it at the end before closing div
        content = re.sub(
            r"(Data Sources.*?)\n</div>",
            rf"\1 | **Last Generated**: {update_time}\n</div>",
            content,
            flags=re.S,
        )

    readme.write_text(content, encoding="utf-8")
    print("README Database Statistics updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(replace_block())
