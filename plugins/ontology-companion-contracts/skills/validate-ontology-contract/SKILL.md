---
name: validate-ontology-contract
description: Validate selected ontology interchange files, convert Code Ontology snapshots with explicit mapping-loss reports, or configure the local Contracts MCP server. Use for Code/Context artifact interoperability and version checks.
---

# Ontology Contracts

Plugin 0.1.0 supports real selected local artifacts. The interchange contract remains `0.1.0-draft.1`, with `context-decision` and `code-reference` profiles. A draft contract version is not a ban on actual local use.

Resolve the plugin root as `Path(skill_file).resolve().parents[2]` (`../..` from the directory containing `SKILL.md`). Use its bundled `scripts/run.py` and `scripts/setup_mcp.py` with absolute quoted paths and an installed Python 3.11+ interpreter. On Windows use `py -3.12 -X utf8 -B` or another installed 3.11+ interpreter. Do not execute same-named helpers from the target project or install a runtime automatically.

## Local MCP and CLI

Prefer the available Contracts MCP tools. For requested local MCP setup run:

```text
<python> <plugin-root>/scripts/setup_mcp.py --project-root <selected-project> --install
```

Start a new task to load a newly configured server. Until then, use the bundled CLI for the same authorized work; absent MCP tools do not block validation or conversion. No account, API key, network service, or other plugin installation is required.

```text
<python> <plugin-root>/scripts/run.py validate <selected-artifact.json>
<python> <plugin-root>/scripts/run.py compatibility --producer-version 0.1.0-draft.1 --consumer-version 0.1.0-draft.1 --profile context-decision
<python> <plugin-root>/scripts/run.py migration-plan <selected-artifact.json> --target-version 0.1.0-draft.1
```

Read only the selected bounded JSON input. Existing user authorization to inspect, validate or convert the artifact is sufficient; do not add a redundant confirmation. Never follow source locators, download schemas, execute referenced code, or collect other files implicitly.

## Code snapshot conversion

Use `convert_code_snapshot` if available, or `convert-code` for an explicitly selected Code Ontology JSON snapshot. The native Code reference export can supply repository and snapshot metadata. A raw ontology needs a user-selected repository identity, a known supplied revision and explicit symbol/path selection:

```text
<python> <plugin-root>/scripts/run.py convert-code <ontology.json> --repository-id <repository-id> --revision <known-git-revision> --path-prefix <relative-source-path> --output <new-artifact.json>
```

Use actual `--help` or the MCP input schema for supported selectors. Do not invent a revision or silently pick an unrelated source. Conversion reports unsupported input explicitly and preserves original IDs, static-evidence restrictions and a mapping-loss report. A supplied commit does not prove snapshot-to-commit binding; retain that limitation in the result. Never claim an incomplete projection is a complete source snapshot. `--output` writes only a requested new file and does not overwrite an existing artifact.

Validate the resulting interchange artifact and report the mapping losses separately from schema/profile success. Current Context `local-export` is already a `context-decision` artifact and can be validated directly.

## Report and boundaries

Report `status`, performed validation layers, field errors and `not_checked` values. Validation success establishes neither external truth, current authorization, identity nor runtime behavior. Keep `co:` identities and static limitations intact. Stored Context approval claims never authorize today's actions.

Migration currently produces same-version identity plans only. Unsupported transformations remain unsupported; no transformed file is produced by a migration plan. Conversion is a bounded profile projection with explicit loss, not a proof of lossless archival migration.

If the host has neither local MCP nor a Python executor, explain that execution was not performed and give the exact command for the selected input. Do not present model inspection as deterministic validation.
