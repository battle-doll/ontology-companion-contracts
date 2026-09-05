# Changelog

## Plugin 0.1.1 — conversation application candidate

- Add the independently discoverable `apply-ontology-contracts` skill and same-bundle helper for applying actual artifact validation to the current conversation.
- Route explicit product selections before generic availability. Keep installation, exposed skill, exposed MCP and verified CLI observations separate; a plan or MCP handoff remains unexecuted.
- Bind validation to the selected file path, content SHA-256 and expected profile. Missing targets, unsupported inputs and profile mismatches remain incomplete instead of falling back to a demonstration.
- Reuse a current-conversation receipt only after a fresh file/digest/profile check and host evidence comparison. The ledger is not persisted and does not authorize or prove an operation by itself.
- Keep Code and Context optional, preserve mapping-loss and unchecked claims, and retain contract version `0.1.0-draft.1`. Conversation application makes no project or global configuration changes.

## Plugin 0.1.0 — local use and Code conversion

- Accept real selected local artifacts while keeping the interchange contract at `0.1.0-draft.1`.
- Add `convert-code` and the read-only `convert_code_snapshot` MCP tool for Code Ontology Companion 0.6.0 snapshots and native selected references version 1.0.0.
- Preserve selected symbol IDs and static evidence, report omitted information, and keep supplied revision binding `not_checked`; conversion never certifies source-to-commit equivalence or runtime behavior.
- Add a project-scoped local MCP setup helper with an existing Python 3.11+ interpreter. The bundled CLI remains available before a new host task loads the connection.
- Allow bounded snapshot inputs up to 16 MiB while retaining the draft artifact's 512 KiB output limit. CLI `--output` creates only an explicitly requested new file and refuses overwrites.
- Verify actual current-project Python snapshot conversion through the CLI and local stdio MCP, including matching artifacts, independent output-schema checks, and source-file preservation. Current-version hosted ChatGPT and OS CI status remain separate release gates.

## Plugin 0.1.0-draft.1 — 2026-09-06 public preview

- Published independent source and a complete skills-only GitHub marketplace package under Apache-2.0.
- Passed all nine CI jobs: macOS, Windows, and Linux with Python 3.11, 3.12, and 3.13 ([run](https://github.com/battle-doll/ontology-companion-contracts/actions/runs/33975563666)).
- Installed from the public GitHub marketplace on macOS Codex 0.153.3 and ran the installed CLI from outside the source checkout.
- Added standalone deterministic plugin ZIP builds, Windows UTF-8 instructions, and five README languages.
- Universal Directory status is tracked in [release-state.json](release-state.json). This remains a synthetic preview, with no production authentication or hosted MCP service.

## Historical local snapshot — 2026-09-05

- Prepared English, Korean, Japanese, Simplified Chinese, and Russian README and documentation entrypoints.
- Added macOS, Windows, and Linux guidance for Python 3.11+; execution evidence remains separate from the supported-platform target.
- Local Python 3.12.14 synthetic tests passed on macOS; Windows/Linux CI is configured but remains `not_run`.
- Passed a manually configured local stdio smoke test with macOS Codex 0.153.3 using labeled trial artifacts. Verified validation, explicit version comparison, and non-writing migration planning through the actual local Codex host. Hosted ChatGPT, plugin marketplace installation/Directory publication, and actual human approval remain unverified.
- Added privacy, security, support, contribution, version, release, and rollback policies plus issue templates.
- Prepared the Apache-2.0 license text for owner confirmation before public release.
- Public source publication, hosted ChatGPT integration, marketplace installation, submission, review approval, and plugin-directory publication remain pending. The local Codex smoke test does not establish production real-data readiness.
