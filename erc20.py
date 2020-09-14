#coding: utf-8

from core.guid import GUID
from core.types import Mapping
from core.contract import Contract

class ERC20(Contract):
    def __init__(self):
        super(ERC20, self).__init__()

    @Contract.public
    def constructor(self, name: str, symbol: str, decimals: int):
        self._name = name
        self._symbol = symbol
        self._decimals = decimals
        self._balances = Mapping(str, int)
        self._approval = Mapping(str, Mapping(str, int))
        self._total_supply = 0

    @Contract.public
    def name(self):
        return self._name

    @Contract.public
    def symbol(self):
        return self._symbol

    @Contract.public
    def decimals(self):
        return self._decimals

    @Contract.public
    def total_supply(self):
        return self._total_supply

    @Contract.public
    def balanceOf(self, account):
        return self._balances[account]

    @Contract.public
    def approve(self, spender, amount):
        self._approval[self.msg.sender][spender] = amount

    @Contract.public
    def allowance(self, owner, spender):
        return self._approval[owner][spender]

    @Contract.public
    def transfer(self, dst, amount):
        self.transfer_from(self.msg.sender, dst, amount)

    @Contract.public
    def transfer_from(self, src, dst, amount):
        self._balances[src] = self._balances[src] - amount
        self._balances[dst] = self._balances[dst] + amount

    @Contract.public
    def mint(self, account, amount):
        self._balances[account] = self._balances[account] + amount
        self._total_supply = self._total_supply + amount

    @Contract.public
    def burn(self, account, amount):
        self._balances[account] = self._balances[account] - amount
        self._total_supply = self._total_supply - amount