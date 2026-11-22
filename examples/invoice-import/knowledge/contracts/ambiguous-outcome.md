---
type: DomainRule
title: "Elapsed time does not authorize replay of an unknown submission"
description: "Interpret caught submission timeouts without inferring failure or permission to resubmit."
status: draft
x-okf-interview-synthetic: true
sources:
  - id: scenario
    resource: "Fictional interview on 2026-11-22, rounds 1 and 2 and curated readback; actual retained messages in examples/invoice-import/evidence/interview.md outside this bundle"
    title: "Synthetic partner invoice-import scenario"
  - id: caller
    resource: "Synthetic examples/invoice-import/fixture/client.py, SHA-256 dc69af0659648a499bc71aa459e865e6648a563977eedfb4b540f3956a1c890f; static evidence in examples/invoice-import/evidence/source-analysis.md outside this bundle"
    title: "BatchClient source snapshot"
  - id: requests-exceptions
    resource: "https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/src/requests/exceptions.py"
    title: "Requests exceptions.py at 3c7baaa05ab4aa49cc819ce3a819d260de19c157"
  - id: requests-models
    resource: "https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/src/requests/models.py"
    title: "Requests models.py at 3c7baaa05ab4aa49cc819ce3a819d260de19c157"
  - id: requests-sessions
    resource: "https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/src/requests/sessions.py"
    title: "Requests sessions.py at 3c7baaa05ab4aa49cc819ce3a819d260de19c157"
generated:
  by: "process:okf-interview-author"
  at: "2026-11-22T11:24:07+00:00"
---

**Synthetic scenario knowledge; complete decision boundary, unreviewed draft.**

For this fictional invoice integration, a caught submission timeout means the remote outcome is unknown, rather than failed. Elapsed time alone never permits replay.[^scenario]

The caller catches `requests.Timeout` around the POST and returns `{"state": "unknown"}`. It has no lookup, reconciliation or replay implementation.[^caller] Requests distinguishes connect and read timeout exception types; its ConnectTimeout documentation says that such requests are safe to retry, but this caller collapses caught timeout types into one state.[^requests-exceptions]

Requests can wrap a body-read `ReadTimeoutError` as `ConnectionError`, and Session.send normally reads the body before returning. Such failures can escape this caller's Timeout catch; the rule here defines the meaning of the returned `unknown` state, not a universal exception classification.[^requests-models][^requests-sessions]

[Queue acceptance](submission-meaning.md) also does not establish business completion.

[^scenario]: Fictional engineer scenario, 2026-11-22; not real maintainer or operator testimony.
[^caller]: Synthetic BatchClient source snapshot identified in frontmatter.
[^requests-exceptions]: [Pinned Requests exceptions.py](https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/src/requests/exceptions.py).
[^requests-models]: [Pinned Requests models.py](https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/src/requests/models.py).
[^requests-sessions]: [Pinned Requests sessions.py](https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/src/requests/sessions.py).
