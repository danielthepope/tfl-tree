import json

import tfltree.raspberrypi.subtitle as subtitle


def test_srt_generation():
    expected = open('tfltree/test/fixtures/many_issues.srt', 'r').read()
    audio_files = json.loads(open('tfltree/test/fixtures/audio_files.json', 'r').read())
    actual = subtitle._convert_to_srt_text(audio_files)
    print(actual)
    assert actual == expected


def test_srt_fragment():
    expected = '3\n00:01:04,345 --> 00:01:24,172\nThere are minor delays on the\nCentral Line.\n\n'
    actual = subtitle._create_srt_fragment(3, 64345, 19827, 'There are minor delays on the Central Line.')
    assert actual == expected


def test_convert_timestamp():
    actual = subtitle._convert_ms_to_timestamp(64345)
    assert actual == '00:01:04,345'
