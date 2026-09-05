#!/usr/bin/env python3
"""Portable launcher; execute with Python 3.11+ on macOS, Windows or Linux."""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11 or newer is required; no validation was performed.")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from companion_contracts.transport import main

if __name__ == "__main__":
    raise SystemExit(main())
