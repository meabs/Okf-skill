# Engineer review log — synthetic BatchClient scenario

All domain testimony is fictional scenario input from the parent acting as engineer, received on 2026-11-22. It is not real Requests maintainer evidence. Source revision: Requests `3c7baaa05ab4aa49cc819ce3a819d260de19c157`; caller `fixture/client.py` SHA-256 `dc69af0659648a499bc71aa459e865e6648a563977eedfb4b540f3956a1c890f` (untracked fixture at experiments base `f10e1b05e2957d75c3c3d07548a1023014a993ad`). File/symbol references below use these revisions unless otherwise stated. Static code analysis is in `evidence/source-analysis.md`; actual interview questions, received fictional answers and readback are in `evidence/interview.md`.

No individual owner, contact identity or review deadline was supplied. No content is human-verified. Entries retain unanswered questions even when a separately complete restriction was incorporated. No vendor absence-of-guarantee claim follows from an unknown answer.

## K01 — Submission meaning and scope

- State: `incorporated`
- Area and revision: BatchClient.submit; Requests Response.json/raise_for_status, models.py, at source snapshots above.
- Observed evidence: The caller parses JSON after HTTP error checks without restricting status or receipt schema.
- Response history (2026-11-22, fictional): Round 1: fictional maintainer covers partner-account invoice-import contract. Accepted means queued; intended 200/202 object with nonempty submission_id identifies vendor submission; separate completion event needed. Readback confirmed intended meaning, not current enforcement.
- Why clarification matters: Define completion correctly; prevent accepted being interpreted as posted invoices.
- Exact clarification or incorporation: Completed definition incorporated in `knowledge/contracts/submission-meaning.md`. Remaining event protocol and validation policy are K03 and K04.

## K02 — Vendor deduplication and authorized reconciliation/replay

- State: `open`
- Area and revision: BatchClient.submit Timeout branch; HTTPAdapter initialization, adapters.py; exceptions.py Timeout classes, at source snapshots above.
- Observed evidence: Caller returns unknown on caught Timeout; no reconciliation/replay implementation; payload unconstrained.
- Response history (2026-11-22, fictional): Round 1: payload carries application batch reference, but vendor deduplication and guarantee duration cannot be confirmed. Elapsed time never authorizes replay. Lookup, escalation and approved replay instructions unavailable.
- Why clarification matters: Replay could duplicate a remote submission; unknown cannot imply failure.
- Exact clarification or incorporation: Supply vendor guarantee/version and scope, reference identity constraints and lifetime, reconciliation evidence, authorized lookup access/steps, success and stop conditions, and actual escalation/permission route. Rule only incorporated separately in `knowledge/contracts/ambiguous-outcome.md`; recovery remains open.

## K03 — Completion event schema, correlation and SLA

- State: `open`
- Area and revision: BatchClient.submit accepted branch; models.py Response.json, at source snapshots above.
- Observed evidence: The fixture processes submission response only; no completion event consumer is present.
- Response history (2026-11-22, fictional): Round 1: a separate completion event is required; its schema, correlation rule and delivery SLA are unavailable.
- Why clarification matters: Receipt meaning can be defined, but completion matching or waiting/escalation procedure cannot.
- Exact clarification or incorporation: Supply versioned event schema, how event correlates to submission_id and application batch reference, conditions establishing business completion, delivery timing/recovery contract and event ownership route.

## K04 — Policy for malformed or out-of-contract submission responses

- State: `open`
- Area and revision: BatchClient.submit; models.py Response.raise_for_status/json, at source snapshots above.
- Observed evidence: Code accepts any parsed JSON after non-error status and non-redirect branch; it does not enforce intended 200/202 object/nonempty string submission_id. Decode errors and HTTPError propagate.
- Response history (2026-11-22, fictional): Round 1 stated intended response contract; final readback acknowledged source observation. No desired handling for contract violation or authorization to implement change supplied. No actual incident established.
- Why clarification matters: A technically returned accepted label may lack required receipt identity; callers need an agreed handling contract.
- Exact clarification or incorporation: Clarify required treatment of unsupported status, wrong receipt type, absent/empty submission_id and invalid JSON, including outcome ambiguity and tests. Is validation owned by this caller or another boundary? No fix or incident cause is presumed.

## K05 — Dedicated worker environment and TLS decision

- State: `incorporated`
- Area and revision: BatchClient.__init__; sessions.py Session defaults/prepare_request/merge_environment_settings, at source snapshots above.
- Observed evidence: trust_env=False gates environment proxies, CA bundle vars and netrc; verify defaults True.
- Response history (2026-11-22, fictional): Round 2: supported dedicated workers use direct public-CA HTTPS and supplied bearer identity. Ambient settings must not change route, CA or identity; keep TLS verification on. Proxy/private-CA needs designed explicit change, not environment workaround or verify=False. Readback confirmed.
- Why clarification matters: Preserve deployment assumptions and identify a supported-scope change.
- Exact clarification or incorporation: Complete decision in `knowledge/decisions/worker-configuration.md`; conditional extension design tracked K06.

## K06 — Proxy or private-CA extension design if deployment scope expands

