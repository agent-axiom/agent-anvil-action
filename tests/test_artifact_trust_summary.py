from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_artifact_trust_summary.py"


def render_summary(payload: dict[str, object]) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload),
        text=True,
        check=True,
        capture_output=True,
    )
    return result.stdout


def test_render_artifact_trust_summary_for_verified_manifest() -> None:
    summary = render_summary(
        {
            "artifact_trust": {
                "trace_index_verified": True,
                "manifest_present": True,
                "manifest_required": True,
                "manifest_file_count": 5,
                "manifest_hashes_verified": 5,
                "manifest_sizes_verified": 5,
                "manifest_coverage_verified": True,
            }
        }
    )

    assert "### Artifact trust" in summary
    assert "- Trace index: verified" in summary
    assert "- Manifest: verified 5 artifacts" in summary


def test_render_artifact_trust_summary_for_missing_required_manifest() -> None:
    summary = render_summary(
        {
            "artifact_trust": {
                "trace_index_verified": True,
                "manifest_present": False,
                "manifest_required": True,
            }
        }
    )

    assert "- Trace index: verified" in summary
    assert "- Manifest: not present (required)" in summary
