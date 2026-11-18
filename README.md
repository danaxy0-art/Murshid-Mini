# Murshid Mini | مرشد

**Training context: SDAIA Academy — أكاديمية سدايا**  
**Course: LLM Application Engineering — هندسة تطبيقات النماذج اللغوية الكبيرة (SDA-AIE-213)**  
**Trainer: Meaad Al-Marri**  
**Academy GitHub:** https://github.com/SDAIAAcademy

A fictional service assistant demonstrating LLM application engineering: validated tickets, authorized read-only lookup, guardrails, evaluation and safe public-response caching.

**Core mode: `mock`.** `FakeClient` is deterministic Python, not a trained language model. The real-model homework uses FLAN-T5-small separately on CPU. All service records are synthetic. No API keys or paid inference endpoints are used.

## Open the deliverables

| Work | Notebook | Results |
|---|---|---|
| Cumulative core, 14 code cells | [murshid.ipynb](notebooks/murshid.ipynb) | [Core reports](results/core/) |
| Day 1: real model | [day1_real_model.ipynb](homework/day1_real_model.ipynb) | [Day 1](results/day1/) |
| Day 2: validated tools | [day2_tools.ipynb](homework/day2_tools.ipynb) | [Day 2](results/day2/) |
| Day 3: error handling | [day3_errors.ipynb](homework/day3_errors.ipynb) | [Day 3](results/day3/) |
| Day 4: model evaluation | [day4_evaluation.ipynb](homework/day4_evaluation.ipynb) | [Day 4](results/day4/) |

[Arabic handoff](START_HERE_AR.md) · [Technical notes](docs/project-notes.md) · [Homework explanations](docs/homework-explanations.md) · [Evaluation](docs/evaluation.md) · [Submission checklist](docs/submission-checklist.md)

## Problem and intended users
A user asking about a service needs a supported answer or a request for missing information. A reference number alone must not grant access to another person's status. This training implementation demonstrates those decisions without real personal data or a live government integration.

## Run in Google Colab
1. Upload `notebooks/murshid.ipynb` to Colab and save your own copy in Drive.
2. Select Python 3 with CPU/no accelerator; the core needs no installation.
3. Restart the session and run all 14 cells from the top.
4. Check `checks=passed`, golden tests `10/10`, and mock-call comparison `3 → 1`.
5. Download your saved notebook separately from `murshid_submission.zip`, which contains JSON only.
6. Open each homework notebook separately. Days 1 and 4 install the specified dependencies and download `google/flan-t5-small`; allow time for the first download. Keep these installs out of the core runtime.

The seven core JSON reports were replaced with the learner’s uploaded Colab export. Notebook outputs, automated unit-test logs and homework evidence are from the earlier local execution; see `results/core/provenance.json`. Replace the core notebook with the learner’s downloaded Colab copy before submission. Saving personal Drive copies and verifying access to the submitted GitHub URL are learner handoff steps.

## Run locally
Python 3.9+ is sufficient for the core and Days 2/3. From this repository's root:

```bash
python tools/run_notebook.py
python tools/run_notebook.py homework/day2_tools.ipynb
python tools/run_notebook.py homework/day3_errors.ipynb
python -m unittest discover -s tests -v
```

Core JSON is generated in `murshid_outputs/`; checked-in run evidence is under `results/core/`. The runner saves actual stdout into the executed notebook. Re-run before updating evidence after edits.

For the real-model notebooks use the supplied Colab setup cell, or an isolated Python 3.12 environment with CPU PyTorch 2.6.0, Transformers 4.49.0 and SentencePiece 0.2.0. Do not downgrade an existing Colab PyTorch installation. With these dependencies already installed:

```bash
python tools/run_notebook.py homework/day1_real_model.ipynb --installed
python tools/run_notebook.py homework/day4_evaluation.ipynb --installed
```

The `--installed` mode records installed versions instead of executing the install cell, while retaining the original Colab setup source and annotating that distinction. Inference still executes the actual model code.

## Four training stages
| Stage | Cells | Behavior |
|---|---:|---|
| Day 1 | 1–3 | Directory, mock, answer contract and blank-input check |
| Day 2 | 4–6 | Ticket validation, tool, ownership and five scenarios |
| Day 3 | 7–10 | Versioned prompt, input/output guards and ten golden cases |
| Day 4 | 11–14 | Public exact cache, metrics, regression, cost illustration and JSON export |

These are curriculum stages, not a claim of historical daily commits. Preserve and submit your genuine earlier commits if available. This package was assembled with AI assistance; it does not establish attendance or four-day participation.

## Examples
| Input | Expected result |
|---|---|
| `كيف أتابع طلبي؟` | Public Arabic directory answer |
| `How can I check my application status?` | Public English answer; repeated exact request may hit cache |
| `ما حالة طلبي REF-1001 في الرياض؟` | `under_review`, one tool call |
| `أريد حالة طلبي` | Ask for reference, zero tool calls |
| `REF-9999` | Internal `not_found`, generic unavailable answer |
| `REF-1002` | Internal `access_denied`, same unavailable answer |
| `Cancel REF-1001` | Read-only refusal; no mutation |

## Evaluation and limitations
The ten core golden cases and eight repository tests are separate checks, not a combined model-accuracy score. Cache hit rate is 66.7% over three identical public requests. Time is measured Python execution time; core token counts and USD 0.0036 cost are hypothetical. Real-model homework records actual tokenizer counts and local inference time, separately from the mock. See [the evaluation report](docs/evaluation.md).

The project has finite routing, limited keyword guards and a synthetic identity fixture. Passing these tests does not establish production security, real authentication or broad language understanding. A future improvement is a larger human-reviewed bilingual evaluation, followed by trusted identity and a separately controlled model integration.

## Attribution and assistance
LLM Application Engineering — SDA-AIE-213 · Trainer **Meaad Al-Marri** · SDAIA Academy training context · [SDAIA Academy](https://github.com/SDAIAAcademy).

Based on the trainer's [course repository](https://github.com/almiyead-rgb/murshid-llm-application-engineering-sda-aie-213). Course blocks and homework solutions are attributed; this package adds reproducible execution, report metadata, boundary checks, explanations and submission documentation with AI assistance. The learner should review and understand it and comply with the training provider's assistance rules. No endorsement, accreditation or certificate is claimed.
