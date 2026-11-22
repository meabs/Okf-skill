---
type: Decision
title: "Keep dedicated worker routing and identity explicit"
description: "Preserve the fictional supported direct-access HTTPS deployment boundary."
status: draft
x-okf-interview-synthetic: true
sources:
  - id: scenario
    resource: "Fictional interview on 2026-11-22, rounds 1 and 2 and curated readback; actual retained messages in examples/invoice-import/evidence/interview.md outside this bundle"
    title: "Synthetic partner invoice-import scenario"
  - id: caller
    resource: "Synthetic examples/invoice-import/fixture/client.py, SHA-256 dc69af0659648a499bc71aa459e865e6648a563977eedfb4b540f3956a1c890f; static evidence in examples/invoice-import/evidence/source-analysis.md outside this bundle"
    title: "BatchClient source snapshot"
  - id: requests-sessions
    resource: "https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/src/requests/sessions.py"
    title: "Requests sessions.py at 3c7baaa05ab4aa49cc819ce3a819d260de19c157"
generated:
  by: "process:okf-interview-author"
  at: "2026-11-22T11:24:07+00:00"
---

**Synthetic scenario knowledge; complete configuration decision, unreviewed draft.**

This caller's supported fictional deployment is dedicated production workers with direct access to the partner's public-CA HTTPS endpoint. Use the bearer token supplied to `BatchClient` as the account identity and keep TLS verification enabled.[^scenario]

Ignoring host proxy configuration, environment CA-bundle selection and netrc is deliberate: worker-image settings or a developer login must not silently alter the route, CA source or account identity. Ambient environment inheritance is therefore excluded for this integration.[^scenario]

`BatchClient.__init__` sets `session.trust_env = False` and the Authorization bearer header.[^caller] In the inspected Requests revision, that flag gates netrc lookup, environment proxy discovery and `REQUESTS_CA_BUNDLE`/`CURL_CA_BUNDLE` selection. Session TLS verification still defaults to True. Explicit session configuration remains technically possible; the flag does not itself disable verification.[^requests-sessions]

A deployment needing a proxy or private CA falls outside this supported scope and triggers an explicitly designed and configured integration change. An environment-variable workaround or `verify=False` is not an approved extension of this decision.[^scenario] Endpoint changes also obey [the redirect boundary](redirect-boundary.md).

[^scenario]: Fictional engineer scenario, 2026-11-22; not real maintainer or operator testimony.
[^caller]: Synthetic BatchClient source snapshot identified in frontmatter.
[^requests-sessions]: [Pinned Requests sessions.py](https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/src/requests/sessions.py).
