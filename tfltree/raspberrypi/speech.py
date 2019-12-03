import subprocess
from tempfile import mkstemp

from pymediainfo import MediaInfo
from tfltree import logger as log
from tfltree.raspberrypi import LineStatus
from tfltree.raspberrypi.tfl import _remove_line_name_from_reason


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


def map_tube_id_to_name_plural(tube_id_set):
    id_list = sorted(list(tube_id_set))
    name_list = list(map(map_tube_id_to_name, id_list))
    if len(name_list) == 1:
        return name_list[0] + ' Line'
    return ', '.join(name_list[:-1]) + ' and ' + name_list[-1] + ' Lines'


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
    good_lines = set()
    for line_status in line_statuses:
        disruption_phrase = _generate_disruption_phrase(line_status)
        line_status.phrase = disruption_phrase
        if disruption_phrase:
            output_statuses.append(line_status)
        else:
            good_lines.update(line_status.affected_lines)
    if len(output_statuses) == 0:
        return [LineStatus(affected_lines=good_lines,
                           phrase='There is a good service on all London Underground lines.',
                           status_codes=set([10]))]
    if good_lines:
        output_statuses.append(LineStatus(affected_lines=good_lines,
                                          phrase=_generate_good_line_phrase(good_lines),
                                          status_codes=set([10]))
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
    if len(good_lines) > 3:
        return 'There is a good service on all other lines.'

    line_names = map_tube_id_to_name_plural(good_lines)
    return 'There is a good service on the %s.' % line_names[0]


def _generate_disruption_phrase(line_status):
    plural = len(line_status.affected_lines) > 1
    many_issues = len(line_status.status_codes) > 1
    line_name = map_tube_id_to_name_plural(line_status.affected_lines)
    is_are = 'are' if plural else 'is'

    if many_issues:
        message = 'There are multiple issues on the %s.' % line_name
    else:
        severity = list(line_status.status_codes)[0]

        if severity == 0:
            message = 'The %s %s running a special service.' % (line_name, is_are)
        elif severity == 1 or severity == 20:
            message = 'The %s %s closed.' % (line_name, is_are)
        elif severity == 2:
            message = 'The %s %s suspended.' % (line_name, is_are)
        elif severity == 3:
            message = 'The %s %s part suspended.' % (line_name, is_are)
        elif severity == 4:
            message = 'There is a planned closure on the %s.' % line_name
        elif severity == 5:
            message = 'There is a partial closure on the %s.' % line_name
        elif severity == 6:
            message = 'There is disruption on the %s.' % line_name
        elif severity == 7:
            message = 'The %s %s running a reduced service.' % (line_name, is_are)
        elif severity == 8:
            message = 'The %s %s operating as a bus service.' % (line_name, is_are)
        elif severity == 9:
            message = 'There is disruption on the %s.' % line_name
        elif severity == 10:
            return None
        elif severity == 11:
            message = 'The %s %s part closed.' % (line_name, is_are)
        elif severity == 12:
            message = 'The %s %s exit only.' % (line_name, is_are)
        elif severity == 13:
            message = 'The %s has no step free access.' % line_name
        elif severity == 14:
            message = 'There is a change of frequency on the %s.' % line_name
        elif severity == 15:
            message = 'The %s %s being diverted.' % (line_name, is_are)
        elif severity == 16:
            message = 'The %s %s not running.' % (line_name, is_are)
        elif severity == 17:
            message = 'There are issues reported on the %s.' % line_name
        elif severity == 18:
            message = 'There are no issues on the %s.' % line_name
        elif severity == 19:
            message = 'Information about the %s.' % line_name
        else:
            return None

    if line_status.reason:
        return '%s %s' % (message, line_status.reason)
    else:
        return message
