from configparser import ConfigParser
import argparse
import logging
import sys


log = logging.getLogger(__name__)
LOG_FORMAT = '%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configfile', help='path to config file')
    options = parser.parse_args()
    config = ConfigParser()
    config.read(options.configfile)
    config = config['default']
    logging.basicConfig(stream=sys.stdout, format=LOG_FORMAT,
                        level=config.get('loglevel', 'WARNING'))


if __name__ == '__main__':
    main()
