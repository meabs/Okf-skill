---
type: DomainRule
title: "An accepted invoice batch is queued, not complete"
description: "Interpret the intended submission receipt without mistaking queue acceptance for invoice completion."
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
generated:
  by: "process:okf-interview-author"
  at: "2026-11-22T11:24:07+00:00"
---

**Synthetic scenario knowledge; complete intended semantics, unreviewed draft.**

For this fictional partner invoice-import integration, a batch is a submitted group of invoice records belonging to one partner account. An accepted submission means queued for asynchronous processing. It does not establish that invoices were posted or business processing completed. Consumers must require a separate completion event before marking the work complete.[^scenario]

The intended submission response is HTTP 200 or 202 with a JSON object containing a nonempty string `submission_id`, which identifies the vendor submission. The outgoing payload carries an application batch reference.[^scenario]

### What the caller actually establishes

`BatchClient.submit` returns `accepted` with the parsed response as `receipt` after `raise_for_status()` and JSON decoding. It does not enforce the intended 200/202 status set, object shape or `submission_id` requirement.[^caller] Requests raises HTTP errors for 4xx/5xx and its JSON parser can return JSON types other than objects.[^requests-models] Therefore the caller's `accepted` label alone does not prove a contract-conforming receipt. This comparison concerns the inspected caller implementation and the fictional intended contract.

For a returned unknown submission outcome, apply [the ambiguous-outcome rule](ambiguous-outcome.md).

[^scenario]: Fictional engineer scenario, 2026-11-22; not real maintainer or operator testimony.
[^caller]: Synthetic BatchClient source snapshot identified in frontmatter.
[^requests-models]: [Pinned Requests models.py](https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/src/requests/models.py).
