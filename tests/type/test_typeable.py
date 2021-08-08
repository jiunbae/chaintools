import pytest

from chaintools import Typeable


class TypeableTest(metaclass=Typeable):
    @staticmethod
    def is_test():
        return True


def test_typeable_is():
    assert TypeableTest.is_int(1)


def test_typeable_to():
    assert TypeableTest.to_int('1') == 1


def test_typeable_static_methods():
    assert TypeableTest.is_test() == True


def test_is_type():
    def is_list():
        return (True, False, False) == tuple(map(TypeableTest.is_list, [[], (), {}]))

    def is_tuple():
        return (False, True, False) == tuple(map(TypeableTest.is_tuple, [[], (), {}]))

    def is_str():
        return (True, False, False) == tuple(map(TypeableTest.is_str, ['a', 3.1, 3]))

    def is_dict():
        return (True, True) == tuple(map(TypeableTest.is_dict, [{}, {'a': 1}]))
    
    def is_iterable():
        return (True, False, True, True) == tuple(map(TypeableTest.is_iterable, ['a', 3, [], (0, )]))

    assert all([
        is_list(),
        is_tuple(),
        is_str(),
        is_dict(),
        is_iterable(),
    ])


def test_to_type():
    def to_list():
        return all(map(
            TypeableTest.is_list, 
            map(
                TypeableTest.to_list, 
                [[], (), {}],
            ),
        ))

    def to_tuple():
        return all(map(
            TypeableTest.is_tuple,
            map(
                TypeableTest.to_tuple,
                [[], (), {}]
            ),
        ))

    def to_str():
        return all(map(
            TypeableTest.is_str,
            map(TypeableTest.to_str, ['a', 3.1, 3],
            ),
        ))

    def to_dict():
        return all(tuple(map(
            TypeableTest.to_dict, 
            [((3, 2), ), {'a': 1}],
        )))
    
    assert all([
        to_list(),
        to_tuple(),
        to_str(),
        to_dict(),
    ])
