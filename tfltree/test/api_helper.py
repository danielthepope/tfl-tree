import json

from tfltree.raspberrypi import LineStatus


PICCADILLY_METROPOLITAN_ENGINEERING = json.loads(
    open('tfltree/test/fixtures/piccadilly_metropolitan_engineering.json', 'r').read()
)


NIGHT_TUBE_WITH_ENGINEERING = json.loads(
    open('tfltree/test/fixtures/night_tube_with_engineering.json', 'r').read()
)


MANY_DISRUPTIONS = json.loads(
    open('tfltree/test/fixtures/many_disruptions.json', 'r').read()
)


GOOD_SERVICE = json.loads(
    open('tfltree/test/fixtures/good_service.json', 'r').read()
)


STATUS_DESCRIPTIONS = {
    0: 'Special Service',
    1: 'Closed',
    2: 'Suspended',
    3: 'Part Suspended',
    4: 'Planned Closure',
    5: 'Part Closure',
    6: 'Severe Delays',
    7: 'Reduced Service',
    8: 'Bus Service',
    9: 'Minor Delays',
    10: 'Good Service',
    11: 'Part Closed',
    12: 'Exit Only',
    13: 'No Step Free Access',
    14: 'Change of frequency',
    15: 'Diverted',
    16: 'Not Running',
    17: 'Issues Reported',
    18: 'No Issues',
    19: 'Information',
    20: 'Service Closed'
}


def create_test_line_status(status_code, message):
    output = {
        '$type': 'Tfl.Api.Presentation.Entities.LineStatus, Tfl.Api.Presentation.Entities',
        'id': 0,
        'lineId': 'piccadilly',
        'statusSeverity': status_code,
        'statusSeverityDescription': STATUS_DESCRIPTIONS[status_code],
        'created': '0001-01-01T00:00:00'
    }
    if message:
        output['reason'] = message
    return LineStatus(affected_lines=['piccadilly'], raw_status=output, status_code=status_code)
