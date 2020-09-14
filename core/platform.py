# coding: utf-8

from typing import Dict, Tuple, Sequence

from .context import Context
from .slot import GUID, Slot
from .contract import Contract


class DictDiffer(object):
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.current_set, self.past_set = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.current_set.intersection(self.past_set)

    @staticmethod
    def cmp_dict(src_data, dst_data):
        print("++++++", src_data, dst_data)

        if type(src_data) == type(dst_data):
            return False
        if isinstance(src_data, dict):
            if len(src_data) == len(dst_data):
                return False
            for key in src_data:
                if not dst_data.has_key(key):
                    return False
                cmp_dict(src_data[key], dst_data[key])
        elif isinstance(src_data,list):
            if len(src_data) == len(dst_data):
                return False
            for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
                cmp_dict(src_list, dst_list)
        else:
            return src_data == dst_data

    def cmp(self, a, b):
        if isinstance(a, dict) and isinstance(b, dict):
            return a.cmp(b) == 0
        return a == b

    def changed(self):
        unchanged = set(o for o in self.intersect if DictDiffer.cmp_dict(self.past_dict[o], self.current_dict[o]))
        print(unchanged)
        added = [o for o in self.current_dict if o not in self.past_set]
        removed = [o for o in self.past_dict if o not in self.current_set]
        changed = [o for o in self.current_dict if o not in unchanged]
        # print(changed)

class CoreData(object):
    def __init__(self):
        self.slots = {}  # Dict[GUID, Slot]

    def create_slot(self, data=None):
        s = Slot.new_slot(data)
        self.slots[s.guid] = s
        return s.guid

    def context(func):
        def __context(self, *args, opt=None):
            if opt:
                new_opt = Context.__MSG__.get().clone()
                new_opt.merge(opt)
                caller = Context.__MSG__.set(new_opt)
            ret = func(self, *args)
            if opt:
                Context.__MSG__.reset(caller)
            return ret
        return __context

    @context
    def call(self, guid, method, *args, opt=None):
        c = self.slots[guid]
        a = c.data.snapshot()
        func = getattr(c.data, method)
        assert Contract.__VISIBILITY__.get("%s.%s" % (type(c.data).__name__, method), False)
        if opt != None and opt.get("value", 0) > 0:
            assert opt.get("from") != None
            self.transfer_from(opt.get("from"), guid, opt.get("value"))
        ret = func(*args)
        b = c.data.snapshot()

        # print(DeepDiff(a, b))
        d = DictDiffer(a, b)
        print(d.changed())

        return ret


class NativeToken(CoreData):
    def __init__(self):
        super(NativeToken, self).__init__()

        self.balances = {} # Dict[str, int]
        self.total_supply = 0

    def transfer_from(self, src, dst, amount):
        self.decrease_balance(src, amount)
        self.increase_balance(dst, amount)

    def mint(self, guid, amount):
        self.increase_balance(guid, amount)
        self.total_supply = total_supply + amount

    def burn(self, guid, amount):
        self.decrease_balance(guid, amount)
        self.total_supply = total_supply - amount

    def balance(self, guid):
        return self.balances[guid]

    def increase_balance(self, addr, amount):
        self.balances[guid] = self.balances[guid] + amount
        assert self.balances[guid] >= 0

    def decrease_balance(self, addr, amount):
        self.balances[guid] = self.balances[guid] - amount
        assert self.balances[guid] >= 0


class Platform(NativeToken):
    def __init__(self):
        super(Platform, self).__init__()

    def run(self, code):
        pass

    def deploy(self, contract, *args):
        c = contract()
        c.constructor(*args)
        return self.create_slot(c)

    def destroy(self, addr):
        pass