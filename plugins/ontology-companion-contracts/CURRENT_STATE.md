# Current implementation and packaging state

Plugin **0.1.1** is the conversation-application candidate after the published 0.1.0 product. Its two interchange profiles remain `context-decision` and `code-reference` at contract version **0.1.0-draft.1**.

The new [apply-ontology-contracts skill](skills/apply-ontology-contracts/SKILL.md) routes actual current capabilities, validates the selected artifact and continues the task. Its helper distinguishes routing, fresh receipt checks, same-bundle CLI execution and unexecuted MCP handoffs. A matching current-conversation receipt may avoid duplicate validation only after fresh path/digest/profile checking and comparison with the actual prior result. No activation ledger or configuration is persisted.

The existing [validation skill](skills/validate-ontology-contract/SKILL.md), Python 3.11+ CLI, four read-only MCP tools, schemas, Code conversion and explicit local MCP setup remain available. Code and Context are optional independent products. Ordinary conversation application does not install, configure or execute them implicitly.

At this checkpoint, **88 local tests** pass on macOS Python 3.12.14. The candidate helper validates an actual selected bounded artifact through its same-bundle CLI, and its MCP handoff has been dispatched through the actual local stdio server with matching profile and preserved source bytes. A coordinator plan or handoff is not that execution result. Current-host skill discovery, final bundle verification, current-version OS CI and portal actions remain separate gates.

[Release state](release-state.json) records this pre-publication candidate separately from the previous release. Final approval and Publish belong to the owner. Validation remains evidence about structure and profile rules, never truth, runtime behavior or current authority; mapping-loss and unchecked findings remain attached to their original reports.

[Artifact digests](artifact-manifest.json) · [Application tests](tests/test_apply_workflow.py) · [Local MCP setup](docs/LOCAL_MCP.md) · [Submission preparation](chatgpt-app-submission.json)
