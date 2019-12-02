from unittest import TestCase

from tfltree.raspberrypi import speech, tfl, LineStatus
from tfltree.test import api_helper


class TestSpeech(TestCase):

    def test_phrase_generator(self):
        line_statuses = tfl._map_status_to_model(api_helper.PICCADILLY_METROPOLITAN_ENGINEERING)
        actual = speech.generate_phrases_for_status(line_statuses)
        self.assertIsInstance(actual, list)
        self.assertIsInstance(actual[0], LineStatus)
        self.assertEqual(
            actual[0].phrase,
            'There is a partial closure on the Metropolitan Line. Saturday 24, Sunday 25 and Bank Holiday Monday 26 August, no'
            ' service between Rayners Lane and Uxbridge. Replacement buses operate.'
        )
        self.assertEqual(
            actual[1].phrase,
            'There is a partial closure on the Piccadilly Line. Saturday 24, Sunday 25 and Bank Holiday Monday 26 August, no'
            ' service between Rayners Lane and Uxbridge. Replacement buses operate.'
        )
        self.assertEqual(
            actual[2].phrase,
            'There is a good service on all other lines.'
        )

    def test_phrase_generator_night_tube(self):
        line_statuses = tfl._map_status_to_model(api_helper.NIGHT_TUBE_WITH_ENGINEERING)
        actual = speech.generate_phrases_for_status(line_statuses)
        phrases = [s.phrase for s in actual]
        self.assertListEqual(phrases, [
            'The Bakerloo Line is closed. The service will resume again later on this morning. ',
            'The Circle Line is closed. The service will resume again later on this morning. ',
            'The District Line is closed. The service will resume again later on this morning. ',
            'The Hammersmith & City Line is closed. The service will resume again later on this morning. ',
            'There is a partial closure on the Metropolitan Line. Saturday 24, Sunday 25 and Bank Holiday Monday 26 August, no'
            ' service between Rayners Lane and Uxbridge. Replacement buses operate.',
            'The Metropolitan Line is closed. The service will resume again later on this morning. ',
            'There is a partial closure on the Piccadilly Line. Saturday 24, Sunday 25 and Bank Holiday Monday 26 August, no'
            ' service between Rayners Lane and Uxbridge. Replacement buses operate.',
            'The Waterloo & City Line is closed. The service will resume again at 08:00 on Monday. ',
            'There is a good service on all other lines.'
        ])

    def test_many_disruptions(self):
        line_statuses = tfl._map_status_to_model(api_helper.MANY_DISRUPTIONS)
        actual = speech.generate_phrases_for_status(line_statuses)
        phrases = [s.phrase for s in actual]
        self.assertEqual(phrases, [
            "There are severe delays on the Bakerloo Line. Minor delays between Queen's Park and Harrow and Wealdstone due to"
            " an earlier fire alert at Kilburn High Road. ",
            'There are severe delays on the Central Line. Severe delays between Leytonstone and Epping and Woodford via'
            ' Hainault and Newbury Park and MINOR DELAYS on the rest of the line, while we fix a signal failure at'
            ' Leytonstone. Tickets will be accepted on London Buses, Greater Anglia via any reasonable route and Chiltern'
            ' Railways between West Ruislip and Marylebone. ',
            'There are minor delays on the Central Line. Severe delays between Leytonstone and Epping and Woodford via'
            ' Hainault and Newbury Park and MINOR DELAYS on the rest of the line, while we fix a signal failure at'
            ' Leytonstone. Tickets will be accepted on London Buses, Greater Anglia via any reasonable route and Chiltern'
            ' Railways between West Ruislip and Marylebone. ',
            "There are severe delays on the District Line. Severe delays between Wimbledon and Edgware Road and Minor delays"
            " between Earl's Court and Richmond / Ealing Broadway due to an earlier signal failure at Earl's Court, your"
            " tickets will be accepted on the buses. ",
            "There are minor delays on the District Line. Severe delays between Wimbledon and Edgware Road and Minor delays"
            " between Earl's Court and Richmond / Ealing Broadway due to an earlier signal failure at Earl's Court, your"
            " tickets will be accepted on the buses. ",
            'There is a partial closure on the Metropolitan Line. Saturday 24, Sunday 25 and Bank Holiday Monday 26 August, no'
            ' service between Rayners Lane and Uxbridge. Replacement buses operate.',
            'There is a partial closure on the Piccadilly Line. Saturday 24, Sunday 25 and Bank Holiday Monday 26 August, no'
            ' service between Rayners Lane and Uxbridge. Replacement buses operate.',
            'The Waterloo & City Line is closed. The service will resume again at 08:00 on Monday. ',
            'There is a good service on all other lines.'
        ])

    def test_good_service(self):
        line_statuses = tfl._map_status_to_model(api_helper.GOOD_SERVICE)
        actual = speech.generate_phrases_for_status(line_statuses)
        self.assertEqual(actual[0].phrase, 'There is a good service on all London Underground lines.')

    def test_remove_line_name(self):
        actual = speech._remove_line_name_from_reason('PICCADILLY LINE: No service between Rayners Lane and Uxbridge.')
        self.assertEqual(actual, 'No service between Rayners Lane and Uxbridge.')

    def test_remove_line_name_no_line(self):
        actual = speech._remove_line_name_from_reason('Line is closed.')
        self.assertEqual(actual, 'Line is closed.')

    def test_disruption_phrase_0(self):
        line_status = api_helper.create_test_line_status(0, 'PICCADILLY LINE: The service is special.')
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'The Piccadilly Line is running a special service. The service is special.')

    def test_disruption_phrase_1(self):
        line_status = api_helper.create_test_line_status(1, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'The Piccadilly Line is closed.')

    def test_disruption_phrase_2(self):
        line_status = api_helper.create_test_line_status(2, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'The Piccadilly Line is suspended.')

    def test_disruption_phrase_3(self):
        line_status = api_helper.create_test_line_status(3, 'PICCADILLY LINE: No service between Rayners Lane and Uxbridge.')
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(
            actual, 'The Piccadilly Line is part suspended. No service between Rayners Lane and Uxbridge.')

    def test_disruption_phrase_4(self):
        line_status = api_helper.create_test_line_status(4, 'PICCADILLY LINE: Entire line closed due to engineering works.')
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(
            actual, 'There is a planned closure on the Piccadilly Line. Entire line closed due to engineering works.')

    def test_disruption_phrase_5(self):
        line_status = api_helper.create_test_line_status(5, 'PICCADILLY LINE: No service between Rayners Lane and Uxbridge.')
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(
            actual,
            'There is a partial closure on the Piccadilly Line. No service between Rayners Lane and Uxbridge.'
        )

    def test_disruption_phrase_6(self):
        line_status = api_helper.create_test_line_status(6, 'Severe delays between Rayners Lane and Uxbridge.')
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(
            actual,
            'There are severe delays on the Piccadilly Line. Severe delays between Rayners Lane and Uxbridge.'
        )

    def test_disruption_phrase_7(self):
        line_status = api_helper.create_test_line_status(7, 'PICCADILLY LINE: Reduced service due to a staff strike.')
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(
            actual, 'The Piccadilly Line is running a reduced service. Reduced service due to a staff strike.')

    def test_disruption_phrase_8(self):
        line_status = api_helper.create_test_line_status(8, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'The Piccadilly Line is operating as a bus service.')

    def test_disruption_phrase_9(self):
        line_status = api_helper.create_test_line_status(9, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'There are minor delays on the Piccadilly Line.')

    def test_disruption_phrase_10(self):
        # I don't know if that's the right thing to do
        line_status = api_helper.create_test_line_status(10, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, None)

    def test_disruption_phrase_11(self):
        line_status = api_helper.create_test_line_status(11, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'The Piccadilly Line is part closed.')

    def test_disruption_phrase_12(self):
        line_status = api_helper.create_test_line_status(12, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'The Piccadilly Line is exit only.')

    def test_disruption_phrase_13(self):
        line_status = api_helper.create_test_line_status(13, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'The Piccadilly Line has no step free access.')

    def test_disruption_phrase_14(self):
        line_status = api_helper.create_test_line_status(14, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'There is a change of frequency on the Piccadilly Line.')

    def test_disruption_phrase_15(self):
        line_status = api_helper.create_test_line_status(15, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'The Piccadilly Line is being diverted.')

    def test_disruption_phrase_16(self):
        line_status = api_helper.create_test_line_status(16, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'The Piccadilly Line is not running.')

    def test_disruption_phrase_17(self):
        line_status = api_helper.create_test_line_status(17, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'There are issues reported on the Piccadilly Line.')

    def test_disruption_phrase_18(self):
        line_status = api_helper.create_test_line_status(18, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'There are no issues on the Piccadilly Line.')

    def test_disruption_phrase_19(self):
        line_status = api_helper.create_test_line_status(19, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'Information about the Piccadilly Line.')

    def test_disruption_phrase_20(self):
        line_status = api_helper.create_test_line_status(20, None)
        actual = speech._generate_disruption_phrase(line_status)
        self.assertEqual(actual, 'The Piccadilly Line is closed.')

    def test_pico_convert(self):
        actual = speech.convert_to_pico_text('The Hammersmith & City Line is closed.')
        expected = 'The Hammersmith and City Line is closed.'
        self.assertEqual(actual, expected)
