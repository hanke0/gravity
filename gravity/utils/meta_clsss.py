# -*- coding: utf-8 -*-
import abc


class Map(dict):
    def __setitem__(self, key: object, value: object) -> None:
        raise NotImplementedError

    def register(self, cls: type) -> None:
        key = cls.__name__
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


class SimpleEnumMeta(type):
    def __new__(mcs, name, bases, attrs):
        mapping = {v: k for k, v in attrs.items() if not k.startswith("_")}
        attrs["__map"] = mapping
        attrs["__key"] = set(mapping.keys())
        attrs["__name"] = name
        return type.__new__(mcs, name, bases, attrs)

    def __getitem__(self, item):
        _map = self.__dict__["__map"]
        if item not in self.__dict__["__key"]:
            raise KeyError("unknown %s(%s)" % (self.__name__, item))
        return _map[item]

    def __contains__(self, item):
        return item in self.__dict__["__key"]

    def __setattr__(self, key, value):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __call__(cls, *args, **kwargs):
        raise ValueError("can't get a enum instance")

    def register_new(cls, name, value):
        if name in cls.__dict__["__key"]:
            raise ValueError("duplicated key '%s'" % name)
        for v in cls.__dict__["__map"].values():
            if v == value:
                raise ValueError("duplicated value %s" % value)
        cls.__dict__["__key"].add(name)
        cls.__dict__["__map"][value] = name
        super().__setattr__(name, value)

    def __repr__(self):
        return "%s(%s)" % (
            self.__dict__["__name"],
            ", ".join("%s=%s" % (v, k) for k, v in self.__dict__["__map"].items()),
        )

    __str__ = __repr__


class SimpleEnum(metaclass=SimpleEnumMeta):
    pass


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
