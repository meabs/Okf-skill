# Saved fictional interview — 2026-11-22

All caller/domain testimony below is invented scenario input supplied by the parent acting as engineer. It is not evidence from Requests maintainers, actual operators or customers. The task explicitly requested retaining questions and received answers. No personal identity was supplied; none is attributed. These are actual messages received in this test, not answers invented by the interviewing agent.

## Round 1 — questions sent

Source understanding before interview: BatchClient posts JSON to /batches with bearer auth, disables environment config and redirects, and catches requests.Timeout as unknown. Requests 3c7baaa05ab4aa49cc819ce3a819d260de19c157 shows default Retry(0, read=False), tuple connect/read timeouts (not total deadline), is_redirect requires Location plus supported status, and accepted is returned after raise_for_status + JSON decode without receipt validation. Inspected sessions request/post/send/config, adapter errors, response decoding/status, timeout/redirect/env tests and docs.

1. What is your responsibility and the caller's applicable deployment/domain, and what does a batch represent?
2. submit's unknown branch cannot establish whether the service committed; what submission identity/deduplication guarantee exists, and what evidence permits retry/replay?
3. What does accepted and its receipt mean downstream—durable receipt, queued work or completed work—and what response/status/schema does the service promise?

## Round 1 — received answer

Fictional engineer answers, round 1 (all invented scenario inputs, no real Requests or customer testimony):

1. I maintain this synthetic caller for a fictional partner invoice-import integration. A batch is a submitted group of invoice records for one partner account. This capture covers the caller's intended integration contract and operator decisions, not the vendor internals.
2. Each payload carries an application batch reference, but I cannot confirm whether the vendor deduplicates it or how long any guarantee lasts. We treat a timeout as unknown, not failed, and elapsed time alone does not permit replay. I do not have the vendor lookup/escalation procedure or approved replay instructions today; keep those questions open.
3. In this fictional contract, accepted means queued for asynchronous processing, not invoices posted or business processing complete. A separate completion event is required to mark the work complete. The documented submission response is HTTP 200 or 202 with a JSON object containing a nonempty string submission_id; that identifies the vendor submission. I can state those semantics as the intended contract, but I cannot provide the completion event's schema, correlation rule or delivery SLA today. Please follow up on other code-driven questions you consider valuable.

## Round 2 — questions sent

1. __init__ sets trust_env=False, disabling ambient proxies, CA bundle env vars and netrc while preserving default TLS verification. Why is that intended, what deployment scope/exceptions apply, and how should proxy/custom-CA requirements be handled?
2. submit disallows redirects and returns endpoint_changed for Requests-recognized redirects. Who authorizes an endpoint change and what should the caller/operator do with Location; are redirects a supported migration mechanism?
3. timeout=(3,20) is connect/read inactivity, not a total deadline. What constraint chose these values, is changing them approved/local or coordinated, and what evidence would trigger reconsideration?

Also important source caveat: response-body ReadTimeoutError is wrapped as ConnectionError in models.iter_content, so not every timeout-like body failure reaches the Timeout catch.

## Round 2 — received answer

Fictional engineer answers, round 2:

1. This caller is intended for dedicated production workers with direct network access to the partner's public-CA HTTPS endpoint. We deliberately ignore host environment and netrc so a worker image or developer login cannot silently change the proxy route, CA source, or account identity; the bearer token supplied to BatchClient is the intended identity. TLS verification must remain enabled. A deployment requiring a proxy or private CA is outside that supported deployment scope and needs an explicitly designed/configured integration change, not an environment-variable workaround or verify=False. I have no approved proxy/private-CA design to supply.
2. Redirects are not a supported endpoint-migration mechanism for these invoice writes. Do not follow a Location header to resubmit invoices or send the bearer token. Endpoint changes require confirmation by the partner integration owner and a reviewed base_url configuration change. I cannot supply the owner/contact identity, confirmation artifact, or exact approval/runbook steps today. The restriction itself is the intended rule; its recovery/migration procedure is unresolved.
3. The 3/20 timeout values are inherited. I cannot establish a business deadline, benchmark rationale, or approval policy for changing them. Keep the justification/budget question open. On the body-read timeout caveat, I cannot say whether the intended contract is to normalize it to unknown or surface an error; please record that exact code-backed clarification request rather than inventing desired behaviour. All answers remain synthetic. You can now finish with independently complete concepts and a separate log for the unresolved questions; no human verification is implied.

## Curated readback sent before writing

- `knowledge/contracts/submission-meaning.md`: one partner-account invoice batch; intended 200/202 object receipt with nonempty submission_id identifies queued work, completion needs separate event; current caller does not validate those constraints.
- `knowledge/contracts/ambiguous-outcome.md`: caught timeout means unknown, elapsed time cannot authorize replay, payload batch reference is not an established dedup guarantee.
- `knowledge/decisions/worker-configuration.md`: direct-access dedicated workers/public-CA HTTPS; explicit bearer identity, ambient proxy/CA/netrc excluded; TLS remains enabled; proxy/private-CA deployments require a designed integration change.
- `knowledge/decisions/redirect-boundary.md`: Location is not an authorized migration/resubmission mechanism; require partner integration-owner confirmation plus reviewed base_url change, with no executable migration runbook claimed.

Separate open-log topics were also sent: vendor dedup/reconciliation/replay authorization; completion event schema/correlation/SLA; receipt-validation policy; proxy/private-CA design if scope expands; migration contact/artifact/steps; timeout rationale/change policy; body-read ConnectionError outcome policy. No reply to this final readback is treated as confirmation or verification.

## Received readback response

As the fictional engineer: no corrections to those intended rules. I am not confirming that the caller currently validates the response contract; the code observation that it does not is accurate from the inspected fixture. Missing deduplication and recovery details remain unanswered; do not turn them into claims that the vendor lacks a guarantee. Finish the files and validation. This is still simulated testimony, not human review.
