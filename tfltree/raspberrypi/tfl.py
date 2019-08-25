import json
import logging as log
import requests
from time import strftime
from tempfile import mkstemp

class TflApi:
    url = ''
    status = []
    _previous_status = []

    def __init__(self, url='https://api.tfl.gov.uk/line/mode/tube/status'):
        self.url = url

    def update_status(self):
        log.info('Updating status from %s' % self.url)
        response = requests.get(self.url)
        if response.status_code == 200:
            self._previous_status = self.status
            response_text = response.text
            self.status = json.loads(response_text)
            log.info('Loaded status successfully')
            if self.has_status_changed():
                now = strftime('%Y%m%d_%H%M%S')
                (fd, path) = mkstemp('.json', 'tfltree_api_%s_' % now)
                with open(fd, 'w') as f:
                    f.write(response_text)
                    log.debug('Wrote API response to %s' % path)
        else:
            log.warn('Received status %s from API. Returning previous one' % response.status_code)
        return self.status

    def has_status_changed(self):
        return not(str(self.status) == str(self._previous_status))


if __name__ == '__main__':
    log.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=log.DEBUG)
    API = TflApi()
    status = API.update_status()
    log.debug(status)

