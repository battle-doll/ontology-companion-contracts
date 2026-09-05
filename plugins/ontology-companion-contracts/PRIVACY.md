# Privacy

Status: local-development policy draft. No production privacy service or published plugin is claimed.

The validator reads only the selected input for its current operation. Do not treat stdout capture by your terminal, editor, CI, or plugin host as private storage controlled by this validator. The preview does not provide a history archive or a remote upload service. A future remote adapter would require a separate consent and retention policy.

## Data boundaries

Use synthetic fixtures during development. Do not include actual private conversations, credentials, health or payment records, government identifiers, or proprietary source in Git, tests, logs, screenshots, issue attachments, or public release materials.

The intended core workflow is local and does not require telemetry, external LLM enrichment, account creation, or a remote database. Installing or running it through a third-party host does not change that host's own processing rules. Review the chosen host's rules before sharing any content there.

## Retention and deletion

Temporary files, shell history, redirected output, exports, host transcripts, backups, and CI logs can have separate lifecycles. Removing a local database does not erase those copies. Secure erasure, encrypted storage, backup deletion, and host-history deletion are not certified features of this preview.

No real-data migration or cloud deployment is part of the local preview. New persistence, upload, analytics, or enrichment behavior must update this document and undergo explicit review before release.

[Security](SECURITY.md) · [Support](SUPPORT.md) · [Documentation](docs/README.md)
