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
