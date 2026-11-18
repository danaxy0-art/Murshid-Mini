# DAY 2 - Cell 4: add synthetic records to the SAME notebook
# Re-run Day 1 first after a runtime reset. Session identity is trusted test setup,
# never extracted from the question. This is NOT a production authentication system.
RECORDS = {
    'REF-1001': {'owner': 'demo-user-1', 'status': 'under_review'},
    'REF-1002': {'owner': 'demo-user-2', 'status': 'approved'}
}
INITIAL_RECORDS = deepcopy(RECORDS)
SESSION = 'demo-user-1'


def extract_ticket(question):
    text = question.strip()
    match = re.search(r'\bREF-[0-9]{4}\b', text, re.IGNORECASE)
    ref = match.group().upper() if match else None
    if text in (FAQ_AR, FAQ_EN):
        service = 'service_info'
    elif ref or 'حالة' in text or 'status' in text.lower():
        service = 'application_status'
    else:
        service = 'other'
    city = 'Riyadh' if ('الرياض' in text or 'riyadh' in text.lower()) else 'unknown'
    return {'service': service, 'city': city, 'request_id': ref,
            'needs_clarification': service == 'application_status' and ref is None}


def validate_ticket(ticket):
    if not isinstance(ticket, dict) or set(ticket) != {'service', 'city', 'request_id', 'needs_clarification'}:
        return False
    if ticket['service'] not in ('service_info', 'application_status', 'other'):
        return False
    if ticket['city'] not in ('Riyadh', 'Jeddah', 'unknown'):
        return False
    if type(ticket['needs_clarification']) is not bool:
        return False
    ref = ticket['request_id']
    if ref is not None and (not isinstance(ref, str) or re.fullmatch(r'REF-[0-9]{4}', ref) is None):
        return False
    expected_clarification = ticket['service'] == 'application_status' and ref is None
    return ticket['needs_clarification'] == expected_clarification


# DAY 2 - Cell 5: build the read-only tool and route requests

def check_status(request_id, session):
    if not isinstance(request_id, str) or re.fullmatch(r'REF-[0-9]{4}', request_id) is None:
        return {'request_id': request_id, 'status': 'invalid_reference'}
    record = RECORDS.get(request_id)
    if record is None:
        return {'request_id': request_id, 'status': 'not_found'}
    if record['owner'] != session:
        return {'request_id': request_id, 'status': 'access_denied'}
    return {'request_id': request_id, 'status': record['status']}


def route(question, session=SESSION, ticket_override=None):
    text = question.strip()
    if any(word in text.lower() for word in ('cancel', 'ألغ', 'الغ', 'إلغاء')):
        return {'code': 'unsupported_action', 'answer': 'This demo is read-only; no application was changed.', 'tool_calls': 0}
    ticket = extract_ticket(text) if ticket_override is None else ticket_override
    if not validate_ticket(ticket):
        return {'code': 'invalid_schema', 'answer': 'The structured output was rejected.', 'tool_calls': 0}
    if ticket['needs_clarification']:
        return {'code': 'needs_clarification', 'answer': 'ما رقم مرجع الطلب؟', 'ticket': ticket, 'tool_calls': 0}
    if ticket['service'] == 'application_status':
        tool_result = check_status(ticket['request_id'], session)
        status = tool_result['status']
        # Same outward answer for missing and unauthorized records.
        answer = 'Application status: ' + status if status not in ('not_found', 'access_denied') else 'Unable to provide this application status.'
        return {'code': status, 'answer': answer, 'ticket': ticket, 'tool_result': tool_result, 'tool_calls': 1}
    if ticket['service'] == 'service_info':
        return {'code': 'ok', 'answer': client.generate(text), 'ticket': ticket, 'tool_calls': 0}
    return {'code': 'out_of_scope', 'answer': 'This service is not available in the demo directory.', 'ticket': ticket, 'tool_calls': 0}


# DAY 2 - Cell 6: compare five cases and check yesterday's behavior
DAY2_QUESTIONS = [
    'ما حالة طلبي REF-1001 في الرياض؟', 'أريد حالة طلبي',
    'ما حالة REF-9999؟', 'ألغ طلبي REF-1001', 'ما حالة REF-1002؟'
]
day2_results = [route(q) for q in DAY2_QUESTIONS]
assert [r['code'] for r in day2_results] == ['under_review', 'needs_clarification', 'not_found', 'unsupported_action', 'access_denied']
assert day2_results[0]['ticket'] == {'service': 'application_status', 'city': 'Riyadh', 'request_id': 'REF-1001', 'needs_clarification': False}
assert [r['tool_calls'] for r in day2_results] == [1, 0, 1, 0, 1]
assert route(FAQ_EN)['answer'] == SERVICE_DIRECTORY['en']
assert day2_results[4]['tool_result'] == {'request_id': 'REF-1002', 'status': 'access_denied'}
assert RECORDS == INITIAL_RECORDS
save_json('day2_results.json', day2_results)
print(json.dumps({'day': 2, 'checks': 'passed', 'codes': [r['code'] for r in day2_results], 'tool_calls': [r['tool_calls'] for r in day2_results]}, indent=2))
