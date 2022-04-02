class Base_Entry:
    """Base entry. All common features from all the different
        type of data handled by the program.
        Methods:
            __getitem__ / __setitem__
            keys
            __eq__
        TODO : In child classes, Maybe try to inherit dictos instead of using a base entry?
            if it works, this fille can be deleted.
    """
    def __getitem__(self, key):
        return self.__dict__[key]

    def keys(self):
        return self.__dict__.keys()

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
