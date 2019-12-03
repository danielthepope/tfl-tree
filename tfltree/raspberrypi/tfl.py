import json
from tempfile import mkstemp
from time import strftime

import requests

from tfltree import logger as log
from tfltree.raspberrypi import LineStatus
from tfltree.raspberrypi.config import UPLOAD_FIRST


class TflApi:
    url = ''
    status = []
    _previous_status = []

    def __init__(self, url='https://api.tfl.gov.uk/line/mode/tube/status'):
        self.url = url

    def update_status(self, timestamp=strftime('%Y%m%d_%H%M%S')):
        log.info('Updating status from %s', self.url)
        response = requests.get(self.url)
        if response.status_code == 200:
            self._previous_status = self.status
            response_text = response.text
            self.status = _map_status_to_model(json.loads(response_text))
            log.info('Loaded status successfully')
            if self.has_status_changed():
                (fd, path) = mkstemp('.json', 'tfltree_%s_' % timestamp)
                with open(fd, 'w') as f:
                    f.write(response_text)
                    log.debug('Wrote API response to %s', path)
        else:
            log.warning('Received status %s from API. Returning previous one', response.status_code)
        return self.status

    def has_status_changed(self):
        if self._previous_status or UPLOAD_FIRST:
            return not(_just_status_codes(self.status) == _just_status_codes(self._previous_status))
        else:
            return False


def _just_status_codes(status_model):
    return [s.status_codes for s in status_model]


def _map_status_to_model(status):
    output = []
    reasons = []
    for line in status:
        line_id = line['id']
        for s in line['lineStatuses']:
            reason = s['statusSeverityDescription']
            if 'reason' in s:
                reason = _remove_line_name_from_reason(s['reason'])
            status_code = s['statusSeverity']
            if reason in reasons:
                # Identical message found: merge its details
                line_status_index = reasons.index(reason)
                output[line_status_index].affected_lines.add(line_id)
                output[line_status_index].status_codes.add(status_code)
            else:
                output.append(LineStatus(
                    affected_lines=set([line_id]),
                    reason=reason,
                    status_codes=set([status_code])
                ))
                reasons.append(reason)
    # If there is good service, move it to the end
    if 'Good Service' in reasons:
        output.append(output.pop(reasons.index('Good Service')))
    # Return a list of deduplicated LineStatus objects
    return output


def _remove_line_name_from_reason(message):
    index = message.lower().find('line: ')
    if index >= 0:
        return message[index + 6:]
    else:
        return message


if __name__ == '__main__':
    API = TflApi()
    status = API.update_status()
    status2 = API.update_status()
    log.debug(status)
    log.debug(API.has_status_changed())
