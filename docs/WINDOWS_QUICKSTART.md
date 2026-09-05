# Windows quickstart — PowerShell

Use Python 3.11 or newer and the complete plugin package. No Docker, Node.js, API key or administrator access is required for the local workflow.

## Install and connect

```powershell
codex plugin marketplace add battle-doll/ontology-companion-contracts
codex plugin marketplace upgrade ontology-contracts-preview
codex plugin add ontology-companion-contracts@ontology-contracts-preview
```

The installation prints the installed plugin directory. Alternatively, extract the complete `*-plugin.zip` from [GitHub Releases](https://github.com/battle-doll/ontology-companion-contracts/releases). Keep `scripts`, `src`, `skills`, examples and all bundled schema resources together. Copying only `SKILL.md` is insufficient.

Set the paths below to the installed or extracted bundle and the project you want to use:

```powershell
$CompanionPlugin = "C:\path\ontology-companion-contracts"
$CompanionProject = "C:\path\My Project"
py -3.12 --version
py -3.12 -X utf8 -B "$CompanionPlugin\scripts\setup_mcp.py" --project-root "$CompanionProject" --install
```

If Python 3.11 is installed, replace `py -3.12` with `py -3.11`. If the Python launcher is unavailable, use an existing Python 3.11+ executable with PowerShell's call operator:

```powershell
& "C:\Path To Python\python.exe" -X utf8 -B "$CompanionPlugin\scripts\setup_mcp.py" --project-root "$CompanionProject" --install
```

Open a new Codex task in the selected project and invoke `$validate-ontology-contract`. The setup helper writes only its owned server block in that project's `.codex\config.toml` and preserves other settings. After a plugin update, rerun the helper from the new installed version to refresh the MCP command path.

## Validate or convert directly

```powershell
py -3.12 -X utf8 -B "$CompanionPlugin\scripts\run.py" validate "C:\path\selected-context-export.json"
py -3.12 -X utf8 -B "$CompanionPlugin\scripts\run.py" convert-code "C:\path\ontology.json" --repository-id "selected-repository" --revision "KNOWN_GIT_REVISION" --path-prefix src --output "C:\path\new-code-reference.json"
```

Replace `KNOWN_GIT_REVISION` with the actual supplied revision. Conversion does not establish snapshot-to-commit binding; retain its mapping-loss report. Output must be a new file. Native Code reference exports can supply their own repository metadata; consult `convert-code --help` for selectors.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Python runtime is missing or older than 3.11 | Select an already installed supported interpreter. |
| MCP tools are absent after setup | Open a new task in the configured project; use the CLI meanwhile. |
| Module or schema is missing | Extract the full bundle and preserve its directory structure. |
| A path with spaces fails | Quote it; use `&` when calling a quoted Python executable. |
| JSON text is garbled or rejected for a BOM | Keep `-X utf8` and write UTF-8 without a BOM. |

Native Windows and WSL are separate runtimes. Keep their Python executables, project paths and storage locations separate.

[Local MCP](LOCAL_MCP.md) · [Usage](LOCAL_USE.md) · [Support](../SUPPORT.md)
