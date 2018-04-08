from configparser import ConfigParser
from datetime import datetime, timedelta
import argparse
import caldav
import logging
import requests.auth
import sys
import uuid
import vobject


log = logging.getLogger(__name__)
LOG_FORMAT = '%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
HOUR = timedelta(hours=1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configfile', help='path to config file')
    options = parser.parse_args()
    config = ConfigParser()
    config.read(options.configfile)
    config = config['default']
    logging.basicConfig(stream=sys.stdout, format=LOG_FORMAT,
                        level=config.get('loglevel', 'WARNING'))

    client = caldav.DAVClient(
        config['url'],
        auth=requests.auth.HTTPBasicAuth(
            username=config['username'], password=config['password']))
    calendars = client.principal().calendars()
    for calendar in calendars:
        if calendar.name == config['calendar']:
            break
    else:
        log.info('No calendar named %s was found', config['calendar'])
        return 2

    msg = vobject.iCalendar().add('vevent')
    msg.add('dtstart').value = datetime.now()
    msg.add('dtend').value = msg.dtstart.value + HOUR
    msg.add('summary').value = 'caldavcheck'
    msg.add('description').value = str(uuid.uuid4())

    log.info('Storing event on %s, token %s',
             msg.dtstart.value, msg.description.value)
    calendar.add_event(msg.serialize())

    for item in calendar.date_search(
            msg.dtstart.value - HOUR, msg.dtstart.value + HOUR):
        event = vobject.readOne(item.data).vevent
        log.debug('Looking at %s', event)
        if event.description.value == msg.description.value:
            log.info('Found token %s, deleting event', msg.description.value)
            item.delete()
            return 0
    log.info('Token %s not found, giving up', msg.description.value)
    return 1


if __name__ == '__main__':
    main()
