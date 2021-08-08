import pytest

from chaintools import Chainable


class ChainableTest(metaclass=Chainable):
    def __init__(self):
        self.items = []

    def __rshift__(self, item):
        self.items.append(item)


def test_chainable():
    chainable = ChainableTest()

    chainable >> "foo"
    chainable >> "bar"
    chainable >> "baz"

    assert chainable.items == ["foo", "bar", "baz"]
