# Microsoft Visual C++ Compiler for Python 2.7 Install
# pip install pycrypto
import base64
import hashlib
import sys
from .integrityCheck import *
from Crypto.Cipher import AES
from Crypto import Random
from common.common_func import *
from error.exception import *

class AesCipher:
    def __init__(self):
        self.bs = 32
        self.key = self._getKey()

    def _getKey(self, password = "appmadmin"):
        return hashlib.sha256(password.encode()).digest()

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def encrypt(self, data):
        data = self._pad(data)
        iv = Random.new().read(AES.block_size)
        try:
            encryptor = AES.new(self.key, AES.MODE_CBC, iv)
            encData = base64.b64encode(iv + encryptor.encrypt(data))
        except Exception as err:
            lineno = sys.exc_info()[2].tb_lineno
            raise AesCryptoError(getErrorStr(sys._getframe(), err, lineno))
        encHash(encData)
        return encData
    
    def decrypt(self, data):
        integrityRet = integrity(data)
        try:
            if integrityRet != -1:
                enc = base64.b64decode(data)
                iv = enc[:AES.block_size]
                decryptor = AES.new(self.key, AES.MODE_CBC, iv)
                return bytes.decode(self._unpad(decryptor.decrypt(enc[AES.block_size:])))
            else: 
                raise Exception('Integrity is compromised.')
        except Exception as err:
            lineno = sys.exc_info()[2].tb_lineno
            raise IntegrityCheckError(getErrorStr(sys._getframe(), err, lineno))