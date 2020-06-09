class SingletonBase(object):
    _instance = None
    def __new__(cls, *args, **kargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kargs)

        return cls._instance
