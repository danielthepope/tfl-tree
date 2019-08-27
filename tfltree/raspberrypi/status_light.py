from gpiozero import LED

_led = LED(17)


def on():
    _led.on()


def off():
    _led.off()


def blink(on_time=0.25, off_time=0.25, repetitions=None):
    _led.blink(on_time, off_time, repetitions)
