# Local verification baseline and current release state

The implementation and test notes below are the **historical local snapshot from 2026-09-05**. Consult [release-state.json](release-state.json) for current GitHub remotes, commits, public artifacts, platform CI, submission, and publication evidence. Historical absences are not current release claims.

The initial distribution route is a **skills-only ZIP** containing the skill and its required offline Python runtime, schemas, and examples. This route does not deploy a hosted MCP server. The user has authorized public release; actual upload, review, and publication outcomes are recorded separately in the release state.

Local draft implemented and tested on macOS Python 3.12.14. Independent CLI/Skill and optional stdio use no account, network, or sibling plugin. Context consumes a digest-pinned copy and validates actual synthetic exports. Code mapping preserves observed public schema semantics but is not full Code consumer integration.

[Runtime tests](tests/local-test-evidence.txt) · [Artifact digests](artifact-manifest.json) · [Consumer review](docs/CONTEXT_CONSUMER_REVIEW.md) · [Release state](release-state.json) · [Submission preparation](submission/IMPLEMENTATION_REVIEW.md)

In that snapshot, Windows/Linux CI was configured but not_run. The workspace's manually configured macOS Codex 0.153.3 app-server stdio smoke passed: all three Contracts tools were invoked, including validation of Context's actual synthetic export. No model turn or real human approval was involved. Later platform results belong in the release state.

At the 2026-09-05 local checkpoint there was no stable contract release, GitHub remote, commit/push, hosting, packaged-plugin installation, hosted ChatGPT E2E, submission, or publication. All five documentation languages and three OS targets had been prepared. This paragraph describes that checkpoint only.

The existing `chatgpt-app-submission.json` and implementation review describe a historical draft for three local MCP tools. They have no hosted ChatGPT execution evidence and are not the submission metadata for the initial skills-only ZIP. See [submission routes](submission/README.md) for that distinction.
