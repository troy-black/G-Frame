import logging.config

from pkg_resources import get_distribution, DistributionNotFound

dist_name = 'G-Frame'
__version__ = '0.0.0'

try:
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = '0.0.0'

try:
    from gframe.json.log import log
    logging.config.dictConfig(log.data)
except (FileNotFoundError, ValueError) as e:
    logging.basicConfig(level=logging.INFO)
    logging.critical('Unable to load config.json', exc_info=True)

logging.debug('Starting Application')
