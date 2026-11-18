# Evaluation report — actual local execution

Experiment date: 2026-11-18. CPU, Python 3.12. All five notebooks were executed in this workspace. Core execution used a fresh namespace; the eight repository tests include a clean full run, a repeated full run and replay of each daily milestone. Update: the learner subsequently supplied screenshots and a Colab ZIP containing seven core JSON reports, now used in `results/core/`. The core notebook saved in this package still contains the earlier local outputs; the learner’s downloaded notebook must replace it before upload. Homework and unittest evidence remain from local execution. See `results/core/provenance.json`; the exported environment template string is preserved, not used as runtime evidence.

## Results by experiment

| Experiment | Observed outcome | Interpretation |
|---|---|---|
| Day 1 core | Three baseline answers; blank input adds zero mock calls | Fixed directory contract holds |
| Day 2 core | Five codes and tool counts `[1,0,1,0,1]` | Status, clarification, missing, cancellation, ownership |
| Day 3 core | 10/10 golden cases | These fixed mock cases pass |
| Day 4 core | 10/10 integrated golden cases | Regression after cache integration |
| Cache | 3 calls without cache, 1 with cache; `[false,true,true]`; 66.7% | Reduced simulator calls; no API saving measured |
| Additional core checks | 8/8 unittest tests | Replay, source parity, schema, guards, ownership, TTL and metric privacy |
| Day 1 homework | Nonempty actual FLAN-T5-small answer | Real local generation smoke check |
| Day 2 homework | 7/7 required cases; 4/4 separate reference boundary checks | Simulated tool protocol, not model-selected calling |
| Day 3 homework | Three intended rejections and corrected input accepted | Expected `ValueError` handling |
| Day 4 homework | 3/3 keyword hits | Lexical indicator only, not general model accuracy |

No tests were removed or expected outcomes weakened. No observed execution failures remain. These denominators must not be combined into one accuracy figure.

## Actual generated answers and review

Model: `google/flan-t5-small`, revision `0fc9ddf78a1e988dac52e2dac162b0ede4fd74ab`. PyTorch 2.6.0+cpu, Transformers 4.49.0, SentencePiece 0.2.0. Deterministic generation, maximum 48 new tokens, one beam.

Day 1: **“Use its reference number”**. Input: 34 tokens; output including special tokens: 6; generation: 0.187 seconds. This directly reflects the provided context and invents no fee, deadline or status.

| Case | Observed answer | Input / output tokens | Generation seconds | Meaning review |
|---|---|---:|---:|---|
| E01 | Use its reference number | 34 / 6 | 0.224 | Supported: tells the user how to check status |
| E02 | Reference number | 36 / 4 | 0.124 | Supported: identifies the needed information |
| E03 | Use its reference number | 37 / 6 | 0.153 | Supported: answers the paraphrase consistently |

All three actual answers contain “reference” and “number”; none adds an unsupported fee, date or actual application status. This is an AI-assisted review of the observed outputs, not an external human assessor's sign-off. Future runs may vary in timing or text. Model downloads were needed for setup; inference itself made no external API calls. Day 4 reused the downloaded model in offline mode.

## Cost and speed
Core `hypothetical_cost` uses assumed token counts and USD prices: USD 0.0036 per hypothetical request. Actual provider spend in this exercise is zero; this does not claim CPU or network resources have no cost. Core latency is local Python timing, not live-model latency. Live-homework timing excludes model loading and downloading. No production performance target was measured.

## Limitations and next improvement
Ten fixed mock cases and three simple English paraphrases are a narrow sample. Keyword matching can misclassify meaning. The mock cannot generalize, the guards are incomplete and the trusted user is synthetic. Expand evaluation with human-reviewed unsupported questions, adversarial inputs and Arabic paraphrases before considering wider use. Keep status authorization in application code when experimenting with a real model.

## Evidence
- `results/core/`: baseline, Days 2–4, final report, metrics, synthetic data, environment and unittest log.
- `results/day1/live_demo_result.json`: actual model answer and token/time measurements.
- `results/day2/tools_result.json`: seven required cases and four separately counted boundary checks.
- `results/day3/errors_result.json`: intentional rejections and corrected input.
- `results/day4/evaluation_result.json`: all three actual generated answers.
- Each notebook retains stdout from its execution; the real-model setup cell records installed versions with an explicit local-execution note.
