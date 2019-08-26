import tfltree.raspberrypi.subtitle as subtitle
import tfltree.test.audio_helper as audio_helper

def test_srt_generation():
    expected = open('tfltree/test/fixtures/many_issues.srt', 'r').read()
    actual = subtitle.convert_to_srt(audio_helper.AUDIO_FILES)
    assert actual == expected

def test_srt_fragment():
    expected = '3\n00:01:04,345 --> 00:01:24,172\nThere are minor delays on the\nCentral Line.\n\n'
    actual = subtitle._create_srt_fragment(3, 64345, 19827, 'There are minor delays on the Central Line.')
    assert actual == expected

def test_convert_timestamp():
    actual = subtitle._convert_ms_to_timestamp(64345)
    assert actual == '00:01:04,345'
