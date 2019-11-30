import subprocess
from tempfile import mkstemp

from pymediainfo import MediaInfo
from tfltree import logger as log
from tfltree.raspberrypi import LineStatus


TUBE_ID_TO_NAME = {
    'bakerloo': 'Bakerloo',
    'central': 'Central',
    'circle': 'Circle',
    'district': 'District',
    'hammersmith-city': 'Hammersmith & City',
    'jubilee': 'Jubilee',
    'metropolitan': 'Metropolitan',
    'northern': 'Northern',
    'piccadilly': 'Piccadilly',
    'victoria': 'Victoria',
    'waterloo-city': 'Waterloo & City'
}


def map_tube_id_to_name(tube_id):
    if tube_id in TUBE_ID_TO_NAME:
        return TUBE_ID_TO_NAME[tube_id]
    else:
        log.warning('Tube ID %s not in list', tube_id)
        return tube_id


def generate_audio_files(line_statuses, timestamp):
    audio_statuses = generate_phrases_for_status(line_statuses)
    for index, line_status in enumerate(audio_statuses):
        (file_handle, file_path) = mkstemp('.wav', 'tfltree_%s_%s_' % (timestamp, index))
        log.debug('%s: "%s"', file_path, line_status)
        generate_speech(file_path, line_status.phrase)
        duration_ms = speech_duration_ms(file_path)
        log.debug('%s duration is %sms', file_path, duration_ms)
        line_status.file_handle = file_handle
        line_status.file_path = file_path
        line_status.duration_ms = duration_ms
    return audio_statuses


def generate_phrases_for_status(line_statuses):
    output_statuses = []
    good_lines = []
    for line_status in line_statuses:
        disruption_phrase = _generate_disruption_phrase(line_status)
        line_status.phrase = disruption_phrase
        if disruption_phrase:
            output_statuses.append(line_status)
        else:
            good_lines.append(line_status.affected_lines[0])
    if len(output_statuses) == 0:
        return [LineStatus(affected_lines=good_lines,
                           phrase='There is a good service on all London Underground lines.',
                           status_code=10)]
    if good_lines:
        output_statuses.append(LineStatus(affected_lines=good_lines,
                                          phrase=_generate_good_line_phrase(good_lines),
                                          status_code=10)
                               )
    return output_statuses


def convert_to_pico_text(text):
    return text.replace('&', 'and')


def generate_speech(filename, text):
    pico_text = convert_to_pico_text(text)
    subprocess.check_call(['pico2wave', '-l', 'en-GB', '-w', filename, pico_text])


def speech_duration_ms(filename):
    media_info = MediaInfo.parse(filename)
    return media_info.tracks[0].duration


def _generate_good_line_phrase(good_lines):
    line_names = list(map(map_tube_id_to_name, good_lines))
    if len(line_names) == 1:
        return 'There is a good service on the %s line.' % line_names[0]
    elif len(line_names) == 2:
        return 'There is a good service on the %s and %s lines.' % (line_names[0], line_names[1])
    elif len(line_names) == 3:
        return 'There is a good service on the %s, %s and %s lines.' % (line_names[0], line_names[1], line_names[2])
    elif len(line_names) > 3:
        return 'There is a good service on all other lines.'


def _generate_disruption_phrase_for_status_code(line_id, line_status):
    line_name = map_tube_id_to_name(line_id)
    severity = line_status.status_code
    if 'reason' in line_status.raw_status:
        reason = line_status.raw_status['reason']
    else:
        reason = None

    if severity == 0:
        message = 'The %s Line is running a special service.' % line_name
    elif severity == 1 or severity == 20:
        message = 'The %s Line is closed.' % line_name
    elif severity == 2:
        message = 'The %s Line is suspended.' % line_name
    elif severity == 3:
        message = 'The %s Line is part suspended.' % line_name
    elif severity == 4:
        message = 'There is a planned closure on the %s Line.' % line_name
    elif severity == 5:
        message = 'There is a partial closure on the %s Line.' % line_name
    elif severity == 6:
        message = 'There are severe delays on the %s Line.' % line_name
    elif severity == 7:
        message = 'The %s Line is running a reduced service.' % line_name
    elif severity == 8:
        message = 'The %s Line is operating as a bus service.' % line_name
    elif severity == 9:
        message = 'There are minor delays on the %s Line.' % line_name
    elif severity == 10:
        return None
    elif severity == 11:
        message = 'The %s Line is part closed.' % line_name
    elif severity == 12:
        message = 'The %s Line is exit only.' % line_name
    elif severity == 13:
        message = 'The %s Line has no step free access.' % line_name
    elif severity == 14:
        message = 'There is a change of frequency on the %s Line.' % line_name
    elif severity == 15:
        message = 'The %s Line is being diverted.' % line_name
    elif severity == 16:
        message = 'The %s Line is not running.' % line_name
    elif severity == 17:
        message = 'There are issues reported on the %s Line.' % line_name
    elif severity == 18:
        message = 'There are no issues on the %s Line.' % line_name
    elif severity == 19:
        message = 'Information about the %s Line.' % line_name
    else:
        return None

    if reason:
        return '%s %s' % (message, _remove_line_name_from_reason(reason))
    else:
        return message


def _generate_disruption_phrase(line_status):
    line_name = line_status.affected_lines[0]
    return _generate_disruption_phrase_for_status_code(line_name, line_status)


def _remove_line_name_from_reason(message):
    index = message.lower().find('line: ')
    if index >= 0:
        return message[index + 6:]
    else:
        return message
