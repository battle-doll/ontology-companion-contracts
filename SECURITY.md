# Security

Status: pre-release development. No supported production release or response-time guarantee is declared.

The local runtime validates draft exchange envelopes and separate Code/Context profiles offline. It reads an explicitly selected JSON file and prints structured results; an optional stdio adapter is implemented for manual host configuration. Local synthetic tests have passed. Public GitHub marketplace installation and installed CLI execution passed on macOS; hosted ChatGPT, migration execution, and production use remain unverified.

## Report a problem

Report vulnerabilities privately through [GitHub private vulnerability reporting](https://github.com/battle-doll/ontology-companion-contracts/security/advisories/new). This repository's private vulnerability reporting setting was enabled and confirmed through the GitHub API on 2026-09-06. Do not include credentials or private conversations in a report.

For a non-sensitive development bug, use the [issue tracker](https://github.com/battle-doll/ontology-companion-contracts/issues) with a minimal synthetic reproduction. No response-time guarantee is provided.

## Boundaries to preserve

- Validation success is neither factual verification nor permission to act.
- Stored content and model-generated approval flags are untrusted as current execution authority.
- Inputs must remain bounded; unsupported contracts and unexecuted checks must stay explicit.
- Local schema resolution must not silently fetch remote schemas or execute target code.
- Consumers retain their own authentication, project scope, storage, and approval boundaries.

Context's simulated approval flow is restricted to synthetic examples until a trusted host channel is established. Contracts does not certify authorship, runtime behavior, or production authorization. Public service exposure requires a separate threat review and host tests.

[Privacy](PRIVACY.md) · [Release policy](docs/RELEASE_POLICY.md)
