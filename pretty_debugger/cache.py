class PrettyCache:
    _instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.__level: int = 0

    @property
    def level(self):
        return self.__level
    @level.setter
    def level(self, level: int):
        if not isinstance(level, int):
            raise TypeError('pretty-debugger level must be an integer')
        self.__level = level
