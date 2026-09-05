---
name: apply-ontology-contracts
description: Apply Ontology Companion Contracts to this conversation or task by validating the actual selected interchange artifact, or route a generic ontology setup request to available companions. Use for "Contracts 여기에 적용해줘" or "온톨로지 여기 설정해줘". Direct validation, conversion and persistent MCP setup belong to validate-ontology-contract; explicit Code-only or Context-only requests keep their own product scope.
---

# Apply Ontology Contracts

Apply the selected companions to the current work and continue that work. “Here” means this conversation unless the user names another scope. Do not write activation markers, a persistent ledger, `AGENTS.md`, global settings or project configuration for conversation use. An application plan or a generated prompt does not mean a product ran.

## Select actual capabilities once per application flow

Honor explicit product names first, including more than one named product. For a generic ontology request, inspect this conversation's inventory and select the runnable subset of Code, Context and Contracts: zero, one, two or three. Keep each observation separate: `installed`, `skill_exposed`, `mcp_exposed`, `verified_cli`. An installed directory, development checkout, manifest declaration or exposed skill does not prove a callable MCP. A CLI route needs a verified interpreter, fixed installed-bundle helper and actual `--help` interface. Optional products also need their current skill's supported workflow. Do not install or configure a missing product to manufacture availability.

Coordinate one application flow in the current conversation with `{version:1, products:{code|context|contracts:{request_key, status, evidence}}}`. Use `pending`, `verified` or `incomplete` status. Product flags and supplied ledger JSON are host reports, not execution evidence or authorization. Keep the actual operation results behind each entry. When another selected skill joins the same flow, reuse its completed product result instead of invoking that product again.

Hand off a selected product with that product explicitly named and the same flow ledger. A delegated Contracts call handles Contracts only; it does not restart generic routing or hand Context back to an upstream skill. Missing Contracts input leaves that step pending and never triggers another Context write.

Before reusing a Contracts result, freshly inspect the same selected path and compare its SHA-256, requested profile and request key with the actual validation receipt already held in this task. Reuse only when all match and the real prior result was valid with the same profile; retain its unchecked and loss findings. Otherwise validate again. A plan's `already_applied_recheck_freshness` route never skips this check by itself. A new explicit helper run always validates again. Do not claim combined completion while any requested product is pending, unsupported or incomplete.

## Validate the selected artifact

Use the actual JSON exchanged in this task. Select its profile explicitly as `context-decision` or `code-reference`; the declared profile may resolve this choice after the user selected that file. Missing target or ambiguous profile means `needs_input`, while independent task work may continue. Do not scan for arbitrary artifacts, create an example, or substitute version compatibility for real validation.

Prefer exposed Contracts MCP. Read the selected bounded artifact, record the absolute selected path, SHA-256 and expected profile, then call the actual `validate_artifact` tool with those bytes as `artifact_json`. Check the actual returned `status` and `profile`, retaining the path/digest binding. A helper handoff is `NOT_EXECUTED` until that actual call succeeds. Do not mark MCP absent merely to force a CLI route.

If MCP is absent and a trusted bundled CLI is verified, run the helper below. It reads at most the supported artifact limit, verifies its own product bundle and validates the same bytes it hashed. It imports only its fixed sibling validator and never executes referenced target code. File or profile mismatch, malformed input and tool failures remain incomplete; unsupported versions remain unsupported.

Resolve this skill's plugin root as `Path(skill_file).resolve().parents[2]`. Its helper is `scripts/apply_workflow.py` relative to this skill directory. Use an absolute quoted helper path and an installed Python 3.11+ interpreter (`python3 -I -B` or Windows `py -3.12 -I -B`, with another installed supported version allowed). Never execute a same-named helper from the target project.

```text
<python> <apply-helper> plan --capabilities <observed-json> --explicit-product contracts --ledger <conversation-ledger-json>
<python> <apply-helper> inspect-target --artifact <selected.json> --profile context-decision --request-key <current-operation-key> --ledger <conversation-ledger-json>
<python> <apply-helper> run-contracts --capabilities <observed-json> --artifact <selected.json> --profile context-decision --request-key <current-operation-key>
```

Repeat `--explicit-product` for multiple named products. Omit the ledger when none exists. `plan` only routes, and `inspect-target` only checks current bytes for possible receipt reuse; neither validates nor activates anything. `run-contracts` returns an unexecuted host handoff when MCP is exposed. Without MCP, only the observed verified CLI route can execute same-bundle Contracts validation. Other products are always handed back to their currently available skill, never imported or executed here.

## Preserve evidence and continue

Keep the actual validator output, `unsupported`, `not_checked`, conversion mapping-loss reports, original static limitations and source/snapshot bindings. A conversion report wrapper is not automatically a valid artifact; select the actual exported artifact without discarding its separate loss report. Validation does not prove truth, runtime behavior, current authority, Context storage or whole-task completion.

Code and Context remain optional. An explicit Contracts-only request does not select their workflows. A generic flow can continue with Contracts when an optional product is missing, using only the selected supported JSON. Report which products actually ran, which receipt was reused after a fresh check, and what remains incomplete; then continue the original task under its existing authorization.