- State: `open`
- Area and revision: BatchClient.__init__; sessions.py merge_environment_settings, at source snapshots above.
- Observed evidence: Current fixture config excludes ambient settings; explicit session config remains technically possible.
- Response history (2026-11-22, fictional): Round 2: no approved proxy/private-CA design supplied; these deployments are outside supported scope.
- Why clarification matters: An extension cannot be implemented safely from the current decision alone.
- Exact clarification or incorporation: If extension is requested, supply approved routing, CA source, identity boundaries, deployment config, permissions and validation requirements. This is a conditional design gap, not a current supported-deployment defect.

## K07 — Redirect authorization boundary

- State: `incorporated`
- Area and revision: BatchClient.submit allow_redirects=False/is_redirect; models.py Response.is_redirect; sessions.py Session.send, at source snapshots above.
- Observed evidence: Recognized redirects return endpoint_changed; no redirect request automatically sent. Recognition requires Location and supported status.
- Response history (2026-11-22, fictional): Round 2: Location is not an invoice migration mechanism; do not follow to resubmit/send bearer. Endpoint changes need integration-owner confirmation and reviewed base_url change. Readback confirmed.
- Why clarification matters: Do not turn server-provided Location into credential or resubmission authority.
- Exact clarification or incorporation: Complete decision boundary in `knowledge/decisions/redirect-boundary.md`; executable migration steps remain K08.

## K08 — Endpoint migration confirmation and executable runbook

- State: `open`
- Area and revision: BatchClient.submit endpoint_changed; BatchClient.__init__ base_url, at source snapshots above.
- Observed evidence: Caller exposes a state and base_url input but no migration workflow.
- Response history (2026-11-22, fictional): Round 2: integration owner role named, but contact identity, confirmation artifact and exact approval/runbook steps unavailable.
- Why clarification matters: The restriction is usable; a migration procedure lacking authority and success/stop conditions is not.
- Exact clarification or incorporation: Supply actual contact/escalation route, confirmation artifact requirements, permissions, reviewed config-change steps, handling of pending submissions, verification success criteria and stop conditions.

## K09 — Timeout budget rationale and change policy

- State: `open`
- Area and revision: BatchClient.submit timeout=(3,20); adapters.py HTTPAdapter.send; docs/user/quickstart.rst timeout note, at source snapshots above.
- Observed evidence: Tuple establishes connect and read inactivity limits, not end-to-end deadline.
- Response history (2026-11-22, fictional): Round 2: values inherited; business deadline, benchmark rationale and approval policy cannot be established.
- Why clarification matters: Increasing or decreasing limits may affect workload and ambiguity without a supported tradeoff.
- Exact clarification or incorporation: Supply applicable end-to-end deadline if any, measured latency/constraint evidence, rationale for 3/20, who approves changes and what triggers reconsideration. Do not invent a deadline or tuning recommendation.

## K10 — Body-read timeout and other propagated-failure outcome policy

- State: `open`
- Area and revision: models.py Response.iter_content lines 944–945; sessions.py Session.send eager r.content; BatchClient.submit Timeout catch, at source snapshots above.
- Observed evidence: ReadTimeoutError during body consumption is converted to ConnectionError, which the caller does not catch as Timeout. HTTPError and JSON decode failures can also propagate.
- Response history (2026-11-22, fictional): Round 2: engineer cannot say whether body-read timeout should normalize to unknown or surface an error.
- Why clarification matters: The returned-state contract is not a universal classification of ambiguous transport outcomes; consumers need exact intended exception behavior.
- Exact clarification or incorporation: Should body-read ConnectionError remain an exception or normalize to unknown, under what conditions, and what should downstream code infer about remote submission? Supply intended contract and relevant tests; avoid blanket retry instructions.


## Remediation history — 2026-11-22

Same-interview revision after the parent's sentence-level completeness review; no new testimony or answers were obtained. The initial output is retained in `evidence/initial-output/`. Removed commentary from consumable concepts/navigation without closing any open question:

- K02: removed statements about unestablished deduplication effects and missing lookup/recovery procedure from submission-meaning and ambiguous-outcome. Retained only the established unknown-state/elapsed-time rule in the latter; vendor guarantee, lifetime and authorized recovery details remain open here. Requests ConnectTimeout documentation does not answer this wrapper's domain recovery questions.
- K03: removed completion-procedure/delivery-guarantee absence commentary; event schema, correlation and SLA remain open here.
- K04: receipt validation gap remains a directly observed implementation fact; no real incident is established by this exercise.
- K06: removed unavailable-design commentary; proxy/private-CA design remains open here, while the complete supported-deployment boundary remains in the decision.
- K08: removed missing-runbook commentary; migration authority/contact, confirmation artifact and executable steps remain open here. The complete requirement for owner confirmation and reviewed base_url change remains in the decision.
- Source applicability: the actual deployed Requests dependency version is not established; root navigation now states only the inspected revision and fictional scope. Establish a deployed version before applying these static observations to any deployment.

All original item IDs, states, response histories and clarification requests are preserved. No missing procedure or guarantee was fabricated. No verified metadata was added.
