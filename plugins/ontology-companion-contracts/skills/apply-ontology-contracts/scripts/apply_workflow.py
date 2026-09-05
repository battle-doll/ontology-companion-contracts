#!/usr/bin/env python3
"""Conversation-only routing, selected-file inspection and same-bundle validation.

Host observations and ledgers are untrusted reports, not authorization or proof
that a tool ran. This helper never invokes another product, configures a host,
writes an activation marker or persists a ledger.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import stat
import sys

sys.dont_write_bytecode = True
PRODUCTS = ("code", "context", "contracts")
CAPABILITY_KEYS = ("installed", "skill_exposed", "mcp_exposed", "verified_cli")
PROFILES = ("context-decision", "code-reference")
MAX_CONTROL_BYTES = 32768


class ApplicationError(ValueError):
    """Bounded diagnostic without reflecting artifact data."""


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ApplicationError("duplicate_control_key")
        result[key] = value
    return result


def _control(text):
    if not isinstance(text, str) or len(text.encode("utf-8")) > MAX_CONTROL_BYTES:
        raise ApplicationError("control_byte_limit")
    try:
        value = json.loads(text, object_pairs_hook=_pairs,
                           parse_constant=lambda _: (_ for _ in ()).throw(ApplicationError("control_number")))
    except (ValueError, UnicodeError, RecursionError):
        raise ApplicationError("invalid_control_json") from None
    pending, count = [(value, 0)], 0
    while pending:
        item, depth = pending.pop()
        count += 1
        if depth > 12 or count > 2000:
            raise ApplicationError("control_structure_limit")
        if isinstance(item, str) and (len(item) > 8192 or any(0xD800 <= ord(c) <= 0xDFFF for c in item)):
            raise ApplicationError("control_string_limit")
        if isinstance(item, float):
            raise ApplicationError("control_number")
        if isinstance(item, (dict, list)):
            if len(item) > 100:
                raise ApplicationError("control_collection_limit")
            pending.extend((part, depth + 1) for part in (list(item) + list(item.values()) if isinstance(item, dict) else item))
    return value


def observations(value):
    if not isinstance(value, dict) or set(value) - set(PRODUCTS):
        raise ApplicationError("capability_products")
    result = {}
    for product in PRODUCTS:
        entry = value.get(product, {})
        if not isinstance(entry, dict) or set(entry) - set(CAPABILITY_KEYS) or any(type(v) is not bool for v in entry.values()):
            raise ApplicationError("capability_booleans")
        result[product] = {key: entry.get(key, False) for key in CAPABILITY_KEYS}
    return result


def ledger_entries(value):
    if value is None:
        return {}
    if not isinstance(value, dict) or set(value) != {"version", "products"} or type(value["version"]) is not int or value["version"] != 1:
        raise ApplicationError("ledger_version")
    entries = value["products"]
    if not isinstance(entries, dict) or set(entries) - set(PRODUCTS):
        raise ApplicationError("ledger_products")
    for entry in entries.values():
        if (not isinstance(entry, dict) or set(entry) != {"request_key", "status", "evidence"}
                or entry["status"] not in ("pending", "verified", "incomplete")
                or not isinstance(entry["evidence"], dict)):
            raise ApplicationError("ledger_entry")
        _request_key(entry["request_key"])
    return entries


def _request_key(value):
    if not isinstance(value, str) or not 1 <= len(value) <= 160 or any(ord(c) < 33 or ord(c) == 127 for c in value):
        raise ApplicationError("request_key")
    return value


def _scope():
    return {"application": "session_only", "persistentActivation": False,
            "agentsFilesChanged": False, "globalConfigurationChanged": False,
            "otherProductsExecuted": False, "workspaceWrites": "none",
            "targetCodeExecuted": False, "networkAccess": False, "ledgerPersisted": False}


def _available(product, entry):
    return (product == "contracts" or entry["skill_exposed"]) and (entry["mcp_exposed"] or entry["verified_cli"])


def plan(capabilities, *, explicit_products=None, ledger=None):
    observed, entries = observations(capabilities), ledger_entries(ledger)
    explicit = explicit_products or []
    if not isinstance(explicit, list) or any(product not in PRODUCTS for product in explicit):
        raise ApplicationError("explicit_products")
    explicit = list(dict.fromkeys(explicit))
    available = [p for p in PRODUCTS if _available(p, observed[p])]
    selected = explicit or available
    routes = []
    for product in selected:
        prior = entries.get(product, {}).get("status") == "verified"
        route = ("unavailable" if product not in available else "already_applied_recheck_freshness" if prior else
                 "host_mcp_handoff" if observed[product]["mcp_exposed"] else
                 "verified_sibling_cli" if product == "contracts" else "host_cli_handoff")
        routes.append({"product": product, "route": route, "executionPerformed": False,
                       "activationStatus": "NOT_EXECUTED", "observedAvailable": product in available,
                       "capabilityBasis": "host_observation_only", "ledgerBasis": "host_current_conversation_report" if prior else None})
    return {"status": "planned", "activationStatus": "NOT_EXECUTED", "executionPerformed": False,
            "selectionBasis": "explicit_product" if explicit else "observed_availability",
            "selectedProducts": selected, "observedAvailableProducts": available, "availableCount": len(available),
            "unavailableProducts": [p for p in PRODUCTS if p not in available], "observations": observed,
            "routes": routes, "scope": _scope()}


def _regular(root, relative):
    current = root
    for part in ("", *Path(relative).parts):
        current = current / part
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ApplicationError("untrusted_bundle_link")
        if current != root / relative and not stat.S_ISDIR(info.st_mode):
            raise ApplicationError("untrusted_bundle_layout")
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise ApplicationError("untrusted_bundle_file")
    return current


def _validator():
    root = Path(__file__).absolute().parents[3]
    helper = _regular(root, "skills/apply-ontology-contracts/scripts/apply_workflow.py")
    if helper.absolute() != Path(__file__).absolute():
        raise ApplicationError("untrusted_bundle_layout")
    manifest = _control(_regular(root, ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("name") != "ontology-companion-contracts":
        raise ApplicationError("untrusted_bundle_identity")
    if not isinstance(manifest.get("version"), str) or not 1 <= len(manifest["version"]) <= 80:
        raise ApplicationError("untrusted_bundle_version")
    for name in ("envelope", *PROFILES):
        _regular(root, "src/companion_contracts/_schemas/" + name + ".schema.json")
    path = _regular(root, "src/companion_contracts/validator.py")
    spec = importlib.util.spec_from_file_location("_same_bundle_contract_validator", path)
    if spec is None or spec.loader is None:
        raise ApplicationError("untrusted_validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, manifest["version"]


def _base():
    return {"status": "incomplete", "activationStatus": "NOT_EXECUTED", "executionPerformed": False,
            "validation": None, "binding": None, "issues": [], "scope": _scope(),
            "receiptReuseEligible": False, "receiptReused": False,
            "ledgerBasis": "host_current_conversation_report_only"}


def _selected(result, validator, artifact, profile, request_key, ledger):
    entries = ledger_entries(ledger)
    missing = [name for name, value in (("artifact", artifact), ("profile", profile), ("request_key", request_key)) if value is None]
    if missing:
        result.update(status="needs_input", issues=["missing_" + name for name in missing])
        return None
    _request_key(request_key)
    if profile not in PROFILES:
        result.update(status="unsupported", issues=["unsupported_requested_profile"])
        return None
    path = Path(artifact).absolute()
    raw = validator.read_artifact(path)
    if len(raw) > validator.MAX_BYTES:
        result["issues"] = ["artifact_byte_limit"]
        return None
    result["binding"] = {"artifact_path": str(path), "artifact_sha256": hashlib.sha256(raw).hexdigest(), "profile": profile}
    prior = entries.get("contracts", {})
    evidence = prior.get("evidence", {})
    result["receiptReuseEligible"] = (prior.get("status") == "verified" and prior.get("request_key") == request_key
        and all(evidence.get(key) == value for key, value in result["binding"].items())
        and evidence.get("validation_status") == "valid")
    return raw


def _profile_issues(validator, raw, profile):
    try:
        document = validator._parse(raw)
    except validator.InvalidInput:
        return ["artifact_parse_failed"]
    if not isinstance(document, dict) or document.get("profile") != profile:
        return ["artifact_profile_mismatch"]
    return []


def inspect_target(*, artifact=None, profile=None, request_key=None, ledger=None):
    """Fresh read and digest only. Matching reported receipts still need host proof."""
    result = _base()
    try:
        validator, _ = _validator()
        raw = _selected(result, validator, artifact, profile, request_key, ledger)
        if raw is None:
            return result
        result["issues"] = _profile_issues(validator, raw, profile)
        if result["issues"]:
            result["receiptReuseEligible"] = False
        else:
            result["status"] = "inspected"
        return result
    except (OSError, ValueError, TypeError) as exc:
        result["issues"] = [str(exc) if isinstance(exc, ApplicationError) else "selected_input_unavailable"]
        return result


def run_contracts(capabilities, *, artifact=None, profile=None, request_key=None, ledger=None):
    """An explicit run always re-reads; MCP exposure always returns a host handoff."""
    result = _base()
    try:
        entry = observations(capabilities)["contracts"]
        result["capabilityObservation"] = entry
        result["capabilityBasis"] = "host_observation_only"
        if not entry["mcp_exposed"] and not entry["verified_cli"]:
            result.update(status="unavailable", route="unavailable", issues=["no_observed_execution_route"])
            return result
        validator, version = _validator()
        raw = _selected(result, validator, artifact, profile, request_key, ledger)
        if raw is None:
            return result
        profile_issues = _profile_issues(validator, raw, profile)
        if entry["mcp_exposed"]:
            result["route"] = "host_mcp_handoff"
            if profile_issues:
                result["issues"] = profile_issues
                return result
            result.update(status="handoff_required", handoff={
                "product": "contracts", "executor": "host", "tool": "validate_artifact",
                "arguments": {"artifact_json": raw.decode("utf-8")}, "expectedProfile": profile,
                "binding": result["binding"], "requestKey": request_key,
                "completionEvidence": "Actual exposed host tool result must be valid and match expectedProfile; keep binding and every unchecked or loss finding."})
            return result
        result["route"] = "verified_sibling_cli"
        result["executionPerformed"] = True
        result["validation"] = validator.validate_bytes(raw)
        result["issues"] = profile_issues
        validation = result["validation"]
        if validation["status"] == "valid" and validation["profile"] == profile and not profile_issues:
            result.update(status="verified", activationStatus="VERIFIED")
        elif validation["status"] == "unsupported":
            result.update(status="unsupported", activationStatus="INCOMPLETE")
        else:
            result["activationStatus"] = "INCOMPLETE"
        result["ledgerEntry"] = {"request_key": request_key, "status": "verified" if result["status"] == "verified" else "incomplete",
            "evidence": {**result["binding"], "validation_status": validation["status"],
                         "validator_product_version": version, "contract_version": validation["contract_version"],
                         "not_checked": validation["not_checked"], "mapping_loss": "not_assessed_by_validation"}}
        return result
    except (OSError, ValueError, TypeError) as exc:
        result["activationStatus"] = "INCOMPLETE" if result["executionPerformed"] else "NOT_EXECUTED"
        result["issues"] = [str(exc) if isinstance(exc, ApplicationError) else "validation_or_input_failed"]
        return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    routing = commands.add_parser("plan", help="Route observed products; does not execute or verify any product.")
    routing.add_argument("--capabilities", required=True)
    routing.add_argument("--explicit-product", choices=PRODUCTS, action="append", dest="explicit_products")
    routing.add_argument("--ledger")
    run = commands.add_parser("run-contracts", help="Validate a selected file with verified same-bundle CLI, or hand exposed MCP back to the host.")
    run.add_argument("--capabilities", required=True)
    inspect = commands.add_parser("inspect-target", help="Re-read selected bytes for receipt reuse; performs no validation or activation.")
    for child in (run, inspect):
        child.add_argument("--artifact")
        child.add_argument("--profile", choices=PROFILES)
        child.add_argument("--request-key")
        child.add_argument("--ledger")
    args = vars(parser.parse_args(argv))
    command = args.pop("command")
    try:
        if sys.version_info < (3, 11):
            raise ApplicationError("python_3_11_required")
        for key in ("capabilities", "ledger"):
            if args.get(key) is not None:
                args[key] = _control(args[key])
        result = plan(**args) if command == "plan" else inspect_target(**args) if command == "inspect-target" else run_contracts(**args)
        print(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2))
        return 0 if result["status"] in ("planned", "inspected", "handoff_required", "verified") else 2
    except (ApplicationError, UnicodeError):
        print(json.dumps({**_base(), "issues": ["invalid_application_arguments"]}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
