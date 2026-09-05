from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from companion_contracts import CO_NAMESPACE, PRODUCT_VERSION, convert_code_snapshot, validate_artifact
from companion_contracts.code_adapter import (MAX_SOURCE_BYTES, REVISION_LIMITATION, canonical,
                                               read_snapshot, write_new_artifact)
from companion_contracts.transport import CONVERSION_OUTPUT, TOOLS, invoke, _parse_request
from companion_contracts.validator import InvalidInput


def native_fixture():
    """Independently authored minimal native v1 fixture; no Code source dependency."""
    source = {"path": "example/worker.py", "line_start": 2, "line_end": 5}
    value = {"profile": "code-ontology-reference", "profile_version": "1.0.0", "co_namespace": CO_NAMESPACE,
        "source_schema_version": "1.0", "producer": {"name": "code-ontology-companion", "version": "0.6.0"},
        "scope": {"repository_id": "github:example/project", "module_id": "module:" + "c" * 24, "module_root": "."},
        "snapshot": {"id": "snapshot:example", "repository_revision": "a" * 40, "revision_binding": "not_checked",
                     "source_state": "not_checked", "analyzer_version": "0.6.0"},
        "selection": {"requested_ids": ["python:function:example.worker.run"], "mode": "bounded_one_hop",
                      "omitted_relationships": 3, "whole_repository": False},
        "symbols": [{"id": "python:function:example.worker.run", "reference_id": "symbol:" + "b" * 24,
                     "kind": "Function", "qualified_name": "example.worker.run", "source": source,
                     "resolution": "source_located", "runtime_status": "runtime_unknown", "evidence_refs": ["evidence:" + "d" * 24]}],
        "relations": [], "evidence": [{"id": "evidence:" + "d" * 24, "origin": "source_observed",
            "review_status": "not_assessed", "locator": "example/worker.py:2-5", "source": source,
            "code": {"rule_id": "bridge.symbol_reference", "basis": "resolved_static", "runtime_status": "runtime_unknown",
                     "limitations": [REVISION_LIMITATION, "runtime.activation_not_observed"]}}],
        "authority": {"content": "untrusted_data", "current_authorization": "not_checked", "runtime_behavior": "not_checked", "approval": "not_transferred"}}
    return resign(value)


def resign(value):
    value["artifact_id"] = "urn:code-ontology-reference:" + hashlib.sha256(canonical({k: v for k, v in value.items() if k != "artifact_id"})).hexdigest()
    return value


