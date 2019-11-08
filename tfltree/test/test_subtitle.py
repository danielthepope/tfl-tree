import json
from unittest import TestCase

import tfltree.raspberrypi.subtitle as subtitle


class TestSubtitle(TestCase):
    def test_srt_generation(self):
        with open('tfltree/test/fixtures/many_issues.srt', 'r') as f:
            expected = f.read()
        with open('tfltree/test/fixtures/audio_files.json', 'r') as f:
            audio_files = json.loads(f.read())
        actual = subtitle._convert_to_srt_text(audio_files)
        self.assertEqual(actual, expected)

    def test_srt_fragment(self):
        expected = '3\n00:01:04,345 --> 00:01:24,172\nThere are minor delays on the\nCentral Line.\n\n'
        actual = subtitle._create_srt_fragment(3, 64345, 19827, 'There are minor delays on the Central Line.')
        self.assertEqual(actual, expected)

    def test_convert_timestamp(self):
        actual = subtitle._convert_ms_to_timestamp(64345)
        self.assertEqual(actual, '00:01:04,345')
