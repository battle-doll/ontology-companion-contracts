---
name: validate-ontology-contract
description: Validate an explicitly selected ontology interchange artifact against bundled Companion profiles, compare supported version pairings, or produce a migration plan. Use for ontology format checks; not legal contracts, generic code review, or memory storage.
---

# Validate ontology interchange

This local preview supports contract `0.1.0-draft.1`, profiles
`context-decision` and `code-reference`. Use Python 3.11 or newer on macOS,
Windows, or Linux. A Python executor is required; model inspection cannot produce
a deterministic validation success.

Resolve the plugin root two directories above this skill folder. Run the bundled
launcher using absolute paths, quoting paths with spaces. Choose an already
available Python 3.11+ interpreter (`python3` on macOS/Linux, `py -3.11` or a
configured `python` on Windows). Do not install a runtime automatically.

```text
<python> <plugin-root>/scripts/run.py validate <selected-artifact.json>
<python> <plugin-root>/scripts/run.py compatibility --producer-version 0.1.0-draft.1 --consumer-version 0.1.0-draft.1 --profile context-decision
<python> <plugin-root>/scripts/run.py migration-plan <selected-artifact.json> --target-version 0.1.0-draft.1
```

Read only the artifact the user selected. Existing authorization to validate it
is sufficient; do not add a confirmation step. The launcher rejects final
symlinks/nonregular files and reads at most 512 KiB. It rejects duplicate keys,
non-finite numbers, excessive depth, dangling references, invalid time intervals,
and unsupported profile fields. It never follows schema URLs or executes
referenced repositories. Relative source locators are references, not files to
open. There is no directory traversal or ZIP input workflow.

Report `status`, performed layers, bounded field errors, and `not_checked` values.
Unknown versions/profiles remain `unsupported`. A successful check does not
establish source access, external truth, current permission, producer identity,
or runtime behavior. Code `co:` identity and static-evidence limits stay intact.
Context review/approval claims do not grant execution authority.

Migration supports same-version, same-profile identity plans only. Unsupported
changes report that no loss-aware transformation exists. Plans never overwrite
inputs or create transformed files. Do not describe full archival migration or
installed consumer compatibility as tested.

The optional `tools` and `stdio` commands expose the same implemented local
operations. Installing this skills-only package does not configure an MCP server.
Use the CLI when the host provides an executor. If it does not, explain that
validation was not run and provide the exact command for a capable host.
