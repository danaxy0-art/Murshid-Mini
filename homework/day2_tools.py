# Independent additional homework solution. Standard library, no model/API.
import json

RECORDS = {'REF-1001': {'owner': 'demo-user-1', 'status': 'under_review'},
           'REF-1002': {'owner': 'demo-user-2', 'status': 'approved'}}


def dispatch(call, trusted_user):
    # A supplied tool-call object is untrusted data, never executable code.
    if not isinstance(call, dict) or set(call) != {'name', 'arguments'}:
        return {'code': 'invalid_call'}
    if call['name'] != 'check_status':
        return {'code': 'tool_not_allowed'}
    args = call['arguments']
    if not isinstance(args, dict) or set(args) != {'reference'}:
        return {'code': 'invalid_arguments'}
    ref = args['reference']
    if not isinstance(ref, str) or len(ref) != 8 or not ref.startswith('REF-') or not ref[4:].isascii() or not ref[4:].isdigit():
        return {'code': 'invalid_arguments'}
    record = RECORDS.get(ref)
    # Same outward result for absent and unauthorized records.
    if record is None or record['owner'] != trusted_user:
        return {'code': 'unavailable'}
    return {'code': 'ok', 'status': record['status']}


def run_tool_homework():
    before = json.dumps(RECORDS, sort_keys=True)
    cases = [
        ({'name': 'check_status', 'arguments': {'reference': 'REF-1001'}}, {'code': 'ok', 'status': 'under_review'}),
        ({'name': 'check_status', 'arguments': {'reference': 'REF-1002'}}, {'code': 'unavailable'}),
        ({'name': 'check_status', 'arguments': {'reference': 'REF-9999'}}, {'code': 'unavailable'}),
        ({'name': 'delete_record', 'arguments': {'reference': 'REF-1001'}}, {'code': 'tool_not_allowed'}),
        ({'name': 'check_status', 'arguments': {'reference': 'REF-1001', 'owner': 'demo-user-2'}}, {'code': 'invalid_arguments'}),
        ({'name': 'check_status', 'arguments': {'reference': 1001}}, {'code': 'invalid_arguments'}),
        ('not a tool object', {'code': 'invalid_call'}),
    ]
    rows = []
    for index, (call, expected) in enumerate(cases, 1):
        actual = dispatch(call, trusted_user='demo-user-1')
        assert actual == expected, (index, actual, expected)
        rows.append({'case': index, 'result': actual, 'passed': actual == expected})
    assert json.dumps(RECORDS, sort_keys=True) == before
    result = {'mode': 'simulated_tool_protocol', 'passed': len(rows), 'total': len(cases),
              'records_unchanged': True, 'cases': rows}
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    run_tool_homework()
