import pytest

from chaintools import Type as T


def test_is_type():
    def is_list():
        return (True, False, False) == tuple(map(T.is_list, [[], (), {}]))

    def is_tuple():
        return (False, True, False) == tuple(map(T.is_tuple, [[], (), {}]))

    def is_str():
        return (True, False, False) == tuple(map(T.is_str, ['a', 3.1, 3]))

    def is_dict():
        return (True, True) == tuple(map(T.is_dict, [{}, {'a': 1}]))
    
    def is_iterable():
        return (True, False, True, True) == tuple(map(T.is_iterable, ['a', 3, [], (0, )]))

    assert all([
        is_list(),
        is_tuple(),
        is_str(),
        is_dict(),
        is_iterable(),
    ])


def test_instantiation():
    def to_list():
        return all(map(T.is_list, (map(T.to_list, [[], (), {}]))))

    def to_tuple():
        return all(map(T.is_tuple, (map(T.to_tuple, [[], (), {}]))))

    def to_str():
        return all(map(T.is_str, (map(T.to_str, ['a', 3.1, 3]))))

    def to_dict():
        return all(tuple(map(T.to_dict, [((3, 2), ), {'a': 1}])))
    
    assert all([
        to_list(),
        to_tuple(),
        to_str(),
        to_dict(),
    ])
