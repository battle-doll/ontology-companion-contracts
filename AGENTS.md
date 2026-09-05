# Contracts development instructions

Build `ontology-companion-contracts` as both versioned contract artifacts and a
separately useful public validation plugin. The public-plugin goal is an explicit
user requirement, not an optional renaming of a library.

Read README, docs/CONFORMANCE, docs/VERSIONING, and docs/RELEASE first. This folder
is a design scaffold, not an installable or submitted plugin.

Do not change `code-ontology-companion`, execute analyzed repositories, silently
fetch remote schemas, retain user inputs, or assume permission from a context
record. Code/Context consumers must work without the Contracts plugin installed.

Exercise a minimum common envelope and separate profiles with real consumer
fixtures before freezing a release. Do not copy ContextRecord as a universal
ontology type or change legacy code IDs/co: semantics. Keep unsupported versions
explicitly unsupported.

Implement a deterministic validator with bounded resources and offline schema
resolution. Return per-layer results, errors, and not_checked values. Never
convert an LLM review into a deterministic PASS. Add runtime tests before creating
an installable skill package or submission metadata. The sample SKILL is a draft.

Use the actual host's models/tools and current official plugin docs. Astra can be
assigned architect/reviewer; it is not a runtime requirement. Record real tests,
not inferred completion. Check remote state before any repository creation.
