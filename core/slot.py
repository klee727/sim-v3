# coding: utf-8

from .guid import GUID

class Slot(object):
    def __init__(self, guid, data):
        self.guid = guid
        self.data = data

    @staticmethod
    def new_slot(data):
        return Slot(GUID.new_id(), data)

    def is_contract(self):
        return self.data is None