import logging as log
import picamera
from time import sleep, strftime
from tempfile import mkstemp
from tfltree import timeit

class Camera:
    camera = None

    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (720, 720)
        # Warm up
        sleep(2)
        log.debug('Camera warmed up')

    @timeit
    def record_for_seconds(self, seconds):
        now = strftime('%Y%m%d_%H%M%S')
        (fd, path) = mkstemp('.h264', 'tfltree_video_%s_' % now)
        self.camera.start_recording(path)
        self.camera.wait_recording(seconds)
        self.camera.stop_recording()
        log.debug('Saved video to %s' % path)
        return (fd, path)
