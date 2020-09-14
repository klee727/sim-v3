# coding: utf-8

import hashlib

class GUID(object):
    __index__ = 0

    @staticmethod
    def new_id():
        guid = hashlib.sha256(bytes(str(GUID.__index__), 'utf8')).hexdigest()
        GUID.__index__ = GUID.__index__ + 1
        return guid[:16]

    @staticmethod
    def validate(guid):
        return len(guid) == 16
