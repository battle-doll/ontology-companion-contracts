"""Bounded offline projection of explicitly selected Code static references.

No imports of Code or target repositories, revision verification, source scans,
network access or writes occur here. The CLI's separate exclusive output option
is the only writer. The retained input digest identifies evidence bytes, not an
authenticated producer or a source-to-commit binding.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat

from .validator import (CONTRACT_VERSION, CO_NAMESPACE, MAX_BYTES, InvalidInput,
                        _constant, _pairs, _portable, validate_bytes)

PRODUCT_VERSION = "0.1.1"
MAX_SOURCE_BYTES = 16 * 1024 * 1024
MAX_SOURCE_NODES = 20000
MAX_SOURCE_EDGES = 50000
REVISION_LIMITATION = "revision.snapshot_binding_not_verified"
NOT_CHECKED = ["producer_identity", "source_access", "revision_snapshot_equivalence",
               "source_state", "runtime_behavior", "current_authorization"]


def canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")


def _fail(rule):
    raise InvalidInput(rule)


def _obj(value, required, optional=()):
    if not isinstance(value, dict) or set(required) - set(value) or set(value) - set(required) - set(optional):
        _fail("source_object_fields")
    return value


def _text(value, maximum=160, identity=False):
    if (not isinstance(value, str) or not 1 <= len(value) <= maximum
            or any(ord(c) < 32 or ord(c) == 127 or 0xD800 <= ord(c) <= 0xDFFF for c in value)
            or identity and any(c.isspace() for c in value)):
        _fail("source_text")
    return value


def _identity(value):
    value = _text(value, identity=True)
    # Public repository identity is explicit; never accept an absolute path or
    # credential-bearing URL as an apparent repository label.
    if (not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/+-]{0,159}", value)
            or "://" in value or value.startswith("file:") or re.match(r"^[A-Za-z]:[/\\]", value)):
        _fail("repository_identity")
    return value


def _list(value, maximum, minimum=0):
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        _fail("source_collection_limit")
    return value


def _enum(value, allowed):
    if not isinstance(value, str) or value not in allowed:
        _fail("source_enum")
    return value


def _source(value):
    if value is None:
        return None
    _obj(value, ("path", "line_start", "line_end"))
    path = _text(value["path"], 1024)
    if not _portable(path):
        _fail("source_path")
    start, end = value["line_start"], value["line_end"]
    if type(start) is not int or type(end) is not int or not 1 <= start <= end <= 10000000:
        _fail("source_span")
    return dict(value)


def _code(value, raw=False):
    _obj(value, ("rule_id", "basis", "runtime_status"),
         ("limitations", "path", "line_start", "line_end") if raw else ("limitations",))
    rule = _text(value["rule_id"], 80)
    if not re.fullmatch(r"[a-z][a-z0-9_.-]{2,79}", rule):
        _fail("source_rule")
    basis = _enum(value["basis"], ("direct_syntax", "resolved_static", "framework_semantic", "name_heuristic"))
    runtime = _enum(value["runtime_status"], ("not_applicable", "runtime_unknown"))
    limits = [_text(item) for item in _list(value.get("limitations", []), 32)]
    # Preserve partial edge spans behind the immutable input locator. Reject
    # unsafe paths and malformed supplied bounds even when the edge is omitted.
    if raw:
        if "path" in value and not _portable(_text(value["path"], 1024)):
            _fail("source_path")
        for key in ("line_start", "line_end"):
            if key in value and (type(value[key]) is not int or not 1 <= value[key] <= 10000000):
                _fail("source_span")
        if "line_start" in value and "line_end" in value and value["line_start"] > value["line_end"]:
            _fail("source_span")
    return {"rule_id": rule, "basis": basis, "runtime_status": runtime,
            "limitations": limits + ([] if REVISION_LIMITATION in limits else [REVISION_LIMITATION])}


def parse_snapshot(raw):
    if not isinstance(raw, bytes) or len(raw) > MAX_SOURCE_BYTES:
        _fail("source_byte_limit")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant)
    except (ValueError, UnicodeError, RecursionError):
        _fail("source_json")
    pending, count = [(value, 0)], 0
    while pending:
        item, depth = pending.pop()
        count += 1
        if depth > 32 or count > 1000000:
            _fail("source_structure_limit")
        if isinstance(item, str):
            if len(item) > 8192 or any(0xD800 <= ord(c) <= 0xDFFF for c in item):
                _fail("source_string_limit")
        elif isinstance(item, float) and not math.isfinite(item):
            _fail("source_non_finite")
        elif isinstance(item, (list, dict)):
            if len(item) > MAX_SOURCE_EDGES:
                _fail("source_collection_limit")
            if isinstance(item, dict):
                pending.extend((key, depth + 1) for key in item)
                pending.extend((part, depth + 1) for part in item.values())
            else:
                pending.extend((part, depth + 1) for part in item)
    return value


def read_snapshot(path):
    """Read a single explicit regular file without following a final symlink."""
    selected = Path(path)
    before = selected.lstat()
    if not stat.S_ISREG(before.st_mode):
        _fail("regular_file_required")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    with os.fdopen(os.open(selected, flags), "rb") as stream:
        after = os.fstat(stream.fileno())
        if not stat.S_ISREG(after.st_mode) or (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino):
            _fail("file_changed")
        return stream.read(MAX_SOURCE_BYTES + 1)


def write_new_artifact(path, artifact):
    """Only an explicit CLI output request calls this; existing files are refused."""
    raw = canonical(artifact) + b"\n"
    if len(raw) > MAX_BYTES or validate_bytes(raw)["status"] != "valid":
        _fail("output_contract_limit")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    with os.fdopen(os.open(Path(path), flags, 0o600), "wb") as stream:
        stream.write(raw)


def _raw_rows(doc):
    _obj(doc, ("schema_version", "generator", "repository", "nodes", "edges"),
         ("generated_at", "privacy", "statistics", "quality", "warnings", "companion"))
    if doc["schema_version"] != "1.0":
        _fail("unsupported_source_version")
    _obj(doc["generator"], ("name", "version"))
    if doc["generator"] != {"name": "Code Ontology Companion", "version": "0.6.0"}:
        _fail("unsupported_source_producer")
    _obj(doc["repository"], ("name", "path_policy"))
    _text(doc["repository"]["name"])
    if doc["repository"]["path_policy"] != "repository-relative-only":
        _fail("source_path_policy")
    nodes, edges, ignored_metadata = [], [], 0
    for index, item in enumerate(_list(doc["nodes"], MAX_SOURCE_NODES)):
        _obj(item, ("id", "type", "name", "language"), ("path", "qualified_name", "metadata"))
        sid = _text(item["id"], 512, True)
        if "qualified_name" in item:
            _text(item["qualified_name"], 1024)
        kind, name = _text(item["type"]), _text(item.get("qualified_name") or item["name"], 1024)
        _text(item["name"], 1024)
        _text(item["language"])
        metadata = item.get("metadata", {})
        if not isinstance(metadata, dict):
            _fail("source_metadata")
        ignored_metadata += len(set(metadata) - {"line_start", "line_end"})
        path = item.get("path")
        if path is not None and not _portable(_text(path, 1024)):
            _fail("source_path")
        for key in ("line_start", "line_end"):
            if key in metadata and (type(metadata[key]) is not int or not 1 <= metadata[key] <= 10000000):
                _fail("source_span")
        source = _source({"path": path, "line_start": metadata["line_start"], "line_end": metadata["line_end"]}) if path and all(k in metadata for k in ("line_start", "line_end")) else None
        nodes.append({"id": sid, "kind": kind, "qualified_name": name, "source": source,
                      "resolution": "source_located" if source else "external" if kind.startswith("External") else "source_unresolved",
                      "pointer": f"/nodes/{index}", "evidence": [(f"/nodes/{index}", {
                          "rule_id": "bridge.symbol_reference", "basis": "resolved_static", "runtime_status": "runtime_unknown",
                          "limitations": [REVISION_LIMITATION, "runtime.activation_not_observed"]})]})
    for index, item in enumerate(_list(doc["edges"], MAX_SOURCE_EDGES)):
        _obj(item, ("source", "target", "type"), ("evidence",))
        triple = {key: _text(item[key], 160 if key == "type" else 512, key != "type") for key in ("source", "target", "type")}
        edges.append({**triple, "evidence": [(f"/edges/{index}/evidence/{n}", _code(ev, raw=True))
                      for n, ev in enumerate(_list(item.get("evidence", []), 16))]})
    return nodes, edges, ignored_metadata


def _native_rows(doc):
    _obj(doc, ("profile", "profile_version", "co_namespace", "source_schema_version", "artifact_id", "producer",
               "scope", "snapshot", "selection", "symbols", "relations", "evidence", "authority"))
    if (doc["profile"] != "code-ontology-reference" or doc["profile_version"] != "1.0.0"
            or doc["source_schema_version"] != "1.0" or doc["co_namespace"] != CO_NAMESPACE):
        _fail("unsupported_source_version")
    if doc["producer"] != {"name": "code-ontology-companion", "version": "0.6.0"}:
        _fail("unsupported_source_producer")
    expected = "urn:code-ontology-reference:" + hashlib.sha256(canonical({k: v for k, v in doc.items() if k != "artifact_id"})).hexdigest()
    if doc["artifact_id"] != expected:
        _fail("source_digest_mismatch")
    scope, snapshot = doc["scope"], doc["snapshot"]
    _obj(scope, ("repository_id", "module_id", "module_root"))
    _identity(scope["repository_id"])
    if not isinstance(scope["module_id"], str) or not re.fullmatch(r"module:[a-f0-9]{24}", scope["module_id"]):
        _fail("source_module")
    if scope["module_root"] != "." and not _portable(_text(scope["module_root"], 1024)):
        _fail("source_module")
    _obj(snapshot, ("id", "repository_revision", "revision_binding", "source_state", "analyzer_version"))
    _text(snapshot["id"], identity=True)
    _text(snapshot["analyzer_version"])
    if snapshot["revision_binding"] != ("not_checked" if snapshot["repository_revision"] else "unavailable") or snapshot["source_state"] != "not_checked":
        _fail("source_revision_claim")
    if snapshot["repository_revision"] is not None and (not isinstance(snapshot["repository_revision"], str) or not re.fullmatch(r"(?:[a-f0-9]{40}|[a-f0-9]{64})", snapshot["repository_revision"])):
        _fail("source_revision")
    if doc["authority"] != {"content": "untrusted_data", "current_authorization": "not_checked", "runtime_behavior": "not_checked", "approval": "not_transferred"}:
        _fail("source_authority")
    sel = doc["selection"]
    _obj(sel, ("requested_ids", "mode", "omitted_relationships", "whole_repository"))
    requested = [_text(v, 512, True) for v in _list(sel["requested_ids"], 100, 1)]
    if (len(set(requested)) != len(requested) or sel["mode"] != "bounded_one_hop" or sel["whole_repository"] is not False
            or type(sel["omitted_relationships"]) is not int or not 0 <= sel["omitted_relationships"] <= MAX_SOURCE_EDGES):
        _fail("source_selection")
    evidence = {}
    for n, ev in enumerate(_list(doc["evidence"], 3300)):
        _obj(ev, ("id", "origin", "review_status", "locator", "source", "code"))
        eid = _text(ev["id"], identity=True)
        if eid in evidence or not re.fullmatch(r"evidence:[a-f0-9]{24}", eid):
            _fail("source_evidence_identity")
        if ev["origin"] != "source_observed" or ev["review_status"] != "not_assessed":
            _fail("source_authority")
        _text(ev["locator"], 1100)
        _source(ev["source"])
        evidence[eid] = (f"/evidence/{n}", _code(ev["code"]))

    def refs(item):
        ids = [_text(v, identity=True) for v in _list(item["evidence_refs"], 16)]
        if len(set(ids)) != len(ids) or any(eid not in evidence for eid in ids):
            _fail("source_evidence_reference")
        return [evidence[eid] for eid in ids]

    nodes, edges = [], []
    for n, item in enumerate(_list(doc["symbols"], 100, 1)):
        _obj(item, ("id", "reference_id", "kind", "qualified_name", "source", "resolution", "runtime_status", "evidence_refs"))
        if not isinstance(item["reference_id"], str) or not re.fullmatch(r"symbol:[a-f0-9]{24}", item["reference_id"]):
            _fail("source_reference_identity")
        if item["runtime_status"] != "runtime_unknown":
            _fail("source_runtime_claim")
        resolution = _enum(item["resolution"], ("source_located", "external", "source_unresolved", "outside_module"))
        source = _source(item["source"])
        if bool(source) != (resolution in ("source_located", "outside_module")):
            _fail("source_resolution")
        if source:
            inside = scope["module_root"] == "." or source["path"].startswith(scope["module_root"] + "/")
            if inside != (resolution == "source_located"):
                _fail("source_module_resolution")
        nodes.append({"id": _text(item["id"], 512, True), "kind": _text(item["kind"]),
                      "qualified_name": _text(item["qualified_name"], 1024), "source": source,
                      "resolution": resolution, "pointer": f"/symbols/{n}", "evidence": refs(item)})
    if not set(requested) <= {node["id"] for node in nodes}:
        _fail("source_selection")
    for item in _list(doc["relations"], 200):
        _obj(item, ("id", "source", "target", "type", "evidence_refs", "resolution"))
        if not isinstance(item["id"], str) or not re.fullmatch(r"relation:[a-f0-9]{24}", item["id"]):
            _fail("source_reference_identity")
        evs = refs(item)
        if item["resolution"] != ("evidenced" if evs else "evidence_unavailable"):
            _fail("source_resolution")
        edges.append({**{key: _text(item[key], 160 if key == "type" else 512, key != "type") for key in ("source", "target", "type")}, "evidence": evs})
    return nodes, edges, 0


def convert_code_snapshot(raw, *, repository_id=None, revision=None, snapshot_id=None, symbol_ids=None, path_prefixes=None):
    """Return a selected draft artifact and explicit losses; invalid input is bounded."""
    try:
        doc = parse_snapshot(raw)
        if not isinstance(doc, dict):
            _fail("source_object_fields")
        native = "profile" in doc
        if native and len(raw) > MAX_BYTES:
            _fail("source_byte_limit")
        nodes, edges, ignored_metadata = _native_rows(doc) if native else _raw_rows(doc)
        digest = hashlib.sha256(raw).hexdigest()
        ids = [node["id"] for node in nodes]
        triples = [tuple(edge[k] for k in ("source", "target", "type")) for edge in edges]
        if len(set(ids)) != len(ids) or len(set(triples)) != len(triples):
            _fail("source_duplicate_identity")
        source_ids = set(ids)
        if any(edge["source"] not in source_ids or edge["target"] not in source_ids for edge in edges):
            _fail("source_dangling_symbol")
        if native:
            for supplied, original in ((repository_id, doc["scope"]["repository_id"]), (snapshot_id, doc["snapshot"]["id"])):
                if supplied is not None and supplied != original:
                    _fail("source_identity_override")
            repository_id = doc["scope"]["repository_id"]
            snapshot_id = doc["snapshot"]["id"]
            original_revision = doc["snapshot"]["repository_revision"]
            if revision is not None and original_revision is not None and revision != original_revision:
                _fail("source_revision_override")
        else:
            original_revision = None
        revision_basis = "caller_supplied_annotation" if revision is not None else "snapshot_head_observation"
        revision = revision if revision is not None else original_revision
        if revision is None:
            _fail("repository_revision_required")
        if not isinstance(revision, str) or not re.fullmatch(r"(?:[a-f0-9]{40}|[a-f0-9]{64})", revision):
            _fail("source_revision")
        repository_id = _identity(repository_id)
        snapshot_id = _text(snapshot_id or "sha256:" + digest, identity=True)
        selected = [] if symbol_ids is None else [_text(v, 512, True) for v in _list(symbol_ids, 1000, 1)]
        prefixes = [] if path_prefixes is None else [_text(v, 1024) for v in _list(path_prefixes, 100, 1)]
        if selected and prefixes or len(set(selected)) != len(selected) or len(set(prefixes)) != len(prefixes):
            _fail("selection_arguments")
        if any(not _portable(v) for v in prefixes):
            _fail("selection_path")
        if selected and not set(selected) <= set(ids):
            _fail("selected_symbol_not_found")
        if not native and not selected and not prefixes:
            _fail("explicit_selection_required")
        losses = {"outside_selection_symbols": 0, "external_symbols": 0, "source_unresolved_symbols": 0,
                  "outside_module_symbols": 0, "unevidenced_symbols": 0,
                  "unretained_endpoint_relations": 0, "unevidenced_relations": 0,
                  "source_previously_omitted_relations": doc["selection"]["omitted_relationships"] if native else 0,
                  "node_metadata_fields_not_embedded": ignored_metadata}
        evidence, symbols, relations = {}, [], []

        def evrefs(items):
            refs = []
            for pointer, code in items:
                eid = "projection:" + hashlib.sha256((digest + pointer).encode()).hexdigest()[:32]
                evidence[eid] = {"id": eid, "origin": "source_observed", "scope": repository_id,
                                 "locator": "urn:code-snapshot:sha256:" + digest + "#" + pointer, "code": code}
                refs.append(eid)
            return refs

        for node in nodes:
            source = node["source"]
            if selected and node["id"] not in selected or prefixes and not (source and any(source["path"] == prefix or source["path"].startswith(prefix + "/") for prefix in prefixes)):
                losses["outside_selection_symbols"] += 1
                continue
            if node["resolution"] != "source_located":
                losses[node["resolution"] + "_symbols"] += 1
                continue
            if not node["evidence"]:
                losses["unevidenced_symbols"] += 1
                continue
            symbols.append({"id": node["id"], "kind": node["kind"], "qualified_name": node["qualified_name"],
                            "source_path": source["path"], "start_line": source["line_start"], "end_line": source["line_end"],
                            "evidence_refs": evrefs(node["evidence"]), "runtime_status": "runtime_unknown"})
        retained = {item["id"] for item in symbols}
        if not retained:
            _fail("no_source_located_selection")
        for edge in edges:
            if edge["source"] not in retained or edge["target"] not in retained:
                losses["unretained_endpoint_relations"] += 1
            elif not edge["evidence"]:
                losses["unevidenced_relations"] += 1
            else:
                relations.append({**{k: edge[k] for k in ("source", "target", "type")}, "evidence_refs": evrefs(edge["evidence"])})
        artifact = {"contract_version": CONTRACT_VERSION, "profile": "code-reference",
                    "producer": {"name": "ontology-companion-contracts", "version": PRODUCT_VERSION},
                    "evidence": [evidence[k] for k in sorted(evidence)], "payload": {
                        "repository": repository_id, "revision": revision, "snapshot_id": snapshot_id,
                        "co_namespace": CO_NAMESPACE, "symbols": sorted(symbols, key=lambda x: x["id"]),
                        "relations": sorted(relations, key=lambda x: tuple(x[k] for k in ("source", "target", "type")))}}
        artifact["artifact_id"] = "urn:contracts:code-projection:" + hashlib.sha256(canonical(artifact)).hexdigest()
        serialized = canonical(artifact)
        validation = validate_bytes(serialized)
        if len(serialized) + 1 > MAX_BYTES or validation["status"] != "valid":
            _fail("output_contract_limit_reselect")
        report = {"source_format": "code-ontology-reference/1.0.0" if native else "code-ontology-snapshot/1.0",
                  "source_sha256": digest, "source_producer_version": "0.6.0",
                  "revision_basis": revision_basis, "revision_binding": "not_checked", "source_state": "not_checked",
                  "selection_mode": "exact_symbols" if selected else "path_prefixes" if prefixes else "native_selected_artifact",
                  "whole_repository": False, "retained_symbols": len(symbols), "retained_relations": len(relations),
                  "loss_counts": losses, "not_embedded": ["source_diagnostics", "node_metadata", "native_module_selection_authority", "original_evidence_ids_and_spans"],
                  "evidence_retention": "retain_exact_input_bytes_for_sha256_json_pointer_locators",
                  "not_checked": list(NOT_CHECKED)}
        return {"status": "converted", "artifact": artifact, "mapping_report": report, "validation": validation,
                "errors": [], "writes_performed": False}
    except (InvalidInput, ValueError, TypeError, RecursionError) as exc:
        rule = str(exc) if isinstance(exc, InvalidInput) else "source_structure"
        return {"status": "unsupported" if rule.startswith("unsupported_") or rule == "repository_revision_required" else "invalid",
                "artifact": None, "mapping_report": None, "validation": None,
                "errors": [{"pointer": "", "rule_id": rule, "message": "No artifact produced; supply a supported, explicitly selected Code snapshot and revision annotation."}],
                "writes_performed": False}
