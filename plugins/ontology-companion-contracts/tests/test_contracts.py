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
from companion_contracts import (CONTRACT_VERSION, CO_NAMESPACE, MAX_BYTES,
    compatibility, migration_plan, read_artifact, validate_artifact, validate_bytes)
from companion_contracts.transport import MAX_RPC_BYTES, TOOLS, invoke
from companion_contracts.validator import InvalidInput, _schema


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.context = json.loads((ROOT / "examples/context-decision.json").read_text())
        self.code = json.loads((ROOT / "examples/code-reference.json").read_text())

    def invalid(self, artifact, rule=None):
        result = validate_artifact(artifact)
        self.assertEqual("invalid", result["status"], result)
        if rule:
            self.assertIn(rule, [error["rule_id"] for error in result["errors"]], result)
        return result

    def test_both_profiles_valid_with_unchecked_external_facts(self):
        for artifact in (self.context, self.code):
            result = validate_artifact(artifact)
            self.assertEqual("valid", result["status"], result)
            self.assertEqual("not_checked", result["layers"]["external_verification"])
            self.assertEqual("not_checked", result["layers"]["L3_compatibility"])
            self.assertIn("current_authorization", result["not_checked"])

    def test_validation_deterministic_and_input_unchanged(self):
        before = copy.deepcopy(self.context)
        self.assertEqual(validate_artifact(self.context), validate_artifact(self.context))
        self.assertEqual(before, self.context)

    def test_duplicate_json_keys_rejected(self):
        for raw in (b'{"x":1,"x":2}', b'{"nested":{"secret":1,"secret":2}}'):
            result = validate_bytes(raw)
            self.assertEqual("invalid", result["status"])
            self.assertEqual("duplicate_key", result["errors"][0]["rule_id"])
            self.assertNotIn("secret", json.dumps(result))

    def test_non_finite_numbers_rejected(self):
        for raw in (b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}', b'{"x":1e999}'):
            result = validate_bytes(raw)
            self.assertEqual("invalid", result["status"])
            self.assertEqual("non_finite_number", result["errors"][0]["rule_id"])

    def test_byte_limit(self):
        result = validate_bytes(b" " * (MAX_BYTES + 1))
        self.assertEqual("byte_limit", result["errors"][0]["rule_id"])

    def test_depth_limit(self):
        for depth in (33, 1500):
            result = validate_bytes(b"[" * depth + b"0" + b"]" * depth)
            self.assertEqual("invalid", result["status"])
            self.assertEqual("invalid", result["layers"]["L0_parse"])

    def test_collection_limit(self):
        result = validate_bytes(json.dumps([0] * 1001).encode())
        self.assertEqual("collection_limit", result["errors"][0]["rule_id"])

    def test_string_limit(self):
        result = validate_bytes(json.dumps("s" * 8193).encode())
        self.assertEqual("string_limit", result["errors"][0]["rule_id"])

    def test_utf8_and_surrogates(self):
        for raw in (b'"\xff"', b'"\\ud800"'):
            self.assertEqual("invalid", validate_bytes(raw)["status"])

    def test_unknown_versions_and_profiles_fail_unsupported(self):
        for key, value in (("contract_version", "999.0.0"), ("profile", "unknown")):
            artifact = copy.deepcopy(self.context)
            artifact[key] = value
            result = validate_artifact(artifact)
            self.assertEqual("unsupported", result["status"])
            self.assertEqual("not_checked", result["layers"]["L2_profile"])

    def test_missing_field_and_additional_fields(self):
        del self.context["producer"]
        self.invalid(self.context, "required")
        self.context["$ref"] = "https://example.com/private-schema"
        with patch("socket.create_connection", side_effect=AssertionError("network attempted")):
            result = self.invalid(self.context, "additional_properties")
        self.assertNotIn("https://example.com", json.dumps(result))

    def test_wrong_profile_payload(self):
        self.context["payload"] = self.code["payload"]
        self.invalid(self.context, "required")

    def test_dangling_evidence(self):
        self.context["payload"]["decisions"][0]["evidence_refs"] = ["missing"]
        self.invalid(self.context, "dangling_evidence")

    def test_duplicate_evidence_id(self):
        self.context["evidence"].append(copy.deepcopy(self.context["evidence"][0]))
        self.invalid(self.context, "duplicate_id")

    def test_duplicate_record_id(self):
        self.context["payload"]["decisions"].append(copy.deepcopy(self.context["payload"]["decisions"][0]))
        self.invalid(self.context, "duplicate_id")

    def test_cross_scope_rejected(self):
        self.context["evidence"][0]["scope"] = "project:other"
        self.invalid(self.context, "evidence_scope")

    def test_inference_not_upgraded_by_reference(self):
        self.context["evidence"][0]["origin"] = "model_inferred"
        self.invalid(self.context, "origin_lineage")
        self.context["payload"]["decisions"][0]["origin"] = "model_inferred"
        self.assertEqual("valid", validate_artifact(self.context)["status"])

    def test_intervals_empty_and_reversed(self):
        for end in ("2026-09-05T00:00:00Z", "2026-09-04T00:00:00Z"):
            self.context["payload"]["decisions"][0]["valid_until"] = end
            self.invalid(self.context, "interval_order")

    def test_timestamp_utc_calendar_and_missing_timezone(self):
        for value in ("2026-02-30T00:00:00Z", "2026-09-05T00:00:00", "2026-09-05T00:00:00+09:00"):
            self.context["payload"]["decisions"][0]["recorded_at"] = value
            self.invalid(self.context)

    def test_past_effective_time_is_valid(self):
        self.context["payload"]["decisions"][0]["valid_from"] = "2020-01-01T00:00:00Z"
        self.assertEqual("valid", validate_artifact(self.context)["status"])

    def test_duplicate_reference_rejected(self):
        self.context["payload"]["decisions"][0]["evidence_refs"] *= 2
        self.invalid(self.context, "unique_items")

    def test_code_namespace_is_exact_legacy_identity(self):
        self.assertEqual(CO_NAMESPACE, self.code["payload"]["co_namespace"])
        self.code["payload"]["co_namespace"] = "https://example.com/new/schema#"
        self.invalid(self.code, "constant")

    def test_legacy_synthetic_identity_and_triples_preserved(self):
        before = copy.deepcopy(self.code)
        expected = ("java:method:demo.Worker.run", "java:method:demo.Worker.helper", "CALLS")
        self.assertEqual(expected, tuple(self.code["payload"]["relations"][0][k] for k in ("source", "target", "type")))
        self.assertEqual("not_applicable", self.code["evidence"][0]["code"]["runtime_status"])
        self.assertEqual("valid", validate_artifact(self.code)["status"])
        self.assertEqual(before, self.code)

    def test_code_runtime_claim_rejected(self):
        self.code["payload"]["symbols"][0]["runtime_status"] = "verified"
        self.invalid(self.code, "constant")

    def test_code_portable_paths(self):
        for value in ("/private/source.py", "C:\\private\\source.py", "\\\\host\\share", "../private.py", "safe/../x.py", "safe\\x.py", "safe//x.py"):
            self.code["payload"]["symbols"][0]["source_path"] = value
            self.invalid(self.code, "portable_path")

    def test_code_spans_and_booleans(self):
        self.code["payload"]["symbols"][0]["end_line"] = 1
        self.invalid(self.code, "span_order")
        self.code["payload"]["symbols"][0]["start_line"] = True
        self.invalid(self.code, "type")

    def test_code_dangling_endpoint(self):
        self.code["payload"]["relations"][0]["target"] = "missing"
        self.invalid(self.code, "dangling_symbol")

    def test_compatibility_only_explicit_same_version(self):
        for profile in ("context-decision", "code-reference"):
            self.assertEqual("compatible", compatibility(CONTRACT_VERSION, CONTRACT_VERSION, profile)["status"])
            self.assertEqual("unsupported", compatibility(CONTRACT_VERSION, "0.1.0", profile)["status"])
            self.assertEqual("unsupported", compatibility("0.1.0", CONTRACT_VERSION, profile)["status"])

    def test_identity_plan_and_unsupported_loss(self):
        before = copy.deepcopy(self.context)
        plan = migration_plan(self.context, CONTRACT_VERSION)
        self.assertEqual("identity_plan", plan["status"])
        self.assertFalse(plan["writes_performed"])
        self.assertEqual([], plan["losses"])
        for version, profile in (("1.0.0", "context-decision"), (CONTRACT_VERSION, "code-reference")):
            plan = migration_plan(self.context, version, profile)
            self.assertEqual("unsupported", plan["status"])
            self.assertTrue(plan["losses"])
        self.assertEqual(before, self.context)

    def test_errors_are_bounded_and_do_not_echo_payload(self):
        self.context["evidence"] *= 100
        self.context["private-key-SECRET"] = "DO-NOT-LOG"
        result = self.invalid(self.context)
        encoded = json.dumps(result)
        self.assertLessEqual(len(result["errors"]), 32)
        self.assertLess(len(encoded), 32768)
        self.assertNotIn("SECRET", encoded)
        self.assertNotIn("DO-NOT-LOG", encoded)

    def test_file_read_does_not_mutate_source(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text(json.dumps(self.context))
            before = (path.read_bytes(), path.stat().st_mtime_ns)
            self.assertEqual("valid", validate_bytes(read_artifact(path))["status"])
            self.assertEqual(before, (path.read_bytes(), path.stat().st_mtime_ns))
            self.assertEqual(["input.json"], [p.name for p in Path(directory).iterdir()])

    def test_symlink_file_refused_when_supported(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "real.json"
            target.write_text("{}")
            link = Path(directory) / "link.json"
            try:
                link.symlink_to(target)
            except OSError:
                self.skipTest("Host cannot create symlinks without elevated privileges.")
            with self.assertRaises(InvalidInput):
                read_artifact(link)

    def test_directory_and_fifo_refused_without_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(InvalidInput):
                read_artifact(directory)
            if hasattr(os, "mkfifo"):
                pipe = Path(directory) / "pipe"
                os.mkfifo(pipe)
                with self.assertRaises(InvalidInput):
                    read_artifact(pipe)

    def test_tool_descriptors_and_actual_calls(self):
        for tool in TOOLS:
            self.assertTrue(tool["annotations"]["readOnlyHint"])
            self.assertFalse(tool["annotations"]["openWorldHint"])
            self.assertFalse(tool["annotations"]["destructiveHint"])
            self.assertTrue(tool["annotations"]["idempotentHint"])
            self.assertEqual("object", tool["outputSchema"]["type"])
        output = invoke("validate_artifact", {"artifact_json": json.dumps(self.context)})
        self.assertEqual("valid", output["status"])
        with self.assertRaises(InvalidInput):
            invoke("validate_artifact", {"artifact_json": json.dumps(self.context), "path": "/private"})

    def test_actual_tool_outputs_conform_to_declared_schema(self):
        calls = {"validate_artifact": {"artifact_json": json.dumps(self.context)},
                 "compare_versions": {"producer_version": CONTRACT_VERSION, "consumer_version": CONTRACT_VERSION, "profile": "context-decision"},
                 "plan_migration": {"artifact_json": json.dumps(self.context), "target_version": CONTRACT_VERSION},
                 "convert_code_snapshot": {"snapshot_json": "{}"}}
        for tool in TOOLS:
            result = invoke(tool["name"], calls[tool["name"]])
            check = {"errors": []}
            _schema(result, tool["outputSchema"], check)
            self.assertEqual([], check["errors"], (tool["name"], check))

    def test_invalid_migration_preserves_parse_failure(self):
        output = invoke("plan_migration", {"artifact_json": '{"x":1,"x":2}', "target_version": CONTRACT_VERSION})
        self.assertEqual("unsupported", output["status"])
        self.assertEqual("invalid", output["source_validation"]["layers"]["L0_parse"])
        self.assertEqual("duplicate_key", output["source_validation"]["errors"][0]["rule_id"])

    def test_unicode_context_roundtrip(self):
        self.context["payload"]["decisions"][0]["statement"] = "배포 전에 회귀 시험을 수행합니다."
        raw = json.dumps(self.context, ensure_ascii=False).encode("utf-8")
        self.assertEqual(validate_bytes(raw), validate_artifact(self.context))

    def test_schema_parity_with_independent_jsonschema(self):
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("Optional development parity check requires jsonschema; runtime remains stdlib-only.")
        schema_dir = ROOT / "src/companion_contracts/_schemas"
        envelope = Draft202012Validator(json.loads((schema_dir / "envelope.schema.json").read_text()))
        profile_schemas = {name: Draft202012Validator(json.loads((schema_dir / (name + ".schema.json")).read_text()))
                           for name in ("context-decision", "code-reference")}
        for validator in [envelope, *profile_schemas.values()]:
            Draft202012Validator.check_schema(validator.schema)
        corpus = [copy.deepcopy(self.context), copy.deepcopy(self.code)]
        for value in (" prefix:suffix ", "id:embedded space", "id:newline\n", "\nid:prefix", "", "a" * 161, "id:한국어"):
            document = copy.deepcopy(self.context)
            document["artifact_id"] = value
            corpus.append(document)
        for value in ("prefix" + "a" * 40, "a" * 40 + "suffix", "a" * 40 + "\n", "a" * 40, "a" * 64, "A" * 40):
            document = copy.deepcopy(self.code)
            document["payload"]["revision"] = value
            corpus.append(document)
        for value in (True, False, 0, 1.0, 1.5, 10000001, 1e12):
            document = copy.deepcopy(self.code)
            document["payload"]["symbols"][0]["start_line"] = value
            corpus.append(document)
        for value in (" direct.rule", "rule.ok\n", "rule.ok", "UPPER.rule"):
            document = copy.deepcopy(self.code)
            document["evidence"][0]["code"]["rule_id"] = value
            corpus.append(document)
        for index, document in enumerate(corpus):
            with self.subTest(index=index):
                expected = envelope.is_valid(document) and profile_schemas[document["profile"]].is_valid(document["payload"])
                result = validate_artifact(document)
                self.assertEqual(expected, result["layers"]["L1_schema"] == "valid", result)

    def test_cli_independent_arbitrary_working_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            process = subprocess.run([sys.executable, str(ROOT / "scripts/run.py"), "validate", str(ROOT / "examples/context-decision.json")], cwd=directory, capture_output=True, text=True, timeout=10)
            self.assertEqual(0, process.returncode, process.stderr)
            self.assertEqual("valid", json.loads(process.stdout)["status"])
            self.assertEqual([], list(Path(directory).iterdir()))

    def test_stdio_initialize_tools_and_call(self):
        requests = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}},
                    {"jsonrpc": "2.0", "method": "notifications/initialized"},
                    {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
                    {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "validate_artifact", "arguments": {"artifact_json": json.dumps(self.context)}}}]
        raw = "".join(json.dumps(value) + "\n" for value in requests)
        process = subprocess.run([sys.executable, str(ROOT / "scripts/run.py"), "stdio"], input=raw, capture_output=True, text=True, timeout=10)
        self.assertEqual(0, process.returncode, process.stderr)
        rows = [json.loads(line) for line in process.stdout.splitlines()]
        self.assertEqual(3, len(rows))
        self.assertEqual(4, len(rows[1]["result"]["tools"]))
        self.assertEqual("valid", rows[2]["result"]["structuredContent"]["status"])

    def test_stdio_oversize_fail_closed(self):
        process = subprocess.run([sys.executable, str(ROOT / "scripts/run.py"), "stdio"], input=b"x" * (MAX_RPC_BYTES + 1) + b'\n{"jsonrpc":"2.0","id":2,"method":"initialize"}\n', capture_output=True, timeout=10)
        self.assertEqual(2, process.returncode)
        self.assertEqual(1, len(process.stdout.splitlines()))


if __name__ == "__main__":
    unittest.main()
