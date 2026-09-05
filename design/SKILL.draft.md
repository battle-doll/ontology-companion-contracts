# Skill design draft — ontology contract validation

DESIGN_ONLY. This is deliberately not an installable SKILL.md or plugin manifest.

## Trigger

Use for an explicit request to validate an ontology interchange artifact against
a supported Companion schema/profile, inspect a supported version pairing, or
plan a loss-aware migration. Do not trigger for legal contracts, ordinary chat,
generic code review, or storing a user's memories.

## Intended workflow

Confirm the selected artifact and intended profile/version. Check that a supported
deterministic executor is actually available. Enforce size and offline-resolution
limits. Run the implemented validator, report levels performed and not_checked,
and show bounded JSON Pointer errors. A model's visual review is not a validator
PASS. Unknown versions stay unsupported. Do not mutate the input or execute code.

## Prerequisites before packaging

An implemented validator, tests, pinned supported schemas, exact run instructions,
real host capability tests, version/license metadata, and current official plugin
manifest validation. This draft includes no pretend commands or fabricated MCP
names. Resolve those from actual implementation during development.
