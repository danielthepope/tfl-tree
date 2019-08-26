from time import sleep, strftime
from tfltree.raspberrypi.camera import Camera
from tfltree.raspberrypi.tfl import TflApi
from tfltree.raspberrypi import speech, status_light, subtitle, video
from tempfile import mkstemp
import logging as log

API = TflApi()

def generate_audio_files(status, timestamp):
    audio_scripts = speech.generate_phrases_for_status(status)
    audio_files = []
    for index, phrase in enumerate(audio_scripts):
        (file_handle, path) = mkstemp('.wav', 'tfltree_%s_%s_' % (timestamp, index))
        log.debug('%s: "%s"' % (path, phrase))
        speech.generate_speech(path, phrase)
        duration = speech.speech_duration_ms(path)
        log.debug('%s duration is %sms' % (path, duration))
        audio_files.append({
            'file_handle': file_handle,
            'path': path,
            'phrase': phrase,
            'duration': duration
        })
    return audio_files

def main():
    camera = Camera()
    while True:
        timestamp = strftime('%Y%m%d_%H%M%S')
        status = API.update_status(timestamp)
        if API.has_status_changed():
            log.info('Status is different')
            log.debug(status)
            audio_files = generate_audio_files(status, timestamp)
            log.debug('Audio files: %s' % audio_files)
            total_duration = sum([f['duration'] for f in audio_files])
            log.info('Total duration: %sms' % total_duration)
            subtitle_file = subtitle.convert_to_srt_file(audio_files, timestamp)
            video_file = camera.record_for_seconds(total_duration/1000, timestamp)
            status_light.blink(0.02, 0.48)
            packaged_file = video.package_mp4(video_file, audio_files, timestamp)
            status_light.blink()
            subtitled_file = video.encode_mp4_with_subtitles(video_file, audio_files, subtitle_file, timestamp)
            status_light.blink(0.02, 9.98)
        else:
            log.debug('Status is the same')

        sleep(120)

if __name__ == '__main__':
    main()
