class DatabaseError(Exception):
    def __init__(self, msg="DatabaseError"):
        self.msg = msg
    def __str__(self):
        return self.msg

class AesCryptoError(Exception):
    def __init__(self, msg="AesCryptoError"):
        self.msg = msg
    def __str__(self):
        return self.msg

class IntegrityCheckError(Exception):
    def __init__(self, msg="IntegrityCheckError"):
        self.msg = msg
    def __str__(self):
        return self.msg

class LoggerError(Exception):
    def __init__(self, msg="LoggerError"):
        self.msg = msg
    def __str__(self):
        return self.msg