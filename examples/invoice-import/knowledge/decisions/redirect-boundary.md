---
type: Decision
title: "A redirect does not authorize migrating invoice submissions"
description: "Keep Location headers from becoming submission or credential-routing authority."
status: draft
x-okf-interview-synthetic: true
sources:
  - id: scenario
    resource: "Fictional interview on 2026-11-22, rounds 1 and 2 and curated readback; actual retained messages in examples/invoice-import/evidence/interview.md outside this bundle"
    title: "Synthetic partner invoice-import scenario"
  - id: caller
    resource: "Synthetic examples/invoice-import/fixture/client.py, SHA-256 dc69af0659648a499bc71aa459e865e6648a563977eedfb4b540f3956a1c890f; static evidence in examples/invoice-import/evidence/source-analysis.md outside this bundle"
    title: "BatchClient source snapshot"
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

**Synthetic scenario knowledge; complete authorization boundary, unreviewed draft.**

For these fictional partner invoice writes, redirects are not a supported endpoint-migration mechanism. Do not follow a `Location` header to resubmit invoices or send the bearer token. An endpoint change requires confirmation by the partner integration owner and a reviewed `base_url` configuration change.[^scenario]

`BatchClient.submit` explicitly passes `allow_redirects=False` and returns `endpoint_changed` when Requests reports `response.is_redirect`.[^caller] Requests recognizes that condition only when a Location header accompanies a supported redirect status; it is not a general classification of every non-2xx response.[^requests-models] Session may prepare a next request while redirects are disabled, but does not send it automatically.[^requests-sessions]

Treat `endpoint_changed` as a boundary requiring the approved configuration decision, not as authority to accept the advertised URL. Preserve [explicit worker routing and identity](worker-configuration.md) through any separately approved change.

[^scenario]: Fictional engineer scenario, 2026-11-22; not real maintainer or operator testimony.
[^caller]: Synthetic BatchClient source snapshot identified in frontmatter.
[^requests-models]: [Pinned Requests models.py](https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/src/requests/models.py).
[^requests-sessions]: [Pinned Requests sessions.py](https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/src/requests/sessions.py).
