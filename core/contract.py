# coding: utf-8

import copy
from .context import Context


class Contract(object):
    __VISIBILITY__ = {}

    @property
    def visibility(self):
        return Contract.__VISIBILITY__

    def public(func):
        Contract.__VISIBILITY__[func.__qualname__] = True
        def __public(self, *args):
            return func(self, *args)
        return __public

    @property
    def msg(self):
        return Context.__MSG__.get()

    def snapshot(self):
        return copy.deepcopy(self.__dict__)