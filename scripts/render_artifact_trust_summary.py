from __future__ import annotations

import json
import sys
from typing import Any


def render(payload: dict[str, Any]) -> str:
    trust = payload.get("artifact_trust") or {}
    lines = ["", "### Artifact trust"]

    trace_status = "verified" if trust.get("trace_index_verified") else "not verified"
    lines.append(f"- Trace index: {trace_status}")

    if trust.get("manifest_present"):
        count = trust.get("manifest_file_count", 0)
        verified = (
            trust.get("manifest_hashes_verified") == count
            and trust.get("manifest_sizes_verified") == count
            and trust.get("manifest_coverage_verified")
        )
        if verified:
            lines.append(f"- Manifest: verified {count} artifacts")
        else:
            lines.append(f"- Manifest: present {count} artifacts")
    else:
        requirement = "required" if trust.get("manifest_required") else "optional"
        lines.append(f"- Manifest: not present ({requirement})")

    return "\n".join(lines) + "\n"


def main() -> int:
    payload = json.load(sys.stdin)
    sys.stdout.write(render(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
