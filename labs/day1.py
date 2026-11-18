# DAY 1 - Cell 1: environment, synthetic directory, and mock client
# Python standard library only. CPU. No pip, API key, GPU, or model download.
import json
import re
import sys
import time
import uuid
from pathlib import Path
from copy import deepcopy

assert sys.version_info >= (3, 9), 'Use a Python 3.9+ runtime.'
OUTPUT_DIR = Path('murshid_outputs')
OUTPUT_DIR.mkdir(exist_ok=True)
MODE = 'mock'
MODEL = 'training-mock'
SERVICE_DIRECTORY = {
    'ar': 'يمكنك متابعة حالة طلبك باستخدام رقم المرجع.',
    'en': 'You can check your application status using its reference number.'
}
FAQ_AR = 'كيف أتابع طلبي؟'
FAQ_EN = 'How can I check my application status?'


def save_json(name, value):
    path = OUTPUT_DIR / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    return str(path)


class FakeClient:
    def __init__(self):
        self.calls = 0

    def generate(self, question):
        self.calls += 1
        responses = {
            FAQ_AR: SERVICE_DIRECTORY['ar'],
            FAQ_EN: SERVICE_DIRECTORY['en'],
            'ساعدني': 'ما الخدمة التي تحتاج مساعدة بشأنها؟'
        }
        return responses.get(question, 'Please clarify the service you need.')


client = FakeClient()
print('Ready | mode=mock | model=training-mock | external API calls=0')

# DAY 1 - Cell 2: build the baseline application

def ask(question):
    start = time.perf_counter()
    if not isinstance(question, str) or not question.strip():
        answer = 'Please enter a valid question.'
    else:
        answer = client.generate(question.strip())
    return {
        'trace_id': str(uuid.uuid4()),
        'answer': answer,
        'model': MODEL,
        'latency_ms': round((time.perf_counter() - start) * 1000, 4)
    }


# DAY 1 - Cell 3: run, verify, and save the milestone
baseline_results = [ask(q) for q in (FAQ_AR, FAQ_EN, 'ساعدني')]
assert baseline_results[0]['answer'] == SERVICE_DIRECTORY['ar']
assert baseline_results[1]['answer'] == SERVICE_DIRECTORY['en']
assert baseline_results[2]['answer'] == 'ما الخدمة التي تحتاج مساعدة بشأنها؟'
for result in baseline_results:
    assert set(result) == {'trace_id', 'answer', 'model', 'latency_ms'}
    assert result['trace_id'] and result['latency_ms'] >= 0
calls_before = client.calls
assert ask('  ')['answer'] == 'Please enter a valid question.'
assert client.calls == calls_before
save_json('baseline_results.json', baseline_results)
print(json.dumps({'day': 1, 'checks': 'passed', 'answers': [r['answer'] for r in baseline_results]}, ensure_ascii=False, indent=2))
