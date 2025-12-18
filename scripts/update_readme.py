#!/usr/bin/env python3
"""Update README `## Database Statistics` block from data/stats.json."""
import json
from pathlib import Path
from datetime import datetime


def load_stats(path="data/stats.json"):
    p = Path(path)
    if not p.exists():
        return None
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def format_time(iso_str):
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return iso_str


def build_block(stats):
    update_time = format_time(stats.get("update_time") or stats.get("update_time_iso") or "")
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
    stats = load_stats(stats_path)
    if not stats:
        print("No stats available; skipping README update")
        return 1

    readme = Path(readme_path)
    content = readme.read_text(encoding="utf-8")

    import re

    # Replace from '## Database Statistics' until the next '---' separator (inclusive)
    pattern = re.compile(r"## Database Statistics.*?\n---", re.S)
    new_block = build_block(stats) + "---"

    if not pattern.search(content):
        # Fallback: append block near top if not found
        content = new_block + "\n\n" + content
    else:
        content = pattern.sub(new_block, content, count=1)

    readme.write_text(content, encoding="utf-8")
    print("README Database Statistics updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(replace_block())
