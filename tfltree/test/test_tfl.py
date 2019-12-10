import json
from unittest import TestCase

from tfltree.raspberrypi import LineStatus, tfl
from tfltree.test import api_helper


class TestTfl(TestCase):
    def test_map_status_to_model(self):
        api_response = api_helper.MANY_DISRUPTIONS
        actual = tfl._map_status_to_model(api_response)
        self.assertIsInstance(actual, list)
        self.assertIsInstance(actual[0], LineStatus)
        self.assertSetEqual(actual[0].affected_lines, set(['bakerloo']))
        self.assertSetEqual(actual[0].status_codes, set([6]))
        self.assertSetEqual(actual[1].affected_lines, set(['central']))
        self.assertSetEqual(actual[1].status_codes, set([6, 9]))
        self.assertSetEqual(actual[3].affected_lines, set(['metropolitan', 'piccadilly']))
        self.assertSetEqual(actual[3].status_codes, set([5]))

    def test_remove_line_name(self):
        actual = tfl._remove_line_name_from_reason('PICCADILLY LINE: No service between Rayners Lane and Uxbridge.')
        self.assertEqual(actual, 'No service between Rayners Lane and Uxbridge.')

    def test_remove_line_name_no_line(self):
        actual = tfl._remove_line_name_from_reason('Line is closed.')
        self.assertEqual(actual, 'Line is closed.')

    def test_status_equal(self):
        under_test = tfl.TflApi()
        with open('tfltree/test/fixtures/delay_metropolitan.json') as f:
            metropolitan = f.read()
        with open('tfltree/test/fixtures/delay_bakerloo.json') as f:
            bakerloo = f.read()
        under_test.status = tfl._map_status_to_model(json.loads(metropolitan))
        under_test._previous_status = tfl._map_status_to_model(json.loads(bakerloo))
        self.assertTrue(under_test.has_status_changed())
