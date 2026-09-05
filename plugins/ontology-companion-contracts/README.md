# Ontology Companion Contracts

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Русский](README.ru.md)

**P1a development preview · [Current publication and verification status](release-state.json)**

Check an ontology exchange document against an explicitly supported contract and receive deterministic, structured diagnostics. Ontology Companion Contracts is being developed as both versioned contract artifacts and an independent public validation plugin.

The local runtime validates draft exchange envelopes and separate Code/Context profiles offline. It reads an explicitly selected JSON file and prints structured results; an optional stdio adapter is implemented for manual host configuration. Local synthetic tests have passed. A manually configured local stdio smoke test passed on macOS with Codex 0.153.3 using labeled trial artifacts. Installation from the public GitHub marketplace and the installed runtime smoke test also passed on macOS. Hosted ChatGPT integration and actual human approval remain unverified; the universal Directory submission is separate and has not been made. Migration execution and production real-data use remain unsupported.

## Install the public preview

The public preview is available now. Install its complete package with a Codex CLI that supports plugins:

```sh
codex plugin marketplace add battle-doll/ontology-companion-contracts
codex plugin add ontology-companion-contracts@ontology-contracts-preview
```

Start a new Codex task and invoke `$validate-ontology-contract` to validate the installed package's `examples/context-decision.json`. Keep the complete bundle; copying only `SKILL.md` omits its runtime and schema assets. Code and Context plugins are not required for this validation.

[Windows quickstart](docs/WINDOWS_QUICKSTART.md) · [Current release state](release-state.json). GitHub marketplace installation and universal Directory publication are separate statuses. The CI evidence below records the linked completed run. Consult the release state for subsequent publication and platform results.

## Try the local preview

Use Python 3.11 or newer from this repository directory. No additional Python packages are required for the preview commands. See the OS guide for a virtual environment and Windows commands.

```sh
python3 --version
python3 scripts/run.py validate examples/context-decision.json
python3 scripts/check.py
```

These commands run local development code. They do not install a plugin or create a hosted service. Example data is synthetic.

## Platforms and evidence

The supported-platform target is **macOS, Windows, and Linux**. Source portability, an executed OS test, and a working plugin host are separate claims. The linked CI run passed all nine OS/Python combinations; host installation is tested separately.

| OS | Execution evidence |
| --- | --- |
| macOS | CI PASS — Python 3.11, 3.12, 3.13 (3/3) |
| Windows | CI PASS — Python 3.11, 3.12, 3.13 (3/3); Windows Codex host installation not tested |
| Linux | CI PASS — Python 3.11, 3.12, 3.13 (3/3); Linux Codex host installation not tested |
| Plugin host integration | macOS Codex 0.153.3 local stdio smoke and public GitHub marketplace installation passed; Windows/Linux host installation, hosted ChatGPT, and actual human approval unverified |

[CI evidence: all 9 jobs passed](https://github.com/battle-doll/ontology-companion-contracts/actions/runs/33975563666).

[macOS / Windows / Linux guide](docs/PLATFORMS.md)

## Product boundaries

Code, Context, and Contracts are independent products. Consumers may pin or vendor contract artifacts without installing the Contracts plugin. No shared database, inherited permission, automatic cross-plugin call, or change to the existing Code plugin is implied.

A validation pass describes only the checks actually performed. It does not prove factual truth, authorship, user authorization, or runtime behavior. Unsupported versions stay unsupported, unexecuted layers stay `not_checked`, and remote schemas are not silently fetched.

## Documentation

[Documentation index](docs/README.md) · [Architecture and roadmap](docs/ARCHITECTURE_AND_ROADMAP.md) · [Version policy](docs/VERSION_POLICY.md) · [Release and rollback](docs/RELEASE_POLICY.md)

[Security](SECURITY.md) · [Privacy](PRIVACY.md) · [Support](SUPPORT.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md)

Licensed under [Apache-2.0](LICENSE). See [release-state.json](release-state.json) for current publication and verification status.
