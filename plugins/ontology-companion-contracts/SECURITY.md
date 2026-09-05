# Security

Status: pre-release development. No supported production release or response-time guarantee is declared.

The local runtime validates draft exchange envelopes and separate Code/Context profiles offline. It reads an explicitly selected JSON file and prints structured results; an optional stdio adapter is implemented for manual host configuration. Local synthetic tests have passed. Public plugin installation, migration execution, real-data use, and actual host integration remain unsupported or pending.

## Report a problem

Do not place exploit details, credentials, private conversations, or other sensitive payloads in a public issue. This local draft has no verified private reporting endpoint. Before public release, the owner must enable and test a private reporting route and replace this notice with the verified route. Do not assume a GitHub Security Advisory endpoint exists merely because the repository has security documentation.

For a non-sensitive development bug, use the local issue template with a minimal synthetic reproduction. For a sensitive finding discovered during local development, retain the reproduction privately and contact the repository owner through an already established private channel.

## Boundaries to preserve

- Validation success is neither factual verification nor permission to act.
- Stored content and model-generated approval flags are untrusted as current execution authority.
- Inputs must remain bounded; unsupported contracts and unexecuted checks must stay explicit.
- Local schema resolution must not silently fetch remote schemas or execute target code.
- Consumers retain their own authentication, project scope, storage, and approval boundaries.

Context's simulated approval flow is restricted to synthetic examples until a trusted host channel is established. Contracts does not certify authorship, runtime behavior, or production authorization. Public service exposure requires a separate threat review and host tests.

[Privacy](PRIVACY.md) · [Release policy](docs/RELEASE_POLICY.md)
