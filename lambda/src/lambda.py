import logging
import json
import os
import subprocess
from tempfile import mkstemp
from time import strftime

import boto3

log = logging.getLogger(os.path.basename(__file__))
log.setLevel(logging.DEBUG)

s3 = boto3.client('s3')


def handle(event, context):
    log.info('Lambda invoked. event: %s' % event)
    parsed_message = json.loads(event['Records'][0]['Sns']['Message'])
    log.info(parsed_message)
    in_video_file = _download_to_temp_file(parsed_message['video'])
    in_audio_files = [_download_to_temp_file(key) for key in parsed_message['audio']]
    in_subtitle_file = _download_to_temp_file(parsed_message['subtitle'])
    out_video_file = run_ffmpeg(in_video_file, in_audio_files, in_subtitle_file)
    now = strftime('%Y%m%d_%H%M%S')
    destination_key = _upload_to_s3(out_video_file, now)
    return destination_key


def run_ffmpeg(video_file, audio_files, subtitle_file):
    (fd, filename) = mkstemp('.mp4')
    command = _generate_ffmpeg_command(video_file, audio_files, subtitle_file, filename)
    log.debug('Command: %s' % command)
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        log.error('Failed to call ffmpeg')
        log.error(e.output)
    return filename


def _generate_ffmpeg_command(video_file, audio_files, subtitle_file, filename):
    command = ['./ffmpeg', '-y', '-r', '30', '-i', video_file]
    for f in audio_files:
        command += ['-i', f]
    command.append('-filter_complex')
    command.append(_generate_filter(audio_files, 1, 'outa'))
    command += ['-map', '0:0', '-map', '[outa]']
    command += ['-vf', 'subtitles=%s' % subtitle_file]
    command += ['-c:a', 'mp3', filename]
    return command


def _generate_filter(audio_files, start_index, stream_name):
    output = ''
    for i in range(len(audio_files)):
        output += '[%s:0]' % (i + start_index)
    output += 'concat=n=%s:v=0:a=1[%s]' % (len(audio_files), stream_name)
    return output


def _download_to_temp_file(s3_key):
    extension = s3_key.split('.')[-1]
    (fd, filename) = mkstemp('.%s' % extension)
    log.debug('Downloading s3://tfltree/%s to %s' % (s3_key, filename))
    s3.download_file('tfltree', s3_key, filename)
    return filename


def _upload_to_s3(file_name, timestamp):
    extension = file_name.split('.')[-1]
    destination_key = 'output/%s.%s' % (timestamp, extension)
    log.debug('Uploading %s to s3://tfltree/%s' % (file_name, destination_key))
    s3.upload_file(file_name, 'tfltree', destination_key)
    return destination_key
