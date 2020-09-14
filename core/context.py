# coding: utf-8

import contextvars

class Message(object):
    def __init__(self, sender=None):
        self.sender = sender
        self.value = 0

    def __str__(self):
        return "from %s => %s" % (self.sender, self.value)

    def merge(self, data):
        sender = data.get("from")
        if sender:
            self.sender = sender

        value = data.get("value")
        if value:
            self.value = value

    def clone(self):
        return Message(self.sender)


class Context(object):

    __MSG__ = contextvars.ContextVar("msg", default=Message())

    def __init__(self, account):
        self.account = account

    def __enter__(self):
        global msg
        Context.__MSG__ = contextvars.ContextVar("msg", default=Message(self.account))

    def __exit__(self, type, value, trace):
        global msg
        Context.__MSG__ = contextvars.ContextVar("msg", default=Message())
