from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
AGENT_ANVIL_REF = "v0.2.52"


def load_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_action_metadata_defaults_match_documented_release_ref() -> None:
    action = load_yaml(ROOT / "action.yml")
    inputs = action["inputs"]

    assert inputs["agent-anvil-ref"]["default"] == AGENT_ANVIL_REF
    assert inputs["require-manifest"]["default"] == "true"
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert f"| `agent-anvil-ref` | `{AGENT_ANVIL_REF}` |" in readme
    assert "| `require-manifest` | `true` |" in readme


def test_action_uses_stable_external_actions() -> None:
    action = load_yaml(ROOT / "action.yml")
    steps = action["runs"]["steps"]

    uses_refs = [step["uses"] for step in steps if "uses" in step]
    assert uses_refs == ["astral-sh/setup-uv@v8.1.0"]


def test_action_validates_scenario_before_running_eval() -> None:
    action = load_yaml(ROOT / "action.yml")
    run_script = action["runs"]["steps"][1]["run"]

    validate_index = run_script.index('validate --json "${scenario}"')
    run_index = run_script.index('"${anvil[@]}" "${run_args[@]}"')
    assert validate_index < run_index


def test_action_can_require_run_manifest_after_eval() -> None:
    action = load_yaml(ROOT / "action.yml")
    run_step = action["runs"]["steps"][1]
    run_script = run_step["run"]
    env = run_step["env"]

    assert env["AGENT_ANVIL_REQUIRE_MANIFEST"] == "${{ inputs.require-manifest }}"
    assert 'validate_run_args=(validate run "${runs_dir}/latest")' in run_script
    assert 'if [[ "${AGENT_ANVIL_REQUIRE_MANIFEST}" == "true" ]]' in run_script
    assert 'validate_run_args=(validate --require-manifest run "${runs_dir}/latest")' in run_script
    assert '"${anvil[@]}" "${validate_run_args[@]}"' in run_script


def test_repository_runs_metadata_ci() -> None:
    workflow = ROOT / ".github" / "workflows" / "ci.yml"

    assert workflow.exists()
    text = workflow.read_text(encoding="utf-8")
    assert "pytest -q" in text
    assert "tests" in text
