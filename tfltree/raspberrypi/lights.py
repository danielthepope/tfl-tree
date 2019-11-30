import random
from time import sleep

from led_server import led

from tfltree.raspberrypi.config import LED_ENDPOINT


LINE_COLOURS = {
    'bakerloo': [178, 99, 0],
    'central': [220, 36, 31],
    'circle': [255, 211, 41],
    'district': [0, 125, 50],
    'hammersmith-city': [244, 169, 190],
    'jubilee': [161, 165, 167],
    'metropolitan': [155, 0, 88],
    'northern': [10, 10, 10],  # hmmm
    'piccadilly': [0, 25, 168],
    'victoria': [0, 152, 216],
    'waterloo-city': [147, 206, 186]
}

LINE_COUNT = len(LINE_COLOURS.keys())


def start_leds():
    leds = led.LedFactory().create(LED_ENDPOINT)
    if hasattr(leds, 'start'):  # TODO remove after led-server 0.0.5
        leds.start()
    default_sequence(leds)
    return leds


def default_sequence(leds):
    for i, k in enumerate(LINE_COLOURS.keys()):
        leds.set_pixel(i, [LINE_COLOURS[k]], repeat=LINE_COUNT, modifier='sparkle', offset=0.05)


def create_led_for_status_code(status_code, home_colour):
    output = {}
    output['colours'] = []
    output['modifier'] = 'none'
    output['duration'] = 2
    if status_code == 1 or status_code == 2 or status_code == 4 or status_code == 11 or status_code == 20:
        # Closed / suspended / Planned closure / Part closed
        output['colours'].append([0, 0, 0])
        output['colours'].append(home_colour)
        output['modifier'] = 'blink'
        output['duration'] = 1.5
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
        output['colours'].append(led.lerp_colour(home_colour, [0, 0, 0], 0.5))
        output['colours'].append(home_colour)
        output['colours'].append(led.lerp_colour(home_colour, [255, 255, 255], 0.5))
        output['modifier'] = 'noise'
        output['duration'] = 0.5
        output['offset'] = random.random() * 42
    else:
        output['colours'].append(led.lerp_colour([0, 0, 0], home_colour, 0.3))
        output['colours'].append(home_colour)
        output['modifier'] = 'smooth'
        output['duration'] = 2
    return output


def show_all_line_statuses(leds, statuses):
    repeat = len(statuses)
    for i, status in enumerate(statuses):
        home_colour = LINE_COLOURS[status.affected_lines[0]]
        light = create_led_for_status_code(status.status_code, home_colour)
        if 'offset' in light:
            offset = light['offset']
        else:
            offset = i/repeat
        leds.set_pixel(i,
                       colours=light['colours'],
                       modifier=light['modifier'],
                       duration=light['duration'],
                       offset=offset,
                       repeat=repeat)


if __name__ == '__main__':
    from tfltree.raspberrypi import tfl
    from time import strftime

    timestamp = strftime('%Y%m%d_%H%M%S')
    statuses = tfl.map_status_to_model(tfl.TflApi().update_status(timestamp))

    leds = start_leds()
    show_all_line_statuses(leds, statuses)
    try:
        while True:
            sleep(1)
    except:
        leds.all_off()
