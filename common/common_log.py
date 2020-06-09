import os, sys, inspect
import logging
import logging.handlers

from error.exception import *

class Logger:
    def __init__(self, frame, **kwargs):
        try:
            self.initLogging(os.path.abspath(inspect.getfile(frame)), kwargs)
        except Exception as err:
            raise LoggerError(msg=err)

    def initLogging(self, path, kwargs):
        dir, file = os.path.split(path)
        filename = file.split('.')[0]
        logger = logging.getLogger(filename)
        logger.setLevel(logging.DEBUG)

        LOGGING_LEVELS = {'DEBUG':logging.DEBUG, 'ERROR':logging.ERROR, 'INFO':logging.INFO, 'WARNING':logging.WARNING, 'CRITICAL':logging.CRITICAL}

        logfolderpath = dir + '/logs'
        logfilename = logfolderpath + '/' + filename + '.log'

        if not os.path.isdir(logfolderpath): os.mkdir(logfolderpath)
        if kwargs.has_key('streamlevel'):
            if kwargs['streamlevel'] is not None:
                streamHandler = logging.StreamHandler()
                streamHandler.setLevel(LOGGING_LEVELS.get(str(kwargs['streamlevel']).upper() if kwargs.has_key('streamlevel') else 'DEBUG'))
                #streamHandler.setLevel(logging.ERROR)
                logger.addHandler(streamHandler)

        fileHandler = logging.handlers.TimedRotatingFileHandler(filename=logfilename, when='midnight', interval=1)
        fileHandler.setFormatter(logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > \n===[Log message start]===\n%(message)s\n===[Log message end]==='))
        fileHandler.setLevel(LOGGING_LEVELS.get(str(kwargs['filelevel']).upper() if kwargs.has_key('filelevel') else 'DEBUG'))
        #fileHandler.setLevel(logging.DEBUG)

        logger.addHandler(fileHandler)

        self._logger = logger

    def getLogger(self):
        return self._logger
