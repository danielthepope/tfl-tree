import os
import random
from time import sleep, time
from threading import Thread

from led_server import led

from tfltree import logger as log
from tfltree.raspberrypi.config import LAMP_ON_COMMAND, LAMP_OFF_COMMAND, LED_ENDPOINT


LINE_COLOURS = {
    'bakerloo': [178, 99, 0],
    'central': [220, 36, 31],
    'circle': [255, 211, 41],
    'district': [0, 125, 50],
    'hammersmith-city': [244, 169, 190],
    'jubilee': [161, 165, 167],
    'metropolitan': [155, 0, 88],
    'northern': [30, 30, 30],  # hmmm
    'piccadilly': [0, 25, 168],
    'victoria': [0, 152, 216],
    'waterloo-city': [147, 206, 186]
}

LINE_COUNT = len(LINE_COLOURS.keys())


def start_leds():
    leds = led.LedFactory().create(LED_ENDPOINT)
    leds.start()
    default_sequence(leds)
    return leds


def default_sequence(leds):
    for i, k in enumerate(LINE_COLOURS.keys()):
        leds.set_pixel(i, [LINE_COLOURS[k]], repeat=LINE_COUNT, modifier='sparkle', offset=0.05)


def create_leds_for_status(status):
    output = []
    for line in status.affected_lines:
        home_colour = LINE_COLOURS[line]
        for status_code in status.status_codes:
            output.append(create_led_for_status_code(status_code, home_colour))
    return output


def create_led_for_status_code(status_code, home_colour):
    output = {}
    output['colours'] = []
    output['modifier'] = 'none'
    output['duration'] = 2
    output['offset'] = None
    if status_code == 1 or status_code == 2 or status_code == 4 or status_code == 11 or status_code == 20:
        # Closed / suspended / Planned closure / Part closed
        output['colours'].append(home_colour)
        output['colours'] += [[0, 0, 0]] * 5
        output['modifier'] = 'smooth'
        output['duration'] = 2
    elif status_code == 3 or status_code == 5:
        # Part suspended / partial closure
        output['colours'].append(home_colour)
        output['colours'].append(home_colour)
        output['colours'].append(home_colour)
        output['colours'].append([0, 0, 0])
        output['modifier'] = 'smooth'
        output['duration'] = 1
    elif status_code == 6:
        # Severe delays
        output['colours'].append(home_colour)
        output['colours'].append([0, 0, 0])
        output['duration'] = 0.5
    elif status_code == 9:
        # Minor delays
        output['colours'].append(home_colour)
        output['colours'].append(home_colour)
        output['colours'].append([0, 0, 0])
        output['duration'] = 1
    elif status_code == 10:
        # Good service
        output['colours'].append(led.lerp_colour([0, 0, 0], home_colour, 0.6))
        output['colours'].append(home_colour)
        output['colours'].append(led.lerp_colour([0, 0, 0], home_colour, 0.6))
        output['modifier'] = 'noise'
        output['offset'] = random.random() * 42  # Use for 'noise' modifier
        output['duration'] = 0.4
    else:
        output['colours'].append(led.lerp_colour([0, 0, 0], home_colour, 0.3))
        output['colours'].append(home_colour)
        output['modifier'] = 'smooth'
        output['duration'] = 2
    return output


def show_all_line_statuses(leds, statuses):
    repeat = len(statuses)
    all_lights = []
    for status in statuses:
        all_lights += create_leds_for_status(status)
    repeat = len(all_lights)
    for i, light in enumerate(all_lights):
        leds.set_pixel(i,
                       colours=light['colours'],
                       modifier=light['modifier'],
                       duration=light['duration'],
                       offset=light['offset'] or (i / repeat),
                       repeat=repeat)


def _play_sequence(leds, statuses, summary_seconds=None):
    for status in statuses:
        start_time = time()
        expected_duration_s = status.duration_ms / 1000
        light_list = create_leds_for_status(status)
        repeat = len(light_list)
        for i, light in enumerate(light_list):
            leds.set_pixel(i,
                           colours=light['colours'],
                           modifier=light['modifier'],
                           duration=light['duration'],
                           offset=light['offset'] or (i / repeat),
                           repeat=repeat)
        sleep(max(expected_duration_s - (time() - start_time), 0))

    if summary_seconds:
        show_all_line_statuses(leds, statuses)
        sleep(summary_seconds)


def play_a_sequence(leds, statuses, summary_seconds=None):
    thread = Thread(target=_play_sequence, args=(leds, statuses, summary_seconds))
    thread.start()


def lamp_on():
    log.debug(LAMP_ON_COMMAND)
    os.system(LAMP_ON_COMMAND)
    log.debug('done')


def lamp_off():
    log.debug(LAMP_OFF_COMMAND)
    os.system(LAMP_OFF_COMMAND)
    log.debug('done')


if __name__ == '__main__':
    from tfltree.raspberrypi import tfl, speech
    from time import strftime

    log.info('Hello')
    timestamp = strftime('%Y%m%d_%H%M%S')
    statuses = tfl.TflApi().update_status(timestamp)
    audio_statuses = speech.generate_phrases_for_status(statuses)
    for s in audio_statuses:
        s.duration_ms = 5000

    log.info('Starting LEDs')
    leds = start_leds()
    play_a_sequence(leds, audio_statuses, 10)

    try:
        while True:
            sleep(1)
    except Exception as e:
        leds.all_off()
        raise e
