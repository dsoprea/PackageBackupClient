from logging import getLogger, Filter, Formatter, DEBUG, StreamHandler
from sys import platform

default_logger = getLogger()
default_logger.setLevel(DEBUG)

log_console = StreamHandler()
log_format = '%(asctime)s %(name)-12s %(levelname)-7s %(message)s'
log_console.setFormatter(Formatter(log_format))
default_logger.addHandler(log_console)

