#!/usr/bin/env python3
"""Portable checks without downloads or external package dependencies."""
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11 or newer is required; checks were not performed.")
ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    subprocess.run([sys.executable, "-B", *args], cwd=ROOT, check=True)


run("-m", "unittest", "discover", "-s", "tests", "-v")
run("scripts/run.py", "--help")
run("scripts/run.py", "validate", "examples/context-decision.json")
run("scripts/run.py", "validate", "examples/code-reference.json")
run("scripts/artifact_manifest.py")
manifest_path = ROOT / ".codex-plugin/plugin.json"
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["name"] == ROOT.name
    assert manifest["version"] == "0.1.0-draft.1"
    assert (ROOT / "skills/validate-ontology-contract/SKILL.md").is_file()
    assert "mcpServers" not in manifest and "apps" not in manifest
print("Contracts local checks passed. External host integration and public release remain separate gates.")
