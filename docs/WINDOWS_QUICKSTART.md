# Windows quickstart — PowerShell

You can validate the included synthetic artifacts offline with Python 3.11 or 3.12. No API key, extra Python package, administrator access, other Ontology plugin, operator password, or running server is required. The validator does not modify the selected artifact.

This guide provides a local preview workflow. Check the repository's current CI results for Windows execution evidence; commands in documentation do not establish a Windows test pass. A validation result describes performed format and profile checks, not truth, user approval, or runtime behavior.

## Run the downloaded code immediately

Download the complete source ZIP from the repository or a release, extract it with **Extract All**, and locate the folder containing `scripts`, `src`, and `examples`. Keep the schema assets inside `src\companion_contracts\_schemas`. A ZIP may contain an extra top-level folder such as `ontology-companion-contracts-main`.

In PowerShell, replace the example path with the extracted folder. The quotes handle spaces and Korean characters in paths.

```powershell
Set-Location -LiteralPath "C:\Users\You\Downloads\Ontology Companion Contracts\ontology-companion-contracts"
py -3.12 --version
py -3.12 -X utf8 -B .\scripts\run.py validate .\examples\context-decision.json
py -3.12 -X utf8 -B .\scripts\run.py validate .\examples\code-reference.json
```

If Python 3.11 is installed instead:

```powershell
py -3.11 --version
py -3.11 -X utf8 -B .\scripts\run.py validate .\examples\context-decision.json
```

Do not fall back to an older interpreter. If `py` is unavailable, choose an existing Python 3.11+ executable and use PowerShell's call operator:

```powershell
& "C:\Path To Python\python.exe" --version
& "C:\Path To Python\python.exe" -X utf8 -B .\scripts\run.py validate .\examples\context-decision.json
```

Successful example validation returns `status: valid`. `L3_compatibility` and `external_verification` remain `not_checked` during artifact validation. To check the explicitly supported version pair and request a non-writing migration plan:

```powershell
py -3.12 -X utf8 -B .\scripts\run.py compatibility --producer-version 0.1.0-draft.1 --consumer-version 0.1.0-draft.1 --profile context-decision
py -3.12 -X utf8 -B .\scripts\run.py migration-plan .\examples\context-decision.json --target-version 0.1.0-draft.1
```

The results are `compatible` for that exact bundled pairing and `identity_plan` for that same-version migration. This does not test another installed consumer or execute a migration.

To validate a deliberately selected artifact whose path contains spaces:

```powershell
py -3.12 -X utf8 -B .\scripts\run.py validate "C:\Users\You\Documents\Ontology Samples\selected-artifact.json"
```

Use synthetic or non-sensitive artifacts for this preview. The launcher reads only the selected bounded JSON file and never downloads schema URLs. `invalid` or `unsupported` is a result to inspect, not a reason to replace source data.

From a complete source checkout or source-preview ZIP, run the product checks:

```powershell
py -3.12 -X utf8 -B .\scripts\check.py
```

The installed runtime plugin may omit development tests; use the complete source download for `scripts/check.py`. A virtual environment is optional; activation and PowerShell execution-policy changes are unnecessary.

## Install the complete plugin in Codex

Once the public GitHub repository and its marketplace manifest are available, an installed Codex CLI with plugin support can download the complete package:

```powershell
codex --version
codex plugin marketplace add battle-doll/ontology-companion-contracts
codex plugin add ontology-companion-contracts@ontology-contracts-preview
```

These are installation instructions, not a claim that installation has passed on your Windows machine. If `codex` or its `plugin` command is unavailable, use the direct Python validator above. Do not install only the skill folder with `$skill-installer`: the current skill depends on the full bundled runtime and schema assets.

Start a new Codex task and send:

```text
$validate-ontology-contract
Validate the installed plugin's examples/context-decision.json using an existing Python 3.12 or 3.11 interpreter with UTF-8 enabled. Report performed layers and not_checked fields. Do not modify the artifact or treat validation as approval.
```

You can subsequently name the absolute path of another explicitly selected artifact. Plugin installation supplies the skill and runtime; the optional stdio MCP connection is a separate setup and is not needed for this CLI workflow. Code and Context do not need to be installed.

Codex supports explicitly invoking installed skills with `$` and loads their instructions when selected. See [OpenAI's skills guide](https://learn.chatgpt.com/docs/build-skills) and [plugin guide](https://learn.chatgpt.com/docs/build-plugins) for the host's installation and discovery model. Installing from a GitHub marketplace is distinct from publication in the universal Directory.

## Common Windows issues

| Symptom | Next step |
| --- | --- |
| `No suitable Python runtime found` | Select an already installed 3.11+ interpreter; Python provisioning is separate from this package. |
| Missing `companion_contracts` or schema files | Extract the complete archive and preserve `src`, its `_schemas` directory, and `scripts`. |
| A path with spaces fails | Quote the path and use `&` when invoking a quoted executable. |
| Non-ASCII text behaves differently through a pipe | Keep `-X utf8`; select UTF-8 when saving JSON. |
| The marketplace repository is unavailable | Check whether the public release is available; use the downloaded source validator meanwhile. |

Native Windows PowerShell uses `py` and, if a venv is created, `.venv\Scripts\python.exe`. WSL/Linux is a separate runtime: use `python3` and `.venv/bin/python` there. Do not mix Windows and WSL interpreters or paths. Linux CLI success does not establish a desktop-host test pass.
