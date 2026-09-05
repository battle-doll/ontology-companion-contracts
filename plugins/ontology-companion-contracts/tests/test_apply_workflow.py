from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "skills/apply-ontology-contracts/scripts/apply_workflow.py"
spec = importlib.util.spec_from_file_location("contracts_application_test", HELPER)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


def capabilities(*enabled, mcp=False):
    return {product: {"installed": product in enabled, "skill_exposed": product in enabled,
                      "mcp_exposed": mcp and product in enabled, "verified_cli": not mcp and product in enabled}
            for product in app.PRODUCTS}


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name)
        self.path = self.directory / "selected.json"
        self.raw = (ROOT / "examples/context-decision.json").read_bytes()
        self.path.write_bytes(self.raw)
        self.args = {"artifact": str(self.path), "profile": "context-decision", "request_key": "current-task:contracts-check"}

    def tearDown(self):
        self.temporary.cleanup()

    def test_zero_one_two_three_capabilities_remain_plans(self):
        for count in range(4):
            observed = capabilities(*app.PRODUCTS[:count])
            result = app.plan(observed)
            self.assertEqual(count, result["availableCount"])
            self.assertEqual(list(app.PRODUCTS[:count]), result["selectedProducts"])
            self.assertFalse(result["executionPerformed"])
            self.assertEqual("NOT_EXECUTED", result["activationStatus"])
            self.assertTrue(all(not r["executionPerformed"] for r in result["routes"]))

    def test_explicit_single_and_multiple_products_override_availability(self):
        result = app.plan(capabilities(*app.PRODUCTS), explicit_products=["contracts"])
        self.assertEqual(["contracts"], result["selectedProducts"])
        self.assertFalse(result["scope"]["otherProductsExecuted"])
        result = app.plan(capabilities("contracts"), explicit_products=["context", "contracts"])
        self.assertEqual(["context", "contracts"], result["selectedProducts"])
        self.assertEqual("unavailable", result["routes"][0]["route"])
        self.assertEqual("verified_sibling_cli", result["routes"][1]["route"])
        duplicate = app.plan(capabilities(*app.PRODUCTS), explicit_products=["contracts", "context", "contracts"])
        self.assertEqual(["contracts", "context"], duplicate["selectedProducts"])
        self.assertEqual(2, len(duplicate["routes"]))

    def test_installed_or_skill_exposed_is_not_execution_capability(self):
        for key in ("installed", "skill_exposed"):
            result = app.plan({p: {key: True} for p in app.PRODUCTS})
            self.assertEqual([], result["selectedProducts"])
        observed = capabilities(*app.PRODUCTS)
        observed["code"]["skill_exposed"] = False
        observed["context"]["skill_exposed"] = False
        self.assertEqual(["contracts"], app.plan(observed)["selectedProducts"])
        with self.assertRaises(app.ApplicationError):
            app.plan({"contracts": {"verified_cli": "true"}})

    def test_actual_same_bundle_validation_binds_exact_file_bytes(self):
        before = (self.path.read_bytes(), self.path.stat().st_mtime_ns)
        result = app.run_contracts(capabilities("contracts"), **self.args)
        self.assertEqual("verified", result["status"], result)
        self.assertTrue(result["executionPerformed"])
        self.assertEqual("valid", result["validation"]["status"])
        self.assertEqual(str(self.path.absolute()), result["binding"]["artifact_path"])
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), result["binding"]["artifact_sha256"])
        self.assertEqual("context-decision", result["binding"]["profile"])
        self.assertIn("current_authorization", result["validation"]["not_checked"])
        self.assertEqual(before, (self.path.read_bytes(), self.path.stat().st_mtime_ns))
        self.assertEqual(["selected.json"], [p.name for p in self.directory.iterdir()])

    def test_missing_target_profile_and_request_are_needs_input(self):
        for field in self.args:
            args = dict(self.args)
            args[field] = None
            result = app.run_contracts(capabilities("contracts"), **args)
            self.assertEqual("needs_input", result["status"])
            self.assertFalse(result["executionPerformed"])
            self.assertIsNone(result["validation"])
        self.assertEqual("unavailable", app.run_contracts(capabilities(), **self.args)["status"])
        self.assertEqual(["selected.json"], [p.name for p in self.directory.iterdir()])

    def test_wrong_profile_cannot_turn_valid_artifact_into_application_success(self):
        result = app.run_contracts(capabilities("contracts"), **(self.args | {"profile": "code-reference"}))
        self.assertEqual("valid", result["validation"]["status"])
        self.assertEqual("context-decision", result["validation"]["profile"])
        self.assertEqual("incomplete", result["status"])
        self.assertIn("artifact_profile_mismatch", result["issues"])
        result = app.run_contracts(capabilities("contracts", mcp=True), **(self.args | {"profile": "code-reference"}))
        self.assertEqual("incomplete", result["status"])
        self.assertNotIn("handoff", result)

    def test_duplicate_unknown_version_and_invalid_inputs_are_preserved(self):
        self.path.write_bytes(b'{"profile":"context-decision","profile":"context-decision"}')
        result = app.run_contracts(capabilities("contracts"), **self.args)
        self.assertEqual("incomplete", result["status"])
        self.assertEqual("duplicate_key", result["validation"]["errors"][0]["rule_id"])
        artifact = json.loads(self.raw)
        artifact["contract_version"] = "99.0.0"
        self.path.write_text(json.dumps(artifact))
        result = app.run_contracts(capabilities("contracts"), **self.args)
        self.assertEqual("unsupported", result["status"])
        self.assertEqual("unsupported", result["validation"]["status"])
        self.path.write_bytes(b"x" * 524289)
        self.assertEqual("incomplete", app.run_contracts(capabilities("contracts"), **self.args)["status"])

    def test_profile_wrapper_is_not_silently_unwrapped(self):
        self.path.write_text(json.dumps({"artifact": json.loads(self.raw), "mapping_report": {"loss_counts": {"omitted": 1}}}))
        result = app.run_contracts(capabilities("contracts"), **self.args)
        self.assertEqual("incomplete", result["status"])
        self.assertNotEqual("valid", result["validation"]["status"])

    def test_exposed_mcp_is_only_a_handoff_even_with_cli_available(self):
        observed = capabilities("contracts", mcp=True)
        observed["contracts"]["verified_cli"] = True
        result = app.run_contracts(observed, **self.args)
        self.assertEqual("handoff_required", result["status"])
        self.assertEqual("NOT_EXECUTED", result["activationStatus"])
        self.assertFalse(result["executionPerformed"])
        self.assertIsNone(result["validation"])
        self.assertEqual(self.raw.decode(), result["handoff"]["arguments"]["artifact_json"])
        self.assertEqual(result["binding"], result["handoff"]["binding"])

    def test_handoff_raw_stdio_dispatch_returns_actual_matching_validation(self):
        result = app.run_contracts(capabilities("contracts", mcp=True), **self.args)
        handoff = result["handoff"]
        requests = [{"jsonrpc": "2.0", "id": 1, "method": "initialize"},
                    {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": handoff["tool"], "arguments": handoff["arguments"]}}]
        process = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "scripts/run.py"), "stdio"],
                                 input="\n".join(json.dumps(r) for r in requests) + "\n", cwd=self.directory,
                                 capture_output=True, text=True, timeout=10)
        self.assertEqual(0, process.returncode, process.stderr)
        rows = [json.loads(line) for line in process.stdout.splitlines()]
        actual = rows[1]["result"]["structuredContent"]
        self.assertEqual("valid", actual["status"])
        self.assertEqual(handoff["expectedProfile"], actual["profile"])
        self.assertEqual(hashlib.sha256(self.path.read_bytes()).hexdigest(), handoff["binding"]["artifact_sha256"])
        # Transport evidence does not retroactively make the coordinator itself
        # an MCP executor, and no application marker is written.
        self.assertFalse(result["executionPerformed"])
        self.assertEqual(["selected.json"], [p.name for p in self.directory.iterdir()])

    def test_ledger_routes_to_freshness_without_duplicate_validation(self):
        first = app.run_contracts(capabilities("contracts"), **self.args)
        ledger = {"version": 1, "products": {"contracts": first["ledgerEntry"]}}
        plan = app.plan(capabilities(*app.PRODUCTS), ledger=ledger)
        self.assertEqual("already_applied_recheck_freshness", plan["routes"][2]["route"])
        self.assertFalse(plan["executionPerformed"])
        validator, version = app._validator()
        with patch.object(validator, "validate_bytes", side_effect=AssertionError("duplicate validation")), patch.object(app, "_validator", return_value=(validator, version)):
            inspected = app.inspect_target(**self.args, ledger=ledger)
        self.assertEqual("inspected", inspected["status"])
        self.assertTrue(inspected["receiptReuseEligible"])
        self.assertFalse(inspected["receiptReused"])
        self.assertFalse(inspected["executionPerformed"])
        self.assertIsNone(inspected["validation"])
        # The caller holds `first`, the actual previous validator output, and
        # can reuse it after this binding check instead of a second run.
        self.assertEqual(first["binding"], inspected["binding"])
        self.assertEqual("valid", first["validation"]["status"])

    def test_changed_bytes_path_profile_or_request_prevents_receipt_reuse(self):
        first = app.run_contracts(capabilities("contracts"), **self.args)
        ledger = {"version": 1, "products": {"contracts": first["ledgerEntry"]}}
        changed = json.loads(self.raw)
        changed["artifact_id"] = "different:artifact"
        self.path.write_text(json.dumps(changed))
        self.assertFalse(app.inspect_target(**self.args, ledger=ledger)["receiptReuseEligible"])
        self.path.write_bytes(self.raw)
        other = self.directory / "other.json"
        other.write_bytes(self.raw)
        for options in ({"artifact": str(other)}, {"profile": "code-reference"}, {"request_key": "different-task"}):
            self.assertFalse(app.inspect_target(**(self.args | options), ledger=ledger)["receiptReuseEligible"])

    def test_explicit_new_run_revalidates_even_with_matching_ledger(self):
        first = app.run_contracts(capabilities("contracts"), **self.args)
        ledger = {"version": 1, "products": {"contracts": first["ledgerEntry"]}}
        validator, version = app._validator()
        with patch.object(validator, "validate_bytes", wraps=validator.validate_bytes) as called, patch.object(app, "_validator", return_value=(validator, version)):
            second = app.run_contracts(capabilities("contracts"), **self.args, ledger=ledger)
        self.assertEqual(1, called.call_count)
        self.assertEqual("verified", second["status"])
        self.assertTrue(second["receiptReuseEligible"])
        self.assertFalse(second["receiptReused"])

    def test_product_flag_or_fabricated_ledger_is_not_an_execution_receipt(self):
        ledger = {"version": 1, "products": {"contracts": {"request_key": self.args["request_key"], "status": "verified", "evidence": {}}}}
        result = app.inspect_target(**self.args, ledger=ledger)
        self.assertFalse(result["receiptReuseEligible"])
        self.assertFalse(result["executionPerformed"])
        with self.assertRaises(app.ApplicationError):
            app.plan(capabilities(), ledger={"contracts": True})

    def test_validator_failure_and_unavailable_source_never_verify(self):
        validator, version = app._validator()
        with patch.object(validator, "validate_bytes", side_effect=ValueError("private payload")), patch.object(app, "_validator", return_value=(validator, version)):
            result = app.run_contracts(capabilities("contracts"), **self.args)
        self.assertEqual("incomplete", result["status"])
        self.assertNotIn("private payload", json.dumps(result))
        self.path.unlink()
        result = app.run_contracts(capabilities("contracts"), **self.args)
        self.assertEqual("incomplete", result["status"])
        self.assertFalse(result["executionPerformed"])

    def test_cli_arbitrary_directory_controls_and_no_same_named_target_execution(self):
        decoy = self.directory / "validator.py"
        decoy.write_text("raise RuntimeError('target executed')")
        command = [sys.executable, "-I", "-B", str(HELPER), "run-contracts", "--capabilities", json.dumps(capabilities("contracts")),
                   "--artifact", str(self.path), "--profile", self.args["profile"], "--request-key", self.args["request_key"]]
        process = subprocess.run(command, cwd=self.directory, capture_output=True, text=True, timeout=10)
        self.assertEqual(0, process.returncode, process.stderr + process.stdout)
        self.assertEqual("verified", json.loads(process.stdout)["status"])
        self.assertEqual(["selected.json", "validator.py"], sorted(p.name for p in self.directory.iterdir()))
        for control in ('{"contracts":{},"contracts":{}}', '{"contracts":{"verified_cli":1}}', '{"x":1e999}'):
            process = subprocess.run([sys.executable, "-I", "-B", str(HELPER), "plan", "--capabilities", control],
                                     cwd=self.directory, capture_output=True, text=True, timeout=10)
            self.assertEqual(2, process.returncode)

    def test_symlink_source_and_helper_layout_refused(self):
        target = self.directory / "real.json"
        self.path.rename(target)
        try:
            self.path.symlink_to(target)
        except OSError:
            self.skipTest("Host cannot create symlinks.")
        self.assertEqual("incomplete", app.run_contracts(capabilities("contracts"), **self.args)["status"])
        with patch.object(app, "__file__", str(self.directory / "foreign/skills/apply-ontology-contracts/scripts/apply_workflow.py")):
            self.assertEqual("incomplete", app.run_contracts(capabilities("contracts"), **self.args)["status"])


if __name__ == "__main__":
    unittest.main()
