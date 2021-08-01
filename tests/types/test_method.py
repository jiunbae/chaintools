import pytest

from chaintools import Type as T


class A:
    def __init__(self, a: int):
        self.a = a


def test_to():
    f = T.to(A)
    a = f(10)
    assert isinstance(a, A) and a.a == 10


def test_to_instantiation_equality():
    target = (1, 2, 3)
    f = T.to(list)
    g = T.to_list
    assert f(target) == g(target) == list(target)


def test_is_type():
    f = T.is_type(A)
    a = A(10)
    assert f(a)

def test_is_type_equality():
    target_list = [1, 2, 3]
    target_tuple = (1, 2, 3)

    f = T.is_type(list)
    g = T.is_list
    assert f(target_list) == g(target_list)
    assert f(target_tuple) == g(target_tuple)
