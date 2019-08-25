import json
import logging as log
import requests

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
            self.status = json.loads(response.text)
            log.info('Loaded status successfully')
        else:
            log.warn('Received status %s from API. Returning previous one' % response.status_code)
        return self.status

    def has_status_changed(self):
        return not(str(self.status) == str(self._previous_status))


if __name__ == '__main__':
    API = TflApi()
    status = API.update_status()
    print(status)

