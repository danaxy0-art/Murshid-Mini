# Deliberate, caught errors. These are examples to diagnose, not broken setup.
import json


def validate_public_question(question):
    if not isinstance(question, str) or not question.strip():
        raise ValueError('Enter a non-empty question string.')
    if len(question) > 500:
        raise ValueError('Use at most 500 characters.')
    return question.strip()


def run_error_examples():
    cases = [(None, 'Enter a non-empty question string.'),
             ('   ', 'Enter a non-empty question string.'),
             ('x' * 501, 'Use at most 500 characters.')]
    rows = []
    for value, expected in cases:
        try:
            validate_public_question(value)
        except ValueError as error:
            assert str(error) == expected
            rows.append({'error_type': type(error).__name__, 'message': str(error), 'expected_rejection': True})
        else:
            raise AssertionError('Invalid input was accepted.')
    assert validate_public_question(' How can I check my application status? ') == 'How can I check my application status?'
    result = {'intentional_caught_errors': rows, 'corrected_input': 'accepted', 'checks': 'passed'}
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    run_error_examples()
