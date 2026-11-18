# Design and reproducibility

## Scope
Murshid Mini is a training assistant for fictional service users. The core uses standard-library Python, a finite mock client, a small synthetic directory and two fictional records. It does not contact a government service, train a model, cancel applications or authenticate real users.

## Request path
1. Validate nonempty text, maximum length and limited blocked patterns.
2. Reject unsupported cancellation before calling any tool.
3. Extract the ticket and validate its exact keys, types and business rules.
4. Ask for a missing reference, return an exact public FAQ, or call the read-only status tool.
5. Check record existence and ownership against the separate trusted session fixture.
6. Validate the output envelope, add a new trace ID and collect minimal metrics.

Ticket: `service` is `service_info`, `application_status` or `other`; `city` is `Riyadh`, `Jeddah` or `unknown`; `request_id` is null or ASCII `REF-` plus four digits; `needs_clarification` is a boolean and agrees with the missing-reference rule. The teaching extractor recognizes Riyadh only even though the schema accepts Jeddah.

## Data
The bilingual public directory and records are hand-written synthetic teaching fixtures, not scraped records. `REF-1001` belongs to `demo-user-1`, status `under_review`; `REF-1002` belongs to `demo-user-2`, status `approved`; `REF-9999` is absent. The default session is `demo-user-1`. The outward response for an absent and a forbidden record is identical. Internal codes differ for debugging only and would need a separate access policy in production.

## Cache and metrics
Only the two exact public FAQ strings (after outer whitespace trimming) can be cached, without ticket override. The key includes text, language, model, prompt version and directory version. Values contain only answer and creation time. TTL is 300 seconds, tested with a simulated clock. Status requests, errors and personal questions do not enter the shared cache. Each response receives a fresh trace ID. Metrics contain trace, mode, code, hit flag, mock/tool counts and Python elapsed milliseconds, never raw question, answer, owner or reference.

## Cost
The core's hypothetical calculation is `(1000/1000000)*2 + (400/1000000)*4 = USD 0.0036` per request, or USD 3.60 for 1,000 such requests. These are assumed tokens and prices, not billed usage or current provider prices. External inference API calls are zero. Homework model downloads and CPU work are separate from this arithmetic.

## Small documented change
Added experiment date, prompt version, directory version and execution environment to `final_report.json`, making the result self-describing. Retained all ten golden cases and their expectations. Added malformed-reference homework checks (long, Unicode-digit and lowercase references) without changing the seven required cases or their denominator.

## Limits and improvement
The mock cannot understand arbitrary language. Keyword guards are incomplete and no national-ID detector is comprehensive. The identity fixture is not authentication; no production security claim is made. Next steps would be trusted identity, broader evaluation, semantic review and controlled real-model integration in a separate experiment. Prompt text is a visible design artifact; the simulator does not read it.

## Review note to reproduce
Input `What are the visa fees?` returns `out_of_scope`. This is intentional: no fee exists in the directory. Improvement: add reviewed service content and tests before expanding scope. This note is an AI-assisted technical review, not a claim that another student performed a peer review.

## Provenance
Based on course code at https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213 . Adapted and executed with AI assistance. Do not describe this as independently authored from scratch. No copied expected-result file is used as execution evidence. Local checks do not prove a Google Colab or Drive session took place.

Reference source commit inspected: `30b3ebff1ff8b4e744b91625b0aeb24f54b04704`.
