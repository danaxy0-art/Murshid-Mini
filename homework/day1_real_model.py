# OPTIONAL REAL-MODEL EXTENSION: run in a separate notebook/runtime.
# Never paste into or replace cells in the required mock notebook.
import json
import time
from pathlib import Path

LIVE_MODEL_ID = 'google/flan-t5-small'
LIVE_MODEL_REVISION = '0fc9ddf78a1e988dac52e2dac162b0ede4fd74ab'
LIVE_OUTPUT_DIR = Path('murshid_live_outputs')


def run_live_demo():
    import torch
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    torch.set_num_threads(2)
    tokenizer = AutoTokenizer.from_pretrained(
        LIVE_MODEL_ID, revision=LIVE_MODEL_REVISION, trust_remote_code=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        LIVE_MODEL_ID, revision=LIVE_MODEL_REVISION,
        trust_remote_code=False, use_safetensors=True).to('cpu').eval()
    # Public synthetic context only; no private application records or identities.
    context = 'You can check your application status using its reference number.'
    question = 'How can I check my application status?'
    prompt = f'Answer the question using the context.\nContext: {context}\nQuestion: {question}\nAnswer:'
    encoded = tokenizer(prompt, return_tensors='pt', truncation=True, max_length=256)
    started = time.perf_counter()
    with torch.inference_mode():
        generated = model.generate(**encoded, max_new_tokens=48, do_sample=False, num_beams=1)
    answer = tokenizer.decode(generated[0], skip_special_tokens=True).strip()
    # Smoke check only: this does NOT establish factual correctness or safety.
    assert isinstance(answer, str) and answer, 'No answer generated; inspect the runtime.'
    report = {
        'mode': 'real_local_model', 'model': LIVE_MODEL_ID,
        'model_revision': LIVE_MODEL_REVISION, 'device': 'cpu',
        'context': context, 'question': question, 'answer': answer,
        'inference_seconds': round(time.perf_counter() - started, 3),
        'input_tokens': int(encoded['input_ids'].shape[-1]),
        'output_tokens_including_special': int(generated.shape[-1]),
        'external_inference_api_calls': 0,
        'review_required': 'Check whether the answer tells the user to use the reference number. Reject unsupported fees, dates or status claims.'
    }
    LIVE_OUTPUT_DIR.mkdir(exist_ok=True)
    (LIVE_OUTPUT_DIR / 'live_demo_result.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    run_live_demo()
