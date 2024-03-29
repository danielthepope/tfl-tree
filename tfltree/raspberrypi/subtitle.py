from tempfile import mkstemp

from tfltree import logger as log


def convert_to_srt_file(audio_statuses, timestamp):
    (_, path) = mkstemp('.srt', 'tfltree_%s_' % timestamp)
    srt_text = _convert_to_srt_text(audio_statuses)
    with open(path, 'w') as file:
        file.write(srt_text)
    log.debug('Written subtitle file to %s', path)
    return path


def _convert_to_srt_text(audio_statuses):
    # audio_statuses is an array of LineStatus objects.
    # duration_ms and phrase are important fields here
    output = ''
    start = 0
    fragments = []
    for line_status in audio_statuses:
        fragments += _split_file_into_fragments(line_status)
    for index, fragment in enumerate(fragments):
        output += _create_srt_fragment(index + 1, start, fragment['duration'], fragment['phrase'])
        start += fragment['duration']
    return output


CHARACTERS_PER_FRAGMENT = 64
MINIMUM_DURATION_FOR_FRAGMENT = 1000


def _split_file_into_fragments(line_status):
    fragments = [{'phrase': ''}]
    total_duration = line_status.duration_ms
    total_characters = len(line_status.phrase)
    words = line_status.phrase.strip().split(' ')
    char_count = 0
    for word in words:
        if char_count + len(word) > CHARACTERS_PER_FRAGMENT:
            fragments.append({'phrase': ''})
            char_count = 0
        fragments[-1]['phrase'] += word + ' '
        char_count += len(word) + 1
    fragment_durations = [(total_duration/total_characters)*len(f['phrase']) for f in fragments]
    # Fragments must be of a minimum duration
    if fragment_durations[-1] < MINIMUM_DURATION_FOR_FRAGMENT:
        difference = MINIMUM_DURATION_FOR_FRAGMENT - fragment_durations[-1]
        number_of_fragments_to_add = len(fragment_durations) - 1
        for i in range(number_of_fragments_to_add):
            fragment_durations[i] -= difference / number_of_fragments_to_add
        fragment_durations[-1] = MINIMUM_DURATION_FOR_FRAGMENT
    for index, fragment in enumerate(fragments):
        phrase = fragment['phrase'].strip()
        fragment['phrase'] = phrase
        fragment['duration'] = round(fragment_durations[index])
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
