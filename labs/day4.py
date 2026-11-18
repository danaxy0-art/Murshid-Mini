# DAY 4 - Cell 11: cache ONLY the two exact, public directory questions
CACHE = {}
CACHE_TTL_SECONDS = 300
METRICS = []


def run_app(question, session=SESSION, ticket_override=None, use_cache=True,
            prompt_version=None, directory_version=None, now=None):
    prompt_version = PROMPT_VERSION if prompt_version is None else prompt_version
    directory_version = DIRECTORY_VERSION if directory_version is None else directory_version
    start = time.perf_counter()
    clock = time.monotonic() if now is None else now
    text = question.strip() if isinstance(question, str) else ''
    eligible = use_cache and ticket_override is None and text in (FAQ_AR, FAQ_EN)
    language = 'ar' if text == FAQ_AR else 'en'
    key = (text, language, MODEL, prompt_version, directory_version)
    entry = CACHE.get(key) if eligible else None
    hit = entry is not None and 0 <= clock - entry['created_at'] < CACHE_TTL_SECONDS
    calls_before = client.calls
    if hit:
        result = {'code': 'ok', 'answer': entry['answer'], 'tool_calls': 0,
                  'mode': MODE, 'trace_id': str(uuid.uuid4())}
    else:
        result = run_pipeline(question, session, ticket_override)
        if eligible and result['code'] == 'ok':
            CACHE[key] = {'answer': result['answer'], 'created_at': clock}
    result['cache_hit'] = hit
    result['latency_ms'] = round((time.perf_counter() - start) * 1000, 4)
    # Do not log questions, references, owners, or raw answers.
    METRICS.append({'trace_id': result['trace_id'], 'mode': MODE, 'code': result['code'],
                    'cache_hit': hit, 'mock_calls': client.calls - calls_before,
                    'tool_calls': result['tool_calls'], 'latency_ms': result['latency_ms']})
    return result


# DAY 4 - Cell 12: repeatable before/after experiment
CACHE.clear()
METRICS.clear()
client.calls = 0
without_cache = [run_app(FAQ_EN, use_cache=False) for _ in range(3)]
before_calls = client.calls
client.calls = 0
with_cache = [run_app(FAQ_EN, now=0) for _ in range(3)]
after_calls = client.calls
comparison = {'without_cache_mock_calls': before_calls, 'with_cache_mock_calls': after_calls,
              'cache_hit': [r['cache_hit'] for r in with_cache],
              'hit_rate_percent': round(100 * sum(r['cache_hit'] for r in with_cache) / 3, 1),
              'actual_external_api_calls': 0}
assert comparison['without_cache_mock_calls'] == 3
assert comparison['with_cache_mock_calls'] == 1
assert comparison['cache_hit'] == [False, True, True]
assert comparison['hit_rate_percent'] == 66.7
assert not run_app(FAQ_EN, prompt_version='v2', now=1)['cache_hit']
assert not run_app(FAQ_EN, directory_version='dir-v2', now=1)['cache_hit']
assert not run_app(FAQ_EN, now=300)['cache_hit']  # expires at the TTL boundary
size_before = len(CACHE)
for question, expected in [('REF-1001', 'under_review'), ('REF-9999', 'not_found'), ('REF-1002', 'access_denied')]:
    result = run_app(question)
    assert result['code'] == expected and result['cache_hit'] is False
assert len(CACHE) == size_before
assert RECORDS == INITIAL_RECORDS


# DAY 4 - Cell 13: regression, hypothetical cost, and final artifacts
final_tests = evaluate(run_app)
assert final_tests['passed'] == 10, final_tests
# Illustrative USD prices only: NOT provider prices, usage estimates, or savings.
hypothetical_cost = {'label': 'Illustration only; zero actual API spend',
                     'input_tokens': 1000, 'output_tokens': 400,
                     'usd_per_million_input': 2.0, 'usd_per_million_output': 4.0}
hypothetical_cost['usd_per_request'] = round((1000 * 2 + 400 * 4) / 1_000_000, 4)
assert hypothetical_cost['usd_per_request'] == 0.0036
final_report = {'project': 'Murshid Mini', 'course': 'SDA-AIE-213', 'mode': MODE,
                'dataset': 'synthetic-v1', 'golden_tests': final_tests,
                'experiment_date_utc': time.strftime('%Y-%m-%d', time.gmtime()),
                'prompt_version': PROMPT_VERSION, 'directory_version': DIRECTORY_VERSION,
                'environment': 'Python CPU local execution; not a claimed Colab run',
                'cache_experiment': comparison, 'hypothetical_cost': hypothetical_cost,
                'limits': ['No live language model', 'No real authentication',
                           'Finite rule-based routing', 'Educational guards only',
                           'No production readiness claim']}
save_json('day4_results.json', comparison)
save_json('final_report.json', final_report)
save_json('metrics.json', METRICS)
save_json('synthetic_data.json', {'service_directory': SERVICE_DIRECTORY, 'records': RECORDS})
print(json.dumps({'day': 4, 'checks': 'passed', 'golden_passed': final_tests['passed'],
                  'comparison': comparison, 'output_folder': str(OUTPUT_DIR)}, indent=2))

# DAY 4 - Cell 14: optional export (download through Colab's Files panel)
import zipfile
with zipfile.ZipFile('murshid_submission.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(OUTPUT_DIR.glob('*.json')):
        archive.write(path, arcname=path.name)
print('Created murshid_submission.zip. Save/download your notebook separately.')
