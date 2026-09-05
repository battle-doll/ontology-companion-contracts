# Ontology Companion Contracts — Documentation

[English](README.md) | [한국어](ko/README.md) | [日本語](ja/README.md) | [简体中文](zh-CN/README.md) | [Русский](ru/README.md)

Start with the local preview and its limits. The numbered Context design documents, where present, describe the wider roadmap; they do not expand current runtime support.

- [Try the local preview](../README.md)
- [macOS / Windows / Linux guide](PLATFORMS.md)
- [Architecture and roadmap](ARCHITECTURE_AND_ROADMAP.md)
- [Version policy](VERSION_POLICY.md)
- [Release and rollback](RELEASE_POLICY.md)
- [Security](../SECURITY.md)
- [Privacy](../PRIVACY.md)
- [Support](../SUPPORT.md)
- [Contributing](../CONTRIBUTING.md)
- [Changelog](../CHANGELOG.md)
- [Apache-2.0](../LICENSE)

The local runtime validates draft exchange envelopes and separate Code/Context profiles offline. It reads an explicitly selected JSON file and prints structured results; an optional stdio adapter is implemented for manual host configuration. Local synthetic tests have passed. Public plugin installation, migration execution, real-data use, and actual host integration remain unsupported or pending.

Code, Context, and Contracts are independent products. Consumers may pin or vendor contract artifacts without installing the Contracts plugin. No shared database, inherited permission, automatic cross-plugin call, or change to the existing Code plugin is implied.
