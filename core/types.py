#coding: utf-8

class Mapping(dict):
    def __init__(self, type_key, type_value):
        super(Mapping, self).__init__()

        self.type_key = type_key
        self.type_value = type_value

    def __getitem__(self, key):
        assert type(key) == self.type_key
        return super(Mapping, self).get(key, 0)

    def __setitem__(self, key, value):
        assert type(key) == self.type_key
        assert type(value) == self.type_value
        dict.__setitem__(self, key, value)