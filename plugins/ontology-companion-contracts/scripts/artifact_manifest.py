#!/usr/bin/env python3
"""Verify artifact digests; --write intentionally refreshes the local manifest."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def expected():
    paths = [ROOT / "LICENSE"]
    paths += sorted(path for path in (ROOT / "src/companion_contracts").rglob("*")
                    if path.is_file() and "__pycache__" not in path.parts and path.suffix in (".py", ".json"))
    paths += sorted((ROOT / "examples").glob("*.json"))
    return {"contract_version": "0.1.0-draft.1", "state": "local-draft",
            "profiles": ["context-decision", "code-reference"],
            "license": "Apache-2.0",
            "assurance": "File digests identify this artifact only; no signature, truth, authorization, or consumer runtime proof.",
            "files": {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Refresh artifact-manifest.json after an intentional source change.")
    args = parser.parse_args()
    path = ROOT / "artifact-manifest.json"
    value = expected()
    if args.write:
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("Wrote local artifact digest manifest.")
        return 0
    if not path.exists() or json.loads(path.read_text(encoding="utf-8")) != value:
        print("Artifact manifest mismatch; review changes before explicit --write.")
        return 1
    print("Artifact digest manifest verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
