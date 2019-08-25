import logging as log
from time import time


log.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=log.DEBUG)

def timeit(function):
    def timed(*args, **kw):
        start_time = time()
        result = function(*args, **kw)
        end_time = time()
        log.debug('%r %r %r  %2.2f ms',
              function.__name__, args, kw, (end_time - start_time) * 1000)
        return result
    return timed
