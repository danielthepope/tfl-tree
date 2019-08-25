from gpiozero import LED

class RecordingLight:
    led=None

    def __init__(self, pin=17):
        self.led = LED(pin)

    def on(self):
        self.led.on()

    def off(self):
        self.led.off()

    def blink(self, on_time=0.25, off_time=0.25, repetitions=None):
        self.led.blink(on_time, off_time, repetitions)
