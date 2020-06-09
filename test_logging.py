from common.common_log import *
import sys

#LOGGING_LEVELS = DEBUG, ERROR, INFO, WARNING, CRITICA
#STREAMLEVEL = DEBUG, ERROR, INFO, WARNING, CRITICAL
logger = Logger(sys._getframe(), filelevel="DEBUG", streamlevel="ERROR")
log = logger.getLogger()
log.debug('HELLO!!!')