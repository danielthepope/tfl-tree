import logging
from time import time

logger = logging.getLogger('tfltree')
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)


def timeit(function):
    def timed(*args, **kw):
        start_time = time()
        result = function(*args, **kw)
        end_time = time()
        logger.debug('%r %r %r  %2.2f ms',
                     function.__name__, args, kw, (end_time - start_time) * 1000)
        return result
    return timed
