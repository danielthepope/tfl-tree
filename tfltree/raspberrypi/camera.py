import logging as log
import picamera
from time import sleep
from tempfile import mkstemp
from tfltree import timeit
from tfltree.raspberrypi.led import RecordingLight
import subprocess

class Camera:
    camera = None
    recording_light = None

    def __init__(self):
        self.recording_light = RecordingLight()
        self.camera = picamera.PiCamera()
        self.camera.resolution = (720, 720)
        # Warm up
        self.recording_light.blink()
        sleep(2)
        self.recording_light.off()
        log.debug('Camera warmed up')

    @timeit
    def record_for_seconds(self, seconds, timestamp):
        (_, h264_path) = self._record_h264(seconds, timestamp)
        (_, mp4_path) = self._postprocess(h264_path, timestamp)
        return mp4_path

    @timeit
    def _record_h264(self, seconds, timestamp):
        (fd, path) = mkstemp('.h264', 'tfltree_video_%s_' % timestamp)
        self.recording_light.on()
        self.camera.start_recording(path)
        self.camera.wait_recording(seconds)
        self.camera.stop_recording()
        self.recording_light.off()
        log.debug('Saved video to %s' % path)
        return (fd, path)

    @timeit
    def _postprocess(self, h264_path, timestamp):
        (fd, path) = mkstemp('.mp4', 'tfltree_video_%s_' % timestamp)
        self.recording_light.blink()
        subprocess.check_output(['MP4Box', '-fps', '30', '-add', h264_path, path], stderr=subprocess.STDOUT)
        log.debug('Packaged MP4 at %s' % path)
        self.recording_light.off()
        return (fd, path)
