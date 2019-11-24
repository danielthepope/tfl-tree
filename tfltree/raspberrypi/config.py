import os

from dotenv import load_dotenv

from tfltree import logger as log

load_dotenv()

# LEDS
FRAMES_PER_SECOND = os.getenv('FRAMES_PER_SECOND')
BRIGHTNESS = os.getenv('BRIGHTNESS')
PIXEL_COUNT = os.getenv('PIXEL_COUNT')
LED_SIZE = os.getenv('LED_SIZE')

# TWITTER
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

log.info('Configuration:')
log.info('FRAMES_PER_SECOND: %s', FRAMES_PER_SECOND)
log.info('BRIGHTNESS: %s', BRIGHTNESS)
log.info('PIXEL_COUNT: %s', PIXEL_COUNT)
log.info('LED_SIZE: %s', LED_SIZE)
log.info('CONSUMER_KEY: %s', CONSUMER_KEY)
log.info('CONSUMER_SECRET: %s', CONSUMER_SECRET)
log.info('ACCESS_TOKEN_KEY: %s', ACCESS_TOKEN_KEY)
log.info('ACCESS_TOKEN_SECRET: %s', ACCESS_TOKEN_SECRET)
