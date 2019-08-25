from pymediainfo import MediaInfo
import subprocess

def generate_phrases_for_status(status):
    messages = []
    good_lines = []
    for line in status:
        disruption_phrases = _generate_disruption_phrases_for_line(line)
        if disruption_phrases:
            messages += disruption_phrases
        else:
            good_lines.append(line['name'])
    if good_lines:
        messages.append(_generate_good_line_phrase(good_lines))
    return messages


def generate_speech(filename, text):
    subprocess.check_call(['espeak', '-v', 'english', '-w', filename, text])


def speech_duration_ms(filename):
    media_info = MediaInfo.parse(filename)
    return media_info.tracks[0].duration


def _generate_good_line_phrase(good_lines):
    if len(good_lines) == 1:
        return 'There is a good service on the %s line.' % good_lines[0]
    elif len(good_lines) == 2:
        return 'There is a good service on the %s and %s lines.' % (good_lines[0], good_lines[1])
    elif len(good_lines) == 3:
        return 'There is a good service on the %s, %s and %s lines.' % (good_lines[0], good_lines[1], good_lines[2])
    elif len(good_lines) > 3:
        return 'There is a good service on all other lines.'


def _generate_disruption_phrase(line_name, line_status):
    severity = line_status['statusSeverity']
    if 'reason' in line_status:
        reason = line_status['reason']
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
        return []
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
        return []
    
    if reason:
        return ['%s %s' % (message, _remove_line_name_from_reason(reason))]
    else:
        return [message]


def _generate_disruption_phrases_for_line(line):
    line_name = line['name']
    output = []
    for line_status in line['lineStatuses']:
        output += _generate_disruption_phrase(line_name, line_status)
    return output


def _remove_line_name_from_reason(message):
    index = message.lower().find('line: ')
    if index >= 0:
        return message[index + 6:]
    else:
        return message
