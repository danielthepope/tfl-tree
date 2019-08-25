from time import sleep, strftime
from tfltree.raspberrypi.camera import Camera
from tfltree.raspberrypi.tfl import TflApi
import tfltree.raspberrypi.speech as speech
from tempfile import mkstemp
import logging as log

API = TflApi()

def generate_audio_files(status):
    now = strftime('%Y%m%d_%H%M%S')
    audio_scripts = speech.generate_phrases_for_status(status)
    audio_files = []
    for index, phrase in enumerate(audio_scripts):
        (file_handle, path) = mkstemp('.wav', 'tfltree_%s_%s_' % (now, index))
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
        status = API.update_status()
        if API.has_status_changed():
            log.info('Status is different')
            log.debug(status)
            audio_files = generate_audio_files(status)
            total_duration = sum([f['duration'] for f in audio_files])
            log.info('Total duration: %sms' % total_duration)
            camera.record_for_seconds(total_duration/1000)
        else:
            log.debug('Status is the same')

        sleep(120)

if __name__ == '__main__':
    main()
