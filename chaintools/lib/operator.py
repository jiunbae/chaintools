from abc import ABC


class Addable(ABC):
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Addable:
            if any("__add__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


class Subtractable(ABC):
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Addable:
            if any("__sub__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


class Multipliable(ABC):
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Addable:
            if any("__mul__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


class Divisible(ABC):
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Addable:
            if any("__truediv__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented
