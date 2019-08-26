def convert_to_srt(audio_files):
    # audio_files is an array of dictionaries.
    # duration (milliseconds) and phrase are important fields here
    output = ''
    start = 0
    for index, file in enumerate(audio_files):
        output += _create_srt_fragment(index + 1, start, file['duration'], file['phrase'])
        start += file['duration']
    return output

def _create_srt_fragment(index, start, duration, text):
    start_timestamp = _convert_ms_to_timestamp(start)
    end_timestamp = _convert_ms_to_timestamp(start + duration)
    return f'{index}\n{start_timestamp} --> {end_timestamp}\n{text}\n\n'

MILLIS_IN_HOUR = 3600000
MILLIS_IN_MINUTE = 60000
MILLIS_IN_SECOND = 1000

def _convert_ms_to_timestamp(millis):
    hours = int(millis / MILLIS_IN_HOUR)
    minutes = int((millis % MILLIS_IN_HOUR) / MILLIS_IN_MINUTE)
    seconds = int((millis % MILLIS_IN_MINUTE) / MILLIS_IN_SECOND)
    ms = millis % MILLIS_IN_SECOND
    return f'{hours:02d}:{minutes:02d}:{seconds:02d},{ms:03d}'