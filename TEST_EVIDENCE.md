# Test evidence — 2026-09-05

Executed on macOS Python 3.12.14: 41 product tests passed using `python -B scripts/check.py`, including an independent jsonschema comparison in the isolated dev environment. [Raw log](tests/local-test-evidence.txt). Both Context and Code profile CLI examples and artifact-manifest digests passed. Official local plugin and Skill validators passed.

Context's actual exported synthetic decisions were validated by the standalone validator and by its identical digest-pinned vendored copy. The Code profile fixture preserves the inspected Code commit/schema/ID evidence semantics; it does not prove full installed Code consumer integration or runtime truth. [Fixture provenance](examples/code-reference.provenance.json).

Independent reviewer mutation tests ran 600 malformed JSON value cases and found no uncaught exception in that corpus. Exact layer semantics, source truth/auth not_checked, no-network schema handling, duplicate keys, depth/bytes/count/Unicode boundaries, unsupported versions/migrations, malformed requests and output schemas were exercised. This remains bounded testing, not a complete security audit.

Source preview runs without installing a sibling plugin. Windows/Linux CI is configured but not_run; no public hosting, actual plugin host integration, stable contract release, directory submission or publication was performed. Source listing, prototype behavior and actual release evidence remain distinct in release-state.json.

## Current-project application

[Local Codex trial](docs/LOCAL_CODEX_TRIAL.md): 160 lifecycle assertions, 46 schema-validated tool responses, 10 unique tools invoked through Codex 0.153.3 app-server. Explicit simulation approval; hosted ChatGPT and real human approval not verified.