class CodeAdapterTests(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads((ROOT / "examples/code-snapshot-selection.json").read_text())
        self.options = {"repository_id": "github:example/project", "revision": "a" * 40, "path_prefixes": ["example"]}

    def convert(self, doc=None, **options):
        return convert_code_snapshot(canonical(self.doc if doc is None else doc), **(self.options | options))

    def test_real_shape_projection_preserves_exact_static_identity(self):
        before = copy.deepcopy(self.doc)
        result = self.convert()
        self.assertEqual("converted", result["status"], result)
        artifact = result["artifact"]
        self.assertEqual("valid", validate_artifact(artifact)["status"])
        self.assertEqual(CO_NAMESPACE, artifact["payload"]["co_namespace"])
        relation = artifact["payload"]["relations"][0]
        self.assertEqual({k: self.doc["edges"][0][k] for k in ("source", "target", "type")}, {k: relation[k] for k in ("source", "target", "type")})
        by_id = {e["id"]: e for e in artifact["evidence"]}
        code = by_id[relation["evidence_refs"][0]]["code"]
        self.assertEqual("resolved_static", code["basis"])
        self.assertEqual("not_applicable", code["runtime_status"])
        self.assertIn(REVISION_LIMITATION, code["limitations"])
        self.assertEqual(before, self.doc)
        self.assertEqual(result, self.convert())

    def test_exact_byte_provenance_resolves_every_retained_evidence(self):
        raw = canonical(self.doc)
        result = self.convert()
        prefix = "urn:code-snapshot:sha256:" + hashlib.sha256(raw).hexdigest() + "#"
        for evidence in result["artifact"]["evidence"]:
            self.assertTrue(evidence["locator"].startswith(prefix))
            item = self.doc
            for key in evidence["locator"][len(prefix):].strip("/").split("/"):
                item = item[int(key)] if isinstance(item, list) else item[key]
            self.assertIsInstance(item, dict)
        changed = convert_code_snapshot(raw + b"\n", **self.options)
        self.assertNotEqual(result["artifact"]["artifact_id"], changed["artifact"]["artifact_id"])

    def test_loss_report_no_invented_sources_or_dangling_edges(self):
        result = self.convert(path_prefixes=None, symbol_ids=[n["id"] for n in self.doc["nodes"]])
        losses = result["mapping_report"]["loss_counts"]
        self.assertEqual(1, losses["external_symbols"])
        self.assertEqual(1, losses["unretained_endpoint_relations"])
        self.assertEqual(1, losses["node_metadata_fields_not_embedded"])
        self.assertEqual(2, result["mapping_report"]["retained_symbols"])
        self.assertFalse(result["mapping_report"]["whole_repository"])
        self.assertEqual("not_checked", result["mapping_report"]["revision_binding"])
        self.assertFalse(result["writes_performed"])

    def test_missing_span_does_not_invent_line_one(self):
        del self.doc["nodes"][0]["metadata"]["line_end"]
        result = self.convert(path_prefixes=None, symbol_ids=[self.doc["nodes"][0]["id"], self.doc["nodes"][1]["id"]])
        self.assertEqual("converted", result["status"])
        self.assertEqual(1, result["mapping_report"]["loss_counts"]["source_unresolved_symbols"])
        self.assertEqual([], result["artifact"]["payload"]["relations"])

    def test_selection_exact_ids_and_path_segment_boundaries(self):
        result = self.convert(path_prefixes=None, symbol_ids=[self.doc["nodes"][0]["id"]])
        self.assertEqual(1, len(result["artifact"]["payload"]["symbols"]))
        self.assertEqual([], result["artifact"]["payload"]["relations"])
        self.assertEqual("invalid", self.convert(path_prefixes=["exam"])["status"])
        self.assertEqual("invalid", self.convert(path_prefixes=None)["status"])
        self.assertEqual("invalid", self.convert(symbol_ids=["missing"])["status"])
        self.assertEqual("invalid", self.convert(path_prefixes=["../example"])["status"])

    def test_revision_required_and_never_inferred_from_fingerprint(self):
        self.doc["companion"] = {"sourceFingerprint": "f" * 64, "snapshotId": "private-id"}
        result = self.convert(revision=None)
        self.assertEqual("unsupported", result["status"])
        self.assertIsNone(result["artifact"])
        for revision in ("a" * 40 + "\n", "A" * 40, "commit:main", True):
            self.assertEqual("invalid", self.convert(revision=revision)["status"])

    def test_repository_identity_must_be_explicit_and_portable(self):
        for identity in (None, "/private/repo", "C:/private/repo", "https://token@example.com/repo", "file:private", "has space"):
            self.assertEqual("invalid", self.convert(repository_id=identity)["status"])

    def test_unknown_versions_and_semantic_fields_rejected(self):
        for key, value in (("schema_version", "2.0"), ("generator", {"name": "Code Ontology Companion", "version": "0.7.0"})):
            doc = copy.deepcopy(self.doc)
            doc[key] = value
            self.assertEqual("unsupported", self.convert(doc)["status"])
        for section in (None, "nodes", "edges"):
            doc = copy.deepcopy(self.doc)
            target = doc if section is None else doc[section][0]
            target["future_semantics"] = "do not silently reinterpret"
            self.assertEqual("invalid", self.convert(doc)["status"])

    def test_duplicate_id_and_dangling_edge_rejected_before_selection(self):
        self.doc["nodes"].append(copy.deepcopy(self.doc["nodes"][0]))
        self.assertEqual("invalid", self.convert()["status"])
        self.doc["nodes"].pop()
        self.doc["edges"][1]["target"] = "not-in-source"
        self.assertEqual("invalid", self.convert()["status"])

    def test_invalid_paths_spans_and_evidence_fail_closed(self):
        changes = [("path", "/private/secret"), ("path", "x/../y"), ("metadata", {"line_start": True, "line_end": 5}),
                   ("metadata", {"line_start": 6, "line_end": 2})]
        for key, value in changes:
            doc = copy.deepcopy(self.doc)
            doc["nodes"][0][key] = value
            self.assertEqual("invalid", self.convert(doc)["status"])
        self.doc["edges"][0]["evidence"][0]["runtime_status"] = "verified"
        self.assertEqual("invalid", self.convert()["status"])

    def test_hostile_json_and_bounds(self):
        for raw in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":1e999}', b'"\\ud800"', b"[" * 1500 + b"0" + b"]" * 1500,
                    b" " * (MAX_SOURCE_BYTES + 1), b'"\xff"'):
            result = convert_code_snapshot(raw, **self.options)
            self.assertEqual("invalid", result["status"])
            self.assertIsNone(result["artifact"])
            self.assertLess(len(json.dumps(result)), 700)

    def test_output_contract_limit_requires_reselection_no_truncation(self):
        template = self.doc["nodes"][0]
        self.doc["nodes"] = [dict(template, id=f"python:function:example.f{i}") for i in range(1001)]
        self.doc["edges"] = []
        result = self.convert()
        self.assertEqual("invalid", result["status"])
        self.assertEqual("output_contract_limit_reselect", result["errors"][0]["rule_id"])
        self.assertIsNone(result["artifact"])

    def test_native_reference_digest_and_limits_preserved(self):
        native = native_fixture()
        result = convert_code_snapshot(canonical(native))
        self.assertEqual("converted", result["status"], result)
        self.assertEqual("snapshot_head_observation", result["mapping_report"]["revision_basis"])
        self.assertEqual(3, result["mapping_report"]["loss_counts"]["source_previously_omitted_relations"])
        self.assertEqual(native["symbols"][0]["id"], result["artifact"]["payload"]["symbols"][0]["id"])
        native["symbols"][0]["qualified_name"] = "changed"
        self.assertEqual("invalid", convert_code_snapshot(canonical(native))["status"])

    def test_native_no_authority_upgrade_or_identity_override(self):
        native = native_fixture()
        for field, value in (("repository_id", "github:other/repo"), ("snapshot_id", "other"), ("revision", "b" * 40)):
            self.assertEqual("invalid", convert_code_snapshot(canonical(native), **{field: value})["status"])
        native["authority"]["approval"] = "approved"
        self.assertEqual("invalid", convert_code_snapshot(canonical(resign(native)))["status"])

    def test_native_null_revision_requires_explicit_annotation(self):
        native = native_fixture()
        native["snapshot"].update(repository_revision=None, revision_binding="unavailable")
        raw = canonical(resign(native))
        self.assertEqual("unsupported", convert_code_snapshot(raw)["status"])
        result = convert_code_snapshot(raw, revision="a" * 40)
        self.assertEqual("converted", result["status"])
        self.assertEqual("caller_supplied_annotation", result["mapping_report"]["revision_basis"])

    def test_native_module_boundary_cannot_be_silently_expanded(self):
        native = native_fixture()
        native["scope"]["module_root"] = "other"
        result = convert_code_snapshot(canonical(resign(native)))
        self.assertEqual("invalid", result["status"])
        self.assertEqual("source_module_resolution", result["errors"][0]["rule_id"])

    def test_mcp_no_files_or_network_and_full_output_schema(self):
        args = {"snapshot_json": canonical(self.doc).decode(), **self.options}
        with patch("socket.create_connection", side_effect=AssertionError("network")), patch("builtins.open", side_effect=AssertionError("file access")):
            result = invoke("convert_code_snapshot", args)
        self.assertEqual("converted", result["status"])
        self.assertFalse(result["writes_performed"])
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("Optional independent schema check requires development jsonschema.")
        checker = Draft202012Validator(CONVERSION_OUTPUT)
        Draft202012Validator.check_schema(CONVERSION_OUTPUT)
        self.assertTrue(checker.is_valid(result), list(checker.iter_errors(result)))
        self.assertTrue(checker.is_valid(convert_code_snapshot(b"{}")))
        broken = copy.deepcopy(result)
        broken["artifact"]["evidence"][0]["code"]["basis"] = "runtime_verified"
        self.assertFalse(checker.is_valid(broken))
        tool = next(t for t in TOOLS if t["name"] == "convert_code_snapshot")
        self.assertTrue(tool["annotations"]["readOnlyHint"])
        with self.assertRaises(InvalidInput):
            invoke("convert_code_snapshot", args | {"output": "/private/out.json"})

    def test_stdio_large_realistic_snapshot_and_existing_artifact_strings(self):
        # Native snapshots easily exceed 512 KiB even when the selection is
        # small. Source diagnostics are retained only behind the input digest.
        self.doc["warnings"] = [{"message": "x" * 800, "path": "example/worker.py"} for _ in range(750)]
        source = canonical(self.doc).decode()
        self.assertGreater(len(source), 524288)
        artifact = self.convert()["artifact"]
        # Add permitted independent evidence so the validator input is > 8 KiB.
        for n in range(30):
            ev = copy.deepcopy(artifact["evidence"][0])
            ev["id"] = f"test:{n}"
            artifact["evidence"].append(ev)
        artifact_json = canonical(artifact).decode()
        self.assertGreater(len(artifact_json), 8192)
        requests = [{"jsonrpc": "2.0", "id": 1, "method": "initialize"},
                    {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "convert_code_snapshot", "arguments": {"snapshot_json": source, **self.options}}},
                    {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "validate_artifact", "arguments": {"artifact_json": artifact_json}}}]
        process = subprocess.run([sys.executable, str(ROOT / "scripts/run.py"), "stdio"], input=b"\n".join(canonical(r) for r in requests) + b"\n", capture_output=True, timeout=10)
        self.assertEqual(0, process.returncode, process.stderr)
        rows = [json.loads(line) for line in process.stdout.splitlines()]
        self.assertEqual("converted", rows[1]["result"]["structuredContent"]["status"])
        self.assertEqual("valid", rows[2]["result"]["structuredContent"]["status"])

    def test_wire_data_exceptions_do_not_expand_metadata_or_structure_limits(self):
        for value in ({"params": {"other": "x" * 8193}}, {"params": {"arguments": {"artifact_json": "x" * 524289}}},
                      {"params": {"arguments": {"snapshot_json": "x" * (MAX_SOURCE_BYTES + 1)}}},
                      {"params": {"items": list(range(1001))}}):
            with self.assertRaises(InvalidInput):
                _parse_request(canonical(value))
        for raw in (b'{"x":1e999}', b'{"x":1,"x":2}', b'"\\ud800"'):
            with self.assertRaises(InvalidInput):
                _parse_request(raw)

    def test_explicit_file_reads_refuse_symlink_and_nonregular(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_bytes(canonical(self.doc))
            self.assertEqual(path.read_bytes(), read_snapshot(path))
            with self.assertRaises(InvalidInput):
                read_snapshot(directory)
            link = Path(directory) / "link.json"
            try:
                link.symlink_to(path)
            except OSError:
                return
            with self.assertRaises(InvalidInput):
                read_snapshot(link)

    def test_cli_arbitrary_cwd_output_only_explicit_and_exclusive(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / "snapshot.json"
            raw = canonical(self.doc)
            source.write_bytes(raw)
            command = [sys.executable, str(ROOT / "scripts/run.py"), "convert-code", str(source),
                       "--repository-id", self.options["repository_id"], "--revision", self.options["revision"], "--path-prefix", "example"]
            process = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=10)
            self.assertEqual(0, process.returncode, process.stderr + process.stdout)
            self.assertEqual(["snapshot.json"], sorted(p.name for p in folder.iterdir()))
            output = folder / "projection.json"
            process = subprocess.run(command + ["--output", str(output)], cwd=directory, capture_output=True, text=True, timeout=10)
            self.assertEqual(0, process.returncode, process.stderr + process.stdout)
            self.assertTrue(json.loads(process.stdout)["writes_performed"])
            saved = output.read_bytes()
            self.assertEqual("valid", validate_artifact(json.loads(saved))["status"])
            again = subprocess.run(command + ["--output", str(output)], cwd=directory, capture_output=True, text=True, timeout=10)
            self.assertEqual(2, again.returncode)
            self.assertEqual(saved, output.read_bytes())
            self.assertEqual(raw, source.read_bytes())
            self.assertEqual(["projection.json", "snapshot.json"], sorted(p.name for p in folder.iterdir()))

    def test_product_and_contract_versions_are_separate(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/run.py"), "--version"], capture_output=True, text=True, timeout=10)
        self.assertEqual(PRODUCT_VERSION, result.stdout.strip())
        self.assertEqual("0.1.0-draft.1", self.convert()["artifact"]["contract_version"])


if __name__ == "__main__":
    unittest.main()
