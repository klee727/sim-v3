# coding: utf-8

from core.context import Context
from core.platform import Platform
from erc20 import ERC20

if __name__ == "__main__":
    p = Platform()
    user_1 = p.create_slot()
    user_2 = p.create_slot()

    with Context(user_1) as ctx:
        erc20 = p.deploy(ERC20, "TestToken", "TTK", 18)
        print(p.call(erc20, "balanceOf", user_1))
        print(p.call(erc20, "name"))
        p.call(erc20, "mint", user_1, 1000)
        print(p.call(erc20, "balanceOf", user_1))

        p.call(erc20, "transfer_from", user_1, user_2, 100)
        print(p.call(erc20, "balanceOf", user_1))
        print(p.call(erc20, "balanceOf", user_2))

        p.call(erc20, "transfer", user_2, 100)
        print(p.call(erc20, "balanceOf", user_1))
        print(p.call(erc20, "balanceOf", user_2))