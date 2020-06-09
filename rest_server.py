#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function

import os, sys

from twisted.web import server
from twisted.internet import reactor

from security import ssl
from core.core import Server
from common.common_func import *
from common.common_log import *
from error.exception import *

logger = Logger(sys._getframe(), filelevel="DEBUG", streamlevel="ERROR")
log = logger.getLogger()

def startServer():
    try:
        s = server.Site(Server())
    except Exception as err:
        lineno = sys.exc_info()[2].tb_lineno
        msg = getErrorStr(sys._getframe(), err, lineno)
        log.critical(msg)
        raise Exception(getErrorStr(sys._getframe(), err, lineno))
    ssl.createSSL(reactor).listen(s)
    reactor.run()

if __name__ == '__main__':
    startServer()
