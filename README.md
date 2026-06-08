# Agent Anvil GitHub Action

Run [Agent Anvil](https://github.com/agent-axiom/agent-anvil) scenario suites in GitHub Actions.

Agent Anvil is a CI-first eval harness for tool-using agents. It records model/tool traces, checks tool choice and arguments, grades semantic criteria with OpenAI when enabled, clusters failures, and writes repair plans.

## Quick Start

```yaml
name: Agent Anvil

on:
  pull_request:
  push:
    branches: [main]

jobs:
  agent-anvil:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: agent-axiom/agent-anvil-action@v1
        with:
          scenario: scenarios/external_jsonl_agent.yaml
          offline: "true"
```

## OpenAI Grading

Pass `OPENAI_API_KEY` from repository secrets and omit `offline`.

```yaml
- uses: agent-axiom/agent-anvil-action@v1
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  with:
    scenario: scenarios/refund_agent.yaml
    agent-mode: openai
    trials: "1"
```

## Intentional Regression Demo

Use `expected-exit-code: "1"` when the scenario is supposed to catch a regression.

```yaml
- uses: agent-axiom/agent-anvil-action@v1
  with:
    scenario: scenarios/refund_agent.yaml
    offline: "true"
    agent-mode: offline
    trials: "1"
    expected-exit-code: "1"
```

## Pull Request Comments

```yaml
- uses: agent-axiom/agent-anvil-action@v1
  with:
    scenario: scenarios/tool_safety.yaml
    offline: "true"
    post-pr-comment: "true"
```

The action also appends a compact eval summary and artifact-trust section to the
GitHub Step Summary by default.
Set `compare-baseline` to a prior Agent Anvil run directory when you want the PR
comment to include baseline-vs-latest pass-rate, failure, scenario, and flaky-run
deltas.

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `scenario` | required | Path to the Agent Anvil YAML scenario suite. |
| `runs-dir` | `runs/agent-anvil` | Directory for run artifacts. |
| `offline` | `false` | Use deterministic offline grading instead of OpenAI semantic grading. |
| `agent-mode` | empty | Demo agent mode: `offline` or `openai`. |
| `trials` | empty | Override scenario trial count. |
| `expected-exit-code` | `0` | Expected `anvil run` exit code. |
| `require-manifest` | `true` | Validate `manifest.json` hashes for the generated run. |
| `github-summary` | `true` | Append a GitHub Step Summary. |
| `pr-comment` | `false` | Render a PR comment body to a file. |
| `post-pr-comment` | `false` | Post the PR comment with `gh pr comment`. |
| `pr-comment-path` | `agent-anvil-pr-comment.md` | Output path for the rendered comment body. |
| `compare-baseline` | empty | Optional baseline run directory for compare-aware PR comments. |
| `compare-path` | `agent-anvil-compare.json` | Output path for the generated compare JSON artifact. |
| `python-version` | `3.12` | Python version used by `uvx`. |
| `uv-cache` | `false` | Enable uv dependency caching. |
| `agent-anvil-ref` | `v0.2.56` | Agent Anvil git tag, branch, or commit to install. |
| `install-source` | `git+https://github.com/agent-axiom/agent-anvil` | Package source passed to `uvx --from`. |

## Artifacts

Agent Anvil writes:

- `runs/agent-anvil/latest/report.md`
- `runs/agent-anvil/latest/results.json`
- `runs/agent-anvil/latest/manifest.json`
- `runs/agent-anvil/latest/traces/*.json`
- optional repair plans and PR comment summaries

Use `actions/upload-artifact` if you want to persist them:

```yaml
- uses: actions/upload-artifact@v5
  if: always()
  with:
    name: agent-anvil-runs
    path: runs/agent-anvil
```

## Security

This action runs the configured Agent Anvil scenarios and any external agent commands declared by those scenarios. Treat scenario files and external commands as code, and run untrusted agents in a sandboxed environment.

OpenAI grading sends redacted trace content to the OpenAI API. Use `offline: "true"` for fully local deterministic runs.

## Versioning

Use the major tag for stable workflows:

```yaml
- uses: agent-axiom/agent-anvil-action@v1
```

Pin `agent-anvil-ref` when you want a specific Agent Anvil engine version.
