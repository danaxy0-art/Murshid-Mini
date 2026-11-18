# Homework explanations / شرح الواجبات

Prepared with AI assistance using the instructor's openly supplied teaching blocks. Read and explain the implementation before submission. Actual execution evidence is in the notebooks and results; reference observations are not substituted for fresh runs.

## Day 1 — Real model
The supplied context says that an application can be tracked using its reference number. The tokenizer converts the prompt into token IDs, FLAN-T5-small generates output token IDs on CPU, and the tokenizer decodes them into text. Unlike `FakeClient`, these outputs come from downloaded model weights rather than a fixed answer dictionary. No inference API is called; downloading model files still needs internet. Review the actual generated answer in `results/day1/live_demo_result.json`.

باليوم الأول نحول السؤال والسياق إلى tokens وندخلها للنموذج ثم نحول ناتجه إلى نص. الفرق أن FakeClient يرجع إجابة محفوظة بينما النموذج الحقيقي يولد الإجابة وقد يخطئ.

## Day 2 — Validation versus authorization
Validation checks the shape, allowed tool name, argument keys and reference format. Authorization checks whether the trusted demo user owns the requested record. `REF-1002` has a valid format but belongs to another user, so it must not reveal its status. The identity is passed separately; adding `owner` to the call arguments is rejected. An absent record and an unauthorized record both return `unavailable` to the caller. All seven reference cases and extra malformed-reference cases are tested; the records remain unchanged.

التحقق من البيانات يتأكد أن الطلب مكتوب بالشكل الصحيح. الصلاحيات تتأكد أن المستخدم يحق له يشوف الطلب؛ صحة رقم المرجع ما تعني أن الطلب ملكه.

## Day 3 — Expected errors
| Input | Prediction / observed behavior | Correction |
|---|---|---|
| `None` | `ValueError: Enter a non-empty question string.` | Supply a string question |
| spaces only | Same non-empty error | Supply nonblank text |
| 501 characters | `ValueError: Use at most 500 characters.` | Shorten to at most 500 |

Corrected input: `How can I check my application status?`
`raise` signals invalid input; `try` surrounds the operation; `except ValueError` catches the intended rejection and allows the other cases to run. An expected rejection is a passing test because accepting bad input would violate the contract. An import/download failure is a setup failure, not an expected validation rejection.

الرفض هنا نتيجة صحيحة لأننا نتعمد إدخال قيمة غير صالحة. نستخدم try وexcept لمعالجة الخطأ بدل ما يتوقف البرنامج كله.

## Day 4 — Evaluation
Three fixed FAQ paraphrases are generated with the same model revision and deterministic decoding (`do_sample=False`, `num_beams=1`, `max_new_tokens=48`). Input counts come from the tokenizer; output counts include special tokens. Timing measures local generation, not download time or remote API latency. The keyword check requires both “reference” and “number”. This is a weak lexical proxy: an incorrect sentence could contain both words, and a correct paraphrase could use different words. Review each actual answer separately in the evaluation report.

One future improvement: add human-reviewed negative and Arabic cases and score supported meaning, unsupported claims and appropriate refusals separately. Preserve failed answers rather than changing the keyword rules to obtain a higher score.
