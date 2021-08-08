from __future__ import annotations
from typing import Callable


class Chainable(type):
    def __rshift__(cls, function: Callable)\
            -> Chainable:
        instance: Chainable = cls()
        instance = instance >> function
        return instance
