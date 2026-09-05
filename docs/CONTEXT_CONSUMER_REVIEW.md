# Context consumer independent implementation review

Review date: 2026-09-05. Reviewer authored Contracts, but did not author or edit
the Context implementation. This review used synthetic data in temporary local
storage on macOS with Python 3.12. It is not an external security audit, a second
model comparison, a Windows/Linux execution result, or a plugin-host approval.

## Result

The reviewed local consumer preserves the intended model-tool versus human
approval boundary. Two reproduced issues were reported to the Context author
and corrected during review. Their targeted retests passed. A remaining output
schema precision issue and explicit platform/host security gates prevent using
this report as a public-submission or production-readiness claim.

## Findings and retests

### R1 — expired proposal retention (P1, corrected execution path)

Initial behavior: after advancing a synthetic clock by 30 days,
`get_change_status` reported `expired`, but the stored proposal still had
`state=pending`, its body, and its nonce. The only automatic purge happened
during a later prepare operation. Expiry blocked approval correctly; it did not
establish a 15-minute physical retention bound for an idle service.

The author added the explicit operator command
`scripts/run.py purge-expired --home <private-directory>` and a 30-second
maintenance interval in `ReviewServer.service_actions`. Independent temporary
storage probes verified that both paths set the proposal state to `expired`,
replace the body with `{}`, and clear the nonce. The command exited zero.

The retention claim must distinguish 15-minute approval validity from cleanup:
the running review service performs periodic cleanup, while stopped processes
retain expired proposal bytes until maintenance runs. Read-only MCP tools do not
silently become deletion operations. Filesystem snapshots/backups and physical
media erasure remain outside this local test.

### R2 — malformed stdio request identifiers (P1, corrected and retested)

Initial behavior: a JSON-RPC request with a lone-surrogate string identifier
(`"\\ud800"`) caused `UnicodeEncodeError` during response serialization and
terminated the stdio process with exit 1. An exponent-overflow number (`1e999`)
was parsed as infinity and reflected in an invalid-request response as the
non-JSON token `Infinity`.

The author added finite-float parsing, Unicode-scalar validation, safe invalid-ID
handling, and ASCII/non-NaN response serialization. A new subprocess received
both malformed requests followed by a valid ping. It returned two `-32700`
errors, then the ping response with ID 3, and exited zero. No traceback or
malformed JSON appeared in stdout.

### R3 — nested output schema precision (P2, open at review snapshot)

The author replaced generic top-level output schemas with explicit success/error
envelopes. All seven read-only tools' real synthetic outputs passed independent
`jsonschema.Draft202012Validator` checks. This is a meaningful improvement;
schemas are present and cover required top-level fields.

However, `search.records[]`, `get_context_history.history[]`, and the inner
`pack`/export objects still accept generic objects. The descriptor alone cannot
reject a malformed record or missing inner provenance. Before submission, reuse
explicit record/history/pack definitions and the pinned export schema, including
the association between `complete` and a real pack versus
`insufficient_budget` and null. This finding does not imply that the current
store emitted a malformed record in the executed tests.

## Verified boundaries

- The seven tools marked `readOnlyHint=true` caused **zero SQLite mutations** in
  an independent `total_changes` probe. `prepare_context_change` is correctly
  marked `readOnlyHint=false`; approving/applying/erasing knowledge is absent
  from model dispatch. Proposal payloads/nonces are not returned by status.
- The configured principal comes from the local operator configuration, rather
  than a model argument. The executed suite covered other-principal denials,
  digest/nonce tampering, replay, stale revision, private POSIX paths, and
  authenticated loopback review. No new principal bypass was found in this
  bounded review.
- Current vendored `vendor/companion_contracts` files matched the frozen
  Contracts source byte for byte, including anchored draft schema patterns.
  `vendor/CONTRACTS_PIN.json` accurately identifies an unpublished local source
  with no invented upstream commit.
- The reviewed public README/release policy distinguishes local synthetic
  preview, OS targets, actual host integration, source publication, submission,
  and licensing adoption. No public release or host approval was demonstrated.

## Evidence and remaining gates

The Context `scripts/check.py` run completed **36 product tests**, the synthetic
demo, tools JSON parsing, and vendored digest checks successfully. Later focused
probes verified the R1/R2 fixes separately; this count is the executed review
snapshot, not a claim about subsequently added tests.

Windows ACL validation remains explicitly unverified. POSIX owner/mode tests do
not establish cross-user Windows protection. A configured three-OS CI matrix
does not establish executed Windows/Linux support. Real hosted authentication,
credential/session rotation, platform permission integration, backup deletion,
and external plugin-host interoperability remain separate gates.

Reviewed sources: Context `src/context_companion/store.py`, `tools.py`, `mcp.py`,
`review.py`, `scripts/run.py`, `scripts/check.py`, `tests_product/`, public README
and release/platform documentation; Contracts vendored source/schema artifacts.
Only this report was written by this reviewer during the Context review.

## Final focused follow-up — 2026-09-05

The Context author added explicit nested `RECORD`, history/CANDIDATE and `PACK`
definitions, and composes the export descriptor from the pinned envelope plus
the full Context payload schema. Independent negative probes now reject a search
record lacking provenance and a Context export decision missing `evidence_refs`.
An intact Context example is accepted by the export descriptor. The nested
record/provenance portion of R3 is therefore resolved. At this follow-up snapshot,
the association between pack status and null/object remains permissive because
the pack field uses `anyOf: [PACK, null]` independently of status.

The author also removed `purge_expired()` from preparation. A focused synthetic
probe created 100 proposals, advanced the clock beyond their validity, and
prepared one more. The new proposal succeeded, while every previous proposal's
payload, nonce, and stored state remained unchanged. Thus expired proposals do
not exhaust the pending-proposal quota, and prepare performs no cleanup/deletion
side effect. `destructiveHint=false` now matches its proposal-only behavior;
cleanup belongs to the operator command and review-service maintenance verified
above. This follow-up did not rerun the whole suite or edit Context code.
