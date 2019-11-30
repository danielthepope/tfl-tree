from time import sleep, strftime

from tfltree import logger as log
from tfltree.raspberrypi import lights, speech, status_light, subtitle, tweets, video
from tfltree.raspberrypi.camera import Camera
from tfltree.raspberrypi.tfl import TflApi, map_status_to_model

API = TflApi()


def main():
    camera = Camera()
    leds = lights.start_leds()
    while True:
        timestamp = strftime('%Y%m%d_%H%M%S')
        status = map_status_to_model(API.update_status(timestamp))
        if API.has_status_changed():
            log.info('Status is different')
            log.debug(status)
            lights.show_all_line_statuses(leds, status)
            audio_statuses = speech.generate_audio_files(status, timestamp)
            log.debug('Audio files: %r', audio_statuses)
            total_duration = sum([f.duration_ms for f in audio_statuses])
            log.info('Total duration: %sms', total_duration)
            subtitle_file = subtitle.convert_to_srt_file(audio_statuses, timestamp)
            # TODO set LED sequence here
            video_file = camera.record_for_seconds(total_duration/1000, timestamp)
            audio_filenames = [f.file_path for f in audio_statuses]
            status_light.blink()
            packaged_file = video.package_mp4(video_file, audio_filenames, timestamp)
            status_light.blink(0.9, 0.1)
            tweets.post_video('Hello from TFL Tree', packaged_file, subtitle_file)
            status_light.blink(0.02, 9.98)
        else:
            log.debug('Status is the same')

        sleep(120)


if __name__ == '__main__':
    main()
