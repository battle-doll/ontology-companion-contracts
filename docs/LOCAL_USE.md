# Validate and convert local ontology files

Use an installed Python 3.11+ interpreter and the complete plugin. [Local MCP setup](LOCAL_MCP.md) exposes the same deterministic operations to Codex without a remote service or API key.

## Validate an artifact

```text
<python> <plugin-root>/scripts/run.py validate <selected-artifact.json>
```

The validator supports `context-decision` and `code-reference` contract `0.1.0-draft.1`. A draft version identifies the format; it does not restrict use to synthetic data. Validation reports performed layers, bounded errors and facts that were not checked. No source locator is fetched and no referenced code is executed.

Context's `local-export` output is directly consumable. Save the exported JSON only where you intend to retain it, then validate that selected file.

## Convert a Code Ontology snapshot

For a raw Code Ontology schema 1.0 snapshot, select the repository identity, supplied Git revision and the symbols or paths to include:

```text
<python> <plugin-root>/scripts/run.py convert-code <ontology.json> --repository-id <repository-id> --revision <known-revision> --path-prefix src --output <new-code-reference.json>
```

Use repeated `--symbol-id` to select known symbol IDs, or repeated `--path-prefix` for source areas. Native `code-ontology-reference` version 1.0.0 artifacts can supply their repository and snapshot metadata. Missing revisions are not invented. Check `convert-code --help` for all selectors.

Conversion returns an artifact, validation result and mapping-loss report. Unsupported or out-of-scope entities and relationships are counted explicitly. A selected projection is not a complete archive. Supplied revisions are annotations: the converter does not prove that the input snapshot belongs to the specified commit.

Without `--output`, results are printed only. With `--output`, the command creates a new file and refuses to overwrite an existing one. Validate the resulting interchange artifact and retain the mapping report beside it when sharing. Very large outputs require a narrower selection; they are not silently truncated.

## Compare versions and plan migration

```text
<python> <plugin-root>/scripts/run.py compatibility --producer-version 0.1.0-draft.1 --consumer-version 0.1.0-draft.1 --profile context-decision
<python> <plugin-root>/scripts/run.py migration-plan <selected-artifact.json> --target-version 0.1.0-draft.1
```

Compatibility reports only supported pairings. Migration currently produces same-version identity plans; it does not overwrite inputs or claim lossless migration between unsupported formats. Code conversion is a separate bounded projection with explicit loss.

## MCP tools

`validate_artifact`, `compare_versions`, `plan_migration` and `convert_code_snapshot` return results without writing selected files. Conversion accepts the chosen snapshot JSON as an argument; it does not inspect arbitrary directories. A successful result does not grant current execution permission or prove source truth, identity or runtime behavior.
