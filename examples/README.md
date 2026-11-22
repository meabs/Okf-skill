# Synthetic worked example

`invoice-import/` contains an actual skill execution against a synthetic Python caller of Requests. The caller and all business testimony are fictional. The Requests library is real and was inspected at revision `3c7baaa05ab4aa49cc819ce3a819d260de19c157`; its source is not redistributed here.

A fresh interviewing agent read the skill and analysed the caller and relevant Requests implementation, tests, and documentation. A separate agent played the engineer, providing both complete answers and deliberate unknowns. The interviewer asked six question groups across two rounds and read back its intended concepts before generating files.

## Read the output

- [Knowledge bundle](invoice-import/knowledge/index.md): four complete, synthetic, unverified concepts.
- [Engineer review log](invoice-import/knowledge-review-log.md): seven open clarification items, alongside incorporated-item history.
- [Caller fixture](invoice-import/fixture/client.py): the synthetic source inspected by the interviewer.
- [Source analysis](invoice-import/evidence/source-analysis.md): inspected code and the resulting knowledge gaps.
- [Interview evidence](invoice-import/evidence/interview.md): actual questions and received fictional answers.

The first output passed format validation but still contained unresolved commentary inside otherwise complete concepts. A sentence-level completeness check was added to the skill. The same interviewer then revised the output using the existing answers; it did not receive invented resolutions to the open questions. The files included here are that revised output.

The final knowledge bundle contains eight Markdown files including navigation and history. It passes the bundled upstream validator with `--strict`. These are observed results from one scenario, not a claim of reliability across repositories or real interviews. No runtime HTTP tests were performed. All concepts remain draft, synthetic, and without human verification.

Evidence records were produced in a temporary test workspace before publication. They may mention the original `code-first` workspace or a downloaded checkout under `/tmp`; the included caller hash and pinned Requests revision identify the analysed source. Concept provenance descriptions have been adjusted to this repository's example paths without changing the captured claims.
