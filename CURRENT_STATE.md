# Current implementation and packaging state

Plugin **0.1.0** supports selected real local ontology artifacts. Its two interchange profiles, `context-decision` and `code-reference`, remain at contract version **0.1.0-draft.1**. The draft version does not prohibit actual local use.

The complete plugin includes the skill, standalone Python 3.11+ CLI, schemas, examples, four local MCP tools, and a project-scoped setup helper. No account, hosted service, sibling plugin, or network access is required for validation and conversion. CLI fallback is available before a host reloads a newly configured MCP connection.

`validate_artifact`, `compare_versions`, `plan_migration`, and `convert_code_snapshot` are read-only MCP computations. The converter accepts selected Code Ontology Companion 0.6.0 snapshots and native reference version 1.0.0. It preserves selected IDs and static evidence, reports omissions, and keeps revision-to-snapshot binding `not_checked`. CLI `--output` creates only an explicitly requested new artifact file.

At this packaging checkpoint, all **71 local tests** pass on macOS Python 3.12.14. Actual current-project static snapshot conversion passes through the CLI and local stdio MCP with identical artifacts and unchanged source bytes. A fresh Codex 0.153.3 host reconnect discovers all four Contracts tools alongside the Context tools and validates the selected Context export. These checks do not establish hosted ChatGPT behavior or current-version Windows/Linux execution.

[Release state](release-state.json) is an immutable pre-publication packaging snapshot. Current-version CI, GitHub deployment, and the new portal draft were pending when the package was built; subsequent outcomes are recorded in the release report. The owner performs portal approval and Publish. Historical evidence remains in its dated files and is not a claim about this version.

[Artifact digests](artifact-manifest.json) · [Current tests](tests/test_code_adapter.py) · [Local MCP setup](docs/LOCAL_MCP.md) · [Submission preparation](chatgpt-app-submission.json)

The submission preparation covers four actual tool descriptors with five positive and three negative review cases. It does not claim a hosted endpoint, remote authentication, a stable contract, or public directory approval for this version.
