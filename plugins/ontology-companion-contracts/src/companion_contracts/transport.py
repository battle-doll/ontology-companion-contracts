"""Offline CLI and local stdio tools; only explicit CLI --output creates a file."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from .code_adapter import MAX_SOURCE_BYTES, PRODUCT_VERSION, convert_code_snapshot, read_snapshot, write_new_artifact

from .validator import (CONTRACT_VERSION, MAX_BYTES, PROFILES, InvalidInput, _parse,
                        _pairs, _constant, compatibility, migration_plan, read_artifact, validate_bytes)

# Source text is supplied as an escaped JSON string. Its own parser still caps
# decoded UTF-8 bytes at 16 MiB, independently of this outer transport envelope.
MAX_RPC_BYTES = 2 * MAX_SOURCE_BYTES + 65536


def _parse_request(raw):
    """Bound request structure while allowing explicitly named artifact strings.

    Artifact strings are data containers, so their dedicated parsers enforce
    their internal depth, collection and byte limits after dispatch. Ordinary
    request metadata retains the smaller string limit.
    """
    if len(raw) > MAX_RPC_BYTES:
        raise InvalidInput("request_byte_limit")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant)
    except (ValueError, UnicodeError, RecursionError):
        raise InvalidInput("request_json") from None
    pending, count = [(value, ())], 0
    while pending:
        item, path = pending.pop()
        count += 1
        if len(path) > 32 or count > 20000:
            raise InvalidInput("request_structure_limit")
        if isinstance(item, str):
            limit = MAX_SOURCE_BYTES if path == ("params", "arguments", "snapshot_json") else MAX_BYTES if path == ("params", "arguments", "artifact_json") else 8192
            if len(item) > limit or any(0xD800 <= ord(c) <= 0xDFFF for c in item):
                raise InvalidInput("request_string_limit")
        elif isinstance(item, float) and not math.isfinite(item):
            raise InvalidInput("request_non_finite")
        elif isinstance(item, (dict, list)):
            if len(item) > 1000:
                raise InvalidInput("request_collection_limit")
            if isinstance(item, dict):
                pending.extend((key, path + ("<key>",)) for key in item)
                pending.extend((part, path + (key,)) for key, part in item.items())
            else:
                pending.extend((part, path + (index,)) for index, part in enumerate(item))
    return value


def _object(properties, required=None):
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else required, "additionalProperties": False}


STRING = {"type": "string"}
NULL_STRING = {"type": ["string", "null"]}
STRINGS = {"type": "array", "items": STRING}
ERROR = _object({"pointer": STRING, "rule_id": STRING, "message": STRING})
VALIDATION_OUTPUT = _object({"status": {"type": "string", "enum": ["valid", "invalid", "unsupported"]},
    "contract_version": NULL_STRING, "profile": NULL_STRING,
    "layers": _object({key: {"type": "string", "enum": ["valid", "invalid", "unsupported", "not_checked"]}
                       for key in ("L0_parse", "L1_schema", "L2_profile", "L3_compatibility", "external_verification")}),
    "errors": {"type": "array", "maxItems": 32, "items": ERROR}, "not_checked": STRINGS})
COMPATIBILITY_OUTPUT = _object({"status": {"type": "string", "enum": ["compatible", "unsupported"]},
    "producer_version": NULL_STRING, "consumer_version": NULL_STRING, "profile": NULL_STRING,
    "basis": STRING, "direction": {"type": "string", "const": "producer_to_consumer"},
    "consumer_runtime": {"type": "string", "const": "not_checked"}})
MIGRATION_OUTPUT = _object({"status": {"type": "string", "enum": ["identity_plan", "unsupported"]},
    "writes_performed": {"type": "boolean", "const": False}, "source_validation": VALIDATION_OUTPUT,
    "target_version": NULL_STRING, "target_profile": NULL_STRING, "preserved": STRINGS,
    "transformed": STRINGS, "losses": STRINGS, "not_checked": STRINGS})
BOUNDED = {"type": "string", "minLength": 1, "maxLength": 160}
ARTIFACT_JSON = {"type": "string", "minLength": 1, "maxLength": MAX_BYTES}
ANNOTATIONS = {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}
CODE_ARTIFACT = json.loads((Path(__file__).parent / "_schemas/envelope.schema.json").read_text(encoding="utf-8"))
CODE_ARTIFACT.pop("$id", None)
CODE_ARTIFACT["properties"]["profile"] = {"const": "code-reference"}
CODE_ARTIFACT["properties"]["payload"] = json.loads((Path(__file__).parent / "_schemas/code-reference.schema.json").read_text(encoding="utf-8"))
CODE_ARTIFACT["properties"]["payload"].pop("$id", None)
COUNT = {"type": "integer", "minimum": 0}
MAPPING_REPORT = _object({
    "source_format": {"enum": ["code-ontology-reference/1.0.0", "code-ontology-snapshot/1.0"]},
    "source_sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
    "source_producer_version": {"const": "0.6.0"},
    "revision_basis": {"enum": ["caller_supplied_annotation", "snapshot_head_observation"]},
    "revision_binding": {"const": "not_checked"}, "source_state": {"const": "not_checked"},
    "selection_mode": {"enum": ["exact_symbols", "path_prefixes", "native_selected_artifact"]},
    "whole_repository": {"const": False}, "retained_symbols": COUNT, "retained_relations": COUNT,
    "loss_counts": _object({key: COUNT for key in ("outside_selection_symbols", "external_symbols", "source_unresolved_symbols",
        "outside_module_symbols", "unevidenced_symbols", "unretained_endpoint_relations", "unevidenced_relations",
        "source_previously_omitted_relations", "node_metadata_fields_not_embedded")}),
    "not_embedded": STRINGS, "evidence_retention": {"const": "retain_exact_input_bytes_for_sha256_json_pointer_locators"},
    "not_checked": STRINGS})
CONVERSION_OUTPUT = {"type": "object", "oneOf": [
    _object({"status": {"const": "converted"}, "artifact": CODE_ARTIFACT, "mapping_report": MAPPING_REPORT,
             "validation": VALIDATION_OUTPUT, "errors": {"type": "array", "maxItems": 0}, "writes_performed": {"const": False}}),
    _object({"status": {"enum": ["invalid", "unsupported"]}, "artifact": {"type": "null"}, "mapping_report": {"type": "null"},
             "validation": {"type": "null"}, "errors": {"type": "array", "minItems": 1, "maxItems": 1, "items": ERROR},
             "writes_performed": {"const": False}})]}
TOOLS = [
    {"name": "validate_artifact", "description": "Validate explicitly supplied ontology artifact JSON offline against bundled draft profiles. No truth, identity, runtime, or authorization check.",
     "inputSchema": _object({"artifact_json": ARTIFACT_JSON}), "outputSchema": VALIDATION_OUTPUT,
     "annotations": dict(ANNOTATIONS)},
    {"name": "compare_versions", "description": "Check the explicit bundled producer-to-reader version/profile fixture pairing. Does not test an installed consumer.",
     "inputSchema": _object({"producer_version": BOUNDED, "consumer_version": BOUNDED, "profile": BOUNDED}),
     "outputSchema": COMPATIBILITY_OUTPUT, "annotations": dict(ANNOTATIONS)},
    {"name": "plan_migration", "description": "Return a plan only. Only same-profile same-version identity preservation is supported; other migrations remain unsupported. Writes no files.",
     "inputSchema": _object({"artifact_json": ARTIFACT_JSON, "target_version": BOUNDED, "target_profile": BOUNDED}, ["artifact_json", "target_version"]),
     "outputSchema": MIGRATION_OUTPUT, "annotations": dict(ANNOTATIONS)},
    {"name": "convert_code_snapshot", "description": "Project explicitly supplied Code 0.6.0 snapshot JSON or native selected reference v1.0.0 into bounded draft code-reference. Raw snapshots require repository_id, revision and exact symbol_ids or path_prefixes. Revision remains an unverified annotation; retain input bytes for evidence locators. Returns losses; no paths read, files written, repository scans or network calls.",
     "inputSchema": _object({"snapshot_json": {"type": "string", "minLength": 1, "maxLength": MAX_SOURCE_BYTES}, "repository_id": BOUNDED, "revision": {"type": "string", "pattern": "^(?:[a-f0-9]{40}|[a-f0-9]{64})$", "maxLength": 64},
         "snapshot_id": BOUNDED, "symbol_ids": {"type": "array", "minItems": 1, "maxItems": 1000, "uniqueItems": True, "items": {"type": "string", "minLength": 1, "maxLength": 512}},
         "path_prefixes": {"type": "array", "minItems": 1, "maxItems": 100, "uniqueItems": True, "items": {"type": "string", "minLength": 1, "maxLength": 1024}}}, ["snapshot_json"]),
     "outputSchema": CONVERSION_OUTPUT, "annotations": dict(ANNOTATIONS)},
]


def invoke(name, arguments):
    tool = next((row for row in TOOLS if row["name"] == name), None)
    if not tool or not isinstance(arguments, dict):
        raise InvalidInput("unknown_tool_or_arguments")
    schema = tool["inputSchema"]
    if set(arguments) - set(schema["properties"]) or set(schema["required"]) - set(arguments):
        raise InvalidInput("tool_arguments")
    if name == "convert_code_snapshot":
        raw = arguments["snapshot_json"]
        if not isinstance(raw, str) or not 1 <= len(raw) <= MAX_SOURCE_BYTES:
            raise InvalidInput("tool_arguments")
        return convert_code_snapshot(raw.encode("utf-8"), **{key: value for key, value in arguments.items() if key != "snapshot_json"})
    for key, value in arguments.items():
        limit = schema["properties"][key]["maxLength"]
        if not isinstance(value, str) or not 1 <= len(value) <= limit:
            raise InvalidInput("tool_arguments")
    if name == "validate_artifact":
        return validate_bytes(arguments["artifact_json"].encode("utf-8"))
    if name == "compare_versions":
        return compatibility(arguments["producer_version"], arguments["consumer_version"], arguments["profile"])
    return plan_bytes(arguments["artifact_json"].encode("utf-8"), arguments["target_version"], arguments.get("target_profile"))


def plan_bytes(raw, target_version, target_profile=None):
    try:
        artifact = _parse(raw)
    except InvalidInput:
        output = migration_plan(None, target_version, target_profile)
        output["source_validation"] = validate_bytes(raw)
        return output
    return migration_plan(artifact, target_version, target_profile)


def _response(request_id, result=None, code=None, message=None):
    value = {"jsonrpc": "2.0", "id": request_id}
    value["error" if code else "result"] = {"code": code, "message": message} if code else result
    return value


def serve_stdin():
    """Bounded newline JSON-RPC subset for initialize, ping and tools methods.

    Local smoke tests cover this transport; external MCP host integration is a
    separate gate. No automatic host/server registration is performed.
    """
    initialized = False
    while True:
        raw = sys.stdin.buffer.readline(MAX_RPC_BYTES + 1)
        if not raw:
            return 0
        request_id = None
        try:
            if len(raw) > MAX_RPC_BYTES:
                print(json.dumps(_response(None, code=-32700, message="Request limit exceeded.")), flush=True)
                return 2  # fail closed; never parse the remainder as another request
            request = _parse_request(raw)
            if not isinstance(request, dict) or request.get("jsonrpc") != "2.0" or not isinstance(request.get("method"), str):
                raise InvalidInput("request")
            request_id = request.get("id")
            if request_id is not None and (type(request_id) not in (str, int) or isinstance(request_id, str) and len(request_id) > 160):
                request_id = None
                raise InvalidInput("request_id")
            method = request["method"]
            params = request.get("params", {})
            if not isinstance(params, dict):
                raise InvalidInput("params")
            if "id" not in request:
                continue
            if method == "initialize":
                initialized = True
                result = {"protocolVersion": "2025-06-18", "capabilities": {"tools": {"listChanged": False}},
                          "serverInfo": {"name": "ontology-companion-contracts", "version": PRODUCT_VERSION}}
            elif not initialized:
                print(json.dumps(_response(request_id, code=-32000, message="Initialize first.")), flush=True)
                continue
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": TOOLS}
            elif method == "tools/call":
                output = invoke(params.get("name"), params.get("arguments", {}))
                result = {"content": [{"type": "text", "text": json.dumps(output, sort_keys=True)}],
                          "structuredContent": output, "isError": False}
            else:
                print(json.dumps(_response(request_id, code=-32601, message="Method not found.")), flush=True)
                continue
            print(json.dumps(_response(request_id, result=result), sort_keys=True), flush=True)
        except (InvalidInput, UnicodeError, ValueError):
            print(json.dumps(_response(request_id, code=-32602, message="Invalid or unsupported request.")), flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Offline bounded ontology contract validator (draft; no authorization checks).")
    parser.add_argument("--version", action="version", version=PRODUCT_VERSION)
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="Validate one explicitly selected regular JSON file; never modifies it.")
    validate.add_argument("path")
    pair = commands.add_parser("compatibility", help="Check a bundled producer-to-reader fixture pairing.")
    pair.add_argument("--producer-version", required=True)
    pair.add_argument("--consumer-version", required=True)
    pair.add_argument("--profile", required=True)
    migrate = commands.add_parser("migration-plan", help="Produce an identity plan or explicit unsupported result; writes nothing.")
    migrate.add_argument("path")
    migrate.add_argument("--target-version", required=True)
    migrate.add_argument("--target-profile")
    convert = commands.add_parser("convert-code", help="Project selected Code 0.6.0 JSON; revision annotation is unverified; no automatic source scanning.")
    convert.add_argument("path", help="Explicit native selected reference or raw ontology.json (16 MiB maximum).")
    convert.add_argument("--repository-id", help="Required for raw snapshots; public identity such as github:owner/repository.")
    convert.add_argument("--revision", help="40/64 lowercase hex revision annotation; does not assert source-to-commit binding.")
    convert.add_argument("--snapshot-id", help="Raw snapshot identity; default is a digest of the input bytes.")
    selection = convert.add_mutually_exclusive_group()
    selection.add_argument("--symbol-id", action="append", dest="symbol_ids", help="Exact ID; repeat for multiple symbols (no neighborhood expansion).")
    selection.add_argument("--path-prefix", action="append", dest="path_prefixes", help="Relative path or directory prefix; repeat as needed.")
    convert.add_argument("--output", help="Explicitly create this new artifact file; existing files are never overwritten. Full report remains on stdout.")
    commands.add_parser("tools", help="Print implemented local tool descriptors.")
    commands.add_parser("stdio", help="Run optional local stdio JSON-RPC tools; no registration performed.")
    args = parser.parse_args(argv)
    if args.command == "stdio":
        return serve_stdin()
    try:
        if args.command == "validate":
            output = validate_bytes(read_artifact(args.path))
        elif args.command == "compatibility":
            output = compatibility(args.producer_version, args.consumer_version, args.profile)
        elif args.command == "migration-plan":
            raw = read_artifact(args.path)
            output = plan_bytes(raw, args.target_version, args.target_profile)
        elif args.command == "convert-code":
            output = convert_code_snapshot(read_snapshot(args.path), repository_id=args.repository_id,
                revision=args.revision, snapshot_id=args.snapshot_id, symbol_ids=args.symbol_ids, path_prefixes=args.path_prefixes)
            if args.output and output["status"] == "converted":
                write_new_artifact(args.output, output["artifact"])
                output["writes_performed"] = True
        else:
            output = {"tools": TOOLS}
        print(json.dumps(output, indent=2, sort_keys=True, ensure_ascii=True))
        return 0 if output.get("status") in (None, "valid", "compatible", "identity_plan", "converted") else 2
    except (OSError, InvalidInput):
        print(json.dumps({"status": "invalid", "errors": [{"pointer": "", "rule_id": "input_file", "message": "Selected file is unavailable, unsafe, or unsupported."}]}))
        return 2
