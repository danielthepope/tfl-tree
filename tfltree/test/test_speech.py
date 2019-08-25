import tfltree.raspberrypi.speech as speech

import tfltree.test.api_helper as api_helper


def test_phrase_generator():
    assert speech.generate_phrases_for_status(api_helper.PICADILLY_METROPOLITAN_ENGINEERING) == [
        'There is a partial closure on the Metropolitan Line. Saturday 24, Sunday 25 and Bank Holiday Monday 26 August, no service between Rayners Lane and Uxbridge. Replacement buses operate.',
        'There is a partial closure on the Piccadilly Line. Saturday 24, Sunday 25 and Bank Holiday Monday 26 August, no service between Rayners Lane and Uxbridge. Replacement buses operate.',
        'There is a good service on all other lines.'
    ]


def test_phrase_generator_night_tube():
    assert speech.generate_phrases_for_status(api_helper.NIGHT_TUBE_WITH_ENGINEERING) == [
        'The Bakerloo Line is closed. The service will resume again later on this morning. ',
        'The Circle Line is closed. The service will resume again later on this morning. ',
        'The District Line is closed. The service will resume again later on this morning. ',
        'The Hammersmith & City Line is closed. The service will resume again later on this morning. ',
        'There is a partial closure on the Metropolitan Line. Saturday 24, Sunday 25 and Bank Holiday Monday 26 August, no service between Rayners Lane and Uxbridge. Replacement buses operate.',
        'The Metropolitan Line is closed. The service will resume again later on this morning. ',
        'There is a partial closure on the Piccadilly Line. Saturday 24, Sunday 25 and Bank Holiday Monday 26 August, no service between Rayners Lane and Uxbridge. Replacement buses operate.',
        'The Waterloo & City Line is closed. The service will resume again at 08:00 on Monday. ',
        'There is a good service on all other lines.'
    ]


def test_remove_line_name():
    actual = speech._remove_line_name_from_reason('PICCADILLY LINE: No service between Rayners Lane and Uxbridge.')
    assert actual == 'No service between Rayners Lane and Uxbridge.'


def test_remove_line_name_no_line():
    actual = speech._remove_line_name_from_reason('Line is closed.')
    assert actual == 'Line is closed.'


def test_disruption_phrase_0():
    line_status = api_helper.create_test_line_status(0, 'PICCADILLY LINE: The service is special.')
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['The Piccadilly Line is running a special service. The service is special.']


def test_disruption_phrase_1():
    line_status = api_helper.create_test_line_status(1, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['The Piccadilly Line is closed.']


def test_disruption_phrase_2():
    line_status = api_helper.create_test_line_status(2, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['The Piccadilly Line is suspended.']


def test_disruption_phrase_3():
    line_status = api_helper.create_test_line_status(3, 'PICCADILLY LINE: No service between Rayners Lane and Uxbridge.')
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['The Piccadilly Line is part suspended. No service between Rayners Lane and Uxbridge.']


def test_disruption_phrase_4():
    line_status = api_helper.create_test_line_status(4, 'PICCADILLY LINE: Entire line closed due to engineering works.')
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['There is a planned closure on the Piccadilly Line. Entire line closed due to engineering works.']


def test_disruption_phrase_5():
    line_status = api_helper.create_test_line_status(5, 'PICCADILLY LINE: No service between Rayners Lane and Uxbridge.')
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['There is a partial closure on the Piccadilly Line. No service between Rayners Lane and Uxbridge.']


def test_disruption_phrase_6():
    line_status = api_helper.create_test_line_status(6, 'Severe delays between Rayners Lane and Uxbridge.')
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['There are severe delays on the Piccadilly Line. Severe delays between Rayners Lane and Uxbridge.']


def test_disruption_phrase_7():
    line_status = api_helper.create_test_line_status(7, 'PICCADILLY LINE: Reduced service due to a staff strike.')
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['The Piccadilly Line is running a reduced service. Reduced service due to a staff strike.']


def test_disruption_phrase_8():
    line_status = api_helper.create_test_line_status(8, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['The Piccadilly Line is operating as a bus service.']


def test_disruption_phrase_9():
    line_status = api_helper.create_test_line_status(9, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['There are minor delays on the Piccadilly Line.']


def test_disruption_phrase_10():
    line_status = api_helper.create_test_line_status(10, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == []


def test_disruption_phrase_11():
    line_status = api_helper.create_test_line_status(11, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['The Piccadilly Line is part closed.']


def test_disruption_phrase_12():
    line_status = api_helper.create_test_line_status(12, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['The Piccadilly Line is exit only.']


def test_disruption_phrase_13():
    line_status = api_helper.create_test_line_status(13, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['The Piccadilly Line has no step free access.']


def test_disruption_phrase_14():
    line_status = api_helper.create_test_line_status(14, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['There is a change of frequency on the Piccadilly Line.']


def test_disruption_phrase_15():
    line_status = api_helper.create_test_line_status(15, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['The Piccadilly Line is being diverted.']


def test_disruption_phrase_16():
    line_status = api_helper.create_test_line_status(16, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['The Piccadilly Line is not running.']


def test_disruption_phrase_17():
    line_status = api_helper.create_test_line_status(17, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['There are issues reported on the Piccadilly Line.']


def test_disruption_phrase_18():
    line_status = api_helper.create_test_line_status(18, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['There are no issues on the Piccadilly Line.']


def test_disruption_phrase_19():
    line_status = api_helper.create_test_line_status(19, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['Information about the Piccadilly Line.']


def test_disruption_phrase_20():
    line_status = api_helper.create_test_line_status(20, None)
    actual = speech._generate_disruption_phrases_for_line(line_status)
    assert actual == ['The Piccadilly Line is closed.']

