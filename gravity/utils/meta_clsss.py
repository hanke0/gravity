# -*- coding: utf-8 -*-
import abc

__all__ = ("create_mapped_meta_class", "Singleton")


class Map(dict):
    def __setitem__(self, key: object, value: object) -> None:
        raise NotImplementedError

    def register(self, cls: type, name=None) -> None:
        key = cls.__name__ if name is None else name
        super().__setitem__(key, cls)

    def __str__(self):
        return "%s%s" % (self.__class__.__name__, super().__str__())

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError as e:
            msg = str(e)
            e.args = ["Unsupported Key %s" % msg]
            raise


_meta_class_define_string = """
class {}(abc.ABCMeta):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        map.register(cls)
        return cls
"""


def create_mapped_meta_class(name):
    """create a class with a meta class that save it's class to a map

    :return:
    """
    local = {"map": Map(), "abc": abc}
    exec(_meta_class_define_string.format(name), local, local)
    return local[name], local["map"]


class SingletonMeta(type):
    __instance = None

    def __call__(cls):
        if cls.__instance is not None:
            return cls.__instance
        self = super().__call__()
        cls.__instance = self
        return self


class Singleton(metaclass=SingletonMeta):
    """Singleton case
    
    __init__ function must receive no arguments
    """

    pass
