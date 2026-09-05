# Changelog

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
