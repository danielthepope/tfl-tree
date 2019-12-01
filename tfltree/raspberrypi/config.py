import os

from dotenv import load_dotenv

from tfltree import logger as log

load_dotenv()

# LEDS
FRAMES_PER_SECOND = int(os.getenv('FRAMES_PER_SECOND', 15))
BRIGHTNESS = float(os.getenv('BRIGHTNESS', 0.1))
PIXEL_COUNT = int(os.getenv('PIXEL_COUNT', 25))
LED_SIZE = int(os.getenv('LED_SIZE', 25))
LED_ENDPOINT = os.getenv('LED_ENDPOINT')

# TWITTER
UPLOAD_FIRST = int(os.getenv('UPLOAD_FIRST', 0))
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

log.info('Configuration:')
log.info('FRAMES_PER_SECOND: %s', FRAMES_PER_SECOND)
log.info('BRIGHTNESS: %s', BRIGHTNESS)
log.info('PIXEL_COUNT: %s', PIXEL_COUNT)
log.info('LED_SIZE: %s', LED_SIZE)
log.info('LED_ENDPOINT: %s', LED_ENDPOINT)
log.info('UPLOAD_FIRST: %s', UPLOAD_FIRST)
log.info('CONSUMER_KEY: %s', CONSUMER_KEY)
log.info('CONSUMER_SECRET: %s', CONSUMER_SECRET)
log.info('ACCESS_TOKEN_KEY: %s', ACCESS_TOKEN_KEY)
log.info('ACCESS_TOKEN_SECRET: %s', ACCESS_TOKEN_SECRET)
