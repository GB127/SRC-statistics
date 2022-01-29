class Run:
    def __init__(self, data:dict):
        self.__dict__ = data
        pass

    def __getitem__(self, key):
        return self.__dict__[key]
