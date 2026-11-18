# Technical documentation

## Architecture

Input → input guard → rule-based ticket extraction → schema/business-rule validation → public mock answer OR read-only tool → output validation → response + minimal metrics.

Day 4 places an exact cache around **only the two known public FAQs**. Status requests, malformed tickets and guarded requests bypass it. The key includes question, language, model label, prompt version and directory version. Entries expire after 300 seconds. Cached entries store the answer and creation time, not record status or session data.

## Components

- `FakeClient.generate`: finite lookup, increments mock-call counter. Never calls an API.
- `ask`: Day 1 baseline with UUID, answer, model label and measured Python latency.
- `extract_ticket`: simple rules and regex; not general NLP.
- `validate_ticket`: exact keys, types, enumerations and missing-reference consistency.
- `check_status`: local lookup with ownership check. Does not mutate records.
- `route`: rejects cancellation, handles clarification, chooses public vs status path.
- `build_prompt`: exposes a versioned teaching template. The mock does not execute prompts.
- `guard_input`: limited length, example injection strings and a ten-digit pattern. Not a comprehensive security/privacy detector.
- `run_pipeline`: coordinates validation and execution.
- `evaluate`: ten fixed cases plus reasons; no network or model judge.
- `run_app`: safe public-cache wrapper and minimal measurements.

## Outputs

`baseline_results.json`, `day2_results.json`, `day3_results.json`, `day4_results.json`, `final_report.json`, `metrics.json`, and `synthetic_data.json` are written under `murshid_outputs/`. The final ZIP packages these JSON files. Save the notebook separately.

Latency measures local Python execution, not model inference. UUIDs and times vary. Exact cache counters and status codes are deterministic when the experiment starts with a cleared cache. The illustrative token-cost calculation is USD 0.0036/request using invented prices; actual external API usage/spend is zero. No actual financial saving or speed target is asserted.

## Use each learning environment correctly

Use the core mock to trace requests, validate contracts and compare repeatable outputs. Explore actual model inference in the [separate real-model notebook](../homework/day1_real_model.ipynb), keeping your cumulative project intact. Keep synthetic identities and records in your exercises, protect private information, and review generated answers before trusting them. Treat the keyword guards as examples to reason about rather than comprehensive security controls.

## Test strategy

Run the notebook from a clean namespace, replay days in order, repeat full runs, verify all fixture results and negative cases, test ownership, schema, cache version isolation/expiry and status exclusion. Keep expected cases unchanged unless requirements actually change. Record failures honestly; 10/10 fixed examples is not a general reliability guarantee.
