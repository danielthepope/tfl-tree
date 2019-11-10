from unittest import TestCase

from tfltree.raspberrypi import LineStatus, tfl
from tfltree.test import api_helper


class TestTfl(TestCase):
    def test_map_status_to_model(self):
        api_response = api_helper.MANY_DISRUPTIONS
        actual = tfl.map_status_to_model(api_response)
        self.assertIsInstance(actual, list)
        self.assertIsInstance(actual[0], LineStatus)
        self.assertListEqual(actual[0].affected_lines, ['Bakerloo'])
        self.assertEqual(actual[0].status_code, 6)
        self.assertDictEqual(actual[0].raw_status, api_response[0]['lineStatuses'][0])
