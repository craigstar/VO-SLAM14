import yaml

class Singleton(object):
    """Test data, Singleton class"""
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance

class Config(Singleton):
    """docstring for Config"""
    file = None

    @staticmethod
    def setParameterFile(filename):
        try:
            stream = open(filename, 'r')
            self.file = yaml.load(stream)
        except Exception as e:
            print(e)

    @staticmethod
    def get(self, key):
        if Config.file is None:
            return print('Set params first!')
        return self.file.get(key)
