import logging as log
from tempfile import mkstemp
from time import sleep

import picamera
from tfltree import timeit
from tfltree.raspberrypi import status_light


class Camera:
    camera = None

    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (720, 720)
        # Warm up
        status_light.blink()
        sleep(2)
        status_light.off()
        log.debug('Camera warmed up')

    @timeit
    def record_for_seconds(self, seconds, timestamp):
        (_, h264_path) = self._record_h264(seconds, timestamp)
        return h264_path

    @timeit
    def _record_h264(self, seconds, timestamp):
        (fd, path) = mkstemp('.h264', 'tfltree_video_%s_' % timestamp)
        status_light.on()
        self.camera.start_recording(path)
        self.camera.wait_recording(seconds)
        self.camera.stop_recording()
        status_light.off()
        log.debug('Saved video to %s' % path)
        return (fd, path)
