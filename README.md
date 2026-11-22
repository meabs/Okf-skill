# OKF Engineer Interview

An agent skill that analyses a codebase, interviews engineers about what the code cannot explain, and creates useful [Open Knowledge Format (OKF)](https://github.com/open-knowledge-format/open-knowledge-format) knowledge for people and agents.

Source code can show what a system does. Engineers can explain why it works that way, which external constraints matter, and what a future change must preserve. This skill captures that context as complete, source-attributed answers rather than interview transcripts.

**Complete answers go into the OKF bundle. Anything needing clarification stays in a separate engineer review log.**

## What it captures

- Design decisions, tradeoffs, rejected alternatives, and reasons to reconsider.
- Business rules, terminology, exceptions, and customer or contractual constraints.
- Operational practices, dependency boundaries, and ownership.
- Known issues, established failure modes, and supported recovery procedures.

Failure Modes and Effects Analysis (FMEA) is one optional interview lens. It is used where useful, without turning every interview into a risk assessment or inventing numerical scores.

## Quick start

Clone this repository:

```sh
git clone https://github.com/meabs/Okf-skill.git
```

Give your coding agent the path to [`skills/okf-interview/SKILL.md`](skills/okf-interview/SKILL.md) and a project to inspect:

> Use the skill at `<checkout>/skills/okf-interview/SKILL.md`. Analyse this project's code and tests first. Interview me about behaviour, constraints, and decisions you cannot infer or do not understand. Write complete OKF answers to `knowledge/` and put anything needing clarification in `knowledge-review-log.md`.

Replace `<checkout>` with the absolute path to this repository. For agents that support skill discovery, copy the entire `skills/okf-interview/` folder into the agent's documented skills directory. The folder is self-contained, apart from the validator's Python dependency.

The skill uses the coding agent you already have. It does not require the upstream OKF plugin, a separate model API key, a database, or a hosted service.

## How it works

1. **Analyse the code first.** Trace relevant entry points, data flow, configuration, tests, error handling, and documentation. Record the revision and the evidence behind each question.
2. **Ask targeted questions.** Interview the engineer in small rounds about missing context, unclear behaviour, and assumptions that matter to future changes. Follow up on partial or conflicting answers.
3. **Curate the knowledge.** Turn supported answers into focused concepts with explicit scope, rationale, provenance, and practical implications. Keep raw dialogue out of concept bodies.
4. **Apply a completeness check.** Publish an answer only when it can be understood and applied without a missing clarification. A partial recovery procedure does not qualify. Check individual sentences as well as the central answer.
5. **Maintain the review log.** Retain open questions, code evidence, provisional answers, and the exact clarification needed outside the consumable bundle. Incorporate answers only after they are complete, preserving the review history.
6. **Validate the bundle.** Run the included upstream validator and read the resulting concepts as a consumer.

## Output

```text
your-project/
├── knowledge/                       # Consumable OKF bundle
│   ├── index.md
│   ├── log.md
│   ├── decisions/
│   │   ├── index.md
│   │   └── worker-configuration.md
│   └── contracts/
│       ├── index.md
│       └── submission-meaning.md
└── knowledge-review-log.md           # Unresolved questions for engineers
```

This is an illustrative layout. The skill reuses an existing bundle's organization and chooses concept types and body sections to suit the knowledge. It does not impose a new OKF taxonomy or mandatory body template.

Each review item has a stable ID, state, affected code, observed evidence, reason the answer matters, and a specific clarification request. Responses and corrections remain in its history. An owner is recorded only when one is supplied.

### Example knowledge

From the included [synthetic invoice-import example](examples/invoice-import/knowledge/index.md):

> An accepted submission means queued for asynchronous processing. It does not establish that invoices were posted or business processing completed. Consumers must require a separate completion event before marking the work complete.

The [full concept](examples/invoice-import/knowledge/contracts/submission-meaning.md) records the intended receipt contract, distinguishes it from what the caller actually validates, and attributes claims to their sources.

### Example clarification request

The separate [engineer review log](examples/invoice-import/knowledge-review-log.md) contains an open timeout-budget question:

> The caller specifies connect and read timeouts, but their values are inherited. Supply the applicable business deadline, measured constraint evidence, rationale for the values, who approves changes, and what triggers reconsideration.

That unanswered rationale is not published as an OKF answer.

## OKF compatibility and trust

The skill targets [OKF v0.3](https://github.com/open-knowledge-format/open-knowledge-format/blob/527e81aff55992be21507e97004286789126f88c/SPEC.md). It uses Markdown concepts with YAML frontmatter, source attribution, generation metadata, normal concept links, indexes, and a change log.

The complete-answer requirement is this skill's authoring policy. OKF itself permits incomplete drafts. Here, `status: draft` can describe a **complete answer awaiting review**; it is not a way to admit unfinished content.

Engineer replies do not automatically verify a generated document. Human verification is recorded only after a real reviewer confirms the final content, supplies their identity, and asks for that verification to be recorded. Synthetic examples remain clearly labelled and unverified.

## Validation

The bundled validator needs Python 3.9 or later and PyYAML. From this repository:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -I skills/okf-interview/scripts/validate.py \
  examples/invoice-import/knowledge --strict --json
```

Replace the example path with your own bundle to validate generated knowledge. Then run `python3 -I skills/okf-interview/scripts/check_links.py <bundle>` to catch dangling links and concepts missing from their index, which the upstream validator does not check. Run `python3 -I skills/okf-interview/scripts/check_content.py <bundle> --log <review-log>` for placeholders, footnote slips, raw dialogue and unknown review-item IDs. Strict mode fails on errors or warnings. Format validation does not establish factual accuracy, answer completeness, or operational safety; those require evidence and content review.

## Testing and limitations

`python3 -I tests/selftest.py` checks the helper scripts against the example and seeded faults (it runs in CI).

The included example was produced by a fresh agent using the skill while another agent acted as a fictional engineer. The interviewer inspected a synthetic Python caller and a pinned Requests checkout, conducted two question rounds, and produced four concepts with seven unresolved review items.

The test exposed unresolved commentary leaking into otherwise complete concepts. The skill was tightened with a sentence-level completeness check, and the output was revised and revalidated. The final bundle passed strict upstream validation. This was one scenario test, not a benchmark or a real engineer interview. See [the example notes](examples/README.md) and retained [interview evidence](examples/invoice-import/evidence/interview.md).

The skill can only capture knowledge supported by accessible code, documentation, and engineer answers. It does not invent missing contracts, incident histories, owners, recovery commands, deadlines, or risk scores.

## Repository contents

| Path | Purpose |
| --- | --- |
| [`skills/okf-interview/SKILL.md`](skills/okf-interview/SKILL.md) | Agent instructions and completeness policy |
| [`skills/okf-interview/references/`](skills/okf-interview/references/) | Interview prompts, OKF authoring guidance, and upstream license |
| [`skills/okf-interview/scripts/validate.py`](skills/okf-interview/scripts/validate.py) | Unmodified upstream OKF validator |
| [`skills/okf-interview/scripts/check_links.py`](skills/okf-interview/scripts/check_links.py) | Navigation check: broken links, orphan concepts, missing indexes (standard library only) |
| [`skills/okf-interview/scripts/check_content.py`](skills/okf-interview/scripts/check_content.py) | Content check: placeholders, footnote slips, raw dialogue, unknown review-item IDs, gap phrases (standard library only) |
| [`skills/okf-interview/scripts/new_concept.py`](skills/okf-interview/scripts/new_concept.py) | Scaffold a concept with correct frontmatter and footnotes |
| [`examples/invoice-import/`](examples/invoice-import/) | Synthetic caller, generated knowledge, separate review log, and evidence |

## License and attribution

Licensed under [Apache-2.0](LICENSE). The validator is copied unchanged from the upstream OKF repository at commit `527e81aff55992be21507e97004286789126f88c` and retains its Google LLC copyright and license notice. See [NOTICE](NOTICE).

This is an independent skill built around the Open Knowledge Format specification; it is not an official upstream OKF project.
