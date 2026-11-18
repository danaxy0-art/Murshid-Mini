# Independent real-model evaluation homework solution. Same pinned dependencies as demo.
import json
import time
from pathlib import Path


def run_evaluation_homework():
    import torch
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    torch.set_num_threads(2)
    model_id = 'google/flan-t5-small'
    revision = '0fc9ddf78a1e988dac52e2dac162b0ede4fd74ab'
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision, trust_remote_code=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id, revision=revision,
        trust_remote_code=False, use_safetensors=True).to('cpu').eval()
    context = 'You can check your application status using its reference number.'
    questions = ['How can I check my application status?',
                 'What do I need to check my application status?',
                 'How can I find out the status of my application?']
    rows = []
    for case_number, question in enumerate(questions, 1):
        prompt = f'Answer the question using the context.\nContext: {context}\nQuestion: {question}\nAnswer:'
        inputs = tokenizer(prompt, return_tensors='pt', truncation=True, max_length=256)
        start = time.perf_counter()
        with torch.inference_mode():
            tokens = model.generate(**inputs, max_new_tokens=48, do_sample=False, num_beams=1)
        answer = tokenizer.decode(tokens[0], skip_special_tokens=True).strip()
        assert answer, 'Empty generation; inspect runtime.'
        # A deliberately weak measurable proxy, not a semantic judge.
        keyword_hit = 'reference' in answer.lower() and 'number' in answer.lower()
        rows.append({'id': f'E{case_number:02d}', 'question': question, 'answer': answer, 'reference_keyword_hit': keyword_hit,
                     'input_tokens': int(inputs['input_ids'].shape[-1]),
                     'output_tokens_including_special': int(tokens.shape[-1]),
                     'inference_seconds': round(time.perf_counter() - start, 3)})
    result = {'mode': 'real_local_model', 'model': model_id, 'model_revision': revision,
              'generation': {'do_sample': False, 'num_beams': 1, 'max_new_tokens': 48},
              'metric': 'reference+number keyword proxy; NOT semantic accuracy',
              'keyword_hits': sum(x['reference_keyword_hit'] for x in rows), 'total': len(rows),
              'external_inference_api_calls': 0, 'cases': rows,
              'manual_review': 'Check every answer for correct meaning and unsupported facts. Record failures; do not edit expected criteria to force a pass.'}
    out = Path('murshid_live_outputs'); out.mkdir(exist_ok=True)
    (out / 'evaluation_result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    run_evaluation_homework()
