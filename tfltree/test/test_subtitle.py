import json
from unittest import TestCase

from tfltree.raspberrypi import LineStatus, subtitle


class TestSubtitle(TestCase):
    def test_srt_generation(self):
        with open('tfltree/test/fixtures/many_issues.srt', 'r') as f:
            expected = f.read()
        with open('tfltree/test/fixtures/audio_files.json', 'r') as f:
            audio_file_list = json.loads(f.read())
        audio_statuses = [LineStatus(duration_ms=f['duration'], phrase=f['phrase']) for f in audio_file_list]
        actual = subtitle._convert_to_srt_text(audio_statuses)
        self.assertEqual(actual, expected)

    def test_srt_fragment(self):
        expected = '3\n00:01:04,345 --> 00:01:24,172\nThere are minor delays on the\nCentral Line.\n\n'
        actual = subtitle._create_srt_fragment(3, 64345, 19827, 'There are minor delays on the Central Line.')
        self.assertEqual(actual, expected)

    def test_convert_timestamp(self):
        actual = subtitle._convert_ms_to_timestamp(64345)
        self.assertEqual(actual, '00:01:04,345')
