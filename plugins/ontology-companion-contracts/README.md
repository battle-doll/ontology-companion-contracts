# Ontology Companion Contracts

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Русский](README.ru.md)

Validate Context and Code interchange artifacts offline, compare supported contract versions, and convert selected Code Ontology data into a `code-reference` artifact with an explicit report of information lost in the conversion.

Runs on macOS, Windows and Linux with Python 3.11 or newer. Works independently of the Code and Context plugins; no API key or remote service is required.

## Install

```text
codex plugin marketplace add battle-doll/ontology-companion-contracts
codex plugin add ontology-companion-contracts@ontology-contracts-preview
```

Install the complete plugin so its skill, server and schemas stay together.

## Connect your project

Open your project in Codex and send:

```text
$validate-ontology-contract
Set up this plugin's local MCP connection for the current project.
```

Then open a new task in the same project to use the MCP tools. For direct setup commands, installed plugin paths and operating system details, see [Local MCP setup](docs/LOCAL_MCP.md) or the [Windows quickstart](docs/WINDOWS_QUICKSTART.md).

## Use it

For a selected file in your project, replace the filename in this request:

```text
$validate-ontology-contract
Validate context-export.json and explain any format errors.
```

To convert a selected Code Ontology snapshot:

```text
$validate-ontology-contract
Convert ontology.json to a code-reference artifact, selecting the src path.
Show the information omitted by the conversion.
Ask me for any required repository identity or revision that the input does not provide.
```

The [local usage guide](docs/LOCAL_USE.md) covers validation, conversion, version comparison and migration planning, including CLI commands for use without MCP. CLI conversion can create a new output file; it does not overwrite existing files.

Supported interchange format: `0.1.0-draft.1`, with `context-decision` and `code-reference` profiles. Code conversion accepts snapshots produced by Code Ontology Companion `0.6.0`: raw schema `1.0` snapshots or native `code-ontology-reference` version `1.0.0` artifacts. Select symbols or paths to keep output focused; omitted data is reported.

Validation checks structure and profile rules. It does not establish factual accuracy, prove that a supplied revision matches a snapshot, or describe runtime behavior. Referenced code is never executed and remote schemas are not fetched. Cloud-only hosts need a separate connection to the local runtime.

## Update

```text
codex plugin marketplace upgrade ontology-contracts-preview
codex plugin add ontology-companion-contracts@ontology-contracts-preview
```

Repeat the project connection request above after updating, then open a new task so the connection uses the installed version.

## Help

[Documentation](docs/README.md) · [Support](SUPPORT.md) · [Privacy](PRIVACY.md) · [Security](SECURITY.md) · [Changelog](CHANGELOG.md)

Licensed under [Apache-2.0](LICENSE).
