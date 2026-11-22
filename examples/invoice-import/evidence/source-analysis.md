# Bounded static source analysis — 2026-11-22

This is a behavioural execution of the OKF interview skill against a synthetic caller. All domain and operator testimony is a labelled fictional scenario supplied by the parent acting as engineer, not real Requests maintainer evidence. No network, HTTP, installation or model-cost actions were used.

## Identity and scope

Requests checkout: `/tmp/okf-interview-review/requests`, origin `https://github.com/psf/requests.git`, revision `3c7baaa05ab4aa49cc819ce3a819d260de19c157`.
Caller: `fixture/client.py`, untracked in experiments working tree at base revision `f10e1b05e2957d75c3c3d07548a1023014a993ad`; SHA-256 `dc69af0659648a499bc71aa459e865e6648a563977eedfb4b540f3956a1c890f`. This hash identifies actual analysed contents; the base commit does not contain this fixture.
No existing knowledge bundle or caller test appeared in the scoped fixture file inventory. Do not infer a deployed Requests version from this downloaded checkout.

## Entry points, data flow and side effects

`BatchClient.__init__` strips trailing slashes, creates a persistent Requests Session, disables `trust_env`, and sets a bearer Authorization header. `submit` posts JSON to `/batches`, no automatic redirects, timeout tuple `(3,20)`. A caught Requests Timeout returns unknown; a recognized redirect returns endpoint_changed; then HTTP error raising and JSON decoding precede accepted. Session pooling/cookies persist between calls; no fixture close method or per-submission idempotency header is present. Payload schema is unconstrained by caller code.

`src/requests/sessions.py` Session defaults (450–510), prepare_request (510–555), request (630–655), post (695+), send (752–829) and merge_environment_settings (831–873) establish request preparation, environment gating, TLS verify=True, response buffering and redirect handling. Disabling trust_env gates netrc, proxy environment discovery and REQUESTS_CA_BUNDLE/CURL_CA_BUNDLE. Explicit session proxy/verify settings remain possible; false does not disable TLS verification.

`src/requests/adapters.py` HTTPAdapter initialization (205–211) sets Retry(0,read=False). send (660–775) converts tuple to connect/read timeout, disables urllib3 redirect following and translates transport errors. `exceptions.py` Timeout/ConnectTimeout/ReadTimeout (82–100) distinguishes exception classes. `models.py` iter_content (944–945) wraps response-body ReadTimeoutError as ConnectionError. Since send eagerly consumes content, the caller's Timeout catch is not a universal normalizer of timeout-like failures.

`models.py` is_redirect (877) requires Location and supported redirect status; raise_for_status (1144+) raises for 4xx/5xx, not all non-2xx; json (1091+) parses arbitrary JSON and raises decoding errors. The caller does not restrict success to 200/202 or validate submission_id. Thus returned accepted cannot itself establish business completion or contract-conforming receipts. This is an observed validation gap relative to subsequently supplied intended contract, not proof of an observed production incident.

## Tests and docs compared with code

Read, not executed: `tests/test_requests.py` TestTimeout (2535–2600) covers tuple shape and distinct connect/read failures; test_env_cert_bundles (990–1024) covers CA env precedence with default session, not this caller's disabled environment; test_manual_redirect_with_partial_body_read (1988–2005) demonstrates explicit redirect processing. Redirect/auth tests located in same module confirm the relevant boundaries but cannot establish a vendor migration policy. `docs/user/quickstart.rst` (533–548) states timeout is not total download time; `docs/user/authentication.rst` (36–55) documents netrc overriding raw auth headers and trust_env opt-out; `docs/user/advanced.rst` documents environment CA settings. No HTTP-dependent test was run under the task constraint. Source tests do not establish the synthetic partner's domain semantics, endpoint policy or deployment requirements.

## Evidence-backed interview gaps

Q1 scope/domain: caller class cannot establish engineer ownership or meaning of batch. Needed to scope all claims.
Q2 replay: submit's Timeout branch, adapter retries and exception taxonomy cannot establish remote commit/dedup guarantees or permission to replay. Needed to avoid treating unknown as failed.
Q3 receipt/completion: submit plus Response.json/raise_for_status cannot establish service receipt schema or business completion. Needed to prevent falsely marking invoices posted.
Q4 environment: __init__ plus Session config establishes disabled mechanisms but not deployment rationale/exceptions. Needed for proxy/CA/auth changes.
Q5 redirects: submit plus is_redirect establishes local detection but not migration authorization. Needed to decide whether Location can change configuration.
Q6 timeouts: submit and adapter tuple conversion establish mechanics but not latency constraints/change ownership. Needed for tuning decisions.
