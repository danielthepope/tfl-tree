import logging as log
import subprocess
from tempfile import mkstemp

from tfltree import timeit


@timeit
def package_mp4(video_file, audio_files, timestamp):
    output_file = _create_temp_output_file('%s_packaged' % timestamp)
    command = _generate_ffmpeg_package_command(video_file, audio_files, output_file)
    _run_ffmpeg(command)
    log.debug('Packaged video file saved to %s', output_file)
    return output_file


@timeit
def encode_mp4_with_subtitles(video_file, audio_files, subtitle_file, timestamp):
    output_file = _create_temp_output_file('%s_subtitled' % timestamp)
    command = _generate_ffmpeg_burn_subtitles_command(video_file, audio_files, subtitle_file, output_file)
    _run_ffmpeg(command)
    log.debug('Subtitled video file saved to %s', output_file)
    return output_file


def _create_temp_output_file(timestamp):
    (_, path) = mkstemp('.mp4', 'tfltree_%s_' % timestamp)
    return path


def _generate_ffmpeg_package_command(video_file, audio_files, output_file):
    return _generate_ffmpeg_command(output_file, video_file, audio_files)


def _generate_ffmpeg_burn_subtitles_command(video_file, audio_files, subtitle_file, output_file):
    return _generate_ffmpeg_command(output_file, video_file, audio_files, subtitle_file)


def _generate_ffmpeg_command(output_file, video_file, audio_files, subtitle_file=None):
    command = ['ffmpeg', '-y', '-r', '30', '-i', video_file]
    for f in audio_files:
        command += ['-i', f]
    command.append('-filter_complex')
    command.append(_generate_filter(audio_files, 1, 'outa'))
    command += ['-map', '0:0', '-map', '[outa]']
    if subtitle_file:
        command += ['-vf', 'subtitles=%s' % subtitle_file]
    else:
        command += ['-c:v', 'copy']
    command += ['-c:a', 'mp3']
    command.append(output_file)
    return command


def _generate_filter(audio_files, start_index, stream_name):
    output = ''
    for i in range(len(audio_files)):
        output += '[%s:0]' % (i + start_index)
    output += 'concat=n=%s:v=0:a=1[%s]' % (len(audio_files), stream_name)
    return output


def _run_ffmpeg(command):
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        log.error('Failed to call ffmpeg')
        log.error(e.output)
