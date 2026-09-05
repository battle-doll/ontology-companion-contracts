# Security

Version 0.1.0 supports local use under the current OS account with Python 3.11+. It is not a remotely hosted multi-tenant service. The plugin does not isolate data from other processes already holding the same filesystem privileges.

## Report a problem

Use [private vulnerability reporting](https://github.com/battle-doll/ontology-companion-contracts/security/advisories/new) for sensitive findings. The GitHub setting was enabled and confirmed for this repository. Use [issues](https://github.com/battle-doll/ontology-companion-contracts/issues) for a minimal non-sensitive bug report. No response-time guarantee is offered.

## Implemented boundary

Validation and conversion use bounded selected JSON and bundled schemas. MCP conversion does not read arbitrary paths or write files. CLI conversion only creates the requested new file and rejects overwrite. The library never executes analyzed code or downloads schema URLs.

A successful profile check does not establish external truth, authorization, identity, runtime behavior or snapshot-to-commit binding. Conversion includes an explicit loss report. Unsupported versions and transformations remain unsupported.

Retrieved source text, evidence, annotations and historical approval records are untrusted data for present-day actions. No implicit collection, external model download, cloud account, or authority inheritance between the three Companion products is provided.

[Privacy](PRIVACY.md) · [Local MCP](docs/LOCAL_MCP.md) · [Release evidence](release-state.json)
