import logging as log
from tempfile import mkstemp


def convert_to_srt_file(audio_files, timestamp):
    (_, path) = mkstemp('.srt', 'tfltree_%s_' % timestamp)
    srt_text = _convert_to_srt_text(audio_files)
    with open(path, 'w') as file:
        file.write(srt_text)
    log.debug('Written subtitle file to %s' % path)
    return path


def _convert_to_srt_text(audio_files):
    # audio_files is an array of dictionaries.
    # duration (milliseconds) and phrase are important fields here
    output = ''
    start = 0
    fragments = []
    for file in audio_files:
        fragments += _split_file_into_fragments(file)
    for index, fragment in enumerate(fragments):
        output += _create_srt_fragment(index + 1, start, fragment['duration'], fragment['phrase'])
        start += fragment['duration']
    return output


CHARACTERS_PER_FRAGMENT = 64


def _split_file_into_fragments(audio_file):
    fragments = [{'phrase': ''}]
    total_duration = audio_file['duration']
    words = audio_file['phrase'].strip().split(' ')
    char_count = 0
    for word in words:
        if char_count + len(word) > CHARACTERS_PER_FRAGMENT:
            fragments.append({'phrase': ''})
            char_count = 0
        fragments[-1]['phrase'] += word + ' '
        char_count += len(word) + 1
    # Calculate duration per fragment
    fragment_duration = int(total_duration / len(fragments))
    for fragment in fragments:
        fragment['phrase'] = fragment['phrase'].strip()
        fragment['duration'] = fragment_duration
    return fragments


CHARACTERS_PER_LINE = 32
MAX_LINES = 2


def _create_srt_fragment(index, start, duration, text):
    start_timestamp = _convert_ms_to_timestamp(start)
    end_timestamp = _convert_ms_to_timestamp(start + duration)
    words = text.split(' ')
    srt_lines = ['']
    char_count = 0
    for word in words:
        if char_count + len(word) > CHARACTERS_PER_LINE and len(srt_lines) < MAX_LINES:
            srt_lines.append('')
            char_count = 0
        srt_lines[-1] += word + ' '
        char_count += len(word) + 1
    srt_text = ''
    for line in srt_lines:
        srt_text += line.strip() + '\n'
    return '%s\n%s --> %s\n%s\n' % (index, start_timestamp, end_timestamp, srt_text)


MILLIS_IN_HOUR = 3600000
MILLIS_IN_MINUTE = 60000
MILLIS_IN_SECOND = 1000


def _convert_ms_to_timestamp(millis):
    hours = int(millis / MILLIS_IN_HOUR)
    minutes = int((millis % MILLIS_IN_HOUR) / MILLIS_IN_MINUTE)
    seconds = int((millis % MILLIS_IN_MINUTE) / MILLIS_IN_SECOND)
    ms = millis % MILLIS_IN_SECOND
    return '%02d:%02d:%02d,%03d' % (hours, minutes, seconds, ms)
