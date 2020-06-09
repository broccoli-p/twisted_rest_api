import cx_Oracle, sys

from subprocess import check_output

from common.Design import Singleton
from common.common_func import *
from error.exception import *



class Connection(Singleton.SingletonBase):
    def __init__(self):
        self.initConnection()

    def initConnection(self):
        try:
            dbpass = check_output(['/home/appm/script/decrypt_passwd'], shell=True).strip()
                        
            self._conn = cx_Oracle.connect('appm', dbpass, 'xe')
            self._cursor = self._conn.cursor()
        except Exception as err:
            lineno = sys.exc_info()[2].tb_lineno
            raise DatabaseError(getErrorStr(sys._getframe(), err, lineno))

    def getCursor(self):
        return self._cursor

    def disconnection(self):
        if self._cursor is not None: self._cursor.close()
        if self._conn is not None: self._conn.close()

    def __del__(self):
        if self._cursor is not None: self._cursor.close()
        if self._conn is not None: self._conn.close()

    def rowsToDictList(self):
        columns = [i[0] for i in self._cursor.description]
        return [dict(zip(columns, row)) for row in self._cursor]

    def commit(self):
        try:
            self._conn.commit()
        except Exception as err:
            lineno = sys.exc_info()[2].tb_lineno
            raise DatabaseError(getErrorStr(sys._getframe(), err, lineno))
        